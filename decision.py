import streamlit as st
import streamlit_book as stb
import json
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from helpers import *
import pandas as pd
from matplotlib import cm


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

    st.session_state['estimated_category_weight'] = crime_categories[selected_category]['crime_category_weight']
    st.session_state['estimated_crime_weight']= crimes_of_category[estimate_crime]['weight']

    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    if btn8.button('Next'):
        st.session_state['state'] = 'antecedents'
        st.experimental_rerun()


def choose_antecedents():
    #First we get some info we are gonna need

    st.subheader('_Antecedents_')
    
    noAntecedents = st.checkbox('There are not any antecedents.') 
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

    #A table to show the chosen antecedents
    selected_antecedents = st.session_state["selected_antecedents"]
    selected_status = st.session_state["selected_status"]
    st.subheader("Antecedents stored")
    df = pd.DataFrame({'Selected Antecedants': selected_antecedents, 'Selected Status': selected_status})
    #TO-DO: hide the row numbers
    df = df.sort_values('Selected Antecedants', ascending=True)

    #Elimination of unwanted antecedents. STATUS: TO-DO    
    col1, col2 = st.columns([1, 1])
    # allow for elimination from the dataframe
    eliminate = col1.button("Eliminate an antecedent")
    if eliminate: 
        options =[]
        for i in range(len(selected_antecedents)):
            options += [i]
        row_to_elim = st.radio("Select the number of the antecedent you want to eliminate.", options)
        
        elim = st.button("Eliminate")
        if elim:
            df= df.drop(row_to_elim, axis=0, inplace=True)
            #we have to reload the page i assume for the df to be printed first
            #otherwise this is it. But doesn't work yet

    st.table(df)
    
    #computation of the antecedent weight
    weight = 0
    for a in range(0,len(selected_antecedents)):
        if selected_status[a] != status[2]:
            weight += category_crimes[selected_antecedents[a]]['weight']
            
    antecedent = st.session_state['antecedant_alpha']
    weight *= antecedent * category_weight
    print("This is the antecedent weight: "+ str(weight))
    st.session_state['antecedent_weight']= weight


    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    #Some warnings so we get the info b4 we go to the next page
    if btn8.button('Next'):
        df = {}
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
    
    if btn1.button('Back'):
        df = {}
        st.session_state['state'] = 'crime estimation' 
        st.experimental_rerun()


def crime_report():

    st.subheader('_Police Report_')

    #First we get some info we are gonna need
    category_weight = st.session_state['estimated_category_weight']
    crime_weight = st.session_state['estimated_crime_weight']
    modifier_weight = st.session_state['modifier_weight']

    estimate_crime = st.session_state['estimated_crime']
    crimes_of_category = st.session_state['estimated_category_crimes']
    modifiers = crimes_of_category[estimate_crime]['modifiers']

    selected_modifiers = []

    col1, col2 = st.columns([1, 1])

    # adjacent crime system STATUS: TO ASK EXPERT
    # explain when it should be national/local report
    report_type = col1.radio("What is the type of a police report?", kb['Police Report Type'])
    st.session_state['report_coefficient'] = kb['Police Report Type'][report_type]['weight']
    report_weight = st.session_state['report_coefficient']

    #explain what modifiers are
    if len(modifiers)>0:
        col2.write("Check all the modifiers of the estimated crime.")
        for modifier in modifiers:
            if col2.checkbox(modifier):
                selected_modifiers += [modifier]
        st.session_state['modifiers'] = selected_modifiers
        df = pd.DataFrame({'Selected Modifiers': selected_modifiers})
        st.table(df)

    #computation of weight  
    weight = category_weight*(crime_weight + report_weight*(len(selected_modifiers)* modifier_weight))
    print("This is the crime weight: "+ str(weight))
    st.session_state['crime_weight'] = weight

    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    if btn8.button('Next'):
        st.session_state['state'] = 'contact information'
        st.experimental_rerun()

    if btn1.button('Back'):
        st.session_state['state'] = 'antecedents'
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
    weight = (category_weight*crime_weight) - n_personal
    weight = round(weight, 4)
    st.session_state['fleeing_weight'] = weight

    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    if btn8.button('Next'):
        st.session_state['state'] = 'report'
        st.experimental_rerun()

    if btn1.button('Back'):
        st.session_state['state'] = 'police report'
        st.experimental_rerun()


def gradientbars(bars):
      
      ax = bars[0].axes
      lim = ax.get_xlim()+ax.get_ylim()
      for bar in bars:
          
          bar.set_zorder(1)
          bar.set_facecolor("none")
          x,y = bar.get_xy()
          w, h = bar.get_width(), bar.get_height()
          grad = np.atleast_2d(np.linspace(0,1*w/1.5,256))
          ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0, norm=cm.colors.NoNorm(vmin=0,vmax=1),
          cmap=plt.get_cmap('RdYlGn').reversed())
      ax.axis(lim) 

def final_conclusions():
    category_weight = st.session_state['estimated_category_weight']
    I_crime_weight = st.session_state['estimated_crime_weight']
    
    Antecedent_weight = st.session_state['antecedent_weight']
    Crime_weight = st.session_state['crime_weight']
    modifiers = st.session_state['modifiers']
    Fleeing_weight = st.session_state['fleeing_weight']

    final_weight = (Antecedent_weight + Crime_weight + Fleeing_weight)


    fig, ax = plt.subplots() 
    bar = ax.barh(0, final_weight, height=0.5)
    gradientbars(bar)
    
    plt.yticks([])
    plt.gca().set_aspect(0.5)
    plt.xlim(0, max(2, final_weight+0.05))
    fig.set_size_inches(8.5, 3.5)
    plt.title("Final Calculation")

    st.pyplot(fig)

    string = "IS"

    if final_weight < 1.5:
        string = "IS NOT"
    
    st.write(final_weight)
    st.subheader("The suspect " + string + " going to the preventive prison.")

    
    # Number of each weight (3), color red the title if made it reach threshold by itself
    with st.expander("Explanation of the results."): 
        col1, col2, col3 = st.columns([1,1,1])
        st.write("The crime weight is one of the main three parts of the calculation of the final weight and it relies on a _category weight_, a degree/crime weight, and modifiers.")
        col1.write("The category weight here was "+ str(round(category_weight, 2)))
        if I_crime_weight >=0.75:
            col1.warning("This is a high evaluation for a crime category.")
        col2.write("The crime weight was "+ str(I_crime_weight))
        if I_crime_weight >=0.75:
            col2.warning("This is a high evaluation for a crime.")
        col3.write("To all this we add the modifiers:")
        col3.write(modifiers)    

    st.write(str(Antecedent_weight))
        # Maybe it'd be cool to have the df here and make comments on that?
    st.write(str(Fleeing_weight))
        # Fleeing only the checked ones (must make it variable that can move) 

    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    if btn1.button('Back'):
        st.session_state['state'] = 'contact information'
        st.experimental_rerun()

    if btn8.button("Restart"):
        st.write("idk")
    

    # Maybe add download button to download the final conclusions as pdf
