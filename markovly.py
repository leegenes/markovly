from random import choice

class Markovly:
    def __init__(self, text=None, n=None, token_type="word"):
        self.text = text
        self.ngram = n
        self.token_type = token_type
        self.tokens =  None

    def tokenize(self):
        if self.token_type == "char":
            text_pieces = list(self.text)
        else:
            text_pieces = self.text.split()
        tokens = {}

        for n, tp in enumerate(text_pieces):
            # ensures enough indices remaining
            # in text_pieces list for key and next word/char
            try:
                next_tp = text_pieces[n:n + self.ngram + 1]
            except IndexError:
                break

            # set key as tuple of length n
            k = tuple(next_tp[:- 1])
            if len(k) != self.ngram:
                break
            # add key if not in token dict
            if k not in tokens:
                tokens[k] = []
            # set
            last_tp = next_tp[-1]
            tokens[k].append(last_tp)
        self.tokens = tokens
        return self.tokens

    def generate_verse(self):
        # determines if a line should break
        # will in all cases with more than
        # 1 word on previous line - unless
        # previous line includes an !
        def insert_break(since_last_break):
            if '!' in since_last_break:
                return True
            elif since_last_break.count(' ') <= 1 or ',' in since_last_break[-4:]:
                return False
            return True

        def get_last_break(line):
            if '\n' in line:
                last_break = len(line) - line[-1::-1].index('\n') -1
            else:
                last_break = 0
            return last_break

        max_len = 5 if self.token_type == "word" else 280
        start_keys = [k for k in self.tokens.keys() if k[0].isupper()]
        k = choice(start_keys)
        verse = list(k)
        while len(verse) < max_len:
            try:
                next_piece = choice(self.tokens[k])
            except KeyError:
                break
            if next_piece[0].isupper():
                last_break = get_last_break(verse)
                since_break = verse[last_break:]
                if insert_break(since_break):
                    verse.append('\n')
            verse.append(next_piece)
            k = k[1:] + (next_piece,)
        if verse[-1] != ' ':
            verse = verse[:get_last_break(verse)]
        return ''.join(verse)

    def generate_song(self, verse_count):
        verses = []
        for i in range(verse_count):
            verses.append(self.generate_verse())
        return '\n\n'.join(verses)

if __name__ == '__main__':
    words = input()
    m = Markovly(text=words, n=8, token_type="char")
    print(m.generate_verse())
