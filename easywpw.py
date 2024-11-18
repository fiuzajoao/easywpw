import streamlit as st

# Title
st.title("EASY-WPW Localization Algorithm")

# Initialize session state for question flow control
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "result" not in st.session_state:
    st.session_state["result"] = None

# Function to reset session state for starting over
def reset():
    st.session_state["step"] = 1
    st.session_state["result"] = None

# Step 1: Lead V1 Polarity
if st.session_state["step"] == 1:
    st.header("Step 1: Lead V1 Polarity")
    v1_polarity = st.radio("What is the delta wave polarity in lead V1?", ["", "Positive", "Negative/Isoelectric"], index=0, key="v1_polarity")
    
    if v1_polarity:
        if v1_polarity == "Negative/Isoelectric":
            st.session_state["pathway"] = "Tricuspid Valve"
        else:
            st.session_state["pathway"] = "Mitral Valve"
        st.session_state["step"] = 2
        st.experimental_rerun()

# Show the pathway so far
if "pathway" in st.session_state:
    st.write(f"**Current Pathway: {st.session_state['pathway']}**")

# Step 2: Tricuspid or Mitral Pathway
if st.session_state["step"] == 2:
    if st.session_state["pathway"] == "Tricuspid Valve":
        st.header("Step 2: Tricuspid Valve Pathway")
        qrs_transition = st.radio("Is the QRS transition ≤ V3?", ["", "Yes", "No"], index=0, key="qrs_tricuspid")
        
        if qrs_transition:
            if qrs_transition == "Yes":
                st.session_state["step"] = 3  # Go to Tricuspid QRS ≤ V3
            else:
                st.session_state["step"] = 4  # Go to Tricuspid QRS > V3
            st.experimental_rerun()
    else:
        st.header("Step 2: Mitral Valve Pathway")
        delta_wave = st.radio("Where is the most positive delta wave?", ["", "aVL", "II or aVR", "III"], index=0, key="delta_mitral")
        
        if delta_wave:
            if delta_wave == "aVL":
                st.session_state["step"] = 5  # Mitral Pathway Refinement
            else:
                if delta_wave == "II or aVR":
                    st.session_state["result"] = "Posterolateral (PL)"
                else:
                    st.session_state["result"] = "Anterolateral (AL)"
                st.session_state["step"] = 6
            st.experimental_rerun()

# Step 3: Tricuspid QRS ≤ V3
if st.session_state["step"] == 3:
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS ≤ V3)")
    delta_wave = st.radio("Where is the most positive delta wave?", ["", "Leads II or III", "Leads aVL or aVR"], index=0, key="delta_tricuspid")
    
    if delta_wave:
        if delta_wave == "Leads II or III":
            st.session_state["result"] = "Anteroseptal (AS)"
        else:
            st.session_state["result"] = "Posteroseptal (PS)"
        st.session_state["step"] = 6
        st.experimental_rerun()

# Step 4: Tricuspid QRS > V3
if st.session_state["step"] == 4:
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS > V3)")
    delta_wave = st.radio("Where is the most positive delta wave?", ["", "Leads II or III", "Leads aVL or aVR"], index=0, key="delta_tricuspid_late")
    
    if delta_wave:
        if delta_wave == "Leads II or III":
            st.session_state["result"] = "Anteroseptal (AS)"
        else:
            st.session_state["result"] = "Posteroseptal (PS)"
        st.session_state["step"] = 6
        st.experimental_rerun()

# Step 5: Mitral Pathway Refinement
if st.session_state["step"] == 5:
    st.header("Step 3: Delta Wave Analysis (Mitral Pathway Refinement)")
    negative_delta_wave = st.radio("Where is the most negative delta wave?", ["", "aVR", "aVL"], index=0, key="negative_delta_mitral")
    
    if negative_delta_wave:
        if negative_delta_wave == "aVR":
            st.session_state["result"] = "Posteroseptal (PS)"
        else:
            st.session_state["result"] = "Posterolateral (PL)"
        st.session_state["step"] = 6
        st.experimental_rerun()

# Step 6: Display Final Result
if st.session_state["step"] == 6:
    st.success(f"**Accessory Pathway: {st.session_state['result']}**")
    st.button("Start Over", on_click=reset)
