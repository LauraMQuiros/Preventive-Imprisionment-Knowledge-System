"""
Run commands: python3 -m streamlit run main.py
To go to initial page: go to 3 lines top right, clear cache and rerun
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
    st.markdown('# Preventive Prison Decision Making System :police_car:')
    st.markdown('')
    st.info('Based on the Spanish Penal Code.')
    st.markdown('---')

init_session_state()
title_section()
if st.session_state['state'] == 'crime estimation':
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
