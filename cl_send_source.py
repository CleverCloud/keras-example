import os
import sys

from bucket_management import ClBucketManagement

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("CELLAR_ADDON_KEY_ID")
HOST = os.getenv("CELLAR_ADDON_HOST")
SECRET_KEY = os.getenv("CELLAR_ADDON_KEY_SECRET")

BUCKET_NAME = os.getenv("BUCKET_SOURCE")


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage : %s path/to/the/source/folder" % sys.argv[0])

    path = os.path.join(os.getcwd(), sys.argv[1])
    if not os.path.exists(path):
        path = sys.argv[1]
    if not os.path.exists(path):
        raise Exception("%s is not a relative or an absolute path" % sys.argv[1])
    if not os.path.isdir(path):
        raise Exception("Path must be a directory")

    bucket_manager = ClBucketManagement(api_key=API_KEY,
                                        secret_key=SECRET_KEY,
                                        host=HOST)

    bucket_name = BUCKET_NAME

    if bucket_name not in bucket_manager.get_all_bucket():
        bucket_manager.create_bucket(bucket_name)
    else:
        ret = input("Already existing source bucket erase it ?")
        if ret.lower() == ("yes" or "y"):
            bucket_manager.delete_bucket(bucket_name, allow_full_bucket_deletion=True)
            bucket_manager.create_bucket(bucket_name)

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            bucket_manager.save_big_files(bucket_name, file, file_path)


if __name__ == '__main__':
    main()
