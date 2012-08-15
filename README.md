## tasty morsels of lobster news

> Lobster Pie is a bot, written in Python, that posts new stories from 
> lobste.rs to Twitter.

Lobster Pie posts from the [@lobsternews](https://twitter.com/lobsterpie)
Twitter account.


## dependencies
    * feedparser
    * requests
    * python-twitter

Please note that lobsterpie needs `python-twitter` and *not* `twitter`. 
The two libraries have different interfaces, therefore the `twitter`
package will not work; confusion arises when both are installed as both
use the name `twitter`. You have been warned.

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

## Links
* lobsterpie fetches stories from [lobste.rs](https://lobste.rs/)
* the stories are posted to [@lobsternews](https://www.twitter.com/lobsternews)
* the [source is on bitbucket](https://bitbucket.org/kisom/lobsterpie/)
* comments are welcome; my email is in the commit log.


