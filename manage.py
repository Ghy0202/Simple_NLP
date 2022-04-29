#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import numpy as np
from django.conf import settings
from django.conf.urls.static import static
#-------------------导入ABSC
# 下面是Tokenizer的具体创建

class Tokenizer(object):
    '''将text转成index'''
    def __init__(self,vocab,max_length,lower):
        self.vocab=vocab
        self.max_length=max_length
        self.lower=lower

    @classmethod
    def from_files(cls,fnames,max_length,lower=True):
        corpus=set()
        for fname in fnames:
            for obj in parseXML(fname):
                text_raw=obj['text']
                if lower:
                    text_raw=text_raw.lower()
                corpus.update(Tokenizer.split_text(text_raw))
        return cls(vocab=Vocab(corpus,add_pad=True,add_unk=True),max_length=max_length,lower=lower)
    @staticmethod
    def pad_sequence(sequence,pad_id,maxlen,dtype='int64',padding='post',truncating='post'):
        x=(np.zeros(maxlen)+pad_id).astype(dtype)
        if truncating=='pre':
            trunc=sequence[-maxlen:]
        else:
            trunc=sequence[:maxlen]
        trunc=np.asarray(trunc,dtype=dtype)
        if padding=='post':
            x[:len(trunc)]=trunc
        else:
            x[-len(trunc):]=trunc
        return x

    @staticmethod
    def split_text(text):
        for ch in ["\'s", "\'ve", "n\'t", "\'re", "\'m", "\'d", "\'ll", ",", ".", "!", "*", "/", "?", "(", ")", "\"", "-", ":"]:
            text=text.replace(ch," "+ch+" ")
        return text.strip().split()

    def position_sequence(self,text,start,end,reverse=False,padding='post',truncating='post'):
        text_left=Tokenizer.split_text(text[:start])
        text_aspect=Tokenizer.split_text(text[start:end])
        text_right=Tokenizer.split_text(text[end:])
        tag_left=[len(text_left)-i for i in range(len(text_left))]
        tag_aspect=[0 for i in range(len(text_aspect))]
        tag_right=[i+1 for i in range(len(text_right))]
        position_tag=tag_left+tag_aspect+tag_right
        if len(position_tag)==0:
            position_tag=[0]
        if reverse:
            position_tag.reverse()
        return Tokenizer.pad_sequence(position_tag,pad_id=0,maxlen=self.max_length,
                                      padding=padding,truncating =truncating)

    def text_to_sequence(self,text,reverse=False,padding='post',truncating='post'):
        if self.lower:
            text=text.lower()
        words=Tokenizer.split_text(text)
        sequence=[self.vocab.word_to_id(w) for w in words]
        if len(sequence)==0:
            sequence=[0]
        if reverse:
            sequence.reverse()

        return Tokenizer.pad_sequence(sequence,pad_id=self.vocab.pad_id,maxlen=self.max_length,padding=padding,truncating=truncating)


# 下面是Vocab的具体创建
class Vocab(object):
    '''数据集的词典'''
    def __init__(self,vocab_list,add_pad,add_unk):
        self._vocab_dict=dict()
        self._reverse_vocab_dict=dict()
        self._length=0
        if add_pad:
            self.pad_word='<pad>'
            self.pad_id=self._length
            self._length+=1
            self._vocab_dict[self.pad_word]=self.pad_id
        if add_unk:
            self.unk_word = '<unk>'
            self.unk_id = self._length
            self._length += 1
            self._vocab_dict[self.unk_word] = self.unk_id
        for w in vocab_list:
            self._vocab_dict[w]=self._length
            self._length+=1

        for w,i in self._vocab_dict.items():
            self._reverse_vocab_dict[i]=w

    def word_to_id(self,word):
        if hasattr(self,'unk_id'):
            return self._vocab_dict.get(word,self.unk_id)
        return self._vocab_dict[word]


    def id_to_word(self,id):
        if hasattr(self,'unk_word'):
            return self._reverse_vocab_dict.get(id,self.unk_word)
        return self._reverse_vocab_dict[id]

    def has_word(self,word):
        return word in self._vocab_dict


    def __len__(self):
        return self._length

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NLP_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    #main()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NLP_system.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
