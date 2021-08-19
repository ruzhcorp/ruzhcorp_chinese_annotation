# ruzhcorp_chinese_annotation

Скачать [finetuned model](https://drive.google.com/drive/folders/1SmqS5sAmTtgBPHGtS8VhOJmaltonDN3q?usp=sharing)

```
>>> from chinese_annotator import ChineseLine
>>> line = ChineseLine('你好，妈妈！')
>>> line.process()
>>> line.line_hieroglyphs
[{'analysis': [{'lex': '你', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': '你'}, {'analysis': [{'lex': '好', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': '好'}, {'text': '，'}, {'analysis': [{'lex': '妈妈', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': '妈妈'}, {'text': '！'}]
>>> line.line_pinyin
[{'analysis': [{'lex': 'nǐ', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': 'nǐ'}, {'analysis': [{'lex': 'hǎo', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': 'hǎo'}, {'text': ','}, {'analysis': [{'lex': 'māma', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': 'māma'}, {'text': '!'}]
```

Атрибут `line_hieroglyphs` возвращает список с разбором китайских токенов в иероглифическом написании.

Атрибут `line_pinyin` возвращает списко с разбором китайских токенов в пиньинь. 

## Методы

Чтобы методы правильно работали, их нужно выполнять в следующем порядке:

1. `preprocessing` предобрабатывает строку китайского текста:
* Убираются символы '<', '>', '\n'
* Точки в заимствованиях приводятся к одному образцу

2. `trad2simp` конвертирует традиционные иероглифы в упроещенные.

3. `tokenize` токенизирует строку с изначальным написанием иероглифов и строку с иероглифами в унифицированном виде. 
А также приписывает PoS-тэги.

4. `custom_rules` применяет кастомные правила к токенам. Сейчас только делит по точке то, что не разделилось.

5. `g2p` конвертирует иероглифы в пиньинь.
6. `postprocessing` преобразовывает токены, PoS-tags и пиньинь в два списка с разбором.

`process` содержит в себе все методы в правильном порядке.

## Атрибуты

`line_trad` исходная строка

`line_simple` строка с упрощенными иероглифами

`line_segmented_trad` список традиционных токенов

`tokens` список упрощенных токенов с PoS-тэгами в формате: [(token, PoS-tag), ...]

`line_g2p` список пиньинь

`line_hieroglyphs` список пословного разбора с иероглифами

`line_pinyin` список пословного разбора с пиньинь
