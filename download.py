import os
import boto3

session = boto3.session.Session()
client = session.client('s3',
                        region_name='sfo2',
                        endpoint_url='https://sfo2.digitaloceanspaces.com',
                        aws_access_key_id='',
                        aws_secret_access_key='')

client.download_file('zend-storage',
                     'documents/19/5gZ1iTwyPhzRUGQ9cttqt6C16kRrg700gJxKDCMn.pdf',
                     'check.pdf')
