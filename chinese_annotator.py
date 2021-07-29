import re
from g2pc import g2pc
from numerical_pinyin_converter import convert_from_numerical_pinyin


class ChineseLine:
    def __init__(self, line: str) -> None:
        self.line = line
        self.line_segmented = []
        self.line_pos = []
        self.line_g2p = []
        self.line_hieroglyphs = '<se lang="zh"></se>'
        self.line_pinyin = '<se lang="zh2"></se>'

    def preprocessing(self) -> None:
        """
        Метод, который предобрабатывает строку китайского текста:
            1. Убираются символы '<', '>', '\n'
            2. Точки в заимствованиях приводятся к одному образцу
        :return: None
        """
        self.line = re.sub('[<>\n]', '', self.line)
        self.line = re.sub('•', '·', self.line)

    def postprocessing(self) -> None:
        """
        Метод, который преобразовывает токены, PoS-tags и пиньинь в две строки xml
        :return: None
        """
        hieroglyphs = []
        pinyin = []
        for i in range(len(self.line_segmented)):
            lex = self.line_segmented[i]
            transcr = self.line_g2p[i]
            gr = self.line_pos[i]
            if gr == 'PU':
                hieroglyphs.append(lex)
                pinyin.append(transcr)
            else:
                hieroglyphs.append(
                    f'<w><ana lex="{lex}" transcr="{transcr}" gr="{gr}"/>{lex}</w>'
                )
                pinyin.append(
                    f'<w><ana lex="{lex}" transcr="{transcr}" gr="{gr}"/>{transcr}</w>'
                )
        hieroglyphs = ''.join(hieroglyphs)
        pinyin = ''.join(pinyin)
        self.line_hieroglyphs = f'<se lang="zh">{hieroglyphs}</se>'
        self.line_pinyin = f'<se lang="zh2">{pinyin}</se>'

    @staticmethod
    def custom_rules(tokens: list) -> list:
        """
        Метод, который применяет кастомные правила к токенам
        :param tokens: токены, полученные с помощью инструментов
        :return: токены после применения правил
        """
        result = []
        last = 0
        for i, token in enumerate(tokens):
            if '·' in token[0] and len(token[0]) > 1:
                last = i+1
                result.extend(tokens[:i])
                parts_hieroglyphs = token[0].split('·')
                parts_pinyin = token[2].split(' · ')
                length = len(parts_hieroglyphs)*2 - 1
                for j in range(length):
                    if j % 2 == 0:
                        result.append((parts_hieroglyphs[int(j/2)], token[1], parts_pinyin[int(j/2)]))
                    else:
                        result.append(('·', 'PU', '·'))
        result.extend(tokens[last:])
        return result

    def process(self, model: str = 'FastHan') -> None:
        """
        Метод, который делает все сразу
        :param model: строка, которая указывает, какой инструмент использовать для сегоментации строки на токены.
                        По дефолту используется FastHan, иначе pkuseg (дефолтный сегментатор в g2pc)
        :return: None
        """
        punctuation = {'。': '.', '、': ',', '，': ',', '”': '"', '？': '?', '《': '"', '》': '"', '！': '!',
                       '……': '...', '（': '(', '）': ')'}
        if model == 'FastHan':
            g2p = g2pc.G2pCFH()
        else:
            g2p = g2pc.G2pC()
        self.preprocessing()
        segments = self.custom_rules(g2p(self.line))
        for segment in segments:
            self.line_segmented.append(segment[0])
            self.line_pos.append(segment[1])
            if re.search(r'[a-zA-Z]+?\d', segment[2]):
                self.line_g2p.append(convert_from_numerical_pinyin(segment[2]))
            elif segment[2] in punctuation:
                self.line_g2p.append(punctuation[segment[2]])
            else:
                self.line_g2p.append(segment[2])
        self.postprocessing()

    def __str__(self) -> str:
        return self.line
