import urllib.request
import requests
from pydub import AudioSegment
from Constants import VOICE_XML_PROCESSED

def vrender(output_name="v1",tempo=80.0,sex="female"):
	request(VOICE_XML_PROCESSED,output_name,sex)
	song = AudioSegment.from_wav(output_name)
	song = song[int(1000*4*60/tempo):]
	song.export(output_name,format="wav")

def request(xml_file_path,wavPath,sex="female"):
	if sex == "male":
		SPKR = 5
	else:
		SPKR = 4

	headers = {'User-Agent': 'Mozilla/5.0'}
	payload = {'SPKR_LANG':'english', 'SPKR':SPKR, 'VIBPOWER':'1', 'F0SHIFT':'0'}
	files = {'SYNSRC': open(xml_file_path,'rb')}

	# Sending post request and saving response as response object 
	r = requests.post(url = 'http://sinsy.sp.nitech.ac.jp/index.php',headers=headers,data=payload,files=files)
	htmlResponse = r.text.split("temp/")

	# Magic scraping of the website to find the name of the wav file generated
	urlfileName = findWavNameOnWebsite(htmlResponse)

	if urlfileName is None:
		raise Exception("No wav file found on sinsy.jp")
	else:
		download(urlfileName,wavPath)

def findWavNameOnWebsite(htmlResponse):
	urlfileName = None
	for line in htmlResponse:
		parts = line.split(".")
		if parts[1][:3] == "wav":
			urlfileName = parts[0]
			break
	return urlfileName

def download(urlfileName,wavPath):
	urllib.request.urlretrieve("http://sinsy.sp.nitech.ac.jp/temp/" + urlfileName + ".wav", wavPath)