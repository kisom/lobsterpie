## tasty morsels of lobster news

> Lobster Pie is a bot, written in Python, that posts new stories from 
> lobste.rs to Twitter.

Lobster Pie posts to the [@lobsternews](https://twitter.com/lobsternews)
Twitter account.


## Dependencies
    * feedparser
    * requests
    * python-twitter

```
sudo pip install feedparser requests python-twitter
```

Please note that lobsterpie needs `python-twitter` and *not* `twitter`. 
The two libraries have different interfaces, therefore the `twitter`
package will not work; confusion arises when both are installed as both
use the name `twitter`. You have been warned.


## Environment
lobsterpie gets information from certain environment variables:

* `LB_TWITTER_CONSUMER_KEY` - twitter consumer key
* `LB_TWITTER_CONSUMER_SECRET` - twitter consumer secret
* `LB_TWITTER_ACCESS_KEY` - twitter access token
* `LB_TWITTER_ACCESS_SECRET` - twitter access secret
* `LB_DATABASE_PATH` - the path to the sqlite database used to store 
previously posted stories.

As lobsterpie is the only user running on the application, I've just used
Twitter's OAuth tool to pre-generate the requisite tokens and secrets.


## Usage
0. You will first need to set up the environment. I do this with a script
called `env.sh` that I source into the environment before running the bot.
0. Create the database using `dbtool.py create`.
0. Run the bot (it requires no arguments).
0. If you have to shutdown the bot (i.e. to migrate it to another host),
you can call `dbtool.py dump` to dump the database as a Python hash. This 
has the benefit of allowing you to play with the entries and use them for 
testing.
0. A dumpfile can be restored with `dbtool.py restore`.


## License
lobsterpie is released under an ISC license:

    THE ISC LICENSE:
    --------------------------------------------------------------------------
    
    the ISC license:
    Copyright (c) 2011, 2012 Kyle Isom <kyle@tyrfingr.is>
    
    Permission to use, copy, modify, and distribute this software for any
    purpose with or without fee is hereby granted, provided that the above 
    copyright notice and this permission notice appear in all copies.
    
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 
    
    --------------------------------------------------------------------------

The license is available as 
[plaintext](http://www.tyrfingr.is/licenses/LICENSE.ISC), as well.


## Links
* lobsterpie fetches stories from [lobste.rs](https://lobste.rs/)
* the stories are posted to [@lobsternews](https://www.twitter.com/lobsternews)
* the [source is on bitbucket](https://bitbucket.org/kisom/lobsterpie/);
if you'd like to contribute I'd prefer 
[git patches](www.tyrfingr.is/notes/notes_patchfiles.html). pull requests via
Github won't be accepted as that repo exists solely for the use of Github 
Pages.
* the project has a [github page](http://kisom.github.com/lobsterpie/)
* comments are welcome; my email is in the commit log.


