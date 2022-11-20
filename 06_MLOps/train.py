import boto3
import tarfile
import os

s3 = boto3.client("s3")

s3.download_file(
    Bucket="datascienceday", Key="model.tar.gz", Filename="models/model.tar.gz"
)

with tarfile.open("models/model.tar.gz") as tar:
    def is_within_directory(directory, target):
        
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
    
        prefix = os.path.commonprefix([abs_directory, abs_target])
        
        return prefix == abs_directory
    
    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
    
        tar.extractall(path, members, numeric_owner=numeric_owner) 
        
    
    safe_extract(tar, "models/.")

os.remove("models/model.tar.gz")