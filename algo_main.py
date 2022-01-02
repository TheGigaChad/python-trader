import enum
import queue
import threading
import time
import warnings
from subprocess import Popen, PIPE

import alpaca_trade_api as tradeapi
import psutil

from algo_config import KEY, SECRET

warnings.filterwarnings("ignore")

# ------------
# API
# ------------
# Get your own key from whatever service you want. In this case, I am using
# the Alpaca paper trading API.
api = tradeapi.REST(KEY, SECRET, 'https://paper-api.alpaca.markets')


# ------------
# Classes
# TODO - Should these be in independent files?
# ------------
class StockType(enum.Enum):
    """
     TODO \n
     Enum used to modify buy/sell/monitor methods and use the relevant exchange. \n
     currently supports: STOCK
     """
    STOCK = 1
    CRYPTO = 2
    FUND = 3


class NamedPopen(Popen):
    """
     Like subprocess.Popen, but returns an object with a .name member
     """

    def __init__(self, *args, name=None, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def terminate(self):
        super().terminate()


class Subprocess:
    f""" 
     Subprocess object that holds everything relevant to the subprocess. \n
     name: name of subprocess ticker. \n
     stock_type: see :class:`StockType` \n
     process: subprocess. see :class:`NamedPopen`  \n
     out_comm_thread: listens to process calls. \n
     comm_queue: contains out_comm_thread data.
     """

    def __init__(self, name, process, in_comm_thread, out_comm_thread, comm_queue, stock_type=StockType.STOCK):
        self.name = name
        self.type = stock_type
        self.process = process
        self.in_comm_thread = in_comm_thread
        self.in_comm_thread.daemon = True
        self.in_comm_thread.start()
        self.out_comm_thread = out_comm_thread
        self.out_comm_thread.daemon = True
        self.out_comm_thread.start()
        self.comm_queue = comm_queue

    def __del__(self):
        self.process.kill()
        self.out_comm_thread.join()
        self.in_comm_thread.join()

    def poll(self):
        """
         Polls process for updates
         """
        self.process.poll()

    def checkRequests(self):
        """
        checks for any requests from the subprocesses. This will typically be a request for allowance.\n
        """
        if self.comm_queue.qsize() > 0 and self.process.returncode is None:
            try:
                interpreted_request = decodeRequest(self.comm_queue.get(False)) + "\n"
                # p1_out, p1_err = self.process.communicate(input=interpreted_request.encode())[0]
                self.process.stdin.write(interpreted_request.encode("UTF-8"))
            except Exception as e:
                print("checkRequests: ", e)
                pass

    def flush(self):
        if not self.process.stdin.closed:
            self.process.stdin.flush()
            pass
        if not self.process.stdout.closed:
            self.process.stdout.flush()
            pass

    def terminate(self):
        self.process.terminate()


class SharedCashPile(object):
    """
    TODO - currently not feeding into subprocs, do this for efficiency \n
    ---- \n
    Controls access to the cash within the exchange, allowing only one request for an allowance at a time by each
    subprocess.  This prevents potential issues to do with funds. \n
    """

    def __init__(self, val=0):
        self.lock = threading.Lock()
        self.balance = val

    def request(self, confidence, name):
        print("Waiting for another request to finish")
        self.lock.acquire()
        try:
            print('Acquired a lock')
            self.balance = getAvailableCash()
            return allocateChildAllowance(self.balance, confidence, name)
        finally:
            print('Released a lock')
            self.lock.release()


# ------------
# GLOBALS
# ------------
MAX_SUBRPOCESS_COUNT = 50
MAX_THREAD_COUNT = 50
MAX_CPU_PERCENT = 90
MAX_MEMORY_PERCENT = 90
MAX_STOCK_ALLOWANCE = 0.2
MAX_SUBPROCESS_INIT = 5
ACTIVE_STOCKS = []
CHILD_SCRIPT_NAME = "algo_spawn.py"
PRIMARY_STOCK_LIST = ['TSLA', 'AAPL', 'AMZN', 'BABA', 'AMD', 'GOLD', 'BA', 'BBY']
SECONDARY_STOCK_LIST = ['AA', 'AAL', 'AAPL', 'AIG', 'AMAT', 'AMC', 'AMD', 'AMGN', 'AMZN', 'APA', 'BA', 'BABA', 'BAC',
                        'BBY', 'BIDU', 'BP', 'C', 'CAT', 'CMG', 'TSLA', 'BABA', 'GOLD', 'AG', 'AFMD', 'AFL', 'AFTR',
                        'AFG', 'AGE', 'ALL', 'ALLY', 'ALRM', 'ALOT', 'ANPC', 'ANY', 'AOS', 'ANZU', 'API',
                        'APO', 'APP', 'APPF', 'ASR', 'ASTC', 'ATHA', 'ATH', 'ATHE', 'ATHN', 'ATEN', 'ATER', 'CBOE',
                        'CBL', 'CBD', 'CBFV', 'CBAY', 'CBAN', 'CANF', 'CAMT', 'CAMP']


def interpretRequest(request, name, data):
    if request == "ALLOWANCE":
        return str(allocateChildAllowance(float(getAvailableCash()), name, float(data)))


def decodeRequest(request_string):
    """
    the notation for request string is defined as request~name~data. \n
    :param request_string: (string) sent from subprocess.
    :return: (str) containing response to request from subprocess.
    """
    request_string = request_string.decode('UTF-8')
    key = "~"
    first_break = request_string.find(key)
    second_break = request_string.find(key, first_break + 1)

    request = request_string[:first_break]
    name = request_string[first_break + 1:second_break]
    data = request_string[second_break + 1:]

    return interpretRequest(request, name, data)


def getAvailableCash():
    """
    Returns available cash. \n
    TODO - add capacity for getting multiple exchanges available cash.
    """
    return api.get_account().cash


def getDailyTradeCount():
    """
    Returns Daily trade count. \n
    TODO - add capacity for multiple exchanges.
    """
    return api.get_account().daytrade_count


def getEquity():
    """
    Returns equity. \n
    TODO - add capacity for multiple exchanges.
    """
    return api.get_account().equity


def getYesterdaysEquity():
    """
    Returns yesterdaus equity. \n
    TODO - add capacity for multiple exchanges.
    """
    return api.get_account().last_equity


def getDailyChangeInEquity():
    """
    Returns daily change in equity. \n
    TODO - add capacity for multiple exchanges.
    """
    return (float(api.get_account().equity) - float(api.get_account().last_equity)) / float(
        api.get_account().last_equity)


def dailyReport():
    print(f"The cash available is: {getAvailableCash()}.")
    print(f"We made {getDailyTradeCount()} trades today.")
    print(f"Our equity is valued at {getEquity()} compared to yesterdays {getYesterdaysEquity()}.")
    print(f"This means there was a daily gain/loss of {getDailyChangeInEquity()}%")


# --------
# Random helper methods
# --------


def startSubprocess(stock_name):
    return NamedPopen(["python", "-u", CHILD_SCRIPT_NAME, stock_name],
                      stdin=PIPE, stdout=PIPE, bufsize=0, name=stock_name)


def readOutput(pipe, q):
    """reads output from `pipe`, when line has been read, puts
        line on Queue `q`"""

    while pipe.returncode is None:
        try:
            line = pipe.stdout.readline()
            if len(line) > 0:
                q.put(line)
        except Exception as e:
            print(f"readOutput error: {e}")
            break


def readInput(pipe, string):
    """reads input from a pipe with name `read_pipe_name`,
writing this input straight into `write_pipe`"""


# ------------
# Bot Manager
# ------------

# Returns sum of child processes.
def childCount():
    current_process = psutil.Process()
    children = current_process.children()
    return len(children)


def listChildren():
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        print(psutil.Process(child.pid).name)


def childPreCreateResourceCheck():
    """
    Determines whether we have capacity to add another child subprocess based on the thread count, child count, cpu and
    memory usage. \n
    :return: (boolean) if we have capacity.
    """
    # Check child count
    if childCount() >= MAX_SUBRPOCESS_COUNT:
        print("Max subprocess count exceeded.")
        return False

    # Check memory capacity
    if childCount() >= MAX_MEMORY_PERCENT:
        print("Max memory allowance exceeded.")
        return False

    # Check CPU capacity
    if childCount() >= MAX_CPU_PERCENT:
        print("Max CPU allowance exceeded.")
        return False

    return True


def allocateChildAllowance(balance, ticker_name, confidence):
    """
    This method allocates the subprocess an allowance to purchase stocks with. \n
    :param balance: the cash available within exchange.
    :param ticker_name: stock name.
    :param confidence: rating for how confident in our call.
    :return: (float) allowance.
    """
    allowance = balance * MAX_STOCK_ALLOWANCE * confidence
    print(f"{ticker_name} has been given an allowance of {allowance}")
    return allowance


def requestedSellOff(whitelisted_ticker_name):
    """
    TODO \n
    when we receive a highly profitable trade, we can request to liquidate assets to get more funds. \n
    :param whitelisted_ticker_name: name of stock we intend to buy.
    :return: nothing, future will be a boolean for whether request was accepted or denied.
    """
    pass


# ------------
# Testing
# ------------

def generateInitList():
    """
    generates a list of currently owned stocks. \n
    :return: (list) of owned stocks.
    """
    init_list = []
    positions = api.list_positions()
    for stock in positions:
        init_list.append(stock.symbol)
    return init_list


def doesChildExist(name):
    """
    returns whether the stock already has an active subprocess. \n
    :param name: (string) name of stock we want to check.
    :return: (boolean) if subprocess already exists for stock.
    """
    for stock in ACTIVE_STOCKS:
        if stock.name == name:
            return True
    return False


def generateSubprocess(stock_name):
    """
    Generates a :class:`Subprocess` for the provided stock. \n
    :param stock_name: (string) name of stock.
    :return: (Subprocess) object
    """
    process = startSubprocess(stock_name)
    comm_queue = queue.Queue()
    in_thread = threading.Thread(target=readInput, args=(process, "teee"))
    out_thread = threading.Thread(target=readOutput, args=(process, comm_queue))
    return Subprocess(stock_name, process, in_thread, out_thread, comm_queue)


def generateSubprocesses(stock_list):
    """
    Generates a :class:`Subprocess` for each stock within the list. \n
    :param stock_list: (list) of stock names we want to create subprocesses for.
    """
    try:
        for idx, val in enumerate(stock_list):
            if not childPreCreateResourceCheck:
                # make sure we have capacity
                print("No capacity for more children")
                return
            if doesChildExist(val):
                # ignore any that already exist
                continue
            # add the subprocess object to the list of active stocks
            ACTIVE_STOCKS.append(generateSubprocess(val))

    except Exception as e:
        print(f"generateSubprocess: {e}")

    finally:
        print(f"child count: {childCount()}")
        print(f"thread count: {threading.active_count()}")


def monitorChildren():
    """
    monitors subprocesses to see if there is any requests inbound or if they have terminated. \n
    """
    for idx, val in enumerate(ACTIVE_STOCKS):
        # Subprocess is finished
        if val.process.returncode == 0:
            ACTIVE_STOCKS.remove(val)
            del val
            continue
        else:
            val.poll()
            val.checkRequests()
            val.flush()


def addChildFromList(in_list, out_list):
    """
    Looks through the input list to see if a process for the relevant stock already exist,
    if not append to the output.\n
    :param in_list: (list) check from this list to see if it already exists.
    :param out_list: (list) the list we are adding to.
    :return: (list) list of unique stocks. max is defined by the global variable MAX_SUBPROCESS_INIT.
    """
    for i in in_list:
        if not childPreCreateResourceCheck():
            break
        if len(out_list) >= MAX_SUBPROCESS_INIT:
            return out_list
        if len(out_list) + len(ACTIVE_STOCKS) >= MAX_SUBRPOCESS_COUNT:
            return out_list
        # if we are already monitoring it, ignore
        elif doesChildExist(i):
            continue
        else:
            out_list.append(i)
    return out_list


def manageChildren():
    """
    Manages the subprocesses, currently it ensures that we have all priority stocks monitored, then fills spare
    capacity with other stocks.
    """
    add_stocks = []
    # First checks that all important stocks are active.  Note, these are not the ones that we own
    # these are just ones we deem as worth continuously watching.
    add_stocks = addChildFromList(PRIMARY_STOCK_LIST, add_stocks)
    # Then tries to add more stocks from our backup list.
    add_stocks = addChildFromList(SECONDARY_STOCK_LIST, add_stocks)

    if len(add_stocks) > 0:
        print(f"list of subprocesses to be created: {add_stocks}")
        generateSubprocesses(add_stocks)


# ------------
# Main
# ------------
def main():
    # Get the currently owned stocks, these are the priority to monitor
    init_list = generateInitList()
    if len(init_list) > 0:
        print(f"We currently own {init_list}, let's spin up some subprocs for them.")
        generateSubprocesses(init_list)
    else:
        print(f"We currently own nothing, let's spin up some subprocs for {PRIMARY_STOCK_LIST}.")
        generateSubprocesses(PRIMARY_STOCK_LIST)
    while True:
        monitorChildren()
        manageChildren()
        if childCount() == 0:
            break
        time.sleep(1)


if __name__ == "__main__":
    main()
