"""Site Connectivity Checker entry point script."""
# site_checker_tool/__main__.py

import asyncio
import pathlib
import sys

from site_checker_tool.checker import site_is_online
from site_checker_tool.checker import site_is_online_async
from site_checker_tool.cli_argparse import read_user_cli_args
from site_checker_tool.cli_argparse import display_check_result


def main():
    """Run site checker."""
    user_args = read_user_cli_args()
    urls = _get_websites_urls(user_args)
    if not urls:
        print("Error: no URLs to check ❗", file=sys.stderr)
        sys.exit(1)

    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)


def _get_websites_urls(user_args):
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)
    return urls


def _read_urls_from_file(file):
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print(f"Error: empty input file, {file} 🤷‍♀️", file=sys.stderr)
    else:
        print("Error: input file not found 🤦‍♀️", file=sys.stderr)
    return []


def _synchronous_check(urls):
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as err:
            result = False
            error = str(err)
        display_check_result(result, url, error)


async def _asynchronous_check(urls):
    async def _check(url):
        error = ""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)
    
    await asyncio.gather(*(_check(url) for url in urls))


if __name__ == "__main__":
    raise SystemExit(main())
