from deeppavlov import build_model

def analyze_with_deeppavlov(text):
    syntax_model = build_model("syntax_ru_syntagrus_bert", download=True, install=True)
    syntax_analysis = syntax_model([text])
    return syntax_analysis

import spacy_udpipe

def analyze_sentences(text):
    udpipe_model = spacy_udpipe.load("ru")
    parsed = udpipe_model(text)
    conll_data = ""
    for token in parsed:
        conll_data += f"{token.i+1}\t{token.text}\t_\t{token.pos_}\t_\t_\t{token.head.i+1 if token.dep_ != 'ROOT' else 0}\t{token.dep_}\t_\t_\n"
    res = []
    res.append(conll_data)
    return res
    
import stanza

def analyze_with_stanza(text):
    # Загрузка модели для русского языка
    nlp = stanza.Pipeline(lang='ru', processors='tokenize, pos, lemma, depparse')

    # Обработка текста
    doc = nlp(text)
    conll_data = ""
    for sentence in doc.sentences:
        for word in sentence.words:
            conll_data += f"{word.id}\t{word.text}\t_\t_\t_\t_\t{word.head}\t{word.deprel}\t_\t_\n"
    res = []
    res.append(conll_data)
    return res
    
from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc

def analyze_with_natasha(text):
    emb = NewsEmbedding()
    segmenter = Segmenter()
    syntax_parser = NewsSyntaxParser(emb)
    
    doc = Doc(text)
    doc.segment(segmenter)

    doc.parse_syntax(syntax_parser)
    
    conll_data = ""
    for token in doc.tokens:
        conll_data += f"{token.id[2:]}\t{token.text}\t_\t_\t_\t_\t{token.head_id[2:]}\t{token.rel}\t_\t_\n"
    res = []
    res.append(conll_data)
    return res
