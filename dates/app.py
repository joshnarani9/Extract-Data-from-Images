from sypht.client import SyphtClient, Fieldset

scc = SyphtClient('JNSJgJF3SEltPf11DZLtdPE9SFPdrmlh','HFbQPHKS_hKCxNTqOala7ZbArrc6jcFx2OPZOuSTIGYTwkvunGcBkLyblIube0dR')
with open(r'C:\Users\Srinivas\Downloads\Desktop\syphtclient\Receipts\0a0ebd53.jpeg', 'rb') as f:
    fid = scc.upload(f, fieldsets=["document"])
ab=scc.fetch_results(fid)
#print(scc.fetch_results(fid))
#ab['document.date']
if not ab:
        #print('none')
                dates='null'
                print(dates)
else:
    dates=ab['document.date']
    print(dates)

if ab['document.date']=='None':
    print('date:null')
else:
    print("date"":""{}".format(ab['document.date']))
    

#import matplotlib.image as mpimg
import os
#import numpy as np
from PIL import Image
from io import BytesIO

#Image.open(BytesIO(r'C:\Users\Srinivas\Downloads\Desktop\syphtclient\Receipts\5bb556be.jpeg'),'rb')

folder=r"C:\Users\..\Downloads\Desktop\syphtclient\Receipts"
# =============================================================================
# 
# def load_images(folder):
#     
#     for filename in os.listdir(folder):
#         img = mpimg.imread(os.path.join(folder, filename))
#         images = []
#         if img is not None:
#             images.append(img)
#     return images
# 
# (os.listdir(folder))[186]
# images = []
# for filename in os.listdir(folder):
#     try:
#         img = mpimg.imread(os.path.join(folder, filename))
#         if img is not None:
#             images.append(img)
#     except:
#         print('Cant import ' + filename)
# images = np.asarray(images)
# len(images)
# =============================================================================

dates=[]
filenames=[]
for filename in os.listdir(folder):
    print(filename)
    #jpgfile = Image.open(os.path.join(folder, filename))
    with open(os.path.join(folder, filename), 'rb') as f:

        fid = scc.upload(f, fieldsets=["document"])
        f.close()
    ab=scc.fetch_results(fid)
    print(scc.fetch_results(fid))
    filenames.append(filename)
    if not ab:
        #print('none')
        dates.append('none')
    else:
        dates.append(ab['document.date'])

import pandas as pd
result=pd.DataFrame({'filenames':filenames,'dates':dates})
#result2.to_csv('result2.csv')

#result1=pd.read_csv('result1.csv')
#result=pd.concat([result1,result2],ignore_index=True)
result.to_csv('result.csv')
re=pd.read_csv('result.csv')
re.head()
#re.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
res=re.iloc[:,[2,3]]
res.fillna(0,inplace=True)

nodates=len(res[res['dates']==0])
total=len(res)
correctdates=total-nodates
#accuracy = (number of receipts for which the service extracted correct date/total receipts)*100%

accuracy=(correctdates/total)*100