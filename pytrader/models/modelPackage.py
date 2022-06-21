from pathlib import Path

from tensorflow.python import keras


class ModelPackage:
    """
    Contains the name, file and directory of a model to make it a little easier.
    """

    def __init__(self, name: str, path: Path, model: keras.Model):
        self.__name = name
        self.__dir: Path = path
        self.__model: keras.Model = model

    @property
    def name(self):
        return self.__name

    @property
    def directory(self):
        return self.__dir

    @property
    def model(self):
        return self.__model
