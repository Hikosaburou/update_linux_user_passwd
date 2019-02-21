# -*- coding:utf-8 -*-
import boto3
import os
import random
import string
import logging

# ログレベル設定
logger = logging.getLogger()
logLevelTable = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
if 'LOG_LEVEL' in os.environ and os.environ['LOG_LEVEL'] in logLevelTable:
    logLevel = logLevelTable[os.environ['LOG_LEVEL']]
else:
    logLevel = logging.WARNING
logger.setLevel(logLevel)


def random_passwd(passwd_len):
    '''
    Description: 長さpasswd_lenのランダムな文字列を取得する
    '''
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=passwd_len))


def runner(event, context):
    '''
    Description: Lambdaエントリポイント
    '''

    ssm = boto3.client('ssm')

    kms_key_id = os.environ['KMS_KEY_ID']
    param_store_passwd_name = os.environ['PARAM_STORE_PASSWD_NAME']
    region = os.environ['AWS_REGION']
    user_name = os.environ['USER_NAME']

    ### SSM Parameter Store 更新する
    _ = ssm.put_parameter(
        Name=param_store_passwd_name,
        Value=random_passwd(20),
        Type='SecureString',
        KeyId=kms_key_id,
        Overwrite=True)

    ### SSM Run Command する
    runcommand_parameters = {
        'workingDirectory': [""],
        'executionTimeout': ["3600"],
        'commands': [
            'aws --region ' + region + ' \\',
            'ssm get-parameters \\',
            '--names \"' + param_store_passwd_name + '\" \\',
            '--with-decryption --query \"Parameters[*].Value\" \\',
            '--output text | \\',
            'passwd ' + user_name + ' --stdin',
        ]
    }

    _ = ssm.send_command(
        Targets=[
            {
                'Key': 'tag:env',
                'Values': [
                    'prd',
                    'stg',
                    'dev',
                ]
            },
        ],
        DocumentName='AWS-RunShellScript',
        DocumentVersion='$DEFAULT',
        Parameters=runcommand_parameters,
        TimeoutSeconds=600,
        MaxConcurrency='50',
        MaxErrors="0",
    )
