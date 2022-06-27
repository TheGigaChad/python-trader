import os
from typing import List, Optional

from pytrader import common, models
from pytrader.ml.mlTrainingInstance import MLTrainingInstance

Log: common.Log = common.Log(__file__)


class MLTrainingManager:

    def __init__(self):
        """
        The Machine Learning Training Manager handles all Training Instances, and is the interface in regard to
        training and generating new models.
        """
        self.__status: common.State = common.State.INIT
        self.__model_manager: models.ModelManager = models.ModelManager()
        self.__instances: List[MLTrainingInstance] = self.__init_instances()

    @property
    def model_manager(self):
        return self.__model_manager

    def refresh_instances(self):
        """
        Called to refresh the instance list, useful after changing the directory for the model manager local stores.
        :return: none.
        """
        self.__instances = self.__init_instances()

    def monitor_instances(self):
        """
        This will run more-or-less indefinitely, watching the instances and managing them as necessary.
        """
        # TODO
        pass

    def get_instance_by_name(self, name: str) -> Optional[MLTrainingInstance]:
        """
        Returns the instance if it exists in our list of instances.
        :param name: name of the training instance we want.
        :return: the instance, or None if it doesn't exist in our instance list.
        """
        for instance in self.__instances:
            if instance.name == name:
                return instance
        return None

    def __get_or_create_instance_by_name(self, name: str) -> MLTrainingInstance:
        """
        Returns the relevant instance if it exists in the instance list or a model exists in the local stores
        else it will create a new model.
        :param name: Name of the asset that the model corresponds to.
        :return: The corresponding instance.
        """
        instance: MLTrainingInstance = self.get_instance_by_name(name)
        if instance is not None:
            return instance

        Log.d(f"No instance exists for {name}, let's create one.")
        self.__model_manager.update_local_model(name)
        model: models.ModelPackage = self.__model_manager.get_model_by_name(name)
        if model is not None:
            return MLTrainingInstance(name, model)

        Log.d(f"No model exists for {name}, let's create one.")
        model = self.__model_manager.create_model_package(name)
        return MLTrainingInstance(name, model)

    def train_all(self):
        """
        Tells each instance to begin training.
        :return: None
        """
        self.__status = common.State.RUNNING
        for instance in self.__instances:
            instance.train()

    def train(self, asset_name: str):
        """
        Trains the specified model.
        :param asset_name: name of the asset we want to train a model for. 
        """
        self.__status = common.State.RUNNING
        instance: MLTrainingInstance = self.__get_or_create_instance_by_name(asset_name)
        if instance is None:
            Log.w(f"Cannot get or create a training instance for {asset_name}.")
            return
        instance.train()

    def create_model(self, name: str) -> models.ModelPackage:
        """
        Creates a new model for the specified asset.
        :param name: name of the asset
        :return:a model package containing all relevant data and info.
        """
        return self.__model_manager.create_model_package(name)

    def create_and_train(self, asset_name: str) -> MLTrainingInstance:
        """
        Creates and trains a model for specified asset.
        :param asset_name: name of asset.
        :return: training instance
        """
        instance: MLTrainingInstance = self.__get_or_create_instance_by_name(asset_name)
        instance.train()
        return instance

    def __init_instances(self) -> List[MLTrainingInstance]:
        """
        Initialises all training instances.  This will download all models and then populate the instance list
        with them.
        :return: All available instances.
        """
        instances: List[MLTrainingInstance] = []
        self.__model_manager.populate_local_repo()
        for root, dirs, files in os.walk(self.__model_manager.directory):
            for file in files:
                if file.__contains__(self.__model_manager.model_suffix):
                    # create a package and add to the instance list
                    file_name: str = file[:file.index('.')]
                    model_package: models.ModelPackage = self.model_manager.create_existing_model_package(file_name)
                    instances.append(MLTrainingInstance(file_name, model_package))
        self.__status = common.State.READY
        return instances

    @staticmethod
    def __file_name_to_asset_name_str(file_name: str) -> str:
        # TODO
        return file_name
