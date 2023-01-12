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

    estimate_crime = col2.radio('What is the estimated committed crime?', crimes)
    st.session_state['estimated_crime'] = estimate_crime
    st.session_state['estimated_category_crimes'] = crimes_of_category
    #This is just to have the category weight
    st.session_state['estimated_category_weight'] = crime_categories[selected_category]['crime_category_weight']

    if col2.button('Next'):
        st.session_state['state'] = 'antecedents'
        st.experimental_rerun()

def choose_antecedents():
    #First we get some info we are gonna need
    crime = st.session_state['estimated_crime']
    category_crimes = st.session_state['estimated_category_crimes']
    status = ['Guilty', 'Not guilty, but was in Preventive Prison for it', 'Not guilty, was not in Preventive Prison']
    #selected_antecedents = [] #dictionary so we can store both crime and status in the same place
    #selected_status= []

    #And we make the terminal show us that the input so far has been collected
    print(crime)
    print(category_crimes)
    print(st.session_state['estimated_category_weight'])
    st.write('What are the antecedents of the same category?')
    
    #I'd like to have a button '+' such that a new template form appears with 3 multiple choice questions: crime, modif, conviction status
    with st.form("Add an antecedent", clear_on_submit=True):
        col1, col2 = st.columns(2)    
        newCrime = col1.radio("What is the antecedent's crime?", category_crimes)
        newStatus = col2.radio("What is the status of the antecedent?", status)
        
        st.warning("Click in the 'done' button to store the antecedent")
        newAntecedent = st.form_submit_button('Done')
        if newAntecedent:
            st.session_state["selected_status"] += [newStatus]
            st.session_state["selected_antecedents"]+= [newCrime]        

            print(st.session_state["selected_status"])
    noAntecedents = st.checkbox('There are not any') 
    
    selected_antecedents = st.session_state["selected_antecedents"]
    selected_status = st.session_state["selected_status"]
    st.header("Antecedents stored")
    df = pd.DataFrame(selected_antecedents, selected_status)
    #It'd be nice if someone could figure out how to order it :)
    #And maybe rename the column 0
    st.table(df)

    #We make the computations and store the first of the 3 fundamental weights


    #Some warnings so we get the info b4 we go to the next page
    if st.button('Next'):
        if noAntecedents:
            if len(selected_antecedents)==0:
                # there are two ways to go to next page, feel free to combine them in one if statement
                st.session_state['state'] = 'police report' 
                st.experimental_rerun()
            else: 
                st.warning("Warning: You seem to have selected antecedents and checked the no-antecedents box.")
        else: 
            if len(selected_antecedents)==0:
                st.warning("Warning: No antecedents selected and unchecked no-antecedents box.")
            else:
                st.session_state['state'] = 'police report'
                st.experimental_rerun()

def crime_report():
    #First we get some info we are gonna need
    crime = st.session_state['estimated_crime']
    category_crimes = st.session_state['estimated_category_crimes']
    #Following is giving issues
    #selected_modifiers = [ m for m in category_crimes[crime] if ((m != "crime_category_weight") and (m != "associated_chapter"))]
    #modifiers = selected_modifiers.copy()
    #modifiers.append('None/not clear')

    st.header('_Crime Report_')
    st.write("**Under construction**")

    col1, col2 = st.columns([1, 1])
    report_type = col1.radio("What is the type of a police report?", kb['Police Report Type'])
    st.session_state['report_coefficient'] = kb['Police Report Type'][report_type]['weight']
    #col2.radio("What are the crime's modifiers?", modifiers)
    # adjacent crime system

    if st.button('Next'):
        st.session_state['state'] = 'contact information'
        st.experimental_rerun()
     

def personal_info():
    st.header('_Personal Information_')
    personal_modifiers = kb['Personal Information']['modifiers']
    st.write("Select all the true statements about the suspect:")

    for modifier in personal_modifiers:
         if st.checkbox(modifier):
            print("Hi")
    if st.button('Next'):
        st.session_state['state'] = 'report'
        st.experimental_rerun()

def final_conclusions():
    print(st.write("**Under construction**"))
    # Like a health bar in a videogame, color coded like a traffic light
    # Maybe add download button to download the final conclusions as pdf
    # Number of each weight (3), color red the title if made it reach threshold by itself
    # Antecedents with higher input organised by status
    # Fleeing only the checked ones (must make it variable that can move)