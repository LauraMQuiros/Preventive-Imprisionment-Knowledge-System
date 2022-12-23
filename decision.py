import streamlit as st
import json
from helpers import *
import pandas as pd

file = open('kb.json', 'r')
kb = json.load(file)

def choose_estimated_crime():
    crime_categories = kb['categoryCrime']
    col1, col2 = st.columns([1, 1])


    selected_crime = col1.radio('What is the estimated committed crime?', crime_categories)

    crimes_of_category =  crime_categories[selected_crime]
    col2.caption('What are the known antecedents?')
    selected_antecedents = []

    for crime in crimes_of_category:
        if col2.checkbox(crime):
            selected_antecedents += [crime]

    


    st.session_state['estimated_crime_coefficient'] = crime_categories[selected_crime]['crime_category_weight']
    print(st.session_state['estimated_crime_coefficient'])
