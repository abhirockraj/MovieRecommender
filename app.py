import boto3
import streamlit as st
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import shutil
import os
import time
import glob
from PIL import Image
st.title('Recommend the movie based on the content :film_projector:')


def dataCall():
    s3 = boto3.resource(service_name = 's3',region_name= 'us-east-2',aws_access_key_id=st.secrets['s3Api'],aws_secret_access_key=st.secrets['s3ApiId'])
    # s3 = boto3.resource(service_name= 's3',region_name= 'us-east-2',aws_access_key_id='AKIAZ2LYTXVXZY3GSJ23',aws_secret_access_key='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')

    objS3= s3.Bucket('recommender-system').Object('X.csv').get()
    x = pd.read_csv(objS3['Body'],header=None) 

    objS3= s3.Bucket('recommender-system').Object('movieId.csv').get()
    movieId = pd.read_csv(objS3['Body'],index_col=1)
    return x, movieId

a=st.slider('Param 1',min_value=-1.53,max_value=8.27,value=4.6)
b=st.slider('Param 2',min_value=-1.55,max_value=8.27,value=4.6)
c=st.slider('Param 3',min_value=-1.56,max_value=8.27,value=4.6)
d=st.slider('Param 4',min_value=-1.52,max_value=8.27,value=4.6)
e=st.slider('Param 5',min_value=-1.54,max_value=8.27,value=4.6)
f=st.slider('Param 6',min_value=-1.53,max_value=8.27,value=4.6)
g=st.slider('Param 7',min_value=-1.54,max_value=8.27,value=4.6)
h=st.slider('Param 8',min_value=-1.54,max_value=8.27,value=4.6)
i=st.slider('Param 9',min_value=-1.54,max_value=8.27,value=4.6)
j=st.slider('Param 10',min_value=-1.54,max_value=8.27,value=4.6)
k=st.slider('Param 11',min_value=-1.54,max_value=8.27,value=4.6)
l=st.slider('Param 12',min_value=-1.54,max_value=8.27,value=4.6)
m=st.slider('Param 13',min_value=-1.54,max_value=8.27,value=4.6)
n=st.slider('Param 14',min_value=-1.54,max_value=8.27,value=4.6)
o=st.slider('Param 15',min_value=-1.54,max_value=8.27,value=4.6)
p=st.slider('Param 16',min_value=-1.54,max_value=8.27,value=4.6)
q=st.slider('Param 17',min_value=-1.54,max_value=8.27,value=4.6)
r=st.slider('Param 18',min_value=-1.34,max_value=-0.77,value=-1.0)

try:
    files = glob.glob('*.jpg')
    for i in files:
            os.remove(i)
except:
        pass

if (st.button('Recommend movie')):
    x,movieId=dataCall()

    userIp = np.array([[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r]])
    l=[]

    for i in  x.index:
        data=x.loc[i]
        data = np.array(data)
        data = np.reshape(data, (1,18))
        ad= cosine_similarity(data,userIp)[0][0]
        l.append(ad)

    ade = sorted(list(enumerate(l)),key= lambda x:x[1], reverse=True)[1:6]    

    ld=[]
    for i in ade:
            ld.append(movieId.index[i[0]])

    
    for i in ld:
        pURL = "https://api.themoviedb.org/3/movie/"
        endUrl = "?api_key="+st.secrets['movieApi']+"&language=en-US"
        URL = pURL+str(i)+endUrl
        r = requests.get(url = URL)
        data = r.json()
        iUrl ="http://image.tmdb.org/t/p/w500"+data['poster_path']
        ir = requests.get(url=iUrl,stream=True)
        with open('img_'+str(i)+'.jpg', 'wb') as out_file:
            shutil.copyfileobj(ir.raw, out_file)
        while not os.path.exists('img_'+str(i)+'.jpg'):
            time.sleep(4)       
    c=1
    files = glob.glob('*.jpg')
    for i in files:
        image = Image.open(i)
        st.image(image, caption='Movie_'+str(c))
        c=c+1
    
        
