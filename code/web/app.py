import streamlit as st
from jina import Client, DocumentArray, Document
import json
import os
import time
import uuid

port = 45679
c = Client(host=f"grpc://localhost:{port}")

# page settings
st.set_page_config(page_title="VCED", page_icon="🔍")
st.title('Welcome to VCED!')

# upload
uploaded_file = st.file_uploader("Choose a video")
if uploaded_file is not None:
    # preview, delete and download the video
    video_bytes = uploaded_file.read()
    st.video(video_bytes)
uid = uuid.uuid1()

# description
text_prompt = st.text_input(
    "Description", placeholder="please input the description", help='The description of clips from the video')

# top N
topn_value = st.text_input(
    "Top N", placeholder="please input an integer", help='The number of results. By default, n equals 1')

def getTime(t: int):
    m,s = divmod(t, 60)
    h, m = divmod(m, 60)
    t_str = "%02d:%02d:%02d" % (h, m, s)
    print (t_str)
    return t_str

def cutVideo(start_t: str, length: int, input: str, output: str):
    os.system(f'ffmpeg -ss {start_t} -i {input} -t {length} -c:v copy -c:a copy -y {output}')

def search_clip(uid, uri, text_prompt, topn_value):
    uri = "/Users/super/Downloads/videoplayback.mp4"
    video = DocumentArray([Document(uri=uri, id=str(uid) + uploaded_file.name)])
    t1 = time.time()
    c.post('/index', inputs=video)
    
    text = DocumentArray([Document(text=text_prompt)])
    print(topn_value)
    resp = c.post('/search', inputs=text, parameters={"uid": str(uid), "maxCount":int(topn_value)})
    data = [{"text": doc.text,"matches": doc.matches.to_dict()} for doc in resp]
    return json.dumps(data)


# search
search_button = st.button("Search")
if search_button:
    if uploaded_file is not None:
        if text_prompt == None or text_prompt == "":
            st.warning('Please input the description first!')
        else:
            if topn_value == None or topn_value == "":
                topn_value = 1
            with st.spinner("Processing..."):
                result = search_clip(uid, "", text_prompt, topn_value)
                result = json.loads(result)
                for i in range(len(result)):
                    matchLen = len(result[i]['matches'])
                    for j in range(matchLen):
                        print(j)
                        left = result[i]['matches'][j]['tags']['leftIndex']
                        right = result[i]['matches'][j]['tags']['rightIndex']
                        print(left)
                        print(right)
                        start_t = getTime(left)
                        end_t = getTime(right)
                        uri = "/Users/super/Downloads/videoplayback.mp4"
                        output = "/Users/super/Downloads/videos/clip" + str(j) +".mp4"
                        cutVideo(start_t,right-left, uri, output)
                        st.video(output)
                st.success("Done!")
    else:
        st.warning('Please upload video first!')

