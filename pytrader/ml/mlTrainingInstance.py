import tensorflow as tf
from pytrader import common, models


gpu_available = tf.config.list_physical_devices('GPU')
print(gpu_available)


class TrainingState(common.State):
    """
    Extends generic state to use specific training states too.  Only used here and potentially in tests.
    """
    INIT = 1
    TRAINING = 9
    UPLOADING = 10
    DOWNLOADING = 11
    COMPLETE = 12


class MLTrainingInstance:

    def __init__(self, name: str, model: models.ModelPackage):
        """
        Training instance that is used to generate Machine Learning Models for each asset.
        :param name: Name of the asset being analysed.
        """
        self.__name: str = name
        self.__status: TrainingState = TrainingState.INIT
        self.__model: models.ModelPackage = model

    @property
    def name(self):
        return self.__name

    @property
    def status(self):
        return self.__status

    def is_training(self) -> bool:
        """
        returns whether the instance is training.
        :return: status is training
        """
        return self.__status == TrainingState.TRAINING

    def is_complete(self) -> bool:
        """
        returns whether the instance is complete.
        :return: status is complete
        """
        return self.__status == TrainingState.COMPLETE

    def is_error(self) -> bool:
        """
        returns whether the instance is in an error state.
        :return: status is error
        """
        return self.__status == TrainingState.ERROR

    def is_uploading(self) -> bool:
        """
        returns whether the instance is uploading.
        :return: status is uploading
        """
        return self.__status == TrainingState.UPLOADING

    def is_downloading(self) -> bool:
        """
        returns whether the instance is downloading.
        :return: status is downloading
        """
        return self.__status == TrainingState.DOWNLOADING

    def train(self):
        self.__status = TrainingState.TRAINING
        pass

