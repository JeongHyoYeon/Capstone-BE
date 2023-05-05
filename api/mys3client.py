import boto3
import uuid

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try:
            file_id = str(uuid.uuid4())
            extra_args = {'ContentType': file.content_type}

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,  # bucket
                    file_id,  # key
                    ExtraArgs=extra_args
                )
            return file_id, f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except Exception as e:
            print(e)
            return None

    # def download(self, file):
    #     # s3_resource = boto3.resource('s3')
    #     # object = s3_resource.Object(self.bucket_name, str(file.file_key))
    #     # metadata = object.metadata
    #     # save_file = file.file_name + metadata['ContentType']
    #     # TODO: 파일 확장자 메타데이터 받아올 수 있으면 수정하기, 다운로드 경로 수정
    #     save_file = file.file_name + ".jpeg"
    #     self.s3_client.download_file(
    #         self.bucket_name,  # bucket
    #         str(file.file_key),  # key
    #         save_file  # filename
    #     )

    def get_file(self, file_key):
        # return self.s3_client.get_object(Bucket=self.bucket_name, Key=str(file_key))
        s3_resource = boto3.resource('s3')
        object = s3_resource.Object(self.bucket_name, str(file_key))
        return object

    def delete(self, file):
        self.s3_client.delete_object(self.bucket_name, str(file.file_key))
