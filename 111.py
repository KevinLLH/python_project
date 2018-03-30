#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tqdm import tqdm

__author__ = 'luhui.liu'
from six.moves import xrange

def sub(filename):
    fw = open('data/sy1111.txt', 'w', encoding="utf-8")
    with open('data/' + filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            data = line.strip()
            print(len(data))
            if len(data) == 0:
                print("############")
                continue
            else:
                print(line)
                fw.write(line)
            #line_new = line.replace(line.strip().split(',')[0],'')
            #line_new = line.strip(",")


        fw.close()
            #query_string = line.strip().split('	')[0]
    for i in xrange(100):
        print(i)


def load_word2vec():
    print ('Loading word2vec embedding...')
    with open("output/word2vec_new.txt") as fin:
        print(fin.readline().split(""))
        _, dim = map(int, fin.readline().split())
        ret = [0. for _ in xrange(10000 + 2)]
        ret[-1] = [0. for _ in xrange(dim)]
        ret[-2] = map(float, fin.readline().rstrip().split()[1:])
        for line in tqdm(fin.readlines()):
            ps = line.rstrip().split()
            # if ps[0] in vocab2idx:
            #     ret[vocab2idx[ps[0]]] = map(float, ps[1:])

    return ret

if __name__ == '__main__':
    #load_word2vec()
    string = "111 222"
    print(string.split())
    _, dim = map(int, string.split())
    print(dim)