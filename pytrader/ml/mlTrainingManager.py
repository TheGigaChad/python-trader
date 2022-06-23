import os
from typing import List

from pytrader import common, models
from pytrader.ml.mlTrainingInstance import MLTrainingInstance


class MLTrainingManager:

    def __init__(self):
        """
        The Machine Learning Training Manager handles all Training Instances, and is the interface in regard to
        training and generating new models.
        """
        self.__status: common.State = common.State.INIT
        self.__model_manager: models.ModelManager = models.ModelManager()
        self.__instances: List[MLTrainingInstance] = self.__get_all_instances()

    def monitor_instances(self):
        """
        This will run more-or-less indefinitely, watching the instances and managing them as necessary.
        """
        # TODO
        pass

    def train_all(self):
        # TODO this is way down the line i think
        self.__status = common.State.RUNNING
        self.__status = common.State.READY
        pass

    def train_model(self, name: str):
        self.__status = common.State.RUNNING
        self.__status = common.State.READY
        pass

    def create_model(self, name: str) -> models.ModelPackage:
        """
        Creates a new model for the specified asset.
        :param name: name of the asset
        :return:a model package containing all relevant data and info.
        """
        return self.__model_manager.create_new_model_package(name)

    def create_and_train(self, asset_name: str):
        """
        Creates and trains a model for specified asset.
        :param asset_name: name of asset.
        """
        model: models.ModelPackage = self.__model_manager.create_new_model_package(asset_name)
        instance: MLTrainingInstance = MLTrainingInstance(model.name, model)
        self.__instances.append(instance)
        instance.train()

    def __get_all_instances(self) -> List[MLTrainingInstance]:
        instances: List[MLTrainingInstance] = []
        self.__model_manager.populate_local_repo()
        for root, dirs, files in os.walk(self.__model_manager.directory):
            for file in files:
                instances.append(MLTrainingInstance(file.name, file))
        self.__status = common.State.READY
        return instances

    @staticmethod
    def __file_name_to_asset_name_str(file_name: str) -> str:
        # TODO
        return file_name
