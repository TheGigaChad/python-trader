from pathlib import Path

import pytest

from pytrader import ml

PATH = Path(__file__).parent
DATA_PATH = PATH / 'data'


def test_create_and_train_instance():
    model_name: str = "test_model"
    train_manager: ml.MLTrainingManager = ml.MLTrainingManager()
    train_manager.model_manager.directory = DATA_PATH
    train_manager.refresh_instances()
    instance: ml.MLTrainingInstance = train_manager.create_and_train(model_name)
    assert instance.status == ml.mlTrainingInstance.TrainingState.COMPLETE


@pytest.mark.dependency(depends=["test_create_and_train_instance"])
def test_train_instance():
    model_name: str = "test_model"
    train_manager: ml.MLTrainingManager = ml.MLTrainingManager()
    # Change directory to test path and refresh the instances.
    train_manager.model_manager.directory = DATA_PATH
    train_manager.refresh_instances()
    # Train the model
    train_manager.train(model_name)
    # Assert the training completed successfully
    instance: ml.MLTrainingInstance = train_manager.get_instance_by_name(model_name)
    assert instance.status == ml.mlTrainingInstance.TrainingState.COMPLETE
