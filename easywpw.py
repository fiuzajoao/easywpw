{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
# Title\
st.title("EASY-WPW Localization Algorithm")\
\
# Step 1: V1 polarity\
v1_polarity = st.radio("What is the delta wave polarity in lead V1?", ["Positive", "Negative/Isoelectric"])\
\
if v1_polarity == "Negative/Isoelectric":\
    # Step 2: Tricuspid pathway\
    qrs_transition = st.radio("Is the QRS transition \uc0\u8804  V3?", ["Yes", "No"])\
    \
    if qrs_transition == "Yes":\
        # Step 3: Most positive delta wave\
        delta_wave = st.radio("Where is the most positive delta wave?", ["Leads II or III", "Leads aVL or aVR"])\
        \
        if delta_wave == "Leads II or III":\
            st.success("Accessory Pathway: Anteroseptal (AS)")\
        else:\
            st.success("Accessory Pathway: Posteroseptal (PS)")\
    else:\
        st.success("Accessory Pathway: Posteroseptal (PS)")\
else:\
    # Step 2: Mitral pathway\
    delta_wave = st.radio("Where is the most positive delta wave?", ["aVL", "II or aVR", "III"])\
    \
    if delta_wave == "aVL":\
        st.success("Accessory Pathway: Posteroseptal (PS)")\
    elif delta_wave == "II or aVR":\
        st.success("Accessory Pathway: Posterolateral (PL)")\
    else:\
        st.success("Accessory Pathway: Anterolateral (AL)")\
}