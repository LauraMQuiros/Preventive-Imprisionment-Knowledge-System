import streamlit as st

def init_session_state():
    st.session_state['report_coefficient'] = 0
    st.session_state['antecedants_coefficient'] = 0
    st.session_state['fleeing_coefficient'] = 0
    st.session_state['modifier_count'] = 0

    st.session_state['antecedant_alpha'] = 0.5
    st.session_state['modifier_weight'] = 0.1

    #This is in an if bc otherwise it never allows to move through pages
    if 'state' not in st.session_state.keys():
        st.session_state['state'] = 'crime estimation'
    if 'category_crime_weight' not in st.session_state.keys():
        st.session_state['category_crime_weight'] = 0
    if 'estimated_crime_coefficient' not in st.session_state.keys():
        st.session_state['estimated_crime_coefficient'] = 0