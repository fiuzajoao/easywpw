import streamlit as st

# Title
st.title("EASY-WPW Localization Algorithm")

# Step 1: V1 polarity
v1_polarity = st.radio("What is the delta wave polarity in lead V1?", ["Positive", "Negative/Isoelectric"])

if v1_polarity == "Negative/Isoelectric":
    # Step 2: Tricuspid pathway
    qrs_transition = st.radio("Is the QRS transition ≤ V3?", ["Yes", "No"])
    
    if qrs_transition == "Yes":
        # Step 3: Most positive delta wave
        delta_wave = st.radio("Where is the most positive delta wave?", ["Leads II or III", "Leads aVL or aVR"])
        
        if delta_wave == "Leads II or III":
            st.success("Accessory Pathway: Anteroseptal (AS)")
        else:
            st.success("Accessory Pathway: Posteroseptal (PS)")
    else:
        st.success("Accessory Pathway: Posteroseptal (PS)")
else:
    # Step 2: Mitral pathway
    delta_wave = st.radio("Where is the most positive delta wave?", ["aVL", "II or aVR", "III"])
    
    if delta_wave == "aVL":
        st.success("Accessory Pathway: Posteroseptal (PS)")
    elif delta_wave == "II or aVR":
        st.success("Accessory Pathway: Posterolateral (PL)")
    else:
        st.success("Accessory Pathway: Anterolateral (AL)")
