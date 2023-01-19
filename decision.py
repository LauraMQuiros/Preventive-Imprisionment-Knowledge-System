import streamlit as st
import streamlit_book as stb
import json
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from helpers import *
import pandas as pd
from matplotlib import cm
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode 
from st_aggrid.grid_options_builder import GridOptionsBuilder



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

def delete_row(df, grid):
    selected_rows = grid['selected_rows']
    if selected_rows:
        selected_indices = [i['_selectedRowNodeInfo']
                            ['nodeRowIndex'] for i in selected_rows]
        df_indices = st.session_state.df_for_grid.index[selected_indices]
        df = df.drop(df_indices)
    return df

def choose_antecedents():
    #First we get some info we are gonna need

    st.subheader('_Antecedents_')
    
    noAntecedents = st.checkbox('There are not any antecedents.') 
    category_weight = st.session_state['estimated_category_weight']
    category_crimes = st.session_state['estimated_category_crimes']
    status = ['Guilty', 'Not guilty, but was in Preventive Prison', 'Not guilty, was not in Preventive Prison'] 

    # df = pd.DataFrame({'Selected Antecedants':[], 'Selected Status': []})
    if "df_for_grid" not in st.session_state:
            st.session_state.df_for_grid = pd.DataFrame({'Selected Antecedants':[], 'Selected Status': []})
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
                new_row = {'Selected Antecedants': newCrime, 'Selected Status': newStatus}
                st.session_state.df_for_grid = st.session_state.df_for_grid.append(new_row, ignore_index=True)
                print(st.session_state.df_for_grid)

    # A table to show the chosen antecedents
    if  st.session_state.df_for_grid.empty == False:
        st.subheader("Antecedents stored")
        gd = GridOptionsBuilder.from_dataframe(st.session_state.df_for_grid)
        gd.configure_selection(selection_mode='multiple', use_checkbox=True)
        gd.configure_column("Selected Antecedants", editable=False)
        gridoptions = gd.build()
        grid_table = AgGrid(st.session_state.df_for_grid, gridOptions=gridoptions, autoHeight  = False, 
                update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)        elim_button = st.button("Eliminate")
        if elim_button:
            st.session_state.df_for_grid = delete_row(st.session_state.df_for_grid, grid_table)
            st.experimental_rerun()
    else:
        st.write("No antecedents have been selected.")

    #computation of the antecedent weight

    selected_antecedents =  st.session_state.df_for_grid['Selected Antecedants']
    selected_status =  st.session_state.df_for_grid['Selected Status'] 
    weight = 0
    for a in range(0,len(selected_antecedents)):
        if selected_status[a] != status[2]:
            weight += category_crimes[selected_antecedents[a]]['weight']
            
    antecedent = st.session_state['antecedant_alpha']
    weight *= antecedent * category_weight
    st.session_state['antecedent_weight']= weight

    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    #Some warnings so we get the info b4 we go to the next page
    if btn8.button('Next'):
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
        st.session_state.df_for_grid = pd.DataFrame({'Selected Antecedants':[], 'Selected Status': []})
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

    # explain when it should be national/local report
    report_type = col1.radio("What is the type of a police report?", kb['Police Report Type'])
    st.session_state['report_coefficient'] = kb['Police Report Type'][report_type]['weight']
    
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
    weight = category_weight*(crime_weight + (len(selected_modifiers)* modifier_weight))
    #We don't use the police report coefficient here bc its noise affects fleeing risk and
    #crime weights as well
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
    inform = []
    for modifier in personal_modifiers:
        if st.checkbox(modifier):
            inform += [modifier]
            n_personal += amount_reduced
    st.session_state["personal_info"] = inform

    info= st.session_state["personal_info"]
    st.write(info)
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
    crimes_of_category = st.session_state['estimated_category_crimes']
    Antecedent_weight = st.session_state['antecedent_weight']
    Crime_weight = st.session_state['crime_weight']
    modifiers = st.session_state['modifiers']
    information = st.session_state['personal_info']
    Fleeing_weight = st.session_state['fleeing_weight']

    final_weight = (Antecedent_weight + Crime_weight + Fleeing_weight)
    st.write("The final weight amounts to " +str(final_weight))

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
    
    st.subheader("The suspect " + string + " going to the preventive prison.")

    # Number of each weight (3), color red the title if made it reach threshold by itself

    st.markdown('---')
    st.write("The value of the final weight is calculated by the multiplication of the coefficient of reliability of the report and three different factors: how serious are their antecedents (past crimes), how serious is the crime committed and how high is the fleeing risk.")
    if round(Fleeing_weight, 2)<=0:
        Fleeing_weight= 0
    st.write("In this case the antecedent weight was "+ str(Antecedent_weight)+ ", the crime weight was "+ str(Crime_weight)+ " and the fleeing risk was around "+ str(round(Fleeing_weight, 2)))
    
    with st.expander("Values of the antecedent weight"):
        antecedents = st.session_state["selected_antecedents"]
        status = st.session_state["selected_status"]
        selected_antecedents_weights = []
                    
        #Get the antecedents with a weight of 0 out
        selected_antecedents= []
        selected_status = []
        for a in range(len(antecedents)):
            if crimes_of_category[antecedents[a]]['weight'] >= 0.25:
                selected_antecedents += [antecedents[a]]
                selected_status += [status[a]]

        #add the weights of the rest
        for crime in selected_antecedents:
            selected_antecedents_weights += [crimes_of_category[crime]['weight']]


        df = pd.DataFrame({'Selected Antecedants': selected_antecedents, 'Selected Status': selected_status, 'Weight': selected_antecedents_weights})
        df = df.sort_values('Selected Antecedants', ascending=True)
        if len(selected_antecedents)>=1:
            st.subheader("Antecedents that influenced the decision")
            st.table(df)
        else:
            st.write("No antecedents were selected")
            #Make an scenario to make this pretty
        st.write("With a category weight of "+ str(category_weight)+ " multiplied by an antecedent weight of 0.5  and the sum of these weights resulted in "+ str(Antecedent_weight))

    with st.expander("Values of the crime weight"):
        st.write("The crime weight is one of the main three parts of the calculation of the final weight and it relies on a _category weight_, a degree/crime weight, and modifiers.")
        st.write("The category weight here was "+ str(round(category_weight, 2))+ " and the crime itself was given a weight of "+ str(I_crime_weight))
        if category_weight >=0.75 and I_crime_weight >=0.75:
            st.warning("These are very high evaluations for both crime category and crime, so it almost guarantees preventive prision by themselves.")
        else:
            if category_weight >=0.75:    
                st.warning("This is a high evaluation for a crime category.")
            if I_crime_weight >=0.75:
                st.warning("This is a high evaluation for a crime.")
        if len(modifiers)>= 1:
            st.write("To all this we add the modifier(s): " + str(modifiers))   

    with st.expander("Values of the fleeing risk weight"):
        # Fleeing only the checked ones (must make it variable that can move) 
        st.write("The risk of fleeing was initialized as the danger of the crime committed (multiplication between category and crime weight), which resulted in "+ str(category_weight*Crime_weight))
        if len(information)>=1:
            st.write("We subtract to this according to the danger factors asked. In this case, the person's risk of fleeing was lowered by the following factors:")
            st.write(information)
        else:
            st.write("There was no normal behavior that could decrease this person's risk factor")
   
        
    st.markdown('---')
    btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8 = st.columns(8)

    if btn1.button('Back'):
        st.session_state['state'] = 'contact information'
        st.experimental_rerun()

    if btn8.button("Restart"):
        st.write("idk")
    
    #sadly couldn't figure out how to print the viewed page as pdf :(