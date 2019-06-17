import math
import os

from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from filechunkio import FileChunkIO


class ClBucketManagement(object):

    def __init__(self, api_key, secret_key, host):
        self.bucket_dict = dict()

        cf = OrdinaryCallingFormat()
        self.conn = S3Connection(aws_access_key_id=api_key, aws_secret_access_key=secret_key, host=host,
                                 calling_format=cf)

    def _bucket_connection(self, bucket_name):
        if bucket_name in self.bucket_dict.keys():
            return self.bucket_dict[bucket_name]
        bucket_name_list = [x.name for x in self.conn.get_all_buckets()]
        if bucket_name not in bucket_name_list:
            raise Exception("Bucket name [%s] does not exist" % bucket_name)
        self.bucket_dict[bucket_name] = self.conn.get_bucket(bucket_name)
        return self.bucket_dict[bucket_name]

    def save_big_files(self, bucket_name, key_id, source_file_path, chunk_sze=52428800):

        source_size = os.stat(source_file_path).st_size

        bucket = self._bucket_connection(bucket_name)

        mp = bucket.initiate_multipart_upload(key_id)

        chunk_size = chunk_sze
        chunk_count = int(math.ceil(source_size / float(chunk_size)))

        for i in range(chunk_count):
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_file_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)

        mp.complete_upload()

    def save_file(self, bucket_name, source_file_path):
        bucket = self._bucket_connection(bucket_name)

        k = Key(bucket)
        k.set_contents_from_filename(source_file_path)

    def get_data(self, bucket_name, key_id, dest_fld=None):
        if dest_fld is None:
            dest_fld = os.getcwd()
        elif not os.path.exists(dest_fld):
            raise Exception("dest path does not exist : %s" % dest_fld)

        bucket = self._bucket_connection(bucket_name)
        k = Key(bucket)
        k.key = key_id
        k.get_contents_to_filename(os.path.join(dest_fld, key_id))

    def get_all_key(self, bucket_name):
        bucket = self._bucket_connection(bucket_name)
        return [x.name for x in bucket.list()]

    def get_all_from_bucket(self, bucket_name, dest_fld=None):
        if dest_fld is None:
            dest_fld = os.getcwd()
        elif not os.path.exists(dest_fld):
            raise Exception("dest path does not exist : %s" % dest_fld)

        for key in self.get_all_key(bucket_name):
            self.get_data(bucket_name, key, dest_fld)

    def get_all_bucket(self):
        return [x.name for x in self.conn.get_all_buckets()]

    def create_bucket(self, bucket_name):
        bucket_name_list = self.get_all_bucket()
        if bucket_name in bucket_name_list:
            raise Exception("Already existing Bucket")

        bucket = self.conn.create_bucket(bucket_name)
        self.bucket_dict[bucket_name] = bucket
        return bucket

    def delete_keys(self, bucket_name, keys):
        bucket = self._bucket_connection(bucket_name)
        keys = keys if isinstance(keys, list) else [keys]
        for k in keys:
            bucket.get_key(k).delete()

    def delete_bucket(self, bucket_name, allow_full_bucket_deletion=False):
        bucket = self._bucket_connection(bucket_name)
        if allow_full_bucket_deletion:
            for key in bucket.list():
                key.delete()
        self.conn.delete_bucket(bucket_name)
        del self.bucket_dict[bucket_name]
