

###importing libraries
from flask import Flask, request, redirect, url_for,render_template,jsonify
from werkzeug.utils import secure_filename

from sypht.client import SyphtClient, Fieldset  ##sypht is used to extract insights data for all types of files
#import matplotlib.image as plt
#import requests
import os
app = Flask(__name__)
#from io import BytesIO
#from PIL import Image
##give a folder to store uploaded images
app.config['UPLOAD_FOLDER'] = 'static/'
##sypht clientid,secretkey can be obtained by registering in sypht.com
##please enter your own secretkey as i replaced my secretkey with dots for security reasons...
scc = SyphtClient('JNSJgJF3SEltPf11DZLtdPE9SFPdrmlh','••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••')
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        #if file:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   ##saving file into folder
        with open('static/{}'.format(filename),'rb') as f:
        #print(flpth)
        #file=bytes(file, 'utf-8')
        #with open((filename),'rb') as f:
        #with Image.open(BytesIO(file)) as f:
            fid = scc.upload(f, fieldsets=["document"])
        ab=scc.fetch_results(fid)        ###fetching the information present in the receipts
            #ab['document.date']
        if not ab:           ###checking if the dictionary is empty or not and returning respective result
        #print('none')
                dates='null'
        else:
                dates=ab['document.date']  ###extracting date of the uploaded file from the obtained dictionary result
        path_to_image = url_for('static', filename = filename)
        return render_template('result.html',dates=dates,path_to_image=path_to_image)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=4996,debug=True)
	

