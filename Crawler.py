"""Crawler class"""

# Written by Kevin Keraudren, 14/06/2011

import urllib
import htmldata # http://pypi.python.org/pypi/htmldata/1.1.1
import urlparse
import os
import re
import hashlib

# CAVEATS:
# * I did not work specifically on the HTML parsing and instead did a search on
# http://pypi.python.org/
# to find the most appropriate/easy to use module.
# Using a more complex/up-to-date module might have avoided dealing with bugs in htmldata,
# but on the other hand resulted in more time spent reading doc, and longer code.
#
# * urls with queries: I might be getting several times the same data under
# different names.
#
# * default user-agent, no respect for robots rules.
#
# * I should gently open the files to check whether it is HTML data. I chose to
# do a "try".
#
# * I do not "localize" the urls: it will not be possible to browse offline

class Crawler(object):
    def __init__(self,seed, rootdir='./', verbose=False):
        if not re.search( r'^http://', seed ):
            seed = 'http://' + seed
            
        if not re.search( r'/$', rootdir ):
            rootdir += '/'

        # I chose "hanzoarchives.com" as a "domain definition",
        # which means we crawl "web.hanzoarchives.com", "code.hanzoarchives.com",...
        splitted_url = urlparse.urlsplit( seed )
        domain = splitted_url.netloc
        self.domain = re.sub( r'^www\.', '', domain)

        self.domain_regexp = re.compile( self.domain + "$")
        self.queue = [seed]
        self.seen = []
        self.root = rootdir
        self.verbose = verbose

    def __str__(self):
         rep =  "Domain:\t" + self.domain + "\n"
         rep += "Rootdir:\t" + str(self.root) + "\n"
         rep += "Queue:\t" + str(self.queue) + "\n"
         rep += "Seen:\t" + str(self.seen) + "\n"
         rep += "Verbose:\t" + str(self.verbose) + "\n"
         return rep

    def crawl(self):

        # are there more pages to crawl ?
        if len(self.queue) == 0:
            return # task done

        # get a URL
        url = self.queue.pop()

        # process it only if it is a new one
        if url not in self.seen:
            self.seen.append(url)
            splitted_url = urlparse.urlsplit( url )
            local_file = self.root + splitted_url.path
            (head,tail) = os.path.split( local_file )
            if tail == '':
                tail = 'index.html'
                local_file = local_file + '/' + tail
            if os.path.isdir(local_file):
                local_file += '/index.html'

            if splitted_url.query:  # query strings could contain anything, let's      
                md5 = hashlib.md5() # not put them raw in filenames
                md5.update(splitted_url.query)
                local_file += '.' + md5.hexdigest()
                
            if os.path.exists( head ): # main logic for "unnamed pages"
                if os.path.isfile(head):
                    os.rename( head, head + '.tmp')
                    os.makedirs( head )
                    os.rename(head + '.tmp', head+ '/index.html')
            else:
                os.makedirs( head )

            if self.verbose: print 'saving', url, 'to', local_file
            urllib.urlretrieve( url, local_file )

            # is it HTML ?
            f = open( local_file, 'rb' )
            try: # brutal, I know...
                for u in htmldata.urlextract(f.read(), url):
                    # get rid of url "fragments"
                    new_split = urlparse.urlparse(u.url)
                    new_url = 'http://' + new_split.netloc + new_split.path
                    if new_split.query:
                        new_url += '?' + new_split.query
                    if self.valid(new_url) and new_url not in self.seen and new_url not in self.queue:
                        self.queue.append(new_url)
            except:
                if self.verbose:
                    print url, 'is not HTML'

        # recurse
        if self.verbose: print "QUEUE LENGTH:", len(self.queue)
        self.crawl()

    def valid(self,url):
        if re.search(r'\s',url): # bug in htmldata
            return False
        if re.search(r'([^/]+)/\1/\1/\1', url): # bug in htmldata, certainly due
            # to "../../../hsimage" urls
            return False
        splitted_url = urlparse.urlsplit( url )
        if re.search( self.domain_regexp, splitted_url.netloc):
            if self.verbose: print url, "YES"                
            return True
        else:
            if self.verbose: print url, "NO"  
            return False


                
