from flask import Flask, render_template, request, redirect, url_for
from startup import trap
import time

app = Flask(__name__)
text = ""

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    error = ""
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        text = request.form['text'].split("\n")
        speed = float(request.form['speed'])
        # Validate form data
        if len(text) == 0:
            # Form data failed validation; try again
            error = "Please supply an input text"
        else:
            # Form data is valid; move along
            trap(text,oct=5,sample="sample.wav")
            return redirect(url_for('thank_you'))

    return render_template('index.html', message=error)

@app.route('/synthesize', methods=['GET'])
def synthesize():
    text = request.args.get('text')
    try:
        speed = float(request.args.get('speed'))
    except:
        speed = 1.0
    # Form data is valid; move along
    model, waveglow, denoiser = init_model()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = "sample_"+timestamp+".wav"
    generate_voice(text,speed,model,waveglow,denoiser,filename)
    return filename

from flask import send_from_directory
import os

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/sample/<path:path>')
def sample(path):
    return send_from_directory(os.path.join(app.root_path, 'static'), path, mimetype='audio/wav')

# Run the application
#app.run(host="0.0.0.0",port=5555,ssl_context=context,debug=True)
app.run(host="0.0.0.0",port=5555,debug=True)
