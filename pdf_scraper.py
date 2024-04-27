from lib_helpers.pdf_helpers import download_pdfs_to_s3
import os

data_dir = "temp_data"

CONFIGURATION = (os.environ['API_KEY'], os.environ['SECRET_KEY'], 
                 os.environ['ARXIV_REGION'], os.environ['TARGET_REGION'])

BUCKET = os.environ['BUCKET_NAME']

if __name__ == "__main__":
    download_pdfs_to_s3(CONFIGURATION, BUCKET, data_dir, max_files=3, 
                        year=2024, clean_data_directory=True)
