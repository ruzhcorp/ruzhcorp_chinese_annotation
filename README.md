# ruzhcorp_chinese_annotation

To download [finetuned model](https://drive.google.com/drive/folders/1SmqS5sAmTtgBPHGtS8VhOJmaltonDN3q?usp=sharing)

```
>>> from chinese_annotator import ChineseLine
>>> line = ChineseLine('你好，妈妈！')
>>> line.process()
>>> line.line_hieroglyphs
[{'analysis': [{'lex': '你', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': '你'}, {'analysis': [{'lex': '好', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': '好'}, {'text': '，'}, {'analysis': [{'lex': '妈妈', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': '妈妈'}, {'text': '！'}]
>>> line.line_pinyin
[{'analysis': [{'lex': 'nǐ', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': 'nǐ'}, {'analysis': [{'lex': 'hǎo', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': 'hǎo'}, {'text': ','}, {'analysis': [{'lex': 'māma', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': 'māma'}, {'text': '!'}]
```

Attribute `line_hieroglyphs` gives a list of analysis of Chinese words in hieroglyphs.

Attribute `line_pinyin` gives a list of analysis of Chinese words in pinyin. 
