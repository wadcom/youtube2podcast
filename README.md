# youtube2podcast: Create Audio Podcasts From YouTube Channels

This utility takes an RSS feed of YouTube channel, downloads corresponding
videos, extracts audio tracks from them and creates an audio podcast feed.
You can now subscribe to that feed and just listen to the audio.

The utility is packaged as a Docker image.

## How To Build The Docker Image

    $ ./build.sh

This will build Docker image `wadcom/youtube2podcast`.

## How To Use The Image

You have to specify the YouTube RSS feed and the root URL of where you want
to host the podcast. After the initial pass youtube2podcast will poll the RSS
feed every 15 minutes for updates and update the podcast as needed.

[Here](https://danielmiessler.com/blog/rss-feed-youtube-channel/) is how to
obtain the YouTube RSS feed URL if you know the YouTube channel URL.

For example, if the YouTube feed URL is this:

    https://www.youtube.com/feeds/videos.xml?channel_id=UCKkg7omDlPvUPxLY-dho8Pg

...and you want to host the resulting podcast at
`http:://example.com/podcasts/my-podcast`, run the Docker image this way:

    $ docker run -d -v /www/podcasts/my-podcast:/y2p/output --restart always \
        wadcom/youtube2podcast \
        https://www.youtube.com/feeds/videos.xml?channel_id=UCKkg7omDlPvUPxLY-dho8Pg \
        http://test.com/podcast

The audio files and the podcast feed will land in `/www/podcasts/my-podcast`
(you'll need a web server, e.g. nginx, to expose those files at the right URL).

You can then subscribe to the podcast at
`http://example.com/podcasts/my-podcast/feed.xml`.
