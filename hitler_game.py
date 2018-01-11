from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('start_title')
parser.add_argument('--target_title', default='Adolf_Hitler')
args = parser.parse_args()


wikipedia_base = 'https://en.wikipedia.org'
already_visited = set()
to_be_visited = []

def build_node(title, parent):
    return {'title': title, 'parent': parent}


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

    for idx, title in enumerate(all_titles, start=1):
        print idx, title
    
    print



wiki_node = build_node(args.start_title, None)

while True:
    
    url = wikipedia_base + '/wiki/' + wiki_node['title']
    print 'Visiting', url 
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    all_hrefs = [link.get('href') for link in soup.findAll('a')]
    # A valid link starts with /wiki/ and does not contain the characters :, otherwise it's gonna be some special Wikipedia page
    wiki_hrefs = [href[6:] for href in all_hrefs if href is not None and href.startswith('/wiki/') and ':' not in href]

    # Hack for removing duplicates
    wiki_hrefs = list(set(wiki_hrefs))

    if args.target_title in wiki_hrefs:
        print_solution(wiki_node)
        sys.exit()
    else:
        already_visited.add(wiki_node['title'])
        children = [build_node(wiki_href, parent=wiki_node) for wiki_href in wiki_hrefs]
        
        # Bread-first: append children and remove first (FIFO)
        to_be_visited += [child for child in children if child['title'] not in already_visited]
        

        # the pop will fail when the list will be empty, which means when you we'll have visited all the existing Wikipedia links (that takes a looong time), and you didn't find the target title (which means the target title was probably wrong. Sorry!)
        wiki_node = to_be_visited.pop(0)


