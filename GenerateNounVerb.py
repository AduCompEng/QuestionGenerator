class Generate:

    def generateNoun(word):

        print('Generating nouns.\n')

        word = 'armut'
        number = ['A3sg', 'A3pl']
        possessives = ['P1sg', 'P2sg', 'P3sg']
        cases = ['Dat', 'Loc', 'Abl']

        morphology = (_morph.builder().setLexicon(word).disableCache().build())

        item = morphology.getLexicon().getMatchingItems(word).get(0)

        for number_m in number:
            for possessive_m in possessives:
                for case_m in cases:
                    for result in morphology.getWordGenerator().generate(item, number_m, possessive_m, case_m):
                        print(str(result.surface))
                        # generateNoun("armut")

    def generateVerb(word, stem):

        print('Generating verbs.\n')

        positive_negatives = ['', 'Neg']
        times = ['Imp', 'Aor', 'Past', 'Prog1', 'Prog2', 'Narr', 'Fut']
        people = ['A1sg', 'A2sg', 'A3sg', 'A1pl', 'A2pl', 'A3pl']

        morphology = (_morph.builder().setLexicon(word).disableCache().build())

        for pos_neg in positive_negatives:
            for time in times:
                for person in people:
                    seq = java.util.ArrayList()
                    if pos_neg:
                        seq.add(pos_neg)
                    if time:
                        seq.add(time)
                    if person:
                        seq.add(person)
                    results = morphology.getWordGenerator().generate(stem, seq)

                    if not results:
                        print((
                            f'Cannot generate Stem = ["{stem}"]'
                            f'\n | Morphemes = {[str(morph) for morph in seq]}'
                        ))
                        continue
                    print(' '.join(str(result.surface) for result in results), [str(morph) for morph in seq])

    # generateVerb("yatmak","yat")