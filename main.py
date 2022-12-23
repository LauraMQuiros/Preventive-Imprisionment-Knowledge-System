"""
Run commands: python3 -m streamlit run main.py
opens in localhost with   Local URL: http://localhost:8501
Network URL: http://145.97.162.212:8501
"""

import streamlit as st
import numpy as np
import pandas as pd
from helpers import *
from decision import *
import json 

st.set_page_config(
    page_title='Preventive Prison Decision Making System',
    layout='wide'
)

def title_section():
    st.markdown('# Preventive Prison Decision Making System')
    st.markdown('---')

init_session_state()
title_section()
if st.session_state['state']== 'crime estimated':
    choose_estimated_crime()
else:
    if st.session_state['state'] == 'antecedents':
        choose_antecedents()
    elif st.session_state['state'] == 'police report':
        #includes crime report
        crime_report()
    elif st.session_state['state'] == 'contact information':
        personal_info()
    elif st.session_state['state'] == 'report':
        final_conclusions()
