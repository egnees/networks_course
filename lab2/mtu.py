import subprocess
import argparse
import platform


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True, help="host")
    return parser


host = setup_parser().parse_args().host

HEADER_SIZE = 28


def make_ping(package: int) -> bool:
    sys = platform.system().lower()

    if sys == 'windows':
        command = ["ping", host, "-f", "-l", str(package)]
    else:
        command = ["ping", host, "-c", "1", "-s", str(package)]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        print("exception on making ping: " + str(e))
        return False


def is_available() -> bool:
    sys = platform.system().lower()
    if sys == 'windows':
        command = ["ping", "-n", "5", host]
    else:
        command = ["ping", "-c", "5", host]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        print("exception on checking: " + str(e))
        return False


def find_mtu() -> int:
    left = 0
    right = 10000 - HEADER_SIZE

    while right - left > 1:
        checking_mtu = (left + right) // 2
        possible = make_ping(checking_mtu)
        print(f"left={left}, right={right}, checking_mtu={checking_mtu}, possible={possible}")
        if possible:
            left = checking_mtu
        else:
            right = checking_mtu

    return left


print(f"checking availability to {host}...")

available = is_available()
if not available:
    print(f"host {host} is not available")
else:
    print(f"host {host} is available")
    print("starting to find mtu...")

    mtu = find_mtu() + HEADER_SIZE

    print(f"MTU = {mtu}")
