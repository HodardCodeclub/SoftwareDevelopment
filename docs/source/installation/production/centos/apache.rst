Apache
======

.. _centos-apache-epel:

1. Enable EPEL
--------------

.. code-block:: shell

    yum install -y epel-release

.. note::

    If you use CC7, EPEL is already enabled and this step is not necessary


.. _centos-apache-pkg:

2. Install Packages
-------------------

Edit ``/etc/yum.repos.d/CentOS-Base.repo`` and add ``exclude=postgresql*``
to the ``[base]`` and ``[updates]`` sections, as described in the
`PostgreSQL wiki`_.

.. code-block:: shell

    yum install -y https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm
    yum install -y postgresql96 postgresql96-server postgresql96-libs postgresql96-devel postgresql96-contrib
    yum install -y httpd mod_proxy_uwsgi mod_ssl mod_xsendfile
    yum install -y gcc redis uwsgi uwsgi-plugin-python
    yum install -y python-devel python-virtualenv libjpeg-turbo-devel libxslt-devel libxml2-devel libffi-devel pcre-devel libyaml-devel
    /usr/pgsql-9.6/bin/postgresql96-setup initdb
    systemctl start postgresql-9.6.service redis.service


.. _centos-apache-db:

3. Create a Database
--------------------

We create a user and database for fossir and enable the necessary
Postgres extensions (which can only be done by the Postgres superuser)

.. code-block:: shell

    su - postgres -c 'createuser fossir'
    su - postgres -c 'createdb -O fossir fossir'
    su - postgres -c 'psql fossir -c "CREATE EXTENSION unaccent; CREATE EXTENSION pg_trgm;"'

.. warning::

    Do not forget to setup a cronjob that creates regular database
    backups once you start using fossir in production!


.. _centos-apache-web:

4. Configure uWSGI & Apache
---------------------------

The default uWSGI and Apache configuration files should work fine in
most cases.

.. code-block:: shell

    cat > /etc/uwsgi.ini <<'EOF'
    [uwsgi]
    uid = fossir
    gid = apache
    umask = 027
    pidfile = /run/uwsgi/uwsgi.pid

    processes = 4
    enable-threads = true
    socket = 127.0.0.1:8008
    stats = /opt/fossir/web/uwsgi-stats.sock
    protocol = uwsgi

    master = true
    auto-procname = true
    procname-prefix-spaced = fossir
    disable-logging = true

    plugin = python
    single-interpreter = true

    touch-reload = /opt/fossir/web/fossir.wsgi
    wsgi-file = /opt/fossir/web/fossir.wsgi
    virtualenv = /opt/fossir/.venv

    vacuum = true
    buffer-size = 20480
    memory-report = true
    max-requests = 2500
    harakiri = 900
    harakiri-verbose = true
    reload-on-rss = 2048
    evil-reload-on-rss = 8192
    EOF


.. note::

    Replace ``YOURHOSTNAME`` in the next files with the hostname on which
    your fossir instance should be available, e.g. ``fossir.yourdomain.com``


.. code-block:: shell

    cat > /etc/httpd/conf.d/fossir-sslredir.conf <<'EOF'
    <VirtualHost *:80>
        ServerName YOURHOSTNAME
        RewriteEngine On
        RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
    </VirtualHost>
    EOF

    cat > /etc/httpd/conf.d/fossir.conf <<'EOF'
    <VirtualHost *:443>
        ServerName YOURHOSTNAME
        DocumentRoot "/var/empty/apache"

        SSLEngine               on
        SSLCertificateFile      /etc/ssl/fossir/fossir.crt
        SSLCertificateChainFile /etc/ssl/fossir/fossir.crt
        SSLCertificateKeyFile   /etc/ssl/fossir/fossir.key
        SSLProtocol             all -SSLv2 -SSLv3
        SSLCipherSuite          ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS
        SSLHonorCipherOrder     on

        XSendFile on
        XSendFilePath /opt/fossir
        CustomLog /opt/fossir/log/apache/access.log combined
        ErrorLog /opt/fossir/log/apache/error.log
        LogLevel error
        ServerSignature Off

        AliasMatch "^/static/assets/(core|(?:plugin|theme)-[^/]+)/(.*)$" "/opt/fossir/assets/$1/$2"
        AliasMatch "^/(css|images|js|static(?!/plugins|/assets|/themes|/custom))(/.*)$" "/opt/fossir/web/htdocs/$1$2"
        Alias /robots.txt /opt/fossir/web/htdocs/robots.txt

        SetEnv UWSGI_SCHEME https
        ProxyPass / uwsgi://127.0.0.1:8008/

        <Directory /opt/fossir>
            AllowOverride None
            Require all granted
        </Directory>
    </VirtualHost>
    EOF


Now enable the uwsgi proxy module in apache:

.. code-block:: shell

    echo 'LoadModule proxy_uwsgi_module modules/mod_proxy_uwsgi.so' > /etc/httpd/conf.modules.d/proxy_uwsgi.conf


.. _centos-apache-ssl:

5. Create an SSL Certificate
----------------------------

First, create the folders for the certificate/key and set restrictive
permissions on them:

.. code-block:: shell

    mkdir /etc/ssl/fossir
    chown root:root /etc/ssl/fossir/
    chmod 700 /etc/ssl/fossir

If you are just trying out fossir you can simply use a self-signed
certificate (your browser will show a warning which you will have
to confirm when accessing your fossir instance for the first time).


.. note::

    Do not forget to replace ``YOURHOSTNAME`` with the same value
    you used above

.. code-block:: shell

    openssl req -x509 -nodes -newkey rsa:4096 -subj /CN=YOURHOSTNAME -keyout /etc/ssl/fossir/fossir.key -out /etc/ssl/fossir/fossir.crt


While a self-signed certificate works for testing, it is not suitable
for a production system.  You can either buy a certificate from any
commercial certification authority or get a free one from
`Let's Encrypt`_.


.. note::

    There's an optional step later in this guide to get a certificate
    from Let's Encrypt. We can't do it right now since the Apache
    config references a directory yet to be created, which prevents
    Apache from starting.


.. _centos-apache-selinux:

6. Configure SELinux
--------------------

fossir works fine with SELinux enabled, but you need to load a custom
SELinux module to tell SELinux about fossir's files and how they
should be handled.

.. code-block:: shell

    cat > /tmp/fossir.cil <<'EOF'
    ; define custom type that logrotate can access
    (type fossir_log_t)
    (typeattributeset file_type (fossir_log_t))
    (typeattributeset logfile (fossir_log_t))
    (roletype object_r fossir_log_t)

    ; allow logrotate to reload systemd services
    (allow logrotate_t init_t (service (start)))
    (allow logrotate_t policykit_t (dbus (send_msg)))
    (allow policykit_t logrotate_t (dbus (send_msg)))

    ; make sure the uwsgi socket is writable by the webserver
    (typetransition unconfined_service_t usr_t sock_file "uwsgi.sock" httpd_sys_rw_content_t)
    (filecon "/opt/fossir/web/uwsgi\.sock" socket (system_u object_r httpd_sys_rw_content_t ((s0)(s0))))

    ; set proper types for our log dirs
    (filecon "/opt/fossir/log(/.*)?" any (system_u object_r fossir_log_t ((s0)(s0))))
    (filecon "/opt/fossir/log/apache(/.*)?" any (system_u object_r httpd_log_t ((s0)(s0))))
    EOF
    semodule -i /tmp/fossir.cil


.. _centos-apache-install:

7. Install fossir
-----------------

Celery runs as a background daemon. Add a systemd unit file for it:

.. code-block:: shell

    cat > /etc/systemd/system/fossir-celery.service <<'EOF'
    [Unit]
    Description=fossir Celery
    After=network.target

    [Service]
    ExecStart=/opt/fossir/.venv/bin/fossir celery worker -B
    Restart=always
    SyslogIdentifier=fossir-celery
    User=fossir
    Group=apache
    UMask=0027
    Type=simple
    KillMode=mixed
    TimeoutStopSec=300

    [Install]
    WantedBy=multi-user.target
    EOF
    systemctl daemon-reload


Now create a user that will be used to run fossir and switch to it:

.. code-block:: shell

    useradd -rm -g apache -d /opt/fossir -s /bin/bash fossir
    su - fossir


You are now ready to install fossir:

.. code-block:: shell

    virtualenv ~/.venv
    source ~/.venv/bin/activate
    pip install -U pip setuptools
    pip install --pre fossir


.. _centos-apache-config:

8. Configure fossir
-------------------

Once fossir is installed, you can run the configuration wizard.  You can
keep the defaults for most options, but make sure to use ``https://YOURHOSTNAME``
when prompted for the fossir URL. Also specify valid email addresses when asked
and enter a valid SMTP server fossir can use to send emails.  When asked for the
default timezone make sure this is the main time zone used in your fossir instance.

.. code-block:: shell

    fossir setup wizard


Now finish setting up the directory structure and permissions:

.. code-block:: shell

    mkdir ~/log/apache
    chmod go-rwx ~/* ~/.[^.]*
    chmod 710 ~/ ~/archive ~/assets ~/cache ~/log ~/tmp
    chmod 750 ~/web ~/.venv
    chmod g+w ~/log/apache
    restorecon -R ~/
    echo -e "\nSTATIC_FILE_METHOD = 'xsendfile'" >> ~/etc/fossir.conf


9. Create database schema
-------------------------

Finally you can create the database schema and switch back to *root*:

.. code-block:: shell

    fossir db prepare
    exit


.. _centos-apache-launch:

10. Launch fossir
-----------------

You can now start fossir and set it up to start automatically when the
server is rebooted:

.. code-block:: shell

    systemctl restart uwsgi.service httpd.service fossir-celery.service
    systemctl enable uwsgi.service httpd.service postgresql-9.6.service redis.service fossir-celery.service


.. _centos-apache-firewall:

11. Open the Firewall
---------------------

.. code-block:: shell

    firewall-cmd --permanent --add-port 443/tcp --add-port 80/tcp
    firewall-cmd --reload

.. note::

    This is only needed if you use CC7 as CentOS7 has no firewall enabled
    by default


.. _centos-apache-letsencrypt:

12. Optional: Get a Certificate from Let's Encrypt
--------------------------------------------------

To avoid ugly SSL warnings in your browsers, the easiest option is to
get a free certificate from Let's Encrypt. We also enable the cronjob
to renew it automatically:


.. code-block:: shell

    yum install -y python-certbot-apache
    certbot --apache --rsa-key-size 4096 --no-redirect --staple-ocsp -d YOURHOSTNAME
    rm -rf /etc/ssl/fossir
    systemctl start certbot-renew.timer
    systemctl enable certbot-renew.timer


.. _centos-apache-user:

13. Create an fossir user
-------------------------

Access ``https://YOURHOSTNAME`` in your browser and follow the steps
displayed there to create your initial user.


Optional: Shibboleth
--------------------

If your organization uses Shibboleth/SAML-based SSO, follow these steps to use
it in fossir:

1. Install Shibboleth
^^^^^^^^^^^^^^^^^^^^^

Add the Shibboleth yum repository:

.. note::

    If you use CC7, Shibboleth is already available and there is no
    need to add the repo manually.


.. code-block:: shell

    curl -fsSL -o /etc/yum.repos.d/shibboleth.repo 'https://shibboleth.net/cgi-bin/sp_repo.cgi?platform=CentOS_7'


Now install Shibboleth itself.  When prompted to accept the GPG key
of the Shibboleth yum repo, confirm the prompt.

.. code-block:: shell

    setsebool httpd_can_network_connect 1
    yum install -y shibboleth xmltooling-schemas opensaml-schemas

2. Configure Shibboleth
^^^^^^^^^^^^^^^^^^^^^^^

This is outside the scope of this documentation and depends on your
environment (Shibboleth, SAML, ADFS, etc).  Please contact whoever
runs your SSO infrastructure if you need assistance.

3. Enable Shibboleth in Apache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add the following code to your ``/etc/httpd/conf.d/fossir.conf`` right
before the ``AliasMatch`` lines:

.. code-block:: apache

    <LocationMatch "^(/Shibboleth\.sso|/login/shib-sso/shibboleth)">
        AuthType shibboleth
        ShibRequestSetting requireSession 1
        ShibExportAssertion Off
        Require valid-user
    </LocationMatch>


4. Enable Shibboleth in fossir
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../_sso_fossir.rst


.. _PostgreSQL wiki: https://wiki.postgresql.org/wiki/YUM_Installation#Configure_your_YUM_repository
.. _Let's Encrypt: https://letsencrypt.org/
