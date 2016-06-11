# subreddit-image-scraper
Download media from the "top posts of all time" for each subreddit.
 
### Calling
**command line --**
``python {main.py} {count} {data}``
``{main.py}`` => the file path to main.py
``{count}`` => the amount of posts to traverse starting from the top of all time, going downward count
``{data}`` =>  a file path to a text file containing a list of subreddits delimited by a comma and space, or just those subreddits delimited by comma and spaces

e.g. ``python main.py 20 scorpion, astrophotography, birdpics``
Download the top 20 pictures from /r/scorpion, /r/astrophotography, and /r/birdpics

**OR**

**interactive --**
``python {main.py}``
Prompts will come up for the same arguments as the commandline to be filled out in exactly the same way.

### Usage notes
The output directory is hard set in tools.py, you'll have to change this until I change it later to be a setting. All subreddits in your list will have a folder created here and any media from those subreddits will be downloaded into those folders.