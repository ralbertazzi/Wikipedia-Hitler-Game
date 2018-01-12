from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import argparse
from multiprocessing import Pool
import threading
from Queue import Queue


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('start_title', help='The url of the start wiki page after https://en.wikipedia.org/wiki/')
parser.add_argument('--target_title', default='Adolf_Hitler', help='The url of the target wiki page after https://en.wikipedia.org/wiki/')
parser.add_argument('--nb_workers', type=int, default=4, help='Number of working processes')
args = parser.parse_args()


if args.start_title == args.target_title:
    print 'Too easy!'
    sys.exit()

wikipedia_base = 'https://en.wikipedia.org'
already_visited = set()
to_be_visited = []

def build_node(title, parent):
    return {'title': title, 'parent': parent, 
            'depth': parent['depth'] + 1 if parent is not None else 0}


def print_solution(wiki_node):
    
    print
    print 'Found it!'
    print

    all_titles = []

    def recursive_go_to_parent(node):
        
        all_titles.append(node['title'])
        if node['parent'] is not None:
            recursive_go_to_parent(node['parent'])

    recursive_go_to_parent(wiki_node)

    all_titles = all_titles[::-1]  # Reverse list
    all_titles.append(args.target_title)

    for idx, title in enumerate(all_titles):
        print idx, title
    
    print


input_queue = Queue()
output_queue = Queue()


def get_links(wiki_node):

    url = wikipedia_base + '/wiki/' + wiki_node['title']
    # print '({}) Visiting {}'.format(wiki_node['depth'], url)

    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)

    # Get all the hrefs in the page
    all_hrefs = [link.get('href') for link in soup.findAll('a')]
  
    # A valid link starts with /wiki/ and does not contain the characters :, otherwise it's gonna be some special Wikipedia page
    # href[6:] removes the '/wiki/' part
    wiki_hrefs = [href[6:] for href in all_hrefs if href is not None
                             and href.startswith('/wiki/') and ':' not in href]

    # Hack for removing duplicates (unnecessary)
    wiki_hrefs = list(set(wiki_hrefs))
    return wiki_node, wiki_hrefs


def main_underground_thread():

    pool = Pool(args.nb_workers)
    
    while True:
        links = input_queue.get()
        for wiki_node, wiki_hrefs in pool.imap_unordered(get_links, links):
            output_queue.put((wiki_node, wiki_hrefs))




######################   Let's compute   ###########################################

wiki_node = build_node(args.start_title, None)
mu_thread = threading.Thread(target=main_underground_thread)
mu_thread.daemon = True
mu_thread.start()

input_queue.put([wiki_node])

while True:	

    wiki_node, wiki_hrefs = output_queue.get()
    print '({}) Visiting {}'.format(wiki_node['depth'], wiki_node['title'])
    
    if args.target_title in wiki_hrefs:
        print_solution(wiki_node)
        sys.exit()
    else:
        already_visited.add(wiki_node['title'])
        children = [build_node(wiki_href, parent=wiki_node) for wiki_href in wiki_hrefs]
        
        # Bread-first: append children and remove first (FIFO)
        children_to_be_visited = [child for child in children if child['title'] not in already_visited]
        input_queue.put(children_to_be_visited)        
        # the pop will fail when the list will be empty, 
        # which means when you we'll have visited all the existing 
        # Wikipedia links (that takes a looong time), and you didn't find the target title 
        # (which means the target title was probably wrong. Sorry!)


