from Constants import LAST_MIDI,VOICE_XML_ORIGINAL,VOICE_XML_PROCESSED
from Composer import compose
from VoiceSpecificator import generateVoiceSpecification
from VRender import vrender

def renderizeVoice(outputName,lyrics,notes,durations,tempo,scale,root_note,octave,languageCode):

	compose(notes,durations,scale,root_note,octave,LAST_MIDI,VOICE_XML_ORIGINAL)

	lyrics = tokenize(lyrics)

	generateVoiceSpecification(lyrics,tempo,VOICE_XML_ORIGINAL,VOICE_XML_PROCESSED)

	vrender(outputName,tempo)

def tokenize(text):
	print("Text input:", text)
	textSyllables = cleanText(text)
	return list(filter(lambda x: len(x) > 0, textSyllables.split(" ")))

def cleanText(text):
	text.replace("\n"," ")
	text = text.lower()

	symbolsToDelete = ".,'!?" + '"'
	for symbol in symbolsToDelete:
		text = text.replace(symbol,"")

	return text

def voice(notes, **kwargs):
        if "lyrics" in kwargs:
            lyrics = kwargs['lyrics']
        else:
            lyrics = "oo "

        if "dur" in kwargs:
            durations = list(map(float,kwargs['dur']))
        else:
            durations = [1.0]

        if 'file' in kwargs:
            filename = kwargs['file']
        else:
            filename = 'v1'

        if "sex" in kwargs:
            sex = kwargs["sex"]
        else:
            sex = "female"

        if "octave" in kwargs:
            octave = kwargs["octave"]
        else:
            octave = 6

        if "lang" in kwargs:
            language = kwargs["lang"]
        else:
            language = "es"

        if "scale" in kwargs:
            scale = kwargs["scale"]
        else:
            scale = [0,1,2,3,4,5,6,7,8,9,10,11]

        if "tempo" in kwargs:
            tempo = float(kwargs["tempo"])
        else:
            tempo = 80.0

        notes = list(map(int,notes))

        dst_path = 'static/' + filename

        root_note = 0
        renderizeVoice(dst_path,lyrics,notes,durations,tempo,scale,root_note,octave,language)