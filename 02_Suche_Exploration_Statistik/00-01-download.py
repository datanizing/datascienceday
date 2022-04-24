#!/usr/bin/env python

import os
import requests
import gzip
from tqdm.auto import tqdm

# auch ersetzbar urls-all2020.txt.gz
urls = "urls-toplevel2020.txt.gz"
if not os.path.isfile(urls):
    r = requests.get("https://github.com/datanizing/ix-reddit/raw/main/" + urls)
    open(urls, 'wb').write(r.content)

s = requests.Session()
# User-Agent wird benötigt, sonst lässt Reddit keine Anfragen zu
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62 header=accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" }
with gzip.open(urls, "rb") as fh:
    for sc in tqdm(fh.readlines()):
        shortcode = sc.decode("utf-8").strip()
        filename = f"comments/{shortcode}.json"
        if not os.path.isfile(filename):
            url = f"https://www.reddit.com/r/technology/comments/{shortcode}.json"
            r = s.get(url, headers=headers)
            open(filename, 'wb').write(r.content)




