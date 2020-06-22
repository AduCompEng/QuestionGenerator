import stanfordnlp
from IPython.display import clear_output
from Zemberek_ import ZemberekInit


class ParseSentence:

    def __init__(self, sentence):
        self.sentence = sentence

    def zemberekParser(self):
        _morph = ZemberekInit(libjvmpath=r"C:\Program Files\Java\jdk1.8.0_151\jre\bin\server\jvm.dll").zemberek()
        zemberek = _morph.createWithDefaults()
        analysis = zemberek.analyzeSentence(self.sentence[:-1])
        disambiguate = zemberek.disambiguate(self.sentence[:-1], analysis)
        abbv = {'Noun': 'n', 'Verb': 'v', 'Adj': 'adj', 'Adv': 'adv', 'Conj': 'conj', 'Pron': 'pron', 'Postp': 'prep',
                'Det': 'a', 'Punc': 'p', 'Num': 'num'}

        kelimeler_pos = [str(kelime.getPos().shortForm) for kelime in disambiguate.bestAnalysis()]
        kelimeler_kok = [str(kelime.getLemmas()[0]) for kelime in disambiguate.bestAnalysis()]
        kelimeler_pos_short = [abbv.get(kelimeler_pos[index]) for index in range(len(kelimeler_kok))]

        kelime_case = [str(kelime.formatMorphemesLexical()) for kelime in disambiguate.bestAnalysis()]
        kelime_case_hazır_array_list = [kelime.getMorphemeDataList() for kelime in disambiguate.bestAnalysis()]
        kelime_case_hazır = convertArrayListtoList(kelime_case_hazır_array_list)
        kelimeler = [str(kelime.getNormalizedInput()) for kelime in analysis]

        par_kelime_pos = [str(kelime.getDictionaryItem().primaryPos.shortForm) for kelime in disambiguate.bestAnalysis()]
        par_kelime_kok = [str(kelime.getDictionaryItem().lemma) for kelime in disambiguate.bestAnalysis()]
        par_kelime_pos_short = [str(abbv.get(par_kelime_pos[index])) for index in range(len(par_kelime_pos))]

        zemdictionary = dict(zip(["kelimeler_pos", "kelimeler_kok", "kelimeler_pos_short",
                                  "par_kelime_pos", "par_kelime_kok", "par_kelime_pos_short",
                                  "kelime_case", "kelime_case_hazır", "kelimeler"],
                                 [kelimeler_pos, kelimeler_kok, kelimeler_pos_short,
                                  par_kelime_pos, par_kelime_kok, par_kelime_pos_short,
                                  kelime_case, kelime_case_hazır, kelimeler]))
        return zemdictionary

    def standfordNlpParser(self):
        nlp = stanfordnlp.Pipeline(lang="tr", treebank="tr_imst")
        doc = nlp(self.sentence)
        clear_output(wait=True)
        words = [token[2].text for token in doc.sentences[0].dependencies]
        dep_rel = [token[2].dependency_relation for token in doc.sentences[0].dependencies]
        upos = [token[2].upos for token in doc.sentences[0].dependencies]
        case = []

        for token in doc.sentences[0].dependencies:
            index = token[2].feats.find('Case')
            if index >= 0:
                case.append(token[2].feats[index + 5:index + 8])
            else:
                case.append('')

        standfordictionary = dict(zip(["words", "dep_rel", "upos", "case"], [words, dep_rel, upos, case]))
        return standfordictionary

    def printZemberekResults(self):
        zemberekParser = self.zemberekParser()
        print("kelimeler_kok_zem:", zemberekParser["kelimeler_kok"])
        print("kelimeler_pos_zem:", zemberekParser["kelimeler_pos"])
        print("kelimeler_pos_short:", zemberekParser["kelimeler_pos_short"])
        print()
        print("par_kelime_kok_zem:", zemberekParser["par_kelime_kok"])
        print("par_kelime_pos_zem:", zemberekParser["par_kelime_pos"])
        print("par_kelime_pos_short:", zemberekParser["par_kelime_pos_short"])
        print()
        print("kelime_case_zem:", zemberekParser["kelime_case"])
        print("kelimeler_zem:", zemberekParser["kelimeler"])
        print("kelime_case_hazır_zem:", [kelime for kelime in zemberekParser["kelime_case_hazır"]])

    def printStanfordNLPResults(self):
        stanfordParser = self.standfordNlpParser()
        print("words:", stanfordParser["words"])
        print("dep_rel:", stanfordParser["dep_rel"])
        print("upos:", stanfordParser["upos"])
        print("case:", stanfordParser["case"])


def convertArrayListtoList(arraylist):
    matrix = []
    for index, i in enumerate(arraylist):
        matrix.append([])

        for index2, j in enumerate(i):
            matrix[index].append(str(j))
    return matrix


#sentence = "Topu bana at."
#ParseSentence(sentence).printStanfordNLPResults()
