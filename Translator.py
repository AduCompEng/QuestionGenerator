import json
import hashlib
import requests
from collections import OrderedDict, Callable

class DefaultOrderedDict(OrderedDict):

    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))
def get_result(word):
    result = dict()
    m = hashlib.md5()
    m.update("{}46E59BAC-E593-4F4F-A4DB-960857086F9C".format(word).encode("UTF-8"))
    code = m.hexdigest()
    url = "http://ws.tureng.com/TurengSearchServiceV4.svc/Search"
    data = {"Term": word, "Code": code}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    obj = json.loads(response.text)

    mobil_results = obj['MobileResult']
    is_found = bool(mobil_results['IsFound'])

    if is_found:
        result_group = DefaultOrderedDict(list)
        for row in mobil_results['Results']:
            result_group[row['CategoryEN']].append(row)
        result['results'] = result_group
        return result
    else:
        result['suggestions'] = mobil_results['Suggestions']
        return result

def run(_word):
    translate_result = get_result(_word)

    if 'results' in translate_result:
        result_group = translate_result['results']

        words = []
        titles = []
        allWords = []

        for category_en, items in result_group.items():
            word = []

            if items[0]['CategoryTR'][-8:] == '(tr->en)':
                titles.append("{}/{}".format(category_en[:-9], items[0]['CategoryTR'][:-9]))
                for item in items:
                    my_types = "/".join(filter(lambda x: x!=None, [item['TypeEN'], item['TypeTR']]))
                    my_types = (" (%s)" % my_types) if my_types else ""
                    word.append("{} {}".format(item['Term'], my_types))
                    allWords.append(item['Term'])
                words.append(word)
        return dict(zip(titles, words)), allWords
    else:
        return None