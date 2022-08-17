import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(page_title="Hello Streamlit")

st.title('This is your first Streamlit page!')  # 标题

st.markdown('Streamlit is **_really_ cool**.')  # markdown

code = '''def hello():
     print("Hello, Streamlit!")'''
st.code(code, language='python')  # code

df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))
st.dataframe(df)  # dataframe

st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')  # latex
