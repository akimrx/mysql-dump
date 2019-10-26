#!/usr/bin/env python3

import os
import boto3
import pathlib
import configparser

from logger import logger
from datetime import datetime



try:
    config_path = pathlib.Path.home().joinpath('.ya-tools/')
    if not os.path.exists(config_path):
            os.system('mkdir -p {path}'.format(path=config_path))
    config_file = pathlib.Path.home().joinpath('.ya-tools/sqlbackup.cfg')
    config = configparser.RawConfigParser()
    config.read(config_file)
    home = config.get('Database', 'HomeUser')
    db_host = config.get('Database', 'Host')
    db_user = config.get('Database', 'User')
    db_pass = config.get('Database', 'Pass')
    db_names = config.get('Database', 'DB').split(' ')
    backup_path = config.get('Database', 'BackupPath')
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
    s3_bucket = config.get('S3', 'Bucket')
except configparser.NoSectionError:
    print("Corrupted config or no config file present. Check ~/.ya-tools/sqlbackup.cfg ")
    logger.error("Corrupted config or no config file present. Check ~/.ya-tools/sqlbackup.cfg")
    quit()


def call_time():
    current_time = datetime.now()
    raw_time = current_time.strftime('%d-%m-%Y')
    return str(raw_time)


def create_backup(host, user, passwd, database):
    backup_name = f'{backup_path}{call_time()}-{database}.sql'
    if os.path.isfile(backup_name):
        logger.info(f'Backup {backup_name} already exist')
    else:
        dump = f'mysqldump -h{host} -u{user} -p{passwd} {database} > {backup_name}'
        command = os.system(dump)
        if os.path.isfile(backup_name):
            logger.info(f'Backup for {database} created')
        else:
            logger.error(f'Backup not created for {database}')


# Later...
def delete_local_backups(path):
    directory = os.listdir(path)
    for file in directory:
        pass


# S3 storage upload
# https://github.com/boto/boto3/blob/develop/README.rst#quick-start
# https://cloud.yandex.ru/docs/storage/instruments/boto

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


def upload_file(file):
    s3.upload_file(f'{backup_path}{file}', f'{s3_bucket}', f'sql-backups/{file}')
    get_object_response = s3.get_object(Bucket=f'{s3_bucket}',Key=f'sql-backups/{file}')
    return get_object_response


def main():
    for database in db_names:
        create_backup(db_host, db_user, db_pass, database)
    files = os.listdir(backup_path)
    for file in files:
        result = upload_file(file)
        final = result['ResponseMetadata']['HTTPStatusCode']
        if final == 200:
            os.system(f'rm -f {backup_path}{file}')
            logger.info(f'File {file} uploaded to S3 and deleted from local storage')
        else:
            logger.warning(f'Upload failed for {file}')


if __name__ == '__main__':
    main()
