import os
from pathlib import Path

import pytest
from tensorflow.python import keras

from pytrader import models, common

PATH = Path(__file__).parent
DATA_PATH = PATH / 'data'


def test_delete_local_model():
    model_mgr: models.ModelManager = models.ModelManager()
    model_mgr.directory = DATA_PATH
    model_name: str = "test_model.h5"
    model_mgr.delete_local_model_by_name(model_name)
    file_path: Path = DATA_PATH / model_name
    if file_path.is_file():
        os.remove(file_path)
    assert not file_path.is_file()


@pytest.mark.dependency(depends=["test_delete_local_model"])
def test_create_local_model():
    model_name: str = "test_model.h5"
    file_path: Path = DATA_PATH / model_name
    model: keras.models.Model = keras.models.Sequential([
        keras.Input(shape=784)
    ])
    model.save(filepath=file_path, overwrite=False)
    assert file_path.is_file()


@pytest.mark.dependency(depends=["test_create_local_model"])
def test_push_local_model():
    asset_name: str = "test_model"
    model_manager: models.ModelManager = models.ModelManager()
    model_manager.directory = DATA_PATH
    model_pkg: models.ModelPackage = model_manager.get_model_by_name(asset_name)
    status: common.GenericStatus = model_manager.upload_cloud_model(model_pkg)
    assert status == common.GenericStatus.SUCCESSFUL


@pytest.mark.dependency(depends=["test_push_local_model"])
def test_pull_remote_model():
    model_mgr: models.ModelManager = models.ModelManager()
    model_mgr.directory = DATA_PATH
    model_name: str = "test_model"
    model_filename: str = "test_model.h5"
    model_mgr.delete_local_model_by_name(model_name)
    model_path: Path = model_mgr.directory / model_filename
    assert not model_path.is_file()
    model_mgr.download_model_by_name(model_name)
    assert model_path.is_file()


@pytest.mark.dependency(depends=["test_pull_remote_model"])
def test_update_local_model():
    asset_name: str = "test_model"
    model_manager: models.ModelManager = models.ModelManager()
    model_manager.directory = DATA_PATH
    status: common.GenericStatus = model_manager.update_local_model(asset_name)
    assert status == common.GenericStatus.SUCCESSFUL


@pytest.mark.dependency(depends=["test_update_local_model"])
def test_populate_dir():
    model_mgr: models.ModelManager = models.ModelManager()
    model_mgr.directory = DATA_PATH
    status: common.GenericStatus = model_mgr.download_all_models()
    assert status == common.GenericStatus.SUCCESSFUL


@pytest.mark.dependency(depends=["test_update_local_model", "test_train_instance", "test_create_and_train_instance"])
def test_delete_remote_model():
    asset_name: str = "test_model"
    model_manager: models.ModelManager = models.ModelManager()
    model_manager.directory = DATA_PATH
    model_pkg: models.ModelPackage = model_manager.get_model_by_name(asset_name)
    status: common.GenericStatus = model_manager.delete_cloud_model(model_pkg)
    assert status == common.GenericStatus.SUCCESSFUL
