# Building a Site Connectivity Checker CLI Tool

The project is taking the core strengths of Python wherein we will be able to build seamless command-line tools that will be useful for a developer on their day-to-day workflow. On this specific case, we will be building a site-connectivity checker tool from the command line using a third-party library *Typer* CLI library (or we can use Python's built-in *argparse* library). Next, in order to check if a certain website is online, we will be using Python's *http.client* from the standard library. Then we proceed in implementing *synchronous checks* for multiple websites, and check if a website is online using the *aiohttp* third-party library. And then we implement *asynchronous checks* for multiple websites.

From our command-line site-connectivity checker app, we will be able to provide few options:

* *-u* or *--urls* allows us to provide one or more target URLs at the comment line.
* *-f* or *--input-file* allows us to supply a file containing a list of URLs to check.
* *-a* or *--asynchronous* allows us to run the connectivity checks asynchronously

By default, our application will run the connectivity checks asynchronously. With the -a or --asynchronous option, we can modify this behaviour and make the app run the connectivity checks concurrently. We will be taking advantage of Python's *asynchronous features* and the *aiohttp* third-party library.

Internally, our application will be using the standard-library *http.client* module to create a connection to the target website.

## Our project structure

Inside the site-checker-tool/ directory, we will have the following files:

* __init__.py enables site-checker-tool/ as a Python package.
* __main__.py works as an entry-point script for the app
* *checker.py* provides the application's core functionality
* *cli.py* contains the command-line interface for the application.

### Implementing the Site Connectivity Checker Function

Using the Python's standard library *urllib* package, which provides several modules for handling HTTP requests. For example, to check if a website is online, we can use the urlopen() function from the urllib.request module:

```[python]
>>> from urllib.request import urlopen
>>> response = urlopen("https://python.org")
>>> response.read()
```

But we don't need the whole page to be loading all at tonce, instead we will be having lower-level control over our HTTP request! That's where the *http.client* module comes into play.

*HTTPConnection class* inside of http.client module has a .request() method that allows us to perform HTTP requests using the different *HTTP methods*. For this project, we can use the *HEAD* http method to ask for a response containing only the *headers* of the target website. This option will reduce the amount of data to download, making our connectivity checker app more efficient

```[python]
>>> from http.client import HTTPConnection
>>>
>>> connection = HTTPConnection("pypi.org", port=80, timeout=10)
>>> connection.request("HEAD", "/")
>>>
>>> response = connection.getresponse()
>>> response.getheaders()
[('Server', 'Varnish'), ('Retry-After', '0'), ('Location', 'https://pypi.org/'), ('Content-Length', '0'), ('Accept-Ranges', 'bytes'), ('Date', 'Mon, 16 May 2022 03:33:56 GMT'), ('Connection', 'close'), ('X-Served-By', 'cache-mnl9729-MNL'), ('X-Cache', 'HIT'), ('X-Cache-Hits', '0'), ('X-Timer', 'S1652672036.128485,VS0,VE0'), ('X-Frame-Options', 'deny'), ('X-XSS-Protection', '1; mode=block'), ('X-Content-Type-Options', 'nosniff'), ('X-Permitted-Cross-Domain-Policies', 'none')]
```

### Parsing Website URLs from the command line

Code snippet:

```[python]
import argparse


def read_user_cli_args():
    """Handle the CLI arguments and options."""
    parser = argparse.ArgumentParser(
        prog="sitechecker", description="check the availability of websites",
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
    # By calling the method .parse_args(), we would be returning a Namespace object containing the parsed arguments
    return parser.parse_args()
```

### Load Website URLs from a File

Sample Code Snippet

```[python]
def read_user_cli_args():
    ...
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",
    )
```

### Displaying Check Results

Sample Code Snippet

```[python]
def display_check_result(result, url, error=""):
    """Display the result of a connectivity check."""
    print(f"The status of '{url}' is:", end=" ")
    if result:
        print('"Online!" ✅')
    else:
        print(f'"Offline?" ❌ \n Error: "{error}"')
```

### Putting everything together on our App's Main Script

Sample Code Snippet

```[python]
"""Site Connectivity Checker entry point script."""
# site_checker_tool/__main__.py

import pathlib
import sys

from site_checker_tool.checker import site_is_online
from site_checker_tool.cli_argparse import read_user_cli_args
from site_checker_tool.cli_argparse import display_check_result


def main():
    """Run site checker."""
    user_args = read_user_cli_args()
    urls = _get_websites_urls(user_args)
    if not urls:
        print("Error: no URLs to check ❗", file=sys.stderr)
        sys.exit(1)
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


if __name__ == "__main__":
    raise SystemExit(main())
```

Sample Code output:

![Site Checker result](/img/site_checker_output_synchronous.png)

### Checking Websites Asynchronously

Being able to asynchronously call your website urls will help to significantly improve performance of your application

#### Implementing an Asynchronous Connectivity Checker

Sample Code Snippet:

```[python]
# checker.py

import asyncio
from http.client import HTTPConnection
from urllib.parse import urlparse

import aiohttp


def site_is_online(url, timeout=2):
    ...


async def site_is_online_async(url, timeout=2):
    """Return True if the target URL is online.
    
    Raise an exception otherwise.
    """
    error = Exception("unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for scheme in ("http", "https"):
        target_url = scheme + "://" + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception("timed out")
            except Exception as e:
                error = e
        raise error
```

### Adding asynchronous option to the application's CLI

```[python]
# Adding the asynchronous functionality
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchronously",
    )
```

### Add asynchronous checks to the Site Connectivity Checker tool

![Synchronous and Asynchronous Connectivity Checks](/img/site_checker_output_async.png)

## Possible Additional Feature upgrades

* [ ] *Timing Support* : Measure the response time of every targeted website
* [ ] *Check Scheduling Support* : Schedule multiple rounds of connectivity checks in case some websites are offline.
