from Voice import voice
import pyphen

dic = pyphen.Pyphen(lang='en')

def esVocal(texto):
    return texto in "aeiouáéíóú"

def findSmallers(silabas):
    smallers = -1
    min = 1000000
    for i in range(len(silabas)-1):
        if min > len(silabas[i]) + len(silabas[i+1]):
            min = len(silabas[i]) + len(silabas[i+1])
            smallers = i
    return i

def silabas_word(text):
    return list(filter(lambda x : len(x) > 0, dic.inserted(text).replace(" ", "").split("-")))

def silabas_sentence(sentence):
    sentence = sentence.lower().replace(".","").replace(",","") # limpio un toque el string
    return sum([silabas_word(word) for word in sentence.split()],[])

def vocals(text,n):
 silabas = silabas_sentence(text)
 if len(silabas) == n:
     return silabas
 elif len(silabas) < n:
     index = 0
     while(len(silabas) < n):
        index = (index + 1) % len(silabas)         
        if esVocal(silabas[index][-1]) and len(silabas[index]) > 1:
            silabas = silabas[:index+1] + [silabas[index][-1]] + silabas[index+1:]
     return silabas
 else:
     while(len(silabas) > n):
         i = findSmallers(silabas)
         silabas = silabas[:i] + [silabas[i] + silabas[i+1]] + silabas[i+2:]
     return silabas     

def fillSpaces(text):
    missing_values = 12-len(text)
    return text + ["."]*missing_values

def stretch_text(notas, texto, durs, removed_values=1):    
    missing_values = texto.count(".")
    removed_values = min(removed_values,missing_values)

    lastWord = len(durs) - missing_values - 1

    durs = durs[0:lastWord] + [sum(durs[lastWord:lastWord+1+removed_values])] + durs[lastWord+1+removed_values:]
    texto = texto[0:lastWord+1] + texto[lastWord+1+removed_values:]
    notas = notas[0:lastWord+1] + notas[lastWord+1+removed_values:]
    return notas, texto, durs
                                           
def trap(textos,sample="v1",oct=5,lang="en"):
    texto_l = []
    durs_l = []
    notas_l = []
    for texto in textos:
        texto = silabas_sentence(texto)

        missing_values = 12-len(texto)

        notas = [0]*len(texto) + [-99]*missing_values
        texto = texto + ["."]*missing_values
        durs = [2/6]*len(texto)
        notas, texto, durs = stretch_text(notas, texto, durs,0)

        texto_l += texto
        durs_l += durs
        notas_l += notas
    voice(notas_l,dur=durs_l,lyrics=" ".join(texto_l),file=sample,octave=oct,lang=lang)