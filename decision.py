import streamlit as st
import streamlit_book as stb
import json
from helpers import *
import pandas as pd

file = open('kb.json', 'r')
kb = json.load(file)

def choose_estimated_crime():
    crime_categories = kb['categoryCrime']
    col1, col2 = st.columns([1, 1])
    selected_category = col1.radio('What is the category the estimated crime belongs to', crime_categories)


    crimes_of_category = [ d for d in crime_categories[selected_category] if ((d != "crime_category_weight") and (d != "associated_chapter"))]
    crimes = crimes_of_category.copy()
    crimes.append('None/not clear')
    #Try make it radio I don't like that it collapses


    estimate_crime = col2.radio('What is the estimated committed crime?', crimes)
    st.session_state['estimated_crime'] = estimate_crime
    st.session_state['estimated_category_crimes'] = crimes_of_category

    #I am missing here the multiplication by the crime itself?
    st.session_state['estimated_crime_coefficient'] = crime_categories[selected_category]['crime_category_weight']

    if col2.button('Next'):
        st.session_state['state'] = 'antecedents'
        st.experimental_rerun()

def choose_antecedents():
    st.write('What are the antecedents of the same category?')
    noAntecedents = st.checkbox('There are not any')
    selected_antecedents = []
    #I'd like to have a button '+' such that a new template form appears with 3 multiple choice questions: crime, modif, conviction status
    #i want them to be stacked one in top of the next one but that may present a difficulty since streamlit does not seem to have default component for it

    #I think it's possible if we just iteratively increase the antecedents. However, we may be interested in having the answers of those 3 questions
    #plus the total amount that is added for reporting purposes. My suggestion is to use arrays and make index number each of the antecedents. 
    # Antecedent 0: antecedent0_crime= antecedent_crimes[0] antecedent0_increment = antecedent_additions[0] and so on

    #The following is placeholder
    for crime in st.session_state['estimated_category_crimes']:
        if st.checkbox(crime):
            selected_antecedents += [crime]
            st.session_state['antecedants_coefficient']+= crime*st.session_state['modifier_weight']
    
    #Some warnings so we get the info b4 we go to the next one
    if st.button('Next'):
        if noAntecedents:
            if len(selected_antecedents)==0:
                st.session_state['state'] = 'police report' # there is a dublicate here 
                st.experimental_rerun()
            else: 
                st.write("Warning: You seem to have selected antecedents and checked the no-antecedents box.")
        else: 
            if len(selected_antecedents)==0:
                st.write("Warning: No antecedents selected and unchecked no-antecedents box.")
            else:
                st.session_state['state'] = 'police report' # there is a dublicate here 
                st.experimental_rerun()

def crime_report():
    crime_categories = kb['categoryCrime']
    print(st.write("**Under construction**"))

def personal_info():
    crime_categories = kb['categoryCrime']
    print(st.write("**Under construction**"))

def final_conclusions():
    print(st.write("**Under construction**"))