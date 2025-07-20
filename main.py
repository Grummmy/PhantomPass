import argparse
import hashlib
from getpass import getpass
from base64 import b64encode
from math import ceil

def positive_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("Must be a positive integer")
    return ivalue

parser = argparse.ArgumentParser(description="PhantomPass script creates powerful password from your login, using hash algorithm and additional salt.")
parser.add_argument("data", help="data to create pswd from")
parser.add_argument("--length", "-l", help="length of the pswd", type=positive_int, default=12)
parser.add_argument("--index", "-i", help="pswd start index in base64 hash string", type=positive_int, default=0)
parser.add_argument("--algorithm", "-alg", "-a", help="hashing algorithm to use", choices=["sha1", "sha256", "sha512"], default="sha512")
parser.add_argument("--salt", "-s", help="salt to use in pswd creation", default="")
parser.add_argument("--encoding", "-e", help="string encoding and bytes decoding format. default: utf-8", default="utf-8")
parser.add_argument("--copy", "-c", action="store_true", help="copy password to clipboard instead of printing it. has priority over print option")
parser.add_argument("--print", "-p", action="store_true", help="print password to console, instead of coping it to clipboard")
parser.add_argument("--ignore-warnings", "-iw", action="store_true", help="ignores index and length validation. do not use, unless you got the error recommending the flag")

args = parser.parse_args()

# validating index and pswd length, making sure they fit into the base64 string of the hash
if not args.ignore_warnings:
    hash_len = {"sha1": 20, "sha256": 32, "sha512": 64}[args.algorithm]
    max_b64_len = ceil(hash_len / 3) * 4
    max_pswd_length = max_b64_len - args.index - 2
    if args.index + args.length > max_b64_len:
        print(
            f"Password is too long for given algorithm({args.algorithm}) and index({args.index}). Max password length: {max_pswd_length}. Base64 string length: {max_b64_len}\nUse \x1b[1m--ignore-warnings\x1b[22m or \x1b[1m-iw\x1b[22m flag to ignore this."
        )
        exit(1)

def get_salt():
    # gets salt from args, or if not set, prompts to enter salt, at least 1 symbol long
    global args

    if args.salt == "":
        salt = ""
        while True:
            salt = getpass("Enter salt: ")
            if len(salt) == 0:
                print("\x1b[1mSalt is required\x1b[22m, please enter at least 1 symbol.")
            else:
                return salt
    else:
        return args.salt

def get_data() -> str:
    """
    MODIFIABLE

    gets data to create password from, MUST return a string
    """
    global args

    return args.data + get_salt()

def get_pswd(b64str:str) -> str:
    """
    MODIFIABLE EXP.

    gets pswd from base64 string.
    """
    global args

    return b64str[args.index:args.index + args.length]

def enhance(data) -> str:
    """
    MODIFIABLE

    enhances password, by replacing, adding, substracting or any other operation with pswd symbols.
    """
    data = data.replace("a", "@", 1)

    return data

b64str = b64encode(hashlib.new(args.algorithm, get_data().encode(args.encoding)).digest()).replace(b"=", b"").decode(args.encoding)

pr_or_copy = ""
if args.copy:
    pr_or_copy = "2"
elif args.print:
    pr_or_copy = "1"
else:
    pr_or_copy = input("[1] print or [2] copy to clipboard? (default: 1): ")


if pr_or_copy.strip() == "2":
    from pyperclip import copy
    copy(enhance(get_pswd(b64str)))
    print("Password copied to clipboard.")
else:
    print(f"Password: {enhance(get_pswd(b64str))}")
