Upgrade fossir from 1.2
=======================

.. warning::
    **ATTENTION: This process is not yet fully tested, use it at your own risk!**
    We are currently working with some of our users running fossir 1.2 in order to ensure migration works reliably
    and without any data loss. If you'd like to help, please `let us know <https://getfossir.io/contact/>`_!


If you're running a version that is lower than 2.0, you will have to run a special migration command provided by the
``fossir-migrate`` package. This document will guide you over the steps needed to perform the upgrade.


Prerequisites
-------------

In order to migrate to version 2.0 of fossir you will first of all need to make sure you have **at least version 1.2**
of fossir installed. Migration of databases using earlier versions will either **fail** or very likely result in
**data loss**. So, please make sure that you are **on 1.2.x** before migrating.

.. warning::

    If you are running a version of the experimental (thus unsupported) **1.9.x branch**, you will have to perform a
    **step-by-step migration**. We hope that, as advised, no-one upgraded to intermediate 1.9.x releases. If you did and
    need help with it, please **ping us on IRC**.


Backing up ZODB
---------------

The migration script doesn't write to the ZODB, but we still recommend that you **make a backup** just in case:

.. code-block:: shell

    repozo -B -F -r <some-place-safe> -f <fossir-db-dir>/Data.fs --verbose


You should replace ``<some-place-safe>`` with the directory in your filesystem where you want to keep the backup.
As for ``<fossir-db-dir>``, that's the directory where the database file is kept. That should be ``/opt/fossir/db`` in
most fossir installations.

Make sure that backup files have been created (you should have an ``*.index`` and an ``*.fs`` file).

Now, let's shut down the ZEO daemon:

.. code-block:: shell

    zdaemon -C /opt/fossir/etc/zdctl.conf stop

Double check that the daemon is not running:

.. code-block:: shell

    zdaemon -C /opt/fossir/etc/zdctl.conf status


Moving legacy data
------------------

fossir 2.0 will use a directory structure that is similar to fossir 1.x, so first of all you will need to rename the old
tree:

.. code-block:: shell

    mv /opt/fossir /opt/fossir-legacy


.. warning::

    After the migration is done, **do not** delete the ``/opt/fossir-legacy`` directory without first moving the
    ``archive`` dir elsewhere. Please read the full guide until the end.



Installing fossir 2.0
---------------------

The first step should be to have a working fossir 2.0 setup. In order to do that, you should follow the regular fossir
2.x installation instructions up to the "Configure fossir" step.  We provide below direct links to the relevant sections
of the installation guides.

On a **Debian/Ubuntu** system:

=========================  =========================
nginx                      Apache
-------------------------  -------------------------
:ref:`deb-pkg`             :ref:`deb-apache-pkg`
:ref:`deb-db`              :ref:`deb-apache-db`
:ref:`deb-web`             :ref:`deb-apache-web`
:ref:`deb-ssl`             :ref:`deb-apache-ssl`
:ref:`deb-install`         :ref:`deb-apache-install`
:ref:`deb-config`          :ref:`deb-apache-config`
=========================  =========================

On a **CentOS7-based system**:

============================  ============================
nginx                         Apache
----------------------------  ----------------------------
:ref:`centos-epel`            :ref:`centos-apache-epel`
:ref:`centos-pkg`             :ref:`centos-apache-pkg`
:ref:`centos-db`              :ref:`centos-apache-db`
:ref:`centos-web`             :ref:`centos-apache-web`
:ref:`centos-ssl`             :ref:`centos-apache-ssl`
:ref:`centos-selinux`         :ref:`centos-apache-selinux`
:ref:`centos-install`         :ref:`centos-apache-install`
:ref:`centos-config`          :ref:`centos-apache-config`
============================  ============================


Configuration Wizard
--------------------

You will then need to run the Configuration Wizard, following the normal installation guide (Debian/Ubuntu or CentOS).
When the wizard asks you about the **"Old archvive dir"**, make sure to set it to the archive dir in the
``fossir-legacy`` directory.


.. code-block:: none

    ...
    If you are upgrading from fossir 1.2, please specify the path to the
    ArchiveDir of the old fossir version.  Leave this empty if you are not
    upgrading.
    Old archive dir: /opt/fossir-legacy/archive
    ...


Running ``fossir-migrate``
--------------------------

First of all, make sure that you are using the **user** and **virtualenv** created using the step **"Install fossir"** and that the legacy dir is owned by this **user**:

.. code-block:: shell

    chown -R fossir /opt/fossir-legacy
    su - fossir
    source ~/.venv/bin/activate


You should then install the package using:

.. code-block:: shell

   pip install fossir-migrate


``fossir-migrate`` requires a series of parameters that have to be tuned according to your current setup. We now provide
a list of values that should work in most standard fossir installations. However, please **carefully read** the
`documentation of the fossir-migrate command <https://github.com/fossir/fossir-migrate>`_, to make
sure there are no option conflicts with your setup.

Most frequenty, ``fossir-migrate postgresql:///fossir file:///opt/fossir-legacy/db/Data.fs`` will work, followed by the following
parameters:

 * ``--archive-dir /opt/fossir-legacy/archive``
 * ``--storage-backend legacy``
 * ``--default-email default@<organization-hostname>``
 * ``--default-currency EUR``
 * ``--symlink-target ~/archive/legacy_symlinks/``
 * ``--symlink-backend legacy-symlinks``
 * ``--migrate-broken-events`` (optional - use it if you want to migrate events that don't
   belong to any category in v1.2.  If any such events exist, the will be added to a new category
   named *Lost & Found*.

(don't forget to replace ``<organization-hostname>`` with the e-mail hostname of your organization)

An example:

.. code-block:: shell

    fossir-migrate postgresql:///fossir file:///opt/fossir-legacy/db/Data.fs --archive-dir /opt/fossir-legacy/archive --storage-backend legacy --default-email default@acme.example.com --default-currency EUR --symlink-target ~/archive/legacy_symlinks/ --symlink-backend legacy-symlinks --migrate-broken-events


.. note::

    If for some reason the migration fails, ``fossir-migrate`` will ask you whether you would like to post an error report
    on a public pastebin (Gist). The link will not be advertised and only the log information that was shown on screen
    (plus the exception traceback that was printed) will be included. If you are not comfortable with letting
    ``fossir-migrate`` post this on a public pastebin, you can always send us your ``migration.log`` file (which gets
    generated automatically).


Post-migration work
-------------------

After the migration is done you may need to apply some adjustments in your ``fossir.conf``. You may want to read our
guide on how to configure an Identity/Authentication provider.

We really recommend as well that you move your old fossir archive (``/opt/fossir-legacy/archive``) inside your new
fossir directory:

.. code-block:: shell

    mv /opt/fossir-legacy/archive /opt/fossir/legacy-archive

The legacy archive will remain **read-only**. You should update your ``fossir.conf`` (``STORAGE_BACKENDS`` option) to
reflect the new path:

.. code-block:: python

    STORAGE_BACKENDS = {
        # ...
        'legacy': 'fs-readonly:/opt/fossir/legacy-archive'
        # ...
    }


Finishing up
------------

You can now proceed with the remaining installation steps:

On a **Debian/Ubuntu** system:

=============================  =============================
nginx                          Apache
-----------------------------  -----------------------------
:ref:`deb-launch`              :ref:`deb-apache-launch`
:ref:`deb-letsencrypt`         :ref:`deb-apache-letsencrypt`
:ref:`deb-user`                :ref:`deb-apache-user`
=============================  =============================


On a **CentOS7-based system**:

================================  ================================
nginx                             Apache
--------------------------------  --------------------------------
:ref:`centos-launch`              :ref:`centos-apache-launch`
:ref:`centos-firewall`            :ref:`centos-apache-firewall`
:ref:`centos-letsencrypt`         :ref:`centos-apache-letsencrypt`
:ref:`centos-user`                :ref:`centos-apache-user`
================================  ================================


Sanitizing HTML
---------------

fossir 2.0 uses `Markdown <https://en.wikipedia.org/wiki/Markdown>`_ for the descriptions of contributions and
categories. Contribution descriptions that previously contained HTML will still work, but new ones will only support
Markdown syntax (including basic HTML).
As for the descriptions of categories, they are interpreted as Markdown as of version 2.0, which means that some
existing data may be broken. In order to make the lives of users who are migrating easier, we have included with
``fossir-migrate`` a command that automatically performs the migration of Category descriptions to Markdown.

First of all, let's see what would be the impact of running the command:

.. code-block:: shell

    fossir-html-sanitize --dry-run -v -l log.html category_descriptions

By opening ``log.html`` you will be able to check if there are any special cases that will need manual intervention.
If you're happy with the changes, you can just choose to save them:

.. code-block:: shell

    fossir-html-sanitize category_descriptions


Removing old data
-----------------

Even if you're sure the migration succeeded and all data was kept, please keep around the backup of your ZODB you
made at the beginning of this guide. **After** and **only after** having **moved the legacy archive** to the new fossir
dir and stored a **backup of your ZODB** in a safe place, you can proceed to delete the old ``/opt/fossir`` directory:

.. code-block:: shell

    rm -rf /opt/fossir-legacy
