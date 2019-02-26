# -*- coding: utf-8 -*-
import codecs, sys, io
knouns = {
	'i': u'나',
	'I': u'나',
	'store': u'가게',
	'road': u'길',
	'weather': u'날씨',
	'bakery': u'뻥집',
	'book': u'책',
	'read': u'읽다',
}
kverbs = {
	'ing':u'어요' 
}
'''
name = None
with io.open('korean.txt','r',encoding='utf-8') as f:
	for li in f:
		name = li
		print(li.strip())
with codecs.open('korean.txt','r','utf-8') as f:
	for li in f:
		print(li.strip())

print(sys.getdefaultencoding())

print("{} is my name".format(name))
for i in knouns.keys():
	print(i,knouns[i])
'''
sentence = input(">>> ")
tokens = sentence.split()
nouns = []
print("parsing")
for t in tokens:
	print(t)
	if t in knouns.keys():
		nouns.append(knouns[t])
	if t.endswith('ing'):
		verb = t.split('ing')[0]
		print(verb)
		if verb in knouns.keys():
			nouns.append(knouns[verb][0])
		print(kverbs['ing'][0])
		nouns[-1] += kverbs['ing']
print("parsing done")
string = ""
for i in reversed(nouns):
	string += " "+i
if string[-1] == knouns['I']:
	string = string[0:len(string)-1]
print(string)

