"""Script to scrape pdfs from arxiv's S3 buckets"""

import boto3, botocore, configparser
import os, json
from botocore.exceptions import ClientError
from datetime import datetime
import tarfile, logging

import os

def setup(s3resource, configuration):
    """Creates S3 resource & sets configs to enable download.

    Cited from Breanna Herold

    https://towardsdatascience.com/how-to-bulk-access-arxiv-full-text-preprints-58026e19e8ef

    Modified to use environment variables for AWS access keys.
    """

    print("Connecting to Amazon S3...")

    # Securely import configs from private config file
    # configs = configparser.ConfigParser()
    # configs.read("config.ini")

    access_key = configuration[0]
    secret_key = configuration[1]
    region = configuration[2]

    # Create S3 resource & set configs

    s3resource = boto3.resource(
        "s3",  # the AWS resource we want to use
        # aws_access_key_id=configs["DEFAULT"]["ACCESS_KEY"],
        # aws_secret_access_key=configs["DEFAULT"]["SECRET_KEY"],
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,  # same region arxiv bucket is in
    )

    return s3resource


def download_file(s3resource, key, bucket="arxiv"):
    """
    Downloads given filename from source bucket to destination directory.
    Parameters
    ----------
    key : str
        Name of file to download

    Cited from Breanna Herold

    https://towardsdatascience.com/how-to-bulk-access-arxiv-full-text-preprints-58026e19e8ef
    """

    # Ensure src directory exists
    if not os.path.isdir("src"):
        os.makedirs("src")

    # Download file
    print("\nDownloading s3://arxiv/{} to {}...".format(key, key))

    try:
        s3resource.meta.client.download_file(
            Bucket=bucket,
            Key=key,  # name of file to download from
            Filename=key,  # path to file to download to
            ExtraArgs={"RequestPayer": "requester"},
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("ERROR: " + key + " does not exist in arxiv bucket")

    return


def extract_tar(name, data_dir, ext="pdf"):
    """Extracts files from tar file into data directory with given extension."""
    # Open tar file
    tar = tarfile.open(name, "r")

    # List files in tar
    print("\nFiles in tar:")
    for file in tar.getmembers():
        if file.name.endswith(ext):
            print(" Extracting", file.name)
            tar.extract(file, path=data_dir)
        else:
            pass

    # Close tar file
    tar.close()


def begin_download(s3resource, data_dir, max_files=10, year=2024):
    """Sets up download of tars from arxiv bucket.

    Cited from Breanna Herold

    https://towardsdatascience.com/how-to-bulk-access-arxiv-full-text-preprints-58026e19e8ef

    Modified to download only tars from certain years and to download a limited number of files.
    """

    print("Beginning tar download & extraction...")

    file_count = 0
    year = str(year)[-2:]

    # Create a reusable Paginator
    paginator = s3resource.meta.client.get_paginator("list_objects_v2")

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(
        Bucket="arxiv", RequestPayer="requester", Prefix="src/"
    )

    # Download and extract tars
    numFiles = 0
    for page in page_iterator:
        numFiles = 0
        for page in page_iterator:
            numFiles = numFiles + len(page["Contents"])
            for file in page["Contents"]:
                key = file["Key"]
                # If current file is a tar
                if file_count == max_files:
                    break
                elif key.endswith(".tar") and key.split("_")[-2].startswith("24"):
                    download_file(s3resource, key)
                    print("Extracted " + key + "...")
                    extract_tar(key, data_dir)
                    os.remove(key)
                    file_count += 1
                else:
                    pass


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("response for upload is " + response + "for filename:" + file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_pdfs(s3resource, data_dir, bucket):
    """Uploads pdfs in data directory to s3 bucket."""
    for folder in os.listdir(data_dir):
        if os.path.isdir(folder):
            for file in os.listdir(data_dir + "/" + folder):
                print("Uploading " + file + "...")
                try:
                    upload_file(data_dir + "/" + folder + "/" + file, bucket, file)
                except Exception as e:
                    print(e, "Error uploading file")
        else:
            print("File" + folder + "is not a directory")

def clean(data_dir):
    """Cleans data directory of extracted files."""
    for folder in os.listdir(data_dir):
        if os.path.isdir(folder):
            for file in os.listdir(data_dir + "/" + folder):
                os.remove(data_dir + "/" + folder + "/" + file)
        else:
            print("File" + folder + "is not a directory")

    return


def download_pdfs_to_s3(
    configuration,
    s3_bucket_name,
    data_dir,
    max_files=3,
    year=2024,
    clean_data_directory=True,
):

    """Runs the above functions to successfully scrape arxiv and upload to a specific bucket"""

    s3resource = None

    # configuration = (os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])

    s3resource = setup(s3resource, configuration)

    begin_download(s3resource, data_dir, max_files=max_files, year=year)
    print("Am I uploading?")
    upload_pdfs(s3resource, data_dir, s3_bucket_name)
    print("Finished uploading?")
    if clean_data_directory:
        clean(data_dir)

    return


def download_pdfs_from_s3(configuration, bucket, data_dir):
    """Downloads pdfs from bucket to data directory.

    This is to facilitate processing for the Vector Database"""

    print("Beginning pdf download & extraction...")
    s3resource = None
    s3resource = setup(s3resource, configuration)
    s3 = boto3.client("s3")

    # Create a reusable Paginator
    paginator = s3resource.meta.client.get_paginator("list_objects_v2")

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(
        Bucket=bucket,
        RequestPayer="requester",
    )

    # Download and extract tars
    numFiles = 0
    for page in page_iterator:
        numFiles = 0
        for page in page_iterator:
            numFiles = numFiles + len(page["Contents"])
            for file in page["Contents"]:
                key = file["Key"]
                print("Downloading file : ", key)
                s3.download_file(bucket, key, data_dir + key)
                
                # OSAMA AFRICAN SUDANESE SUPERTIME

                # Remove the file from the directory
                os.remove(data_dir + key)