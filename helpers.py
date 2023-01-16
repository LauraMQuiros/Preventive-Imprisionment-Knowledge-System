import streamlit as st

def init_session_state():
    #These are the values that do not need to move through pages
    st.session_state['report_coefficient'] = 0
    st.session_state['antecedant_alpha'] = 0.5
    st.session_state['modifier_weight'] = 0.1
    st.session_state['final_threshold'] = 1.5

    #This is in an if bc otherwise it never allows to move through pages
    if 'state' not in st.session_state.keys():
        st.session_state['state'] = 'crime estimation'
    #These are the main 3 values   
    if 'crime_weight' not in st.session_state.keys():
        st.session_state['crime_weight'] = 0
    if 'antecedent_weight' not in st.session_state.keys():
        st.session_state['antecedent_weight'] = 0
    if 'fleeing_weight' not in st.session_state.keys():
        st.session_state['fleeing_weight'] = 0

    #1st page values
    if 'estimated_crime' not in st.session_state.keys():
        st.session_state['estimated_crime'] = "none"
    if 'estimated_category' not in st.session_state.keys():
        st.session_state['estimated_category'] = "none"
    if 'estimated_category_weight' not in st.session_state.keys():
        st.session_state['estimated_category_weight'] = 0
    if 'estimated_category_crimes' not in st.session_state.keys():
        st.session_state['estimated_category_crimes'] = "none"
    if 'estimated_crime_weight' not in st.session_state.keys():
        st.session_state['estimated_crime_weight'] = 0

    #2nd page values
    if 'selected_antecedents' not in st.session_state.keys():
        st.session_state["selected_antecedents"]= []
    if 'selected_status' not in st.session_state.keys():
        st.session_state["selected_status"]= []

    #3rd page values
    if 'modifiers' not in st.session_state.keys():
        st.session_state['modifiers'] = []