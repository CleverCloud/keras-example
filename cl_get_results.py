import os
import sys

from bucket_management import ClBucketManagement

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("CELLAR_ADDON_KEY_ID")
HOST = os.getenv("CELLAR_ADDON_HOST"
SECRET_KEY = os.getenv("CELLAR_ADDON_KEY_SECRET")

BUCKET_NAME = os.getenv("BUCKET_RESULT")


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage : %s : path to dest folder" %sys.argv[0])

    bucket_manager = ClBucketManagement(api_key=API_KEY,
                                        secret_key=SECRET_KEY,
                                        host=HOST)
    bucket_name = BUCKET_NAME

    if bucket_name not in bucket_manager.get_all_bucket():
        raise Exception("Bucket [%s] does not exist !" % bucket_name)

    dest_folder = os.path.join(os.getcwd(), sys.argv[1])
    os.makedirs(dest_folder, exist_ok=True)

    bucket_manager.get_all_from_bucket(bucket_name, dest_fld=dest_folder)


if __name__ == '__main__':
    main()
