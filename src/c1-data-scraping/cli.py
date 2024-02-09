"""
Module that contains the command line app.
"""
import os
import io
import argparse
import shutil
from google.cloud import storage
from Scraper import *

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

# project and bucket parameters
GCP_PROJECT_ID = "ac215-399020"
BUCKET_NAME = "rehab-image-detection-data"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../secrets/gcp-rehab-ai-secret.json"
path_to_secret_key = "../secrets/gcp-rehab-ai-secret.json"

# local and GCS folders names to store scraped images
FIXER_FOLDER_NAME = "fixer-upper"
RENOVATED_FOLDER_NAME = "renovated"

# URLS to scrape
FIXER_URLS_TO_SCRAPE = ['https://newyork.craigslist.org/search/ossining-ny/rea?bundleDuplicates=1&hasPic=1&lat=41.1673&lon=-73.8379&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://cedarrapids.craigslist.org/search/middle-amana-ia/rea?bundleDuplicates=1&hasPic=1&lat=41.8024&lon=-91.9241&query=fixer%20upper&search_distance=550#search=1~gallery~0~0',
      'https://siouxfalls.craigslist.org/search/lake-park-ia/rea?bundleDuplicates=1&hasPic=1&lat=43.4313&lon=-95.3152&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://oklahomacity.craigslist.org/search/cromwell-ok/rea?bundleDuplicates=1&hasPic=1&lat=35.3627&lon=-96.3548&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://shoals.craigslist.org/search/russellville-al/rea?bundleDuplicates=1&hasPic=1&lat=34.4789&lon=-87.6851&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://littlerock.craigslist.org/search/story-ar/rea?bundleDuplicates=1&hasPic=1&lat=34.5177&lon=-93.4784&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://amarillo.craigslist.org/search/white-deer-tx/rea?bundleDuplicates=1&hasPic=1&lat=35.3671&lon=-101.2498&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://fortdodge.craigslist.org/search/humboldt-ia/rea?bundleDuplicates=1&hasPic=1&lat=42.7087&lon=-94.232&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://wyoming.craigslist.org/search/powder-river-wy/rea?bundleDuplicates=1&hasPic=1&lat=43.3491&lon=-106.8546&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://boise.craigslist.org/search/idaho-city-id/rea?bundleDuplicates=1&hasPic=1&lat=43.9336&lon=-115.7391&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://nashville.craigslist.org/search/dickson-tn/rea?bundleDuplicates=1&hasPic=1&lat=36.0844&lon=-87.4926&query=fixer%20upper&search_distance=390#search=1~gallery~0~0',
      'https://littlerock.craigslist.org/search/hot-springs-national-park-ar/rea?bundleDuplicates=1&hasPic=1&lat=34.5295&lon=-93.0207&query=fixer%20upper&search_distance=370#search=1~gallery~0~0',
      'https://monroe.craigslist.org/search/marion-la/rea?bundleDuplicates=1&hasPic=1&lat=32.9349&lon=-92.2852&query=fixer%20upper&search_distance=290#search=1~gallery~0~0',
      'https://dallas.craigslist.org/search/italy-tx/rea?bundleDuplicates=1&hasPic=1&lat=32.1198&lon=-96.8774&query=fixer%20upper&search_distance=290#search=1~gallery~0~0',
      'https://nacogdoches.craigslist.org/search/garrison-tx/rea?bundleDuplicates=1&hasPic=1&lat=31.8199&lon=-94.5245&query=fixer%20upper&search_distance=220#search=1~gallery~0~0',
      'https://collegestation.craigslist.org/search/burlington-tx/rea?bundleDuplicates=1&hasPic=1&lat=31.0026&lon=-96.8596&query=fixer%20upper&search_distance=168#search=1~gallery~0~0',
      'https://westslope.craigslist.org/search/hanksville-ut/rea?bundleDuplicates=1&hasPic=1&lat=37.9362&lon=-110.4813&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://eastky.craigslist.org/search/pinsonfork-ky/rea?bundleDuplicates=1&hasPic=1&lat=37.5264&lon=-82.2216&query=fixer%20upper&search_distance=590#search=1~gallery~0~0',
      'https://westslope.craigslist.org/search/torrey-ut/rea?bundleDuplicates=1&hasPic=1&lat=38.2037&lon=-110.918&query=fixer%20upper&search_distance=550#search=1~gallery~0~0',
      'https://bozeman.craigslist.org/search/yellowstone-national-park-wy/rea?bundleDuplicates=1&hasPic=1&lat=44.6363&lon=-110.0213&query=fixer%20upper&search_distance=690#search=1~gallery~0~0']

RENOVATED_URLS_TO_SCRAPE = ['https://bgky.craigslist.org/search/woodbury-ky/rea?bundleDuplicates=1&hasPic=1&lat=37.089&lon=-86.6147&min_price=100000&query=renovated&search_distance=810#search=1~gallery~0~0',
      'https://nwks.craigslist.org/search/wilsonville-ne/rea?bundleDuplicates=1&hasPic=1&lat=40.0565&lon=-100.0696&min_price=100000&query=renovated&search_distance=810#search=1~gallery~0~0',
      'https://scottsbluff.craigslist.org/search/crook-co/rea?bundleDuplicates=1&hasPic=1&lat=40.9897&lon=-102.795&min_price=100000&query=renovated&search_distance=630#search=1~gallery~0~0',
      'https://elko.craigslist.org/search/montello-nv/rea?bundleDuplicates=1&hasPic=1&lat=41.5994&lon=-113.9402&min_price=100000&query=renovated&search_distance=630#search=1~gallery~0~0',
      'https://columbiamo.craigslist.org/search/arrow-rock-mo/rea?bundleDuplicates=1&hasPic=1&lat=39.1383&lon=-92.8717&query=renovated&search_distance=600#search=1~gallery~0~0',
      'https://boston.craigslist.org/search/boston-ma/rea?lat=42.3583&lon=-71.0603&min_price=100000&query=renovated&search_distance=1000#search=1~gallery~0~0',
      'https://tulsa.craigslist.org/search/quinton-ok/rea?bundleDuplicates=1&hasPic=1&lat=35.1979&lon=-95.5471&query=renovated&search_distance=600#search=1~gallery~0~0',
      'https://evansville.craigslist.org/search/wheatland-in/rea?bundleDuplicates=1&hasPic=1&lat=38.6386&lon=-87.2612&query=renovated&search_distance=580#search=1~gallery~0~0',
      'https://littlerock.craigslist.org/search/gurdon-ar/rea?bundleDuplicates=1&hasPic=1&lat=33.951&lon=-92.9979&query=renovated&search_distance=330#search=1~gallery~0~0',
      'https://tuscaloosa.craigslist.org/search/bankston-al/rea?bundleDuplicates=1&hasPic=1&lat=33.7833&lon=-87.647&query=renovated&search_distance=330#search=1~gallery~0~0',
      'https://atlanta.craigslist.org/search/roopville-ga/rea?bundleDuplicates=1&hasPic=1&lat=33.4681&lon=-85.1735&query=renovated&search_distance=330#search=1~gallery~0~0',
      'https://jacksonville.craigslist.org/search/saint-george-ga/rea?bundleDuplicates=1&hasPic=1&lat=30.7101&lon=-82.2709&query=renovated&search_distance=330#search=1~gallery~0~0',
      'https://treasure.craigslist.org/search/okeechobee-fl/rea?bundleDuplicates=1&hasPic=1&lat=27.0004&lon=-80.8594&query=renovated&search_distance=152#search=1~gallery~0~0'

      ]



# make local folders if they don't exist yet
def makedirs():
    os.makedirs(RENOVATED_FOLDER_NAME, exist_ok=True)
    os.makedirs(FIXER_FOLDER_NAME, exist_ok=True)


# function to download images from google cloud storage to local folder
def download():
    print("downloading from GCS bucket to local folder")

    # Clear
    shutil.rmtree(FIXER_FOLDER_NAME, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=GCP_PROJECT_ID)

    bucket = storage_client.bucket(BUCKET_NAME)

    blobs = bucket.list_blobs(prefix=FIXER_FOLDER_NAME + "/")
    for blob in blobs:
        print(blob.name)
        if blob.name.endswith(".txt"):
            blob.download_to_filename(blob.name)


# function to scrape images from website
def scrapeCraigslist():
    print("scraping images from Craigslist with default parameters")
    makedirs()
    scrape(FIXER_FOLDER_NAME, FIXER_URLS_TO_SCRAPE)
    scrape(RENOVATED_FOLDER_NAME, RENOVATED_URLS_TO_SCRAPE)


# function to upload images from local folder to google cloud storage
def upload():
    print("Uploading from local folder to GCS bucket")
    makedirs()


    def list_files_in_gcs_folder(bucket_name, folder_prefix): 
        """
        Lists all file paths in a specific GCS folder this will ensure we dont upload the same file twice.

        :param bucket_name: Name of the GCS bucket.
        :param folder_prefix: Folder name (prefix) in GCS.
        :return: List of file paths within the folder.
        """
        
        # Initialize the GCS client
        # storage_client = storage.Client.from_service_account_json('secrets/secret_key_fixer_upper.json')
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Fetch all blob names with the given folder prefix
        blob_names = [blob.name for blob in bucket.list_blobs(prefix=folder_prefix)]
        
        return blob_names
    
    file_paths = list_files_in_gcs_folder(BUCKET_NAME, FIXER_FOLDER_NAME)

    # Recursively list all files in a directory and its subdirectories
    def upload_folder_to_gcs(bucket_name, source_folder_path, destination_folder_path):
        """
        Uploads a local folder to Google Cloud Storage.

        :param bucket_name: Name of the GCS bucket.
        :param source_folder_path: Local path to the folder you want to upload.
        :param destination_folder_path: Path in GCS where the folder should be uploaded.
        """
        
        # Initialize the GCS client
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Check if the root directory already exists in GCS
        root_directory_blob = bucket.blob(destination_folder_path)
        
        # Walk through each file in the local folder
        for dirpath, dirnames, filenames in os.walk(source_folder_path):
            for filename in filenames:
                # Construct the full local path
                local_file = os.path.join(dirpath, filename)
                
                # Construct the full GCS path
                remote_path = os.path.join(destination_folder_path, os.path.relpath(local_file, source_folder_path))
                
                if remote_path not in file_paths:
                # Upload the file
                    blob = bucket.blob(remote_path)
                    blob.upload_from_filename(local_file)
                    print(f"File {local_file} uploaded to {remote_path} in bucket {bucket_name}.")
                else:
                    print('file exists')
    file_paths = list_files_in_gcs_folder(BUCKET_NAME, FIXER_FOLDER_NAME) #bucket name and folder name
    upload_folder_to_gcs(bucket_name=BUCKET_NAME, source_folder_path=FIXER_FOLDER_NAME, destination_folder_path=FIXER_FOLDER_NAME)
    
    file_paths = list_files_in_gcs_folder(BUCKET_NAME, RENOVATED_FOLDER_NAME) #bucket name and folder name
    upload_folder_to_gcs(BUCKET_NAME , RENOVATED_FOLDER_NAME, RENOVATED_FOLDER_NAME)


    # Recursively list all files in a directory and its subdirectories
    
    print("Upload complete!")


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.upload:
        upload()
    if args.scrapeCraigslist:
        scrapeCraigslist()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Generate text from prompt")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download images from GCS bucket",
    )

    parser.add_argument(
        "-s", "--scrapeCraigslist", action="store_true", help="Scrape new images from Craigslist"
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload images to GCS bucket",
    )

    args = parser.parse_args()

    main(args)
