from datetime import datetime
from pathlib import Path
import os.path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.metric_cards import style_metric_cards
import streamlit_authenticator as stauth
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from loginpage import *
st.set_page_config(page_title="KPI Dashboard WebApp",
                   page_icon=":bar_chart:",
                   layout="wide"
)
def save_value(key):
    st.session_state[key] = st.session_state["_"+key]
def get_value(key):
    st.session_state["_"+key] = st.session_state[key] 
def logout():
    st.switch_page("loginpage.py")
#-------------------------------------------------------------------
#----------------------PAGE SIDEBAR---------------------------------
#-------------------------------------------------------------------
with st.sidebar:
    st.header("Main pages")
    st.page_link("pages/company.py", label="Company", icon="🌎")
    st.page_link("pages/department.py", label="Department", icon="📚")
    st.page_link("pages/person.py", label="Person", icon="👨‍💼")
    st.markdown("###")
    st.page_link("loginpage.py",label="Log out", icon="⬅️")
#---------------------------------------------------------
    st.markdown("---")
    st.header("Filter Data")
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_selected = 0
    year_selected = 0
    default_month = 0
    default_year = 0
    if(current_month == 1):
        default_month = 11
        default_year = current_year - 1
    else:
        default_month = current_month - 1
        default_year = current_year
    if "select_month" not in st.session_state:
        st.session_state["select_month"] = default_month
    get_value("select_month")
    selected_month = st.selectbox(
            "Select Month",
            [1,2,3,4,5,6,7,8,9,10,11,12],
            key= "_select_month",
            args=["select_month"],
            on_change=save_value,)
    save_value("select_month")
    if "select_year" not in st.session_state:
        st.session_state["select_year"] = default_year
    get_value("select_year")
    selected_year = st.selectbox(
            "Select Year",
            list(range(default_year-2,default_year+2)),
            key= "_select_year",
            args=["select_year"],
            on_change=save_value,) 
    save_value("select_year")
#-------------------------------------------------------------------
#----------------------PAGE ENVIRONMENT-----------------------------
#-------------------------------------------------------------------
excel_name = './data/' + str(selected_year) + '-' + str(selected_month) +'.xlsx'
checkfile = os.path.isfile(excel_name)
if checkfile == True:
    df = pd.read_excel(io=excel_name, 
        engine='openpyxl',
        sheet_name='Data',
        skiprows=3,
        usecols='B:Q',
        nrows=1000,)
    #---------------------------------------------------------
    with stylable_container(
            key="title",
            css_styles="""
            {   
                text-align: center;
            }"""
        ):
        st.header("3C .Inc Key Performance Indicators Dashboard - " + str(selected_month) + "/" + str(selected_year)) 
    #-----------------------------------------------------------------------------------
    name = st.sidebar.multiselect(
            "Select Person",
            options = df["Name"].unique(),
            max_selections=1
        )
    st.markdown("---")
    df_selection = df.query(
        "Name == @name",
        )

    #-----------------------------------------------------------------------------------
    st.subheader("1️⃣ Statistical Index")
    st.markdown("###")
    statistical_index(df_selection)
    st.markdown("---")
    #-----------------------------------------------------------------------------------
    st.subheader("2️⃣ Works Chart")
    st.markdown("###")
    cols = st.columns([1,2,1])
    with cols[1]:
        person_workbar(df_selection)
    st.markdown("---")
    #-----------------------------------------------------------------------------------  
    st.subheader("3️⃣ Data Frame")
    st.markdown("###")   
    st.dataframe(
            df_selection,
            width=1800,
            hide_index=True,
            column_order=["Department","Name","Kpi Works","Kpi Bonus","Kpi Final","Coefficient","Note"],
            column_config={
            "Kpi Works": st.column_config.ProgressColumn("KPI Works", format="%.2f", min_value=50, max_value=150),
            "Kpi Bonus": st.column_config.ProgressColumn("KPI Bonus", format="%.1f", min_value=-20, max_value=20),
            "Kpi Final": st.column_config.ProgressColumn("KPI Final", format="%.2f", min_value=50, max_value=150),
            "Coefficient": st.column_config.ProgressColumn("KPI Coefficient", format="%.1f", min_value=0.0, max_value=2.0),
            "Note": st.column_config.TextColumn("Note", width="large"),
        }
        )
else:
    with stylable_container(
            key="title",
            css_styles="""
            {   
                text-align: center;
            }"""
        ):
        st.header("3C .Inc Key Performance Indicators Dashboard")  
        st.markdown("---")
        st.write("Data " + str(selected_month) + "/" + str(selected_year) + " is not available")