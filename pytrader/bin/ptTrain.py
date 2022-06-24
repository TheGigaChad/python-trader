import sys
from pathlib import Path


import pytrader


def is_help_request(request: str) -> bool:
    """
    Returns whether the request is for help
    :param request: argument related to the type of request
    :return: whether it is a help request
    """
    request_help_options: [str] = ["-h", "-help"]
    return request in request_help_options


def is_train_request(request: str) -> bool:
    """
    Returns whether the request is for training
    :param request: argument related to the type of request
    :return: whether it is a train request
    """
    request_train_options: [str] = ["-t", "-train"]
    return request in request_train_options


def handle_train_request(asset_name: str):
    """
    Handles the request for training a model. \n
    :param asset_name: name of model we want to train.
    """
    sys.exit(f"We are currently handling the train request for {asset_name}....Promise.")


def is_create_request(request: str) -> bool:
    """
    Returns whether the request is for creating a new model
    :param request: argument related to the type of request
    :return: whether it is a create request
    """
    request_create_options: [str] = ["-c", "-create"]
    return request in request_create_options


def handle_create_request(asset_name: str):
    """
    Handles the request for creating a model. \n
    :param asset_name: name of model we want to create.
    """
    sys.exit(f"We are currently handling the create request for {asset_name}....Promise.")


def is_create_and_train_request(request: str) -> bool:
    """
    Returns whether the request is for creating a new model and then training it
    :param request: argument related to the type of request
    :return: whether it is a create and train request
    """
    request_create_and_train_options: [str] = ["-ct", "-createandtrain"]
    return request in request_create_and_train_options


def handle_create_and_train_request(asset_name: str):
    """
    Handles the request for creating and training a model. \n
    :param asset_name: name of model we want to create and train.
    """
    sys.exit(f"We are currently handling the create and train request for {asset_name}....Promise.")


def print_help_docs():
    """
    Prints out the help documentation in the console. \n
    :return: none.
    """
    print("------- pytrader train -------")
    print("This is used to create and/or train a model without having to be running the project.")
    print("The idea being that it should be largely disconnected from the running of the trader.")
    print("")
    print("Arguments: ")
    print("-h help : see all the related documentation.")
    print("-c create: creates a new model to begin training.")
    print("-t train: trains specified model")
    print("-ct create and train: creates and trains specified model.")
    print("")
    print("Example: ")
    print("'ptTrain.py -ct TSLA' will create a model for TSLA and begin training it.")
    sys.exit()


if __name__ == "__main__":
    print(pytrader.common.State.INIT)
    print("reee")
    path: Path = Path(__file__).parent.parent
    # print(common.State.INIT)
    # Return help string
    try:
        if len(sys.argv) > 1:
            arg_one = str(sys.argv[1])
            if is_help_request(arg_one):
                print_help_docs()

        if len(sys.argv) == 3:
            arg_one = str(sys.argv[1])
            arg_two = str(sys.argv[2])
            if is_create_request(arg_one):
                handle_create_request(arg_two)
            elif is_train_request(arg_one):
                handle_train_request(arg_two)
            elif is_create_and_train_request(arg_one):
                handle_create_and_train_request(arg_two)
        else:
            sys.exit("Invalid args.  Please retry with correct formatting.  Use 'ptTrain.py -help' if you're stuck.")
    except IndexError as e:
        sys.exit("Invalid args.  Please retry with correct formatting.  Use 'ptTrain.py -help' if you're stuck.")
