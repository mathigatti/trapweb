from Voice import voice
import pyphen

dic = pyphen.Pyphen(lang='en')

def esVocal(texto):
    return texto in "aeiouáéíóú"

continuation = "-"

def extendWord(text):
    for extensibleEnding in ["all","oh","ah","ad","as","at","al","a","e","i","o","u"]:
        if text.endswith(extensibleEnding) or text.endswith(extensibleEnding+continuation):
            if text.endswith(continuation):
                additional = continuation
            else:
                additional = ""

            if len(extensibleEnding) > 1:
                return text[:-1*len(extensibleEnding) + 1 - len(additional)] + continuation, extensibleEnding + additional
            else:
                return text, extensibleEnding
    return text, None

def findSmallers(silabas):
    smallers = -1
    min = float('inf')
    for i in range(len(silabas)-1):
        if min > len(silabas[i]) + len(silabas[i+1]):
            min = len(silabas[i]) + len(silabas[i+1])
            smallers = i
    return i

def silabas_word(text):
    return dic.inserted(text).replace("-", continuation + "|").split("|")

def silabas_sentence(sentence):
    return sum([silabas_word(word) for word in sentence.split()],[])

def vocals(text,n):
    silabas = silabas_sentence(text)

    if len(silabas) == n:
        return silabas
    elif len(silabas) < n:
        if all([extendWord(silaba)[1] == None for silaba in silabas]):
            silabas += ["a"]            
        index = len(silabas)-1
        while(len(silabas) < n):
            prevPart, extensiblePart = extendWord(silabas[index])
            if extensiblePart:
                silabas = silabas[:index] + [prevPart, extensiblePart] + silabas[index+1:]
            index = (index - 1) % len(silabas)         
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
                                           
def trap(textos,sample="v1",oct=5,lang="en",tempo=80.0):
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
    voice(notas_l,dur=durs_l,lyrics=" ".join(texto_l),file=sample,octave=oct,lang=lang,tempo=tempo)


def synthesize(textos,notes=[0],durs=[8],sample="v1",oct=5,lang="en",tempo=80.0):
    texto_l = []
    durs_l = []
    notas_l = []

    assert len(notes) == len(durs)

    for texto in textos:
        texto = vocals(texto,len(list(filter(lambda x : x != -99,notes))))

        texto = [texto[i] if notes[i] != -99 else "." for i in range(len(notes))]

        texto_l += texto
        durs_l += durs
        notas_l += notes
    voice(notas_l,dur=durs_l,lyrics=" ".join(texto_l),file=sample,octave=oct,lang=lang,tempo=tempo)