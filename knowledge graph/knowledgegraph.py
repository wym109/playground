# https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e
import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt

from spacy.lang.en.stop_words import STOP_WORDS

from extract_text import TXTFILE


def getSentences(text):
    # Creates srtings of sentences
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    # nlp.add_pipe('sentencizer')
    # nlp.add_pipe(create)
    document = nlp(text)
    return [sent.text.strip() for sent in document.sents]

def printToken(token):
    # prints all the tokens
    print(token.text, "->", token.dep_)

def appendChunk(original, chunk):
    # more printing to see what's going on
    return original + ' ' + chunk

def isRelationCandidate(token):
    # Use SpaCy tags to create relations 
    deps = ["ROOT", "adj", "attr", "agent", "amod"]
    return any(subs in token.dep_ for subs in deps)

def isConstructionCandidate(token):
    # Use SpaCy tags to see if they are compound 
    deps = ["compound", "prep", "conj", "mod"]
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens):
    # extracting all types of tokens, split to different category
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    for token in tokens:
        printToken(token)
        # if token.text in ['you']:
        #     print("ignoring stop word")
        #     continue
        if token.dep_ in ["punct"]:
            continue
        if isRelationCandidate(token):
            relation = appendChunk(relation, token.lemma_)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction = appendChunk(objectConstruction, token.text)
        if "subj" in token.dep_:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        if "obj" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''

    print (subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())

def processSentence(sentence):
    tokens = nlp_model(sentence)
    return processSubjectObjectPairs(tokens)

def printGraph(triples):
    # Create the graph
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # read text file
    with open(TXTFILE) as f:
        text = f.read()

    # Coreference resolution from https://github.com/huggingface/neuralcoref
    from IE_conference import coref_resolution
    text_conf=coref_resolution(text)

    sentences = getSentences(text_conf)
    # May need to run python -m spacy download en
    nlp_model = spacy.load('en')

    triples = []
    print (text_conf)
    for sentence in sentences:
        triples.append(processSentence(sentence))

    printGraph(triples)
