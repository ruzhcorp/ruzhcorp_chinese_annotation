# ruzhcorp_chinese_annotation

*For English version scroll down*

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

Атрибут `line_pinyin` возвращает список с разбором китайских токенов в пиньинь. 

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

## English version

Download [finetuned model](https://drive.google.com/drive/folders/1SmqS5sAmTtgBPHGtS8VhOJmaltonDN3q?usp=sharing)

```
>>> from chinese_annotator import ChineseLine
>>> line = ChineseLine('你好，妈妈！')
>>> line.process()
>>> line.line_hieroglyphs
[{'analysis': [{'lex': '你', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': '你'}, {'analysis': [{'lex': '好', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': '好'}, {'text': '，'}, {'analysis': [{'lex': '妈妈', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': '妈妈'}, {'text': '！'}]
>>> line.line_pinyin
[{'analysis': [{'lex': 'nǐ', 'transcr': 'nǐ', 'gr': 'PN', 'form_i': '你'}], 'text': 'nǐ'}, {'analysis': [{'lex': 'hǎo', 'transcr': 'hǎo', 'gr': 'VA', 'form_i': '好'}], 'text': 'hǎo'}, {'text': ','}, {'analysis': [{'lex': 'māma', 'transcr': 'māma', 'gr': 'NN', 'form_i': '妈妈'}], 'text': 'māma'}, {'text': '!'}]
```

Attribute `line_hieroglyphs` returns a list with analysis of Chinese tokens in hieroglyphs.

Attribute `line_pinyin` returns a list with analysis of Chinese tokens in pinyin. 

## Methods

For the correct work of all methods they should be executed in the following order:

1. `preprocessing` preprocesses a string of Chinese text:
* The characters '<', '>', '\n' are removed.
* Dots in borrowings are reduced to the same pattern.

2. `trad2simp` converts traditional characters into simplified characters.

3. `tokenize` tokenizes a string with the original spelling of the characters and a string with the characters in unified form. 
It also attributes PoS tags.

4. `custom_rules` applies custom rules to tokens. Now only splits by a dot that was not split.

5. `g2p` converts hieroglyphs into pinyin.
6. `postprocessing` converts tokens, PoS-tags and pinyin into two parsed lists.

`process` contains all methods in the correct order.

## Attributes

`line_trad` initial string

`line_simple` a string with simplified characters

`line_segmented_trad` a list of tokens in the original spelling of the characters

`tokens` a list of tokens in simplified characters with PoS-tags in the following form: [(token, PoS-tag), ...]

`line_g2p` a list of tokens in pinyin

`line_hieroglyphs` a list on analysis in hieroglyphs

`line_pinyin` a list of analysis in pinyin

## Благодарности

Проект выполнен при поддержке Комиссии по поддержке образовательных инициатив ФГН НИУ ВШЭ в рамках Конкурса проектных групп для обучающихся НИУ ВШЭ ФГН ([название проекта - «Лингвоспецифическая разметка китайских текстов в Русско-китайском параллельном корпусе НКРЯ»](https://ling.hse.ru/ruzhcorp_annotation)), 2020-2021 уч. год. 
![Логотип НИУ ВШЭ](https://www.hse.ru/data/2014/06/24/1310196796/logo_hse_cmyk.jpg)
