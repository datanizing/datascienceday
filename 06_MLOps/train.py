import boto3
import tarfile
import os

s3 = boto3.client("s3")

s3.download_file(
    Bucket="datascienceday", Key="model.tar.gz", Filename="models/model.tar.gz"
)

with tarfile.open("models/model.tar.gz") as tar:
    tar.extractall("models/.")

os.remove("models/model.tar.gz")