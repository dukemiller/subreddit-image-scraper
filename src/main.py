from tools import make_folder, get_arguments
from data import DataWriter
import os.path as path
import web
import praw


def main():
    output_path = make_folder(r'E:\Output\api\reddit\subreddit images')
    count, subreddits = get_arguments()
    data = DataWriter(output_path)
    reddit = praw.Reddit(user_agent="subreddit-image-scraper by /u/dukemiller")

    for subreddit in subreddits:
        print("-- {}".format(subreddit))
        subreddit_path = make_folder(path.join(output_path, subreddit))
        subreddit_data = data[subreddit]
        download_count = 0

        try:
            for submission in reddit.get_subreddit(subreddit).get_top_from_all(limit=count):
                submission_url = submission.url

                # download
                if subreddit_data.does_not_contain(submission_url):
                    subreddit_data.add(submission_url)
                    url = web.get_download_url_for(submission_url)
                    downloaded = web.download(url, subreddit_path)
                    if downloaded:
                        download_count += 1

            if download_count > 0:
                data.save()

        except praw.errors.Forbidden:
            print("-- {} might be a quarantined subreddit and/or removed. Skipping ...".format(subreddit))

if __name__ == '__main__':
    main()
