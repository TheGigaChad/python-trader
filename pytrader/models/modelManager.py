import os
import os.path
from pathlib import Path
from typing import Optional

import boto3
from tensorflow.python import keras
from urllib3.util import Url

from pytrader import common, config
from pytrader.models.modelPackage import ModelPackage

Log: common.Log = common.Log(__file__)


class ModelManager:
    """
    Handles the retrieval of the models used by the trade manager subprocesses to determine trade opportunities.
    """

    def __init__(self):
        self.__status: common.State = common.State.INIT
        self.__local_repo_dir: Path = Path(__file__).parent / "data"
        self.__url: Url = config.MODEL_REPO_URL
        self.__bucket: str = config.AWS_MODEL_BUCKET_NAME

    @property
    def directory(self):
        return self.__local_repo_dir

    def get_model(self, asset: common.Asset) -> Optional[ModelPackage]:
        """
        Retrieves the model as a package from the local directory.
        :param asset: the asset we are trying to find the model for.
        :return: None if there is no file, else the relevant model package.
        """
        asset_filename: str = asset.name + ".h5"
        model_path: Path = self.__local_repo_dir / asset_filename
        try:
            model: keras.Model = keras.models.load_model(model_path)
            return ModelPackage(asset.name, model_path, model)
        except FileNotFoundError as e:
            Log.e(f"No model exists for {asset.name}")
            return None

    @staticmethod
    def delete_local_model(model: ModelPackage) -> common.GenericStatus:
        """
        Deletes the local model from the directory.
        :param model: model to be deleted.
        :return: 
        """
        status: common.GenericStatus = common.GenericStatus.UNKNOWN
        try:
            os.remove(model.directory)
            status = common.GenericStatus.SUCCESSFUL
        except FileNotFoundError as e:
            status = common.GenericStatus.UNSUCCESSFUL
            Log.e(f"deleting local model {model.__str__()} failed. Cannot locate file.")
            Log.e(e)
        finally:
            return status

    def delete_all_local_models(self) -> common.GenericStatus:
        """
        Deletes all local models in our directory.
        :return: the success of the operation.
        """
        for root, dirs, files in os.walk(self.__local_repo_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        return common.GenericStatus.SUCCESSFUL

    def populate_local_repo(self) -> common.GenericStatus:
        """
        Updates local repository with all currently existing models that exist in the db.
        :return: the success of the request to repopulate the local directory
        """
        status: common.GenericStatus = common.GenericStatus.UNKNOWN

        try:
            # delete local files
            status = common.GenericStatus.DELETING
            self.delete_all_local_models()
            # get new files
            status = common.GenericStatus.DOWNLOADING
        #     TODO get files

        except Exception as e:
            status = common.GenericStatus.UNSUCCESSFUL
            Log.e(f"Failed to populate the local model repository with a status of {status}")
            Log.e(e)

        return status

    def upload_cloud_model(self, model: ModelPackage) -> common.GenericStatus:
        """
        Uploads the specified file to the aws s3 bucket.
        :param model: the model package containing all model data we need to upload (name, file, dir)
        :return: the success of the upload
        """
        # TODO - this should check the response of the upload
        s3 = boto3.client("s3")
        s3.upload_file(
            Bucket=self.__bucket,
            Key=model.name,
            Filename=str(model.directory)
        )
        return common.GenericStatus.SUCCESSFUL

    def delete_cloud_model(self, model: ModelPackage) -> common.GenericStatus:
        """
        Deletes the cloud model specified.
        :param model: model to be deleted.
        :return: success state.
        """
        # TODO - this should check the response of the download
        #     delete test item in s3
        s3_res = boto3.resource('s3')
        s3_res.Object(self.__bucket, model.name).delete()
        return common.GenericStatus.SUCCESSFUL

    def replace_cloud_model(self, model: ModelPackage) -> common.GenericStatus:
        """
        Deletes the model in the bucket, then uploads the specified model to the aws s3 bucket.
        :param model: the model package containing all model data we need to upload (name, file, dir)
        :return: the success of the upload
        """
        #     delete test item in s3
        status: common.GenericStatus = self.delete_cloud_model(model)
        if status == common.GenericStatus.UNSUCCESSFUL:
            return status

        # upload model
        status = self.upload_cloud_model(model)

        return status

    def create_model_package(self, asset: common.Asset) -> ModelPackage:
        """
        Creates a model package when given an asset.
        :param asset: the asset we want a model package for.
        :return: the model package
        """
        path: Path = self.__local_repo_dir / (asset.name + ".h5")
        return ModelPackage(asset.name, path, keras.models.load_model(path))
