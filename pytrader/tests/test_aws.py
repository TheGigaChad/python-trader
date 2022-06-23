import os
from pathlib import Path

import boto3

from pytrader import config

THIS_DIR = Path(__file__).parent
DATA_PATH = THIS_DIR / 'data'


def test_aws_bucket_upload_download():
    """
    Tests the uploading and downloading of a test file to the aws S3 server.
    """
    # TODO - use model manager
    # model_manager: models.modelManager = models.ModelManager()
    # Upload test file
    test_file_name: str = "aws_upload_download_test_item.csv"
    input_path: str = str(DATA_PATH / test_file_name)
    # asset: common.Asset = common.Asset("TEST", common.AssetType.UNKNOWN)
    # model: models.ModelPackage = model_manager.create_model_package(asset)
    # model_manager.upload_cloud_model(model)

    s3 = boto3.client("s3")
    s3.upload_file(
        Bucket=config.AWS_MODEL_BUCKET_NAME,
        Key=test_file_name,
        Filename=input_path
    )
    # Download test file
    test_file_name_out: str = "test_out.csv"
    output_path: str = str(DATA_PATH / test_file_name_out)
    s3.download_file(
        Filename=output_path,
        Bucket=config.AWS_MODEL_BUCKET_NAME,
        Key=test_file_name,
    )
    assert Path.is_file(DATA_PATH / test_file_name_out)

    #     Delete test file
    os.remove(output_path)
    assert not Path.is_file(DATA_PATH / test_file_name_out)

    #     delete test item in s3
    s3_res = boto3.resource('s3')
    s3_res.Object(config.AWS_MODEL_BUCKET_NAME, test_file_name).delete()
