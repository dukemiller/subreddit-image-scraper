from data import DataWriter
from typing import Iterable
import os.path as path
import urllib.request
import urllib.error
import handlers
import tools
import praw


def get_download_data_for(url: str) -> Iterable[str]:
    """ Yields a collection of direct content links from the requested url. """

    if url.endswith(".gifv"):
        url = url.replace(".gifv", ".webm")

    if tools.is_file(url):
        yield url

    else:

        if 'imgur' in url:
            images = handlers.imgur(url)

        elif 'gfycat' in url:
            images = handlers.gfycat(url)

        else:
            print("No handler for {}".format(url))
            images = []

        for image in images:
            yield image


def download(url: str, output_path: str) -> bool:
    download_path = path.join(output_path, tools.get_url_filename(url))

    if not path.exists(download_path):
        try:
            urllib.request.urlretrieve(url, download_path)
            return True

        except urllib.error.HTTPError as e:
            # Does not exist
            if e.errno == 404:
                return False

        except urllib.error.URLError as e:
            # Connection did not resolve
            if e.winerror == 10060:
                return False

        except ConnectionResetError as e:
            # Forcibly closed connection;
            # TODO: this can possibly be fixed by adding headers to requests.
            if e.winerror == 10054:
                return False

    return False


def main():
    count = tools.get_count()
    subreddits = tools.get_subreddits()
    output_path = tools.make_folder(tools.OUTPUT_FOLDER)
    reddit = praw.Reddit(user_agent="subreddit-image-scraper by /u/dukemiller")
    data = DataWriter(output_path)

    for subreddit in subreddits:
        print("-- {0}".format(subreddit))
        subreddit_path = tools.make_folder(path.join(output_path, subreddit))
        subreddit_data = data[subreddit]
        download_count = 0

        try:
            # get every submission
            for submission in reddit.get_subreddit(subreddit).get_top_from_all(limit=count):
                submission_url = submission.url

                # if not exist in json
                if subreddit_data.does_not_contain(submission_url):
                    response = get_download_data_for(submission_url)

                    # download each url
                    for url in response:
                        downloaded = download(url, subreddit_path)

                        if downloaded:
                            print("Downloaded {0}.".format(url))
                            subreddit_data.add(url)
                            download_count += 1

                            # Add the base URL (in the case that download url/s are different)
                            if submission_url not in subreddit_data:
                                subreddit_data.add(submission_url)

            if download_count > 0:
                data.save()

        except praw.errors.Forbidden:
            print("{} might be a quarantined subreddit and/or removed. Skipping ...".format(subreddit))


if __name__ == '__main__':
    main()
