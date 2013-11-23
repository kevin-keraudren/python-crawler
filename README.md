Python crawler exercise
=======================

Usage:
`./crawl.py http://www.periapt.co.uk/ --verbose --dir periapt`

I chose http://pypi.python.org/pypi/htmldata/1.1.1 for extracting urls from the
html for its ease of use, even though it is neither perfect nor up-to-date.

I defined the "domain" as being:
  splitted_url = urlparse.urlsplit( seed )
  domain = splitted_url.netloc
  domain = re.sub( r'^www\.', '', domain)

so that subdomains where "www" is replaced by "code" or "web" are also crawled.       

I did not deal with user-agent definitions nor robots rules.

