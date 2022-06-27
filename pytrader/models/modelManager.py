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
    Handles the retrieval of the models. Used by the trade manager subprocesses to determine trade opportunities.
    """

    def __init__(self):
        self.__status: common.State = common.State.INIT
        self.__local_repo_dir: Path = Path(__file__).parent / "data"
        self.__url: Url = config.MODEL_REPO_URL
        self.__bucket: str = config.AWS_MODEL_BUCKET_NAME
        self.__model_suffix: str = ".h5"

    @property
    def directory(self) -> Path:
        return self.__local_repo_dir

    @directory.setter
    def directory(self, path: Path):
        """
        Used for testing purposes.
        :param path: Path for test files
        """
        self.__local_repo_dir = path

    @property
    def model_suffix(self) -> str:
        return self.__model_suffix

    def get_model_by_name(self, asset_name: str) -> Optional[ModelPackage]:
        """
        Retrieves the model as a package from the local directory.
        :param asset_name: the asset we are trying to find the model for.
        :return: None if there is no file, else the relevant model package.
        """
        asset_filename: str = self.__append_model_suffix(asset_name)
        model_path: Path = self.__local_repo_dir / asset_filename
        try:
            model: keras.Model = keras.models.load_model(model_path)
            return ModelPackage(asset_name, self.__local_repo_dir, model)
        except FileNotFoundError as e:
            Log.e(f"No model exists for {asset_name}")
            return None
        except IOError as e:
            Log.e(f"No model exists for {asset_name}")
            return None

    def download_model_by_name(self, name: str) -> common.GenericStatus:
        """
        Downloads the relevant model from aws to local store.
        :param name: Name of asset we want to download model for.
        :return: The success of the download.
        """
        s3 = boto3.client("s3")
        # Download file
        test_file_name_out: str = self.__append_model_suffix(name)
        output_path: Path = self.__local_repo_dir / test_file_name_out

        # return status of download
        status: common.GenericStatus = common.GenericStatus.UNKNOWN
        try:
            s3.download_file(
                Filename=str(output_path),
                Bucket=config.AWS_MODEL_BUCKET_NAME,
                Key=test_file_name_out,
            )
            status = common.GenericStatus.SUCCESSFUL if output_path.is_file() else common.GenericStatus.UNSUCCESSFUL
        except FileNotFoundError as e:
            status = common.GenericStatus.UNSUCCESSFUL
            Log.w(f"Could not download the model for {name} to {self.__local_repo_dir}")
            Log.w(e)

        finally:
            return status

    def __is_valid_key(self, name: str) -> bool:
        """
        Used solely to use TEST FILE for tests, or PROD files in production
        :param name: name of key
        :return: Whether we should download it
        """
        # TODO-TIDY Surely I can think of something nicer...
        if str(self.__local_repo_dir).__contains__("TEST") and name.__contains__("TEST"):
            return True
        elif not str(self.__local_repo_dir).__contains__("TEST") and not name.__contains__("TEST"):
            return True
        else:
            return False

    def __append_model_suffix(self, name: str) -> str:
        """
        Helper method that appends the suffix of the model to the string
        :param name: name of the model
        :return:  appended model name
        """
        return name + self.__model_suffix

    def download_all_models(self) -> common.GenericStatus:
        """
        Downloads all models from aws stores.
        :return: The success of the operation
        """
        model_names: [str] = []
        status: common.GenericStatus = common.GenericStatus.UNKNOWN
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(self.__bucket)
        for obj in my_bucket.objects.all():
            model_name: str = obj.key
            if self.__is_valid_key(model_name):
                model_names.append(model_name[:model_name.index('.')])
        status = common.GenericStatus.DOWNLOADING
        for model_name in model_names:
            status = self.download_model_by_name(model_name)
        return status

    @staticmethod
    def delete_local_model(model: ModelPackage) -> common.GenericStatus:
        """
        Deletes the local model from the directory.
        :param model: model to be deleted.
        :return: the success of the deletion.
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

    def delete_local_model_by_name(self, name: str) -> common.GenericStatus:
        """
        Deletes the local model when referenced by name.
        :param name: name of model to be deleted.
        :return: the success of the deletion.
        """
        status: common.GenericStatus = common.GenericStatus.UNKNOWN
        try:
            os.remove(os.path.join(self.__local_repo_dir, self.__append_model_suffix(name)))
            status = common.GenericStatus.SUCCESSFUL
        except FileNotFoundError as e:
            status = common.GenericStatus.UNSUCCESSFUL
            Log.w(f"Unable to delete local model for {name} at {self.__local_repo_dir}.")
            Log.w(e)
        finally:
            return status

    def update_local_model(self, name: str) -> common.GenericStatus:
        """
        Updates the local model by replacing local model with equivalent cloud model.
        :param name: name of the asset that we want to update the local model for.
        :return: The status of the update.
        """
        self.delete_local_model_by_name(name)
        return self.download_model_by_name(name)

    def delete_all_local_models(self) -> common.GenericStatus:
        """
        Deletes all local models in our local store.
        :return: the success of the operation.
        """
        for root, dirs, files in os.walk(self.__local_repo_dir):
            for file in files:
                if file.__contains__(self.__model_suffix):
                    os.remove(os.path.join(root, file))
        file_count: int = 0
        for files in os.walk(self.__local_repo_dir):
            file_count = len(files)
        return common.GenericStatus.SUCCESSFUL if file_count == 0 else common.GenericStatus.UNSUCCESSFUL

    def populate_local_repo(self) -> common.GenericStatus:
        """
        Updates local repository with all currently existing models that exist in the db.  Note, the AWS is treated
        as the MASTER, so ensure all uploaded progress is successful otherwise it will be lost.
        :return: the success of the request to repopulate the local directory
        """
        status: common.GenericStatus = common.GenericStatus.UNKNOWN

        try:
            # delete local files
            status = common.GenericStatus.DELETING
            # self.delete_all_local_models()
            # get new files
            status = common.GenericStatus.DOWNLOADING
            status = self.download_all_models()
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
            Key=self.__append_model_suffix(model.name),
            Filename=self.__append_model_suffix(str(model.directory / model.name))
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
        s3_res.Object(self.__bucket, self.__append_model_suffix(model.name)).delete()
        return common.GenericStatus.SUCCESSFUL

    def delete_cloud_model_by_name(self, name: str) -> common.GenericStatus:
        """
        Deletes the cloud model specified.
        :param name: name of model to be deleted.
        :return: success state.
        """
        # TODO - this should check the response of the download
        #     delete test item in s3
        s3_res = boto3.resource('s3')
        s3_res.Object(self.__bucket, name).delete()
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

    def create_existing_model_package(self, asset_name: str) -> ModelPackage:
        """
        Creates a model package when given an asset.
        :param asset_name: the asset we want a model package for.
        :return: the model package
        """
        path: Path = self.__local_repo_dir / self.__append_model_suffix(asset_name)
        return ModelPackage(asset_name, path, keras.models.load_model(path))

    def create_model(self, name: str) -> keras.Model:
        """
        This creates a model with a predefined structure that will lay the groundwork for the training to occur.
        :param name: the name of the asset that the model will represent.
        :return: the model.
        """
        pass

    def create_model_package(self, asset_name: str) -> ModelPackage:
        """
        Creates a model package when given an asset.
        :param asset_name: the asset we want a model package for.
        :return: the model package
        """
        # TODO - This should create the model at the expected location and return the common.GenericStatus
        #  of the operation, not the file as this will be seldom used.
        path: Path = self.__local_repo_dir / self.__append_model_suffix(asset_name)
        model: keras.Model = keras.models.Sequential([keras.Input(shape=784)])
        model.save(path)
        return ModelPackage(asset_name, path, model)
