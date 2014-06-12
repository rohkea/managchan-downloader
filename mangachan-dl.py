#!/usr/bin/env python3
from urllib import request
import re, json, shutil, os, time, random, argparse
from os.path import basename

class mangachan:
    def parse_url(url):
        "Gets URL, returns canonical URL and the folder name"
        m = re.search(r'/([0-9]+)-(.*)\.html?$', url)
        if m:
            canonical_url = url
            foldername = m.group(2)
            return (canonical_url, foldername)
        else:
            raise Exception("Wrong Mangachan URL!")

    def get_filenames(url):
        "Return a list of IDs"
        response = request.urlopen(url)
        data = response.read()
        text = data.decode("UTF-8")
        m = re.search(r'"fullimg":\[(.*),\]', text)
        if m:
            json_array = "[" + m.group(1) + "]"
            return json.loads(json_array)
        else:
            raise Exception("Wrong array on Mangachan page!")

    def download_file(url, index, folder, max_timeout=1.5):
        path = os.path.join(folder, basename(url))
        if os.path.exists(path):
            print("The file will NOT be loaded because it already exists!")
            return
        with request.urlopen(url) as response, open(path, 'wb') as out_file:
            time.sleep(max_timeout * random.random())
            shutil.copyfileobj(response, out_file)
            print("Saved file #{} to {}".format(index, path))
    
    def download(user_url, user_folder=None, start_index=0, max_timeout=1.5):
        url, guessed_folder = mangachan.parse_url(user_url)
        folder = user_folder or guessed_folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        filenames = mangachan.get_filenames(url)
        random.seed()
        for index, filename in enumerate(filenames):
            if index >= start_index:
                print("Loading file No. {} ({})...".format(index, basename(filename)))
                mangachan.download_file(filename, index, folder)
            else:
                print("Skipping file No. {} ({})".format(index, filename))

    def main():
        parser = argparse.ArgumentParser(description='Download manga chapters from Mangachan.ru or Yaoichan.ru.',
                                         epilog='It is not recommended to use -f or -s arguments if you need more than 1 URL')
        parser.add_argument('urls', metavar='MANGACHAN_URL', nargs='+',
                            help="URL(s) to Mangachan.ru/Yaoichan.ru chapter page")
        parser.add_argument('-f', dest='folder', nargs=1, default=[None],
                            help='folder where files will be saved (omit it to use default)')
        parser.add_argument('-s', dest='skip', nargs=1, default=[0], type=int,
                            help='how many files should be skipped from the beginnng (default: 0)')
        parser.add_argument('-t', dest='maxtimeout', nargs=1, default=[1.5], type=float,
                            help='maximal timeout (real timeout will be a random value from 0 to maximal timeout; default: 1.5)')
        args_namespace = parser.parse_args()
        if args_namespace:
            args = vars(args_namespace)
            for url in args['urls']:
                print("Loading manga chapter from URL '{}'".format(url))
                mangachan.download(url, args['folder'][0], args['skip'][0], args['maxtimeout'][0])
    
if __name__ == '__main__':
    mangachan.main()
