import streamlit as st

# Title
st.title("EASY-WPW Localization Algorithm")

# Step 1: Lead V1 Polarity
st.header("Step 1: Lead V1 Polarity")
v1_polarity = st.radio("What is the delta wave polarity in lead V1?", ["Positive", "Negative/Isoelectric"], key="v1")

# Determine the pathway based on Step 1
if v1_polarity == "Negative/Isoelectric":
    valve_pathway = "Tricuspid Valve"
else:
    valve_pathway = "Mitral Valve"
st.write(f"**Current Pathway: {valve_pathway}**")

# Proceed based on the selected pathway
if valve_pathway == "Tricuspid Valve":
    # Step 2: Tricuspid QRS Transition
    st.header("Step 2: Tricuspid Valve Pathway")
    qrs_transition = st.radio("Is the QRS transition ≤ V3?", ["Yes", "No"], key="qrs_tricuspid")
    
    if qrs_transition == "Yes":
        # Step 3: Most Positive Delta Wave (Tricuspid ≤ V3)
        st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS ≤ V3)")
        delta_wave = st.radio("Where is the most positive delta wave?", ["Leads II or III", "Leads aVL or aVR"], key="delta_tricuspid")
        
        # Final diagnosis for Tricuspid (QRS ≤ V3)
        if delta_wave == "Leads II or III":
            result = "Anteroseptal (AS)"
        else:
            result = "Posteroseptal (PS)"
    else:
        # Step 3: Most Positive Delta Wave (Tricuspid QRS > V3)
        st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS > V3)")
        delta_wave = st.radio("Where is the most positive delta wave?", ["Leads II or III", "Leads aVL or aVR"], key="delta_tricuspid_late")
        
        # Final diagnosis for Tricuspid (QRS > V3)
        if delta_wave == "Leads II or III":
            result = "Anteroseptal (AS)"
        else:
            result = "Posteroseptal (PS)"

elif valve_pathway == "Mitral Valve":
    # Step 2: Most Positive Delta Wave (Mitral)
    st.header("Step 2: Mitral Valve Pathway")
    delta_wave = st.radio("Where is the most positive delta wave?", ["aVL", "II or aVR", "III"], key="delta_mitral")
    
    # Step 3: Most Negative Delta Wave (Mitral Pathway Refinement)
    if delta_wave == "aVL":
        st.header("Step 3: Delta Wave Analysis (Mitral Pathway)")
        negative_delta_wave = st.radio("Where is the most negative delta wave?", ["aVR", "aVL"], key="negative_delta_mitral")
        
        if negative_delta_wave == "aVR":
            result = "Posteroseptal (PS)"
        else:
            result = "Posterolateral (PL)"
    elif delta_wave == "II or aVR":
        result = "Posterolateral (PL)"
    else:
        result = "Anterolateral (AL)"

# Display the final result only after all questions are answered
if "result" in locals():
    st.success(f"**Accessory Pathway: {result}**")
