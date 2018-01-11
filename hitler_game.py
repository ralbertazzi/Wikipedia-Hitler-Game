from BeautifulSoup import BeautifulSoup
import urllib2
import re
import argparse

parser = argparse.ArgumentParser()

wikipedia_base = 'https://en.wikipedia.org'
already_visited = []


def visit(wiki_title):

    html_page = urllib2.urlopen(wikipedia_base + '/wiki/' + wiki_title)
    soup = BeautifulSoup(html_page)
    all_hrefs = [link.get('href') for link in soup.findAll('a')]
    # A valid link starts with /wiki/ and does not contain the characters :, otherwise it's gonna be some special Wikipedia page
    wiki_hrefs = [href[6:] for href in all_hrefs if href is not None and href.startswith('/wiki/') and ':' not in href]

    # Hack for removing duplicates
    wiki_hrefs = list(set(wiki_hrefs))
    print wiki_hrefs

visit('Edie_Campbell')
