import time


def timed(function):
    """
    Wrapper to time the function call, useful for sql and other tasks that could potentially take a long time.
    TODO - Logging implementation (pass the print to correct log file, default to print if necessary)?
    :param function: the function we want timed.
    :return:
    """

    def wrapper(*args, **kwargs):
        before = time.time()
        value = function(*args, **kwargs)
        after = time.time()
        fn_name = function.__name__
        print(f"{fn_name} took {after - before} seconds to execute.")
        return value

    return wrapper
