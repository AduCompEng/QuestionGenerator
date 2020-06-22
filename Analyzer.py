from nltk.corpus import framenet as fn
from Parser import ParseSentence
from Translator import run


class AnalyzeSentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.z = ParseSentence(self.sentence).zemberekParser()

    # Framelerde aramak için kelimenin cümledeki pos'unu al. Ve ingilizce karşılığında o pos'a sahip kelimeleri döndür.
    # 'august  (n./i.)' -> 'august.n'
    def getWordwithPos(self, wordList, pos):
        wordswithpos = []
        for word in wordList:
            start = word.find('(')
            word_ = word[0:start - 2]
            end = word.find('.')
            pos_ = word[start + 1:end]
            if pos == pos_:
                wordswithpos.append(word_ + '.' + pos)
        return wordswithpos

    # (['dog.n']:['Animal'], ['beach.n']:['Locale'],
    #  ['black.adj']:[], ['cat.n']:['Animal'],
    #  ['chase.v', 'pursue.v']:['Theme', 'Theme'])
    def findCoreType(self, wordList):
        dictim = []
        for word in wordList:
            word_ = '^{}$'.format(word)

            if len(fn.lus(word_)) > 0:
                ID = fn.lus(word_)[0].frame.ID
                dicti = [fename for fename, fe in fn.frame(ID).FE.items() if fe.coreType == 'Core']
                if len(dicti) > 0:
                    dictim.append(dicti[0])
        return dictim

    def findCategory(self, pla_case, wordList):
        place_case = ['de:Loc', 'da:Loc', 'a:Dat', 'e:Dat', 'ya:Dat', 'ye:Dat']
        if 'Person' in wordList:
            return 'Person'
        elif 'Locale' in wordList or 'Building' in wordList:
            if any(set(pla_case).intersection(place_case)):
                return 'Place'
        elif 'Relative_time' in wordList:
            return 'Time'
        elif 'Number' in wordList:
            return 'Number'

    def findCommonUsage(self):
        word_types_list = []

        # Cümledeki kelimelerin köklerini al.
        # "Köpek plajda siyah kediyi kovalıyor." -> köpek, plaj, siyah, kedi, kovalamak
        #  Kelimelerin yaygın kullanılan ing. karşılıklarını bul. -> ( köpek:['dog  (n./i.)'], plaj:['beach  (n./i.)'],
        # siyah:['black  (adj./s.)'], kedi:['cat  (n./i.)'],
        # kovalamak:['chase  (v./f.)', 'pursue  (v./f.)'])
        for index, word in enumerate(self.z["par_kelime_kok"]):
            if not run(word) is None:
                dicti, allwords = run(word)

                eng_words = []
                if 'Common Usage/Yaygın Kullanım' in dicti:
                    eng_words += dicti['Common Usage/Yaygın Kullanım']

                word_ = self.getWordwithPos(eng_words, self.z["par_kelime_pos_short"][index])
                word__ = self.findCoreType(word_)

                if self.findCategory(self.z["kelime_case_hazır"][index], word__) is not None:
                    word_types_list.append((self.z["kelimeler"][index], self.findCategory(self.z["kelime_case_hazır"][index], word__)))
        return word_types_list


analyzer = AnalyzeSentence("Köpek plajda siyah kediyi kovalıyor.")
print(analyzer.findCommonUsage())
