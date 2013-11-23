#!/usr/bin/env python
# Written by Kevin Keraudren, 14/06/2011

import argparse

from Crawler import Crawler

parser = argparse.ArgumentParser(
    usage = "Usage: %(prog)s seed_url [options]" )
parser.add_argument(
    'seed',
    metavar='seed_url',        
    help='url for starting the crawl' )
parser.add_argument(
    '--dir',
    default='./',
    help="root directory to store the result of the crawl" )
parser.add_argument(
    '--verbose',
    action="store_true", default=True,
    help="verbose mode" ) 

args = parser.parse_args()

crawler = Crawler( args.seed, rootdir=args.dir, verbose=args.verbose )

print crawler
crawler.crawl()
print crawler
print "Crawl complete"

