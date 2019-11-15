# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 11:59:02 2019

@author: joshnarani
"""


from flask import Flask, request, redirect, url_for,render_template,jsonify
from werkzeug.utils import secure_filename

from sypht.client import SyphtClient, Fieldset
import matplotlib.image as plt
#import requests
import os
app = Flask(__name__)
from io import BytesIO
#from PIL import Image
app.config['UPLOAD_FOLDER'] = 'static/'
scc = SyphtClient('JNSJgJF3SEltPf11DZLtdPE9SFPdrmlh','HFbQPHKS_hKCxNTqOala7ZbArrc6jcFx2OPZOuSTIGYTwkvunGcBkLyblIube0dR')
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        #if file:
        #file = request.files['file']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open(os.path.join(app.config['UPLOAD_FOLDER'],filename),'rb') as f:
        #print(flpth)
        #file=bytes(file, 'utf-8')
        #with open((filename),'rb') as f:
        #with Image.open(BytesIO(file)) as f:
            fid = scc.upload(f, fieldsets=["document"])
        ab=scc.fetch_results(fid)
            #ab['document.date']
        if not ab:
        #print('none')
                dates='null'
        else:
                dates=ab['document.date']
        path_to_image = url_for('static', filename = filename)
        return render_template('result.html',dates=dates,path_to_image=path_to_image)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=4996,debug=True)
	

