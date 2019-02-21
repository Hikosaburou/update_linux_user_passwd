# -*- coding:utf-8 -*-
import boto3
import os
import unittest
import sys
from moto import mock_ssm

os.environ['AWS_REGION']='ap-northeast-1'
os.environ['KMS_KEY_ID']='xxxxxxxxxx'
os.environ['PARAM_STORE_PASSWD_NAME']='ec2-passwd'
os.environ['USER_NAME']='ec2-user'

import updateEc2UserPassword

class UpdateEc2UserPassword(unittest.TestCase):

    @mock_ssm
    def test_runner(self):
        '''
        Description: ざっくりテスト
        '''
        updateEc2UserPassword.runner({}, None)
