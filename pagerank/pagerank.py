import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Assigning each page a rank of 1/N, where N is the total number of pages
    N = len(corpus)
    allpages = set(corpus.keys())
    pageranks = {}
    pageconv = {}
    numlinks = {}

    # Special handling for page w/o links:
    #     "A page that has no links at all should be interpreted as having
    #      one link for every page in the corpus (including itself)."
    for p in corpus:
        pageranks[p] = 1 / N
        pageconv[p] = 1
        if corpus[p]:
            numlinks[p] = len(corpus[p])
        else:
            # Page has no link
            corpus[p] = allpages
            numlinks[p] = N

    # PageRank formula: PR(p)=(1-d)/N+d*sum_i(PR(i)/NumLinks(i))
    # Where d = the damping factor,
    #       N = the total number of pages in the corpus,
    #       i ranges over all pages that link to page p,
    #       NumLinks(i) = the number of links present on page i.
    while True:
        for p in pageranks:
            # Update page ranks
            summation = 0
            last_rank = pageranks[p]
            for i in corpus:
                if p in corpus[i]:
                    summation += pageranks[i] / numlinks[i]
            pageranks[p] = (1 - damping_factor) / N + damping_factor * summation

            # Update convergence cflag
            if abs(last_rank - pageranks[p]) <= 0.001:
                pageconv[p] = 0
            else:
                pageconv[p] = 1

        if sum(pageconv.values()) == 0:
            break

    return pageranks


if __name__ == "__main__":
    main()
