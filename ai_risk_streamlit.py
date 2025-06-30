import streamlit as st
import json
from pathlib import Path

# Load the JSON Schema
@st.cache_data
def load_schema():
    with open("riskclassification.json", "r", encoding="utf-8") as f:
        return json.load(f)

schema = load_schema()

# --- Render logic engine (simplified to biometrics section as an example) ---
# You can expand this part based on your full schema structure.

def render_biometrics_section():
    st.header("Biometrics")
    responses = {}

    q1 = st.radio(
        schema["JSONSchema"]["definitions"]["biometrics"]["properties"]["5.e.1"]["title"],
        schema["JSONSchema"]["definitions"]["biometrics"]["properties"]["5.e.1"]["enum"]
    )
    responses["5.e.1"] = q1

    if q1 == "Yes":
        q2 = st.radio(
            schema["JSONSchema"]["definitions"]["biometrics"]["dependencies"]["5.e.1"]["oneOf"][1]["properties"]["5.e.2"]["title"],
            schema["JSONSchema"]["definitions"]["biometrics"]["dependencies"]["5.e.1"]["oneOf"][1]["properties"]["5.e.2"]["enum"]
        )
        responses["5.e.2"] = q2
        if q2 == "Yes":
            result = schema["JSONSchema"]["definitions"]["outputForbidden"]["default"]
            st.warning(result)
        else:
            st.info("Further biometric use case questions would follow here.")

    elif q1 == "No":
        q3 = st.selectbox(
            schema["JSONSchema"]["definitions"]["biometrics"]["dependencies"]["5.e.1"]["oneOf"][0]["properties"]["III.1.1"]["title"],
            schema["JSONSchema"]["definitions"]["biometrics"]["dependencies"]["5.e.1"]["oneOf"][0]["properties"]["III.1.1"]["enum"]
        )
        responses["III.1.1"] = q3
        if q3 == "To recognize or infer emotions or intentions...":
            st.info("This may lead to high-risk classification depending on context.")
        else:
            st.success("No high-risk or prohibited use detected in this branch.")

    return responses

# --- Streamlit App ---
st.title("AI System Risk Classification (EU AI Act)")
st.markdown("Answer the following questions to assess the risk level of your AI system.")

section = st.selectbox("Choose a section to evaluate:", ["Biometrics"])  # Can add more later

if section == "Biometrics":
    answers = render_biometrics_section()

st.markdown("---")
st.markdown("\n**Disclaimer:** This tool provides an indication of risk based on the EU AI Act structure. For legal certainty, consult a qualified professional.")
