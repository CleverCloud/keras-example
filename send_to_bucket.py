import os
import sys

from bucket_management import ClBucketManagement

API_KEY = os.getenv("CELLAR_ADDON_KEY_ID")
HOST = os.getenv("CELLAR_ADDON_HOST",)
SECRET_KEY = os.getenv("CELLAR_ADDON_KEY_SECRET",)


def main():
    if len(sys.argv) != 3:
        raise Exception("Usage : %s bucket_target file" % sys.argv[0])

    path = os.path.join(os.getcwd(), sys.argv[2])
    if not os.path.exists(path):
        path = sys.argv[2]
    if not os.path.exists(path):
        raise Exception("%s is not a relative or an absolute path" % sys.argv[2])
    if not os.path.isfile(path):
        raise Exception("%s is not a file" % path)

    bucket_manager = ClBucketManagement(api_key=API_KEY,
                                        secret_key=SECRET_KEY,
                                        host=HOST)

    bucket_name = sys.argv[1]

    if bucket_name not in bucket_manager.get_all_bucket():
        bucket_manager.create_bucket(bucket_name)

    bucket_manager.save_big_files(bucket_name, os.path.basename(path), path)


if __name__ == '__main__':
    main()
