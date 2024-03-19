import nltk
import spacy_udpipe


def analyze_with_maltparser(text):


    parsed_result = []

    return parsed_result


from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc

def analyze_with_natasha(text):
    emb = NewsEmbedding()
    segmenter = Segmenter()
    syntax_parser = NewsSyntaxParser(emb)
    
    doc = Doc(text)
    doc.segment(segmenter)

    doc.parse_syntax(syntax_parser)
    
    parsed_result = []
    for token in doc.tokens:
    #печатает пока просто номер родителя, потом все равно переделывать
        parsed_result.append((token.text, token.rel, token.head_id))
    return parsed_result

from deeppavlov import build_model

def analyze_with_deeppavlov(text):
    syntax_model = build_model("syntax_ru_syntagrus_bert", download=True, install=True)

    syntax_analysis = syntax_model([text])

    return syntax_analysis

import stanza

def analyze_with_stanza(text):
    # Загрузка модели для русского языка
    nlp = stanza.Pipeline(lang='ru', processors='tokenize, pos, lemma, depparse')

    # Обработка текста
    doc = nlp(text)

    parsed_result = []
    for sentence in doc.sentences:
        for word in sentence.words:
            parsed_result.append((word.text, word.deprel, str(word.head)))

    return parsed_result


def analyze_sentences(text):
    udpipe_model = spacy_udpipe.load("ru")
    parsed = udpipe_model(text)
    parsed_result = []
    for token in parsed:
        dep_type = token.dep_
        parent_word = token.head.text
        parsed_result.append((token.text, dep_type, parent_word))
    return parsed_result
