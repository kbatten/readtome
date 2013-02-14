#!/usr/bin/env python

import sys
import re
import atexit
import time

try:
    import speech
except:
    class Speech(object):
        def say(self, text):
            print 'Saying: ' + text
            time.sleep(1)
    speech = Speech()


class Text(object):
    def __init__(self, data):
        self.data = ' '.join(data.split('\n')).strip()
        self.data = re.sub('<[a-zA-Z\/][^>]*>','',self.data)
        self.data = re.sub('(.)\\1{3,}', '\\1', self.data)
        
        self.offset = 0

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.offset))

    def load(self, filename):
        self.offset = 0
        try:
            with open(filename, 'r') as f:
                self.offset = int(f.read())
        except IOError:
            pass

    def words(self):
        offset = self.offset
        for word in self.data.split(' ')[offset:]:
            offset += 1
            self.offset = offset
            yield word

    def sentences(self):
        sentence = ''
        for word in self.words():
            # TODO: use a ' '.join()
            sentence = sentence + ' ' + word
            if re.search('[.?!]$', word):
                yield sentence
                sentence = ''
        if sentence:
            yield sentence


def save(text, filename):
    text.save(filename)

if __name__ == '__main__':
    filename = sys.argv[1]

# open {filename//./_}.sav
# read state
# jump to location
# create if not exist
# every X words write state to file
# on exit write state to file


    with open(filename) as f:
        text = Text(f.read())
        text.load(filename+'.sav')
        atexit.register(save, text, filename+'.sav')
        saved_offset = 0
        for sentence in text.sentences():
            speech.say(sentence)
            # save every 100 words
            if text.offset > saved_offset + 100:
                saved_offset = text.offset
                text.save(filename+'.sav')
