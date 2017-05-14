#! /usr/bin/env python3

import datetime
import hashlib
import os
import ssl
import subprocess
import sys
import time

import feedparser
from feedgen.feed import FeedGenerator
from pytube import YouTube

POLL_INTERVAL_MINUTES = 15

def main():
    relax_ssl_restrictions()
    youtube_feed_url, podcast_root_url = get_feed_url()
    poll_youtube_and_update_podcast(youtube_feed_url, podcast_root_url)


def poll_youtube_and_update_podcast(youtube_feed_url, podcast_root_url):
    while True:
        create_podcast_from_channel(youtube_feed_url, podcast_root_url,
                                    int(os.environ.get('ITEMS_PER_FEED', 5)))
        sleep_until_next_check()


def relax_ssl_restrictions():
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context


def get_feed_url():
    # TODO: should return a configuration object instead
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: {} YOUTUBE_FEED_URL PODCAST_ROOT_URL\n'.format(sys.argv[0]))
        sys.exit(1)
    return sys.argv[1], sys.argv[2]


def sleep_until_next_check():
    next_check = datetime.datetime.now() + datetime.timedelta(minutes=POLL_INTERVAL_MINUTES)
    sys.stderr.write('Sleeping until next poll at {}...'.format(next_check.strftime('%c')))
    time.sleep(POLL_INTERVAL_MINUTES * 60)


def create_podcast_from_channel(url, podcast_root_url, items_to_process):
    feed = feedparser.parse(url)
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title(feed['channel']['title'])
    fg.link(href=feed['channel']['href'], rel='alternate')
    fg.description('Audio tracks from YouTube Channel "{}"'.format(feed['channel']['title']))
    # fg.image(url=feed.image.href, width=feed.image.width, height=feed.image.height)

    output_dir = '/y2p/output'

    for item in feed['items'][:items_to_process]:
        sys.stdout.write(item['link'] + '\n')

        our_id = hashlib.md5(item['link'].encode()).hexdigest()

        audio_fname = our_id + '.m4a'
        audio_fullpath = os.path.join(output_dir, audio_fname)

        if not os.path.exists(audio_fullpath):
            create_audio_file(audio_fullpath, our_id, item['link'])

        p_entry = fg.add_entry()
        p_entry.id(item['id'])
        p_entry.title(item['title'])
        p_entry.description(item['summary'])
        p_entry.enclosure(podcast_root_url + '/' + audio_fname, 0, 'audio/m4a')
        p_entry.published(item['published'])

    fg.rss_str(pretty=True)
    fg.rss_file(os.path.join(output_dir, 'feed.xml'))


def create_audio_file(audio_fname, our_id, video_url):
    yt = YouTube(video_url)
    yt.filename = our_id
    v = yt.get('mp4', '360p')

    download_dir = '/tmp'
    v.download(download_dir)
    video_fname = os.path.join(download_dir, our_id + '.mp4')
    subprocess.check_call(['ffmpeg', '-i', video_fname, '-vn', '-c:a', 'copy', audio_fname])

    os.unlink(video_fname)


if __name__ == '__main__':
    main()