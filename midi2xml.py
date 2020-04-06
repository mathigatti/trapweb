from music21 import converter, musicxml
import sys

s = converter.parse(sys.argv[1])
SX = musicxml.m21ToXml.ScoreExporter(s)

mxPartList = SX.setPartList()
SX.dump(mxPartList)