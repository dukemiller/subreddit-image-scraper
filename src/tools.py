from typing import Tuple, List
import sys
import os


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
        thing = "".join(args[2:])
        if os.path.exists(thing):
            with open(thing) as text:
                subreddits = text.read().split(", ")
        else:
            subreddits = thing.split(", ")

    # Given nothing
    else:
        count = input("How much posts to search in each subreddit: ")

        try:
            count = int(count)
        except ValueError:
            print("Invalid number.")

        thing = input("Put a full filepath or comma + space delimited list of subreddits: ")
        if os.path.exists(thing):
            with open(thing) as text:
                subreddits = text.read().split(", ")
        else:
            subreddits = thing.split(", ")

    return count, subreddits
