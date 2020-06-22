from Parser import ParseSentence

class SentenceCoreParts:

    def __init__(self, sentence):
        self.z = ParseSentence(sentence).zemberekParser()
        self.s = ParseSentence(sentence).standfordNlpParser()

    def findBliIsimTamlamasi(self):

        tamlayan_ekleri = ['ın:Gen', 'in:Gen', 'un:Gen', 'ün:Gen', 'im:Gen', 'nın:Gen', 'nin:Gen', 'nun:Gen', 'nün:Gen']
        tamlanan_ekleri = ['ı:P3sg', 'i:P3sg', 'u:P3sg', 'ü:P3sg', 'sı:P3sg', 'si:P3sg', 'su:P3sg', 'sü:P3sg',
                           'im:P3sg', 'in:P3sg', 'im:P1sg']

        for index in range(len(self.z["kelime_case_hazır"]) - 1):
            if len(set(self.z["kelime_case_hazır"][index]).intersection(set(tamlayan_ekleri))) > 0 and \
                    len(set(self.z["kelime_case_hazır"][index + 1]).intersection(set(tamlanan_ekleri))) > 0:
                print(' '.join(self.z["kelimeler"][index: index + 2]))

    def findSıfatTamlaması(self):

        sıfat_tam = [['Adj', 'Noun'], ['Det', 'Noun'], ['Num', 'Noun'], ['Adj', 'Det', 'Noun']]
        listem = []

        for i in sıfat_tam:

            if len(commonElementIndexes(i, self.z["kelimeler_pos"])) > 0:
                for x in commonElementIndexes(i, self.z["kelimeler_pos"]):
                    start_index = x[0]
                    end_index = x[1]
                    listem.append(' '.join(self.z["kelimeler"][start_index:end_index]))
        return listem

    def findNesne(self):

        if 'obj' in self.s["dep_rel"]:
            object_index = self.s["dep_rel"].index('obj')
            return self.s["words"][object_index]

    def findOzne(self):

        if 'nsubj' in self.s["dep_rel"]:
            subject_index = self.s["dep_rel"].index('nsubj')
            return self.s["words"][subject_index]

    def findZarf(self):

        if 'Adv' in self.z["kelimeler_pos"]:
            subject_index = self.z["kelimeler_pos"].index('Adv')
            return self.z["kelimeler"][subject_index]


def commonElementIndexes(small, big):
    start_end_indexes = []
    for i in range(len(big) - len(small) + 1):
        for j in range(len(small)):
            if big[i + j] != small[j]:
                break
        else:
            start_end_indexes.append([i, i + len(small)])
    return start_end_indexes


core = SentenceCoreParts("Köpek plajda siyah kediyi kovalıyor.")
print("Özne", core.findOzne())
print("Nesne", core.findNesne())
print("Belirtili İsim Tamlaması", core.findBliIsimTamlamasi())
print("Sıfat Tamlaması", core.findSıfatTamlaması())
