from tools import make_folder, get_arguments


def main():
    make_folder(r'E:\Output\api\reddit\subreddit images')
    count, subreddits = get_arguments()

    print(count)
    print(subreddits)

if __name__ == '__main__':
    main()
