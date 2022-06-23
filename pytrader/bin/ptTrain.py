from pytrader import common
import sys
from pathlib import Path

if __name__ == "__main__":

    path: Path = Path(__file__).parent.parent
    print(path)
    if len(sys.argv) == 2:
        arg_one = str(sys.argv[1])
        if arg_one == "-h" or arg_one == "-help":
            sys.exit("This is the help string")
        else:
            sys.exit("Invalid args.  Please retry with correct formatting.")
    elif len(sys.argv) != 3:
        sys.exit("Invalid args.  Please retry with correct formatting.")
