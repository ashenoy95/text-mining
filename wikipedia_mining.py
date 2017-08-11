import requests

'''
Wikipedia Mediawiki API docs:
https://www.mediawiki.org/wiki/API:Info

Wikipedia API Sandbox:
https://www.mediawiki.org/wiki/Special:ApiSandbox

To retrieve different information, only the params have to be changed. 

'''

WIKIPEDIA_API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'


def page_ids(titles):
    """Look up the Wikipedia page ids by title.

    For example, the Wikipedia page id of "Albert Einstein" is 736. 

    Args:
        titles (list of str): List of Wikipedia page titles.

    Returns:
        list of int: List of Wikipedia page ids.

    """
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': '|'.join(titles),
        'format': 'json',
        'formatversion': 2  # version 2 is easier to work with
    }
    payload = requests.get(WIKIPEDIA_API_ENDPOINT, params=params)
    response = payload.json()

    pageids = []
    for i in range(len(titles)):
        pageids.append(response['query']['pages'][i]['pageid'])
    return pageids


def page_lengths(ids):
    """Find the length of a page according to the Mediawiki API.

    A page's length is measured in bytes which, for English-language pages, is
    approximately equal to the number of characters in the page's source.

    Args:
        ids (list of str): List of Wikipedia page ids.

    Returns:
        list of int: List of page lengths.

    """
    page_lengths = []
    ids = list(map(str,ids))

    params = {
        'action': 'query',
        'prop': 'info',
        'pageids': '|'.join(ids),
        'format': 'json',
        'formatversion': 2  
    }
    payload = requests.get(WIKIPEDIA_API_ENDPOINT, params=params)
    response = payload.json()

    for i in range(len(ids)):
        page_lengths.append(response['query']['pages'][i]['length'])
    return page_lengths


def recent_revision_ids(id, n):
    """Find the revision ids of recent revisions to a single Wikipedia page.

    The Wikipedia page is identified by its page id and only the `n` most
    recent revision ids are returned.

    Args:
        id (int): Wikipedia page id
        n (int): Number of revision ids to return.

    Returns:
        list of int: List of length `n` of revision ids.

    """
    revision_ids = []

    params = {
        'action': 'query',
        'prop': 'revisions',
        'pageids': id,
        'format': 'json',
        'formatversion': 2,  
        'rvlimit': n
    }
    payload = requests.get(WIKIPEDIA_API_ENDPOINT, params=params)
    response = payload.json()
    
    for i in range(n):
        revision_ids.append(response['query']['pages'][0]['revisions'][i]['revid'])
    return revision_ids


def revisions(revision_ids):
    """Fetch the content of revisions.

    Revisions are identified by their revision ids.

    Args:
        revision_ids (list of int): Wikipedia revision ids

    Returns:
        list of str: List of length `n` of revision contents.

    """
    revision_contents = []
    revision_ids = list(map(str,revision_ids))

    params = {
        'action': 'query',
        'prop': 'revisions',
        'revids': '|'.join(revision_ids),
        'rvprop': 'content',
        'format': 'json',
        'formatversion': 2 
    }
    payload = requests.get(WIKIPEDIA_API_ENDPOINT, params=params)
    response = payload.json()

    for page in response['query']['pages']:
        for rev in page['revisions']:
            revision_contents.append(rev['content'])
    return revision_contents


if __name__ == '__main__':
    titles = ['Albert Einstein','Germany']
    print('Titles: ', titles)

    ids = page_ids(titles)
    print('Page IDs: ', ids)

    print('Page lengths: ', page_lengths(ids))

    recent_revision_ids = recent_revision_ids(ids, 3)
    print("3 most recent revision ids: ", recent_revision_ids)

    #print('Revision {}:\n'.format(recent_revision_ids[0]), revisions(recent_revision_ids)[0])


