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
    page_title='Preventetive Prison Decision Making System',
    layout='wide'
)

def title_section():
    st.markdown('# Preventetive Prison Decision Making System')
    st.markdown('---')

init_session_state()
title_section()

choose_estimated_crime()



# there will be states: 
# crime_estimation
# antecedants
# crime_report
# police report
# prisoner info
# final report
