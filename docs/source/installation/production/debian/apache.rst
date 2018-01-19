Apache
======

.. _deb-apache-pkg:

1. Install Packages
-------------------

PostgreSQL is installed from its upstream repos to get a much more recent version.

.. code-block:: shell

    apt install -y lsb-release wget
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
    apt update
    apt install -y --install-recommends postgresql-9.6 libpq-dev apache2 libapache2-mod-proxy-uwsgi libapache2-mod-xsendfile python-dev python-virtualenv libxslt1-dev libxml2-dev libffi-dev libpcre3-dev libyaml-dev build-essential redis-server uwsgi uwsgi-plugin-python


If you use Debian, run this command:

.. code-block:: shell

    apt install -y libjpeg62-turbo-dev


If you use Ubuntu, run this instead:

.. code-block:: shell

    apt install -y libjpeg-turbo8-dev zlib1g-dev

Afterwards, make sure the services you just installed are running:

.. code-block:: shell

    systemctl start postgresql.service redis-server.service


.. _deb-apache-db:

2. Create a Database
--------------------

Let's create a user and database for fossir and enable the necessary Postgres
extensions (which can only be done by the Postgres superuser).

.. code-block:: shell

    su - postgres -c 'createuser fossir'
    su - postgres -c 'createdb -O fossir fossir'
    su - postgres -c 'psql fossir -c "CREATE EXTENSION unaccent; CREATE EXTENSION pg_trgm;"'

.. warning::

    Do not forget to setup a cronjob that creates regular database
    backups once you start using fossir in production!


.. _deb-apache-web:

3. Configure uWSGI & Apache
---------------------------

The default uWSGI and Apache configuration files should work fine in
most cases.

.. code-block:: shell

    ln -s /etc/uwsgi/apps-available/fossir.ini /etc/uwsgi/apps-enabled/fossir.ini
    cat > /etc/uwsgi/apps-available/fossir.ini <<'EOF'
    [uwsgi]
    uid = fossir
    gid = www-data
    umask = 027

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

    cat > /etc/apache2/sites-available/fossir-sslredir.conf <<'EOF'
    <VirtualHost *:80>
        ServerName YOURHOSTNAME
        RewriteEngine On
        RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
    </VirtualHost>
    EOF

    cat > /etc/apache2/sites-available/fossir.conf <<'EOF'
    <VirtualHost *:443>
        ServerName YOURHOSTNAME
        DocumentRoot "/var/empty/apache"

        SSLEngine             on
        SSLCertificateFile    /etc/ssl/fossir/fossir.crt
        SSLCertificateKeyFile /etc/ssl/fossir/fossir.key
        SSLProtocol           all -SSLv2 -SSLv3
        SSLCipherSuite        ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS
        SSLHonorCipherOrder   on

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


Now enable the necessary modules and the fossir site in apache:

.. code-block:: shell

    a2enmod proxy_uwsgi rewrite ssl xsendfile
    a2dissite 000-default
    a2ensite fossir fossir-sslredir


.. _deb-apache-ssl:

4. Create an SSL Certificate
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


.. _deb-apache-install:

5. Install fossir
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
    Group=www-data
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

    useradd -rm -g www-data -d /opt/fossir -s /bin/bash fossir
    su - fossir


You are now ready to install fossir:

.. code-block:: shell

    virtualenv ~/.venv
    source ~/.venv/bin/activate
    pip install -U pip setuptools
    pip install --pre fossir


.. _deb-apache-config:

6. Configure fossir
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
    echo -e "\nSTATIC_FILE_METHOD = 'xsendfile'" >> ~/etc/fossir.conf


7. Create database schema
-------------------------

Finally, you can create the database schema and switch back to *root*:

.. code-block:: shell

    fossir db prepare
    exit


.. _deb-apache-launch:

8. Launch fossir
----------------

You can now start fossir and set it up to start automatically when the
server is rebooted:

.. code-block:: shell

    systemctl restart uwsgi.service apache2.service fossir-celery.service
    systemctl enable uwsgi.service apache2.service postgresql.service redis-server.service fossir-celery.service


.. _deb-apache-letsencrypt:

9. Optional: Get a Certificate from Let's Encrypt
-------------------------------------------------

.. note::

    You need to use at least Debian 9 (Stretch) to use certbot.
    If you are still using Debian 8 (Jessie), consider updating
    or install certbot from backports.


If you use Ubuntu, install the certbot PPA:

.. code-block:: shell

    apt install -y software-properties-common
    add-apt-repository -y ppa:certbot/certbot
    apt update


To avoid ugly SSL warnings in your browsers, the easiest option is to
get a free certificate from Let's Encrypt. We also enable the cronjob
to renew it automatically:


.. code-block:: shell

    apt install -y python-certbot-apache
    certbot --apache --rsa-key-size 4096 --no-redirect --staple-ocsp -d YOURHOSTNAME
    rm -rf /etc/ssl/fossir
    systemctl start certbot.timer
    systemctl enable certbot.timer


.. _deb-apache-user:

10. Create an fossir user
-------------------------

Access ``https://YOURHOSTNAME`` in your browser and follow the steps
displayed there to create your initial user.


Optional: Shibboleth
--------------------

If your organization uses Shibboleth/SAML-based SSO, follow these steps to use
it in fossir:

1. Install Shibboleth
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    apt install -y libapache2-mod-shib2
    a2enmod shib2

2. Configure Shibboleth
^^^^^^^^^^^^^^^^^^^^^^^

This is outside the scope of this documentation and depends on your
environment (Shibboleth, SAML, ADFS, etc).  Please contact whoever
runs your SSO infrastructure if you need assistance.

3. Enable Shibboleth in Apache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add the following code to your ``/etc/apache2/sites-available/fossir.conf``
right before the ``AliasMatch`` lines:

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
