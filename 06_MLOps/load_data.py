import boto3

s3 = boto3.client("s3")
s3.download_file(
    Bucket="datascienceday", Key="transport-short.csv", Filename="data/raw/transport-short.csv"
)