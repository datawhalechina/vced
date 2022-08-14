import streamlit as st

# page settings
st.set_page_config(page_title="VCED", page_icon="🔍")
st.title('Welcome to VCED!')

# upload
uploaded_file = st.file_uploader("Choose a video")
if uploaded_file is not None:
    # preview, delete and download the video
    video_bytes = uploaded_file.read()
    st.video(video_bytes)

# description
text_prompt = st.text_input(
    "Description", placeholder="please input the description", help='The description of clips from the video')

# top N
topn_value = st.text_input(
    "Top N", placeholder="please input an integer", help='The number of results. By default, n equals 1')

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
                #  后端函数
                #  result = search_clip(uploaded_file.name, text_prompt, int(topn_value))
                result = [1, 2, 3, 4, 5]
                for item, index in enumerate(result):
                    st.video(uploaded_file.read())
                    st.download_button(
                        label="download",
                        data=uploaded_file,
                        file_name=f"clip{index}.mp4",
                        mime='application/octet-stream',
                    )
                st.success("Done!")
    else:
        st.warning('Please upload video first!')
