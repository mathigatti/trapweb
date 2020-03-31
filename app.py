from flask import Flask, render_template, request, redirect, url_for
from startup import trap
import time
from flask import send_from_directory
import os

app = Flask(__name__)
text = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    error = ""
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        text = request.form['text'].split("\n")
        bpm = int(float(request.form['bpm']))
        octave = int(float(request.form['octave']))
        # Validate form data
        if len(text) == 0:
            # Form data failed validation; try again
            error = "Please supply an input text"
        else:
            # Form data is valid; move along
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = "sample_"+timestamp+".wav"
            trap(text,oct=octave,sample=filename,tempo=bpm)
            return redirect('/sample/'+filename)

    return render_template('index.html', message=error)

@app.route('/sample/<path:path>')
def sample(path):
    return send_from_directory(os.path.join(app.root_path, 'static'), path, mimetype='audio/wav')

# Run the application
#app.run(host="0.0.0.0",port=5555,ssl_context=context,debug=True)
app.run(host="0.0.0.0",port=5555,debug=True)
