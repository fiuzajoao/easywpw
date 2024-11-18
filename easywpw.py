import streamlit as st

# Title
st.title("EASY-WPW Localization Algorithm")

# Initialize session state to manage steps and answers
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "answers" not in st.session_state:
    st.session_state["answers"] = {}
if "pathway" not in st.session_state:
    st.session_state["pathway"] = None
if "result" not in st.session_state:
    st.session_state["result"] = None

# Function to reset the app
def reset():
    st.session_state["step"] = 1
    st.session_state["answers"] = {}
    st.session_state["pathway"] = None
    st.session_state["result"] = None

# Function to update state dynamically when answers change
def update_state(step, answer_key, value):
    st.session_state["answers"][answer_key] = value
    st.session_state["step"] = step
    st.session_state["pathway"] = None if step == 1 else st.session_state["pathway"]
    st.session_state["result"] = None if step < 6 else st.session_state["result"]

# Step 1: Lead V1 Polarity
if st.session_state["step"] >= 1:
    st.header("Step 1: Lead V1 Polarity")
    v1_polarity = st.radio(
        "What is the delta wave polarity in lead V1?",
        options=["", "Positive", "Negative/Isoelectric"],
        key="v1_polarity",
        on_change=update_state,
        args=(2, "Step 1", st.session_state.get("v1_polarity")),
        format_func=lambda x: "Select..." if x == "" else x
    )
    if v1_polarity == "Negative/Isoelectric":
        st.session_state["pathway"] = "Tricuspid Valve"
    elif v1_polarity == "Positive":
        st.session_state["pathway"] = "Mitral Valve"

# Show pathway based on Step 1
if st.session_state["pathway"]:
    st.write(f"**Current Pathway: {st.session_state['pathway']}**")

# Step 2: Tricuspid or Mitral Pathway
if st.session_state["step"] >= 2:
    if st.session_state["pathway"] == "Tricuspid Valve":
        st.header("Step 2: Tricuspid Valve Pathway")
        qrs_transition = st.radio(
            "Is the QRS transition ≤ V3?",
            options=["", "Yes", "No"],
            key="qrs_tricuspid",
            on_change=update_state,
            args=(3 if st.session_state.get("qrs_tricuspid") == "Yes" else 4, "Step 2", st.session_state.get("qrs_tricuspid")),
            format_func=lambda x: "Select..." if x == "" else x
        )
    elif st.session_state["pathway"] == "Mitral Valve":
        st.header("Step 2: Mitral Valve Pathway")
        delta_wave = st.radio(
            "Where is the most positive delta wave?",
            options=["", "aVL", "II or aVR", "III"],
            key="delta_mitral",
            on_change=update_state,
            args=(5 if st.session_state.get("delta_mitral") == "aVL" else 6, "Step 2", st.session_state.get("delta_mitral")),
            format_func=lambda x: "Select..." if x == "" else x
        )

# Step 3: Tricuspid QRS ≤ V3
if st.session_state["step"] == 3 and st.session_state["pathway"] == "Tricuspid Valve":
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS ≤ V3)")
    delta_wave = st.radio(
        "Where is the most positive delta wave?",
        options=["", "Leads II or III", "Leads aVL or aVR"],
        key="delta_tricuspid",
        on_change=update_state,
        args=(6, "Step 3", st.session_state.get("delta_tricuspid")),
        format_func=lambda x: "Select..." if x == "" else x
    )
    if delta_wave == "Leads II or III":
        st.session_state["result"] = "Anteroseptal (AS)"
    elif delta_wave == "Leads aVL or aVR":
        st.session_state["result"] = "Posteroseptal (PS)"

# Step 4: Tricuspid QRS > V3
if st.session_state["step"] == 4 and st.session_state["pathway"] == "Tricuspid Valve":
    st.header("Step 3: Delta Wave Analysis (Tricuspid Pathway, QRS > V3)")
    delta_wave = st.radio(
        "Where is the most positive delta wave?",
        options=["", "Leads II or III", "Leads aVL or aVR"],
        key="delta_tricuspid_late",
        on_change=update_state,
        args=(6, "Step 3", st.session_state.get("delta_tricuspid_late")),
        format_func=lambda x: "Select..." if x == "" else x
    )
    if delta_wave == "Leads II or III":
        st.session_state["result"] = "Anteroseptal (AS)"
    elif delta_wave == "Leads aVL or aVR":
        st.session_state["result"] = "Posteroseptal (PS)"

# Step 5: Mitral Pathway Refinement
if st.session_state["step"] == 5 and st.session_state["pathway"] == "Mitral Valve":
    st.header("Step 3: Delta Wave Analysis (Mitral Pathway Refinement)")
    negative_delta_wave = st.radio(
        "Where is the most negative delta wave?",
        options=["", "aVR", "aVL"],
        key="negative_delta_mitral",
        on_change=update_state,
        args=(6, "Step 3", st.session_state.get("negative_delta_mitral")),
        format_func=lambda x: "Select..." if x == "" else x
    )
    if negative_delta_wave == "aVR":
        st.session_state["result"] = "Posteroseptal (PS)"
    elif negative_delta_wave == "aVL":
        st.session_state["result"] = "Posterolateral (PL)"

# Step 6: Display Final Result
if st.session_state["step"] == 6:
    st.success(f"**Accessory Pathway: {st.session_state['result']}**")
    st.button("Start Over", on_click=reset)
