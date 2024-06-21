from argparse import ArgumentParser
from subprocess import check_call
import platform

def check(host, guessed_mtu, do_print=True):
    if do_print:
        print("Checking value", guessed_mtu + 28, end=' ')
    try:
        if platform.system() == "Windows":
            response = check_call(["ping", host, "-n", "1", "-w", "4", "-l", str(guessed_mtu)], stderr=-1, stdout=-1)
        else:
            response = check_call(["ping", host, "-c1", "-w2", "-Mdo", "-s" + str(guessed_mtu)], stderr=-1, stdout=-1)
    except Exception as e:
        if do_print:
            print("\033[31mFailure\033[0m")
        return False
    if response != 0:
        if do_print:
            print("\033[31mFailure\033[0m")
        return False
    if do_print:
        print("\033[32mSuccess\033[0m")
    return response == 0

def main():
    try:
        parser = ArgumentParser()
        parser.add_argument("host", help="Endpoint to measure MTU between")
        parser.add_argument("--verbose", help="Enable logging. Makes it easier to see the progress", default='1')
        args = parser.parse_args()
        host : str = args.host
        verbose : str = args.verbose

        if verbose == '0' or verbose.lower() == 'false':
            verbose = False
        elif verbose == '1' or verbose.lower() == 'true':
            verbose = True
        else:
            print(f"\033[31mBad verbosity value provided. Should be one of '0', 'False' for negative and '1', 'True' for positive \033[0m")
            return

        l = 0
        r = 65508

        is_reachable = check(host, 0, verbose)
        if not is_reachable:
            print(f"\033[31mHost {host} is unreachable \033[0m")
            return
        else:
            print(f"\033[36mHost {host} is reachable \033[0m")
        while r - l > 1:
            mid = (l + r) // 2
            if check(host, mid, verbose):
                l = mid
            else:
                r = mid

        print("MTU of the path between this computer and", host, "is", l + 28)
    except:
        print("Exited due to exception")

if __name__ == "__main__":
    main()
