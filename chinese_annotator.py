import re
from g2pc import g2pc
from numerical_pinyin_converter import convert_from_numerical_pinyin
from hanziconv import HanziConv
from fastHan import FastHan
model = FastHan(model_type='large', url="finetuned_model")
model.set_cws_style('ctb')
g2p = g2pc.G2pCFH()  # измененный класс, который принимает вместо строки список токенов с PoS-тэгами
# в формате: [(token, PoS-tag), ...]


class ChineseLine:
    def __init__(self, line: str) -> None:
        self.line_trad = line  # Исходная строка
        self.line_simple = self.trad2simp()  # Строка с упрощенными иероглифами
        self.line_segmented_trad = []  # Список традиционных токенов
        self.tokens = []  # Список упрощенных токенов с PoS-тэгами в формате: [(token, PoS-tag), ...]
        self.line_g2p = []  # Список пиньинь
        self.line_hieroglyphs = []  # Список пословного разбора с иероглифами
        self.line_pinyin = []  # Список пословного разбора с пиньинь

    def preprocessing(self) -> None:
        """
        Метод, который предобрабатывает строку китайского текста:
            1. Убираются символы '<', '>', '\n'
            2. Точки в заимствованиях приводятся к одному образцу
        :return: None
        """
        self.line_trad = re.sub('[<>\n]', '', self.line_trad)
        self.line_trad = re.sub('•', '·', self.line_trad)

    def trad2simp(self) -> str:
        """
        Метод, который преобразовывает традиционные иероглифы в упрощенные
        :return: строка с упрощенными иероглфами
        """
        return HanziConv.toSimplified(self.line_trad)

    def tokenize(self) -> None:
        """
        Метод, который производит CWS и PoS-tagging
        :return: None
        """
        self.tokens = model(self.line_simple, 'POS')[0]
        for token in self.tokens:
            i = len(token[0])
            self.line_segmented_trad.append(self.line_trad[:i])
            self.line_trad = self.line_trad[i:]

    def custom_rules(self) -> None:
        """
        Метод, который применяет кастомные правила к токенам. Сейчас только делит по точке то, что не разделилось
        :return: None
        """
        i = 0
        while i < len(self.tokens):
            if '·' in self.tokens[i][0] and len(self.tokens[i][0]) > 1:
                parts_hieroglyphs_simp = self.tokens[i][0].split('·')
                parts_hieroglyphs_trad = self.line_segmented_trad[i].split('·')
                length = len(parts_hieroglyphs_simp) * 2 - 1
                self.tokens[i+length:] = self.tokens[i+1:]
                self.line_segmented_trad[i+length:] = self.line_segmented_trad[i+1:]
                for j in range(length):
                    if j % 2 == 0:
                        self.tokens[i+j] = (parts_hieroglyphs_simp[int(j/2)], self.tokens[i][1])
                        self.line_segmented_trad[i+j] = parts_hieroglyphs_trad[int(j/2)]
                    else:
                        self.tokens[i + j] = ('·', 'PU')
                        self.line_segmented_trad[i + j] = '·'
                i += length
            elif re.search(r'^\d+[^0-9]+', self.tokens[i][0]):
                self.tokens[i + 2:] = self.tokens[i + 1:]
                self.line_segmented_trad[i + 2:] = self.line_segmented_trad[i + 1:]
                token = self.tokens[i]
                trad_token = self.line_segmented_trad[i]
                self.tokens[i] = (re.findall(r'\d+', token[0])[0], 'CD')
                self.line_segmented_trad[i] = re.findall(r'\d+', trad_token)[0]
                self.tokens[i+1] = (re.findall(r'\d+(.+)', token[0])[0], token[1])
                self.line_segmented_trad[i+1] = re.findall(r'\d+(.+)', trad_token)[0]
                i += 2
            elif re.search(r'[^0-9]+\d+$', self.tokens[i][0]):
                self.tokens[i + 2:] = self.tokens[i + 1:]
                self.line_segmented_trad[i + 2:] = self.line_segmented_trad[i + 1:]
                token = self.tokens[i]
                trad_token = self.line_segmented_trad[i]
                self.tokens[i] = (re.findall(r'(.+)\d+', token[0])[0], token[1])
                self.line_segmented_trad[i] = re.findall(r'(.+)\d+', trad_token)[0]
                self.tokens[i + 1] = (re.findall(r'\d+', token[0])[0], 'CD')
                self.line_segmented_trad[i + 1] = re.findall(r'\d+', trad_token)[0]
                i += 2
            else:
                i += 1

    def g2p(self) -> None:
        """
        Метод, который преобразовывает иероглифы в пиньинь
        :return: None
        """
        punctuation = {'。': '.', '、': ',', '，': ',', '”': '"', '？': '?', '《': '"', '》': '"', '！': '!',
                       '……': '...', '（': '(', '）': ')'}
        tokens = g2p(self.tokens)
        for token in tokens:
            if re.search(r'[a-zA-Z]+?\d', token[2]):
                self.line_g2p.append(convert_from_numerical_pinyin(token[2]).replace(' ', ''))
            elif token[2] in punctuation:
                self.line_g2p.append(punctuation[token[2]])
            else:
                self.line_g2p.append(token[2])

    def postprocessing(self) -> None:
        """
        Метод, который преобразовывает токены, PoS-tags и пиньинь в два списка с разбором
        :return: None
        """
        for i in range(len(self.tokens)):
            form_i = self.tokens[i][0]
            transcr = self.line_g2p[i]
            gr = self.tokens[i][1]
            form = self.line_segmented_trad[i]
            if gr == 'PU':
                self.line_hieroglyphs.append({'text': form})
                self.line_pinyin.append({'text': transcr})
            else:
                self.line_hieroglyphs.append({'analysis': [{'lex': form, 'transcr': transcr, 'gr': gr, 'form_i': form_i}],
                                              'text': form})
                self.line_pinyin.append({'analysis': [{'lex': transcr, 'transcr': transcr, 'gr': gr, 'form_i': form_i}],
                                         'text': transcr})
                if i < len(self.tokens)-1:
                    if self.tokens[i+1][1] != 'PU':
                        self.line_pinyin.append({'text': ' '})

    def process(self) -> None:
        """
        Метод, который делает все сразу
        :return: None
        """
        self.preprocessing()  # препроцессинг
        self.trad2simp()  # перевод иероглифов из традиционных в упрощенные
        self.tokenize()  # токенизация и присвоение PoS-тэгов
        self.custom_rules()  # применение кастомных правил
        self.g2p()  # перевод в пиньинь
        self.postprocessing()  # сбор всего в нужный формат
