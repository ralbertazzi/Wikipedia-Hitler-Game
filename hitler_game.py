from BeautifulSoup import BeautifulSoup
import urllib2
import re
import argparse
from collections import namedtuple

parser = argparse.ArgumentParser()

target_title = 'Adolf_Hitler'

wikipedia_base = 'https://en.wikipedia.org'
already_visited = []
to_be_visited = []


class Node:

    def __init__(self, title, parent=None, children=[]):
        self.title = title
        self.parent = parent
        self.children = children


def print_solution(wiki_node):
    print 'Found it'


def visit(wiki_node):
    
    url = wikipedia_base + '/wiki/' + wiki_node.title
    print 'Visiting', url 
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    all_hrefs = [link.get('href') for link in soup.findAll('a')]
    # A valid link starts with /wiki/ and does not contain the characters :, otherwise it's gonna be some special Wikipedia page
    wiki_hrefs = [href[6:] for href in all_hrefs if href is not None and href.startswith('/wiki/') and ':' not in href]

    # Hack for removing duplicates
    wiki_hrefs = list(set(wiki_hrefs))

    if target_title in wiki_hrefs:
        print_solution(wiki_node)
    else:
        print wiki_hrefs
        children = [Node(wiki_href, parent=wiki_node) for wiki_href in wiki_hrefs]
        

root = Node('Edie_Campbell')
visit(root)
