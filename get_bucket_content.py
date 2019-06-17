import os
import sys

from bucket_management import ClBucketManagement

API_KEY = os.getenv("CELLAR_ADDON_KEY_ID")
HOST = os.getenv("CELLAR_ADDON_HOST")
SECRET_KEY = os.getenv("CELLAR_ADDON_KEY_SECRET")


def main():
    if len(sys.argv) != 2 or len(sys.argv) != 3:
        raise Exception("Usage : %s bucket_name dest_folder (optional)" % sys.argv[0])

    bucket_manager = ClBucketManagement(api_key=API_KEY,
                                        secret_key=SECRET_KEY,
                                        host=HOST)

    if sys.argv[1] not in bucket_manager.get_all_bucket():
        raise Exception("Bucket [%s] does not exist !" % sys.argv[1])

    if len(sys.argv) == 3:
        dest_folder = os.path.join(os.getcwd(), sys.argv[2])
    else:
        dest_folder = os.path.join(os.getcwd(), "bucket_" + sys.argv[1])
    os.makedirs(dest_folder, exist_ok=True)

    bucket_manager.get_all_from_bucket(sys.argv[1], dest_fld=dest_folder)


if __name__ == '__main__':
    main()
