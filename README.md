# update_linux_user_passwd
EC2(Linux)のユーザパスワードを自動でローテーションするやつ

# 準備

## KMS CMK 作成
適当な鍵を作ってKey IDを控える。

## Parameter 作成
SSM Parameter StoreにSecureStringでパラメータを作成する。先の手順で作成したKMS CMKで暗号化する。

## env-xxx.yml 作成

環境設定ファイルを作成する。(以下はenv-sample.yml)

``` yaml
REGION: "{{ Target Region(ex: ap-northeast-1) }}"
ACCOUNT_ID: "{{ Your AWS Account ID(ex:123456789012) }}"
USER_NAME: "ec2-user"
PARAM_STORE_PASSWD_NAME: "{{ Your Parameter Name }}"
KMS_KEY_ID: "{{ Your KMS CMK Key ID }}"
```

# デプロイ

## Serverless Framework をインストールする
Go [Serverless Framework Document](https://serverless.com/framework/docs/providers/aws/guide/installation/).

## デプロイ

`--stage` には、準備で作成した env-xxx.yml の `xxx` を指定する

```
sls deploy --stage=xxx
```

## 実行

```
sls invoke --function=runner --stage=xxx
```

# パスワード取得方法

```
aws ssm get-parameters --name {{ Parameter Name }} --with-decryption --query 'Parameters[*].Value' --output text
```

# ToDo
- セキュリティ強度をあげる
    - KMS CMKのポリシーを変更する処理を加える
