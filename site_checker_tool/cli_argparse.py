# cli.py

import argparse


def read_user_cli_args():
    """Handle the CLI arguments and options."""
    parser = argparse.ArgumentParser(
        prog="site_checker_tool", description="check the availability of websites",
    )
    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="enter one or more website urls",
    )
    # In the next argument, we didn't use 'nargs' argument because we want the application
    # to be accepting only one input file at the command line.
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",
    )
    # Adding the asynchronous functionality
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchronously",
    )
    # By calling the method .parse_args(), we would be returning a Namespace object 
    # containing the parsed arguments
    return parser.parse_args()


def display_check_result(result, url, error=""):
    """Display the result of a connectivity check."""
    print(f"The status of '{url}' is:", end=" ")
    if result:
        print('"Online!" ✅')
    else:
        print(f'"Offline?" ❌ \n Error: "{error}"')

