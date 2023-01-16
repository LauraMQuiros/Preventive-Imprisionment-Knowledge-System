import streamlit as st
import streamlit_book as stb
import json
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from helpers import *
import pandas as pd

file = open('kb.json', 'r')
kb = json.load(file)

def choose_estimated_crime():
    crime_categories = kb['categoryCrime']
    col1, col2 = st.columns([1, 1])
    selected_category = col1.radio('What is the category the estimated crime belongs to', crime_categories)
    crimes_of_category = crime_categories[selected_category]['Crimes of Category'] 

    estimate_crime = col2.radio('What is the estimated committed crime?', crimes_of_category)
    st.session_state['estimated_crime'] = estimate_crime
    st.session_state['estimated_category_crimes'] = crimes_of_category
    st.session_state['estimated_category'] = selected_category
    #This is just to have the category weight
    st.session_state['estimated_category_weight'] = crime_categories[selected_category]['crime_category_weight']
    st.session_state['estimated_crime_weight']= crimes_of_category[estimate_crime]['weight']
    print(st.session_state['estimated_crime_weight'])
    if col2.button('Next'):
        st.session_state['state'] = 'antecedents'
        st.experimental_rerun()



def choose_antecedents():
    #First we get some info we are gonna need
    category_weight = st.session_state['estimated_category_weight']
    crime = st.session_state['estimated_crime']
    selected_category = st.session_state["estimated_category"]
    category_crimes = st.session_state['estimated_category_crimes']
    status = ['Guilty', 'Not guilty, but was in Preventive Prison', 'Not guilty, was not in Preventive Prison']

    #Antecedent collection
    my_expander = st.expander(label='Add an antecedent')
    with my_expander:
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

    #A table to show the chosen antecedents
    selected_antecedents = st.session_state["selected_antecedents"]
    selected_status = st.session_state["selected_status"]
    st.header("Antecedents stored")
    df = pd.DataFrame({'selected_antecedants': selected_antecedents, 'selected_status': selected_status})
    #TO-DO: hide the row numbers
    df = df.sort_values('selected_antecedants', ascending=True)
    print(df)

    #Elimination of unwanted antecedents. STATUS: TO-DO    
    col1, col2 = st.columns([1, 1])
    # allow for elimination from the dataframe
    eliminate = col1.button("Eliminate an antecedent")
    if eliminate: 
        options =[]
        for i in range(len(selected_antecedents)):
            options += [i]
        eliminate =st.radio("Select the number of the antecedent you want to eliminate", options)
        elim = st.button("Eliminate")
        if elim:
            df= df.drop([1], axis=0, inplace=True)
            print(df)
            #we have to reload the page i assume for the df to be printed first
            #otherwise this is it. But doesn't work yet

    st.table(df)
    
    #computation of the antecedent weight
    weight =0
    for a in range(0,len(selected_antecedents)):
        if selected_status[a] != status[2]:
            weight += category_crimes[selected_antecedents[a]]['weight']
            
    antecedent = st.session_state['antecedant_alpha']
    weight *= antecedent * category_weight
    print("This is the antecedent weight: "+ str(weight))
    st.session_state['antecedent_weight']= weight

    #Some warnings so we get the info b4 we go to the next page
    if col2.button('Confirm'):
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
    category_weight = st.session_state['estimated_category_weight']
    crime_weight = st.session_state['estimated_crime_weight']
    estimate_crime = st.session_state['estimated_crime']
    modifier_weight = st.session_state['modifier_weight']
    crimes_of_category = st.session_state['estimated_category_crimes']
    number_of_modifiers = 0
    selected_modifiers = []
    modifiers = crimes_of_category[estimate_crime]['modifiers']

    st.header('_Crime Report_')
    col1, col2 = st.columns([1, 1])

    # adjacent crime system STATUS: TO ASK EXPERT
    # explain when it should be national/local report
    report_type = col1.radio("What is the type of a police report?", kb['Police Report Type'])
    st.session_state['report_coefficient'] = kb['Police Report Type'][report_type]['weight']
    report_weight = st.session_state['report_coefficient']

    #explain what modifiers are
    if len(modifiers)>0:
        col2.header("Check all the modifiers of the estimated crime.")
        for modifier in modifiers:
            if col2.checkbox(modifier):
                selected_modifiers += [modifier]
                number_of_modifiers+=1
        st.session_state['modifiers'] = selected_modifiers
        st.table(selected_modifiers)

    #computation of weight  
    weight = category_weight* (crime_weight + report_weight*(number_of_modifiers* modifier_weight))
    print("This is the crime weight: "+ str(weight))
    st.session_state['crime_weight'] = weight

    if st.button('Next'):
        st.session_state['state'] = 'contact information'
        st.experimental_rerun()
     

def personal_info():
    st.header('_Personal Information_')
    category_weight = st.session_state['estimated_category_weight']
    crime_weight = st.session_state['estimated_crime_weight']
    personal_modifiers = kb['Personal Information']['modifiers']
    st.write("Select all the true statements about the suspect:")

    n_personal = 0
    amount_reduced = (category_weight*crime_weight)/ len(personal_modifiers)
    amount_reduced =round(amount_reduced, 4)
    for modifier in personal_modifiers:
         if st.checkbox(modifier):
            n_personal += amount_reduced

    #computation of weight
    weight = (category_weight*crime_weight)- n_personal
    weight = round(weight, 4)
    print("This is the fleeing risk weight:" + str(weight))
    st.session_state['fleeing_weight'] = weight

    if st.button('Next'):
        st.session_state['state'] = 'report'
        st.experimental_rerun()

def final_conclusions():
    category_weight = st.session_state['estimated_category_weight']
    I_crime_weight = st.session_state['estimated_crime_weight']
    
    Antecedent_weight = st.session_state['antecedent_weight']
    Crime_weight = st.session_state['crime_weight']
    modifiers = st.session_state['modifiers']
    Fleeing_weight = st.session_state['fleeing_weight']
    final_weight = (Antecedent_weight + Crime_weight + Fleeing_weight)

    # Like a health bar in a videogame, color coded like a traffic light 
    # css snippets included in https://discuss.streamlit.io/t/change-the-progress-bar-color/8189
    # https://altair-viz.github.io/gallery/bar_chart_with_labels.html
    
    #df = pd.DataFrame({'value': final_weight}, index=[0])
    #print(df)
    #bars = alt.Chart(df).mark_bar().encode(
    #    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c']
    #)
    #st.altair_chart(bars,use_container_width=True)

    #At the end I'm using a plain and boring matplotlib 
    # but it may be cool if we do have adjacent crimes i guess
    print("This is the final weight " +str(final_weight))
    fig, ax = plt.subplots()
    ax.hist(final_weight, bins= 1, orientation= 'horizontal')
    fig.set_size_inches(8.5, 3.5)
    ax.set_xlim(0, 3)
    st.pyplot(fig)
    
    # Number of each weight (3), color red the title if made it reach threshold by itself
    with st.expander("The crime weight: " +str(category_weight)): 
        col1, col2, col3 = st.columns([1,1,1])
        st.write("The crime weight is one of the main three parts of the calculation of the final weight and it relies on category weigh, crime weight and modifiers")
        col1.write("The category weight here was "+ str(round(category_weight, 2)))
        if I_crime_weight >=0.75:
            col1.warning("this is a high evaluation for a category")
        col2.write("The crime weight was "+ str(I_crime_weight))
        if I_crime_weight >=0.75:
            col2.warning("this is a high evaluation for a crime")
        col3.write("To all this we add the modifiers")
        col3.write(modifiers)    

    st.write(str(Antecedent_weight))
        # Maybe it'd be cool to have the df here and make comments on that?
    st.write(str(Fleeing_weight))
        # Fleeing only the checked ones (must make it variable that can move) 
    
    rerun = st.button("Do you want to rerun the model?")
    if rerun:
        st.write("idk")

    # Maybe add download button to download the final conclusions as pdf
