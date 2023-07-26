#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 16:55:43 2023

@author: minmyomin
"""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Corps by country", layout="wide")

#st.caches
def get_data_from_dataset():
    df=pd.read_csv('/Users/minmyomin/Desktop/corps dataset/yield_df.csv')
    return df
df=get_data_from_dataset()



##---- Sidebar-----##
st.sidebar.header('Filter:')

area_select=st.sidebar.multiselect(
    'Select the Area:', options=df['Area'].unique(), default=['Australia']
    )


item_select=st.sidebar.multiselect(
    'Select the Corps:', options=df['Item'].unique(), default=['Wheat']
    )

##---- Query ----##
df_selection=df.query(
    "Area==@area_select & Item==@item_select"
    )



## ---- Main Page ---- ##
st.title("Testing User Dashboard")
st.markdown('##')

average_rain=round(df_selection['average_rain_fall_mm_per_year'].mean(),1)
average_hp=round(df_selection['hg/ha_yield'].mean(),1)
average_temp=round(df_selection['avg_temp'].mean(),1)

l_column,m_column, r_column=st.columns(3)

with l_column:
    st.subheader('Average Rain per Year:')
    st.subheader(f"{average_rain:,}")

with m_column:
    st.subheader('Average Hp:')
    st.subheader(f"{average_hp:,}")


with r_column:
    st.subheader('Average Tempature:')
    st.subheader(f"{average_temp:,}")

st.markdown('----')


##----Graph 1---##

temp_by_item=(df_selection.groupby(by=['Item']).sum()[['hg/ha_yield']].sort_values(by='hg/ha_yield')

)

fig_tem_item=px.bar(
    temp_by_item,
    x='hg/ha_yield',
    y=temp_by_item.index,
    orientation='h',
    title='<b> hg/ha_yield by Plants </b>' ,
    color_discrete_sequence=['#0083B8']* len(temp_by_item),
    template='plotly_white',
                                             
    )

##---update layout background---##
fig_tem_item.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
    )

##----Graph 2---##
temp_by_area=(df_selection.groupby(by=['Area']).sum()[['avg_temp']].sort_values(by='avg_temp')

)
fig_tem_area=px.bar(
    temp_by_area,
    y='avg_temp',
    x=temp_by_area.index,
     
    title='<b> Average Temp by Areas</b>' ,
    color_discrete_sequence=['#0083B8']* len(temp_by_area),
    template='plotly_white',
                                             
    )

##---update layout background---##
fig_tem_area.update_layout(
    
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickmode='linear'),
    yaxis=(dict(showgrid=False))
    )


left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_tem_item, use_container_width=True)
right_column.plotly_chart(fig_tem_area, use_container_width=True)


##---Graph 3---##
 



##--list of dataset--##
st.dataframe(df_selection)









##---Hide Streamlit ----##
hide_streamlit="""
            <style> 
            #MainMenu {visibility: hidden;}
            footer{visibility: hidden;}
            header{visibility: hidden;}
            </style> 
            """
st.markdown(hide_streamlit,unsafe_allow_html=True)
