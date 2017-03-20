import json
import urllib
import urllib2

# My strategy is:
# # - retrieve dictionnary of list of all the pins metadata/description of the board
# # - remove from each description string the ponctuation and parse it into a list to get a list of words
# - checking that len>=2 starts and end with letters only, only contains alphabetical letters or ''' or '-' 
# and not in NLTK list. Populate a dictionnary adding word in lowercase.
# # - when done : reverse sort list of dict.items() which will be tuple of (word,count)
# # - add in a set the N first tuple

# Result
# The request is made to the API. The dictionnary get populated.I obtain a set 
# of top_N tuples of the word and its count but it does not quite match 
# the same result as the test case (for example: 3 cream and 3 ice on test case)

ACCESS_TOKEN = 'ASKf64NFBLHNCxziPMsKSGrV1t6xFKHI1qJDH1hDxkduZ6AyDQAAAAA'

NLTK_STOPWORDS = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves','its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did','this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']

def get_request(path, params=None):
    """
    Given a path, e.g. '/v1/me/' and params, return the response in json form.
    Take a look at https://developers.pinterest.com/docs/getting-started/introduction/
    to see what endpoints the Pinterest API has available!

    You may request additional parameters by overriding the params method
    """
    if params:
        params.update({'access_token': ACCESS_TOKEN})
    url = "%s?%s" % (path, urllib.urlencode(params))
    result = urllib2.urlopen(url)
    response_data = result.read()
    return json.loads(response_data)

def top_n_words(board_id, top_N):
    """ Given a and a number top_N, return a set of top_N tuples of the word and its count 
    that a board has in its Pins descriptions. """
    word_repertory = {}
    path = 'https://api.pinterest.com/v1/boards/%s/pins' %(board_id)
    more_data_remain = True
    params = {'fields': 'metadata','limit':'100'}
    
    # making request to API until no more data:
    while more_data_remain:
        response = get_request(path, params)
        all_pins_info = response['data']
        if response['page'].get('next', None) is None:
            more_data_remain = False
        else:
            params.update({'cursor': response['page']['cursor']})

        # adding to the word_rep dictionnary the word after cleaning it:
        for i in range(len(all_pins_info)):
            metadata = all_pins_info[i]['metadata']
            # checking that article exists here
            article = metadata.get('article','')
            if article != '':
                # checking that description exists here
                description = article.get('description', '')
                description_no_punct = ''.join([c for c in description if c not 
                    in (['!', '.', ',', '(', ')', '?','"','#', '/', '@',':',';'])])
                list_description = description_no_punct.split(' ')
                for word in list_description:
                    if is_valid(word):
                        word = word.lower()
                        word_repertory[word] = word_repertory.get(word, 0) + 1
    # collect the top_N words:
    ntop_words = n_valid_words(word_repertory, top_N)
    return ntop_words
    


def is_valid(word):
    """ Given a string return a boolean indicating if the string is valid 
    according to the q3 instructions"""
    if len(word)<2:
        return False 
    elif not(word[0].isalpha()) or not(word[-1].isalpha()):
        return False
    # expression like  http://, https://, or www. will be automatically eliminated by the presence of '.' and '/'
    elif len(list(filter(lambda x:(x.isalpha() or x =='-' or x =="'") , word[1:len(word)-1])))!=len(word)-2:
        return False
    elif word in NLTK_STOPWORDS:
        return False
    return True


def n_valid_words(repertory, top_N):
    """ Given a dictionnary and a top_N value, return the top_N word that are the
     most present """
    valid_world = repertory.items()
    top_words = (sorted(valid_world, key=lambda x:x[1], reverse=True))
    # case if top_N to big compared to the list of words
    if len(top_words) < top_N:
        ntop_words = set(top_words)
    else:
        ntop_words = set(top_words[:top_N])
        # looking for the remaining tie: 
        index = top_N 
        while top_words[index][1] == top_words[top_N-1][1] and index < len(top_words):
            ntop_words.add(top_words[index])
            index += 1
    return ntop_words