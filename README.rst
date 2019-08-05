=================
MySQL Dump Script
=================


Configure boto3
---------------
First, install the library `boto3 <https://github.com/boto/boto3>`__ and set a default region.
Also read documentation for `Yandex.Cloud <https://cloud.yandex.ru/docs/storage/instruments/boto>`__

.. code-block:: sh

    $ pip install boto3

Next, set up credentials (in e.g. ``~/.aws/credentials``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

Then, set up a default region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    region=us-east-1


Edit Script Config
------------------
Example config file:

.. code-block:: cfg

    [S3]
    Bucket = BUCKET_NAME

    [Database]
    HomeUser = /home/YOUR_NAME/
    Host = YOUR_DB_HOST
    User = YOUR_DB_USER
    Pass = YOUR_DB_PASS
    DB = db1 db2 db3 db4
    BackupPath = /home/YOUR_NAME/sql-backups/


Crontab and docs
----------------

Crontab
~~~~~~~
You can use this script in crontab.
See `crontab guide <https://linuxconfig.org/linux-crontab-reference-guide>`__


Yandex.Cloud Object Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you use Yandex.Cloud S3 see `this page <https://cloud.yandex.ru/docs/storage/instruments/boto#preparations>`__


Third party
-----------
`Boto3 <https://github.com/boto/boto3>`__
