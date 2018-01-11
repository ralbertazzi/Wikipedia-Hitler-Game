from BeautifulSoup import BeautifulSoup
import urllib2
import re
import argparse

parser = argparse.ArgumentParser()



html_page = urllib2.urlopen('https://en.wikipedia.org/wiki/Edie_Campbell')
soup = BeautifulSoup(html_page)
all_hrefs = [link.get('href') for link in soup.findAll('a')]
wiki_hrefs = [href[6:] for href in all_hrefs if href is not None and href.startswith('/wiki/') and ':' not in href]
wiki_hrefs = list(set(wiki_hrefs))
print wiki_hrefs
