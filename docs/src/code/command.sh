# bin/bash
nohup streamlit run web/app.py &
python service/app.py --timeout-ready