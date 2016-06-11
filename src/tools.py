from typing import Tuple, List
import sys
import os

REQUESTS_HEADER = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"
OUTPUT_FOLDER = r'E:\Output\api\reddit\subreddit-image-scraper'


def is_file(url: str) -> bool:
    """ Returns if the url is a file judging only by it's extension"""

    return any(url.lower().endswith(ext) for ext in ['.jpeg', '.jpg', '.gif', '.png', '.webm'])


def make_folder(path: str) -> str:
    r""" Creates a path arbitrarily deep if not exists and returns that path.
        e.g. C:\ exists so C:\{The\New\Path} is created, and the whole path is returned. """

    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_url_filename(url: str) -> str:
    """ Returns the filename from a url if there are no slashes in the name.
    e.g. 'http://google.com/{file.png}' """

    return url.split('/')[-1]


def remove_ending_slash(url: str) -> str:
    if url.endswith("/"):
        url = url[:-1]
    return url


def question_mark_filename_strip(url: str) -> str:
    """ For some unusual reason, imgur URLs will semi frequently have a filename with a question mark in it,
    this will remove it and return the correct link """

    if ".jpg?" in url:
        url = url.split(".jpg?")[0] + ".jpg"
    return url


def print_arguments_and_exit(error_message: str = None) -> None:
    if error_message is not None:
        print(error_message)
    print("Invalid number of arguments.")
    print("Argument format: {main.py} {count} {filepath or string}")
    print("--{count}:              the number of posts to search in each subreddit.")
    print("--{filepath or string}: either a path to a file containing"
          "a comma delimited list of subreddits, or just that comma delimited"
          "list of subreddits.")
    exit()


def get_subreddits(path_or_string: str = None) -> List[str]:
    if path_or_string is None:
        path_or_string = input("Put a full file path or comma + space delimited list of subreddits: ")
    if os.path.exists(path_or_string):
        with open(path_or_string) as text:
            subreddits = text.read().split(", ")
    else:
        subreddits = path_or_string.split(", ")
    return subreddits


def get_count() -> int:
    count = None

    while type(count) is not int:
        count = input("How much posts to search in each subreddit: ")
        try:
            count = int(count)
        except ValueError:
            pass

    return count


def get_arguments() -> Tuple[int, List[str]]:
    count, subreddits = None, None
    args = sys.argv

    # Given command line arguments
    if len(args) > 1:

        # Not enough arguments
        if len(args) < 3:
            print_arguments_and_exit()

        # Invalid first argument
        try:
            count = int(args[1])
        except ValueError:
            print_arguments_and_exit("Invalid argument in position 1.")

        # Format second argument
        subreddits = get_subreddits(" ".join(args[2:]))

    # Given nothing
    else:
        count = get_count()
        subreddits = get_subreddits()

    return count, subreddits
