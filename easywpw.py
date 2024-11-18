import streamlit as st

# Title
st.title("EASY-WPW Localization Algorithm")

# Initialize session state for controlling steps and results
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "pathway" not in st.session_state:
    st.session_state["pathway"] = None
if "result" not in st.session_state:
    st.session_state["result"] = None
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# Function to reset the app
def reset():
    st.session_state["step"] = 1
    st.session_state["pathway"] = None
    st.session_state["result"] = None
    st.session_state["answers"] = {}

# Step 1: Lead V1 Polarity
if st.session_state["step"] >= 1:
    st.header("Step 1: Lead V1 Polarity")
    v1_polarity = st.radio(
        "What is the delta wave polarity in lead V1?",
        ["Positive", "Negative/Isoelectric"],
        key="v1_polarity"
    )
    
    if v1_polarity and st.session_state["step"] == 1:
        st.session_state["pathway"] = "Tricuspid Valve" if v1_polarity == "Negative/Isoelectric" else "Mitral Valve"
        st.session_state["answers"]["Step 1"] = f"Lead V1 polarity: {v1_polarity}"
        st.session_state["step"] = 2

# Show the pathway so far
if "pathway" in st.session_state and st.session_state["pathway"]:
    st.write(f"**Current Pathway: {st.session_state['pathway']}**")

# Step 2: Tricuspid or Mitral Pathway
if st.session_state["step"] >= 2:
    if st.session_state["pathway"] == "Tricuspid Valve":
        st.header("Step 2: Tricuspid Valve Pathway")
        qrs_transition = st.radio(
            "Is the QRS transition ≤ V3?",
            ["Yes", "No"],
            key="qrs_tricuspid"
        )
        
        if qrs_transition and st.session_state["step"] == 2:
            st.session_state["answers"]["Step 2"] = f"QRS transition ≤ V3: {qrs_transition}"
            st.session_state["step"] = 3 if qrs_transition == "Yes" else 4
    else:
        st.header("Step 2: Mitral Valve Pathway")
        delta_wave = st.radio(
            "Where is the most positive delta wave?",
            ["aVL", "II or aVR", "III"],
            key="delta_mitral"
        )
        
        if delta_wave and st.session_state["step"] == 2:
            st.session_state["answers"]["Step 2"] = f"Most positive delta wave: {delta_wave}"
            if delta_wave == "aVL":
                st.session_state["step"] = 5  # Mitral Pathway Refinement
            else:
                st.session_state["result"] = "Posterolateral (PL)" if delta_wave == "II or aVR" else "Anterolateral (AL)"
                st.session_state["step"] = 6

# Step 3: Tricuspid QRS ≤ V3
if st.session_state["step"] >= 3 and st.session_state["pathway"] == "Tricuspid Valve":
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS ≤ V3)")
    delta_wave = st.radio(
        "Where is the most positive delta wave?",
        ["Leads II or III", "Leads aVL or aVR"],
        key="delta_tricuspid"
    )
    
    if delta_wave and st.session_state["step"] == 3:
        st.session_state["answers"]["Step 3"] = f"Most positive delta wave: {delta_wave}"
        st.session_state["result"] = "Anteroseptal (AS)" if delta_wave == "Leads II or III" else "Posteroseptal (PS)"
        st.session_state["step"] = 6

# Step 4: Tricuspid QRS > V3
if st.session_state["step"] >= 4 and st.session_state["pathway"] == "Tricuspid Valve":
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS > V3)")
    delta_wave = st.radio(
        "Where is the most positive delta wave?",
        ["Leads II or III", "Leads aVL or aVR"],
        key="delta_tricuspid_late"
    )
    
    if delta_wave and st.session_state["step"] == 4:
        st.session_state["answers"]["Step 3"] = f"Most positive delta wave: {delta_wave}"
        st.session_state["result"] = "Anteroseptal (AS)" if delta_wave == "Leads II or III" else "Posteroseptal (PS)"
        st.session_state["step"] = 6

# Step 5: Mitral Pathway Refinement
if st.session_state["step"] >= 5 and st.session_state["pathway"] == "Mitral Valve":
    st.header("Step 3: Delta Wave Analysis (Mitral Pathway Refinement)")
    negative_delta_wave = st.radio(
        "Where is the most negative delta wave?",
        ["aVR", "aVL"],
        key="negative_delta_mitral"
    )
    
    if negative_delta_wave and st.session_state["step"] == 5:
        st.session_state["answers"]["Step 3"] = f"Most negative delta wave: {negative_delta_wave}"
        st.session_state["result"] = "Posteroseptal (PS)" if negative_delta_wave == "aVR" else "Posterolateral (PL)"
        st.session_state["step"] = 6

# Step 6: Display Final Result
if st.session_state["step"] == 6:
    st.success(f"**Accessory Pathway: {st.session_state['result']}**")
    st.write("### Summary of Answers:")
    for step, answer in st.session_state["answers"].items():
        st.write(f"- {answer}")
    st.button("Start Over", on_click=reset)
