import streamlit as st
import json

# Load JSON schema from file
with open("riskclassification.json", "r", encoding="utf-8") as f:
    schema = json.load(f)["JSONSchema"]

# Utility to resolve $ref definitions
def resolve_ref(ref: str):
    path = ref.strip("#/").split("/")
    ref_obj = schema
    for key in path:
        ref_obj = ref_obj[key]
    return ref_obj

# Render a form section recursively
def render_section(section: dict, responses: dict, prefix=""):
    properties = section.get("properties", {})
    required = section.get("required", [])

    for key, prop in properties.items():
        full_key = f"{prefix}{key}"
        title = prop.get("title", key)

        if "enum" in prop:
            responses[full_key] = st.selectbox(title, prop["enum"], key=full_key)
        elif prop.get("type") == "string":
            responses[full_key] = st.text_input(title, key=full_key)

    # Handle dependencies (oneOf logic)
    deps = section.get("dependencies", {})
    for dep_key, dep_logic in deps.items():
        if dep_key in responses:
            for option in dep_logic.get("oneOf", []):
                expected_val = option["properties"].get(dep_key, {}).get("enum", [None])[0]
                if responses[dep_key] == expected_val:
                    # Check if it has a $ref
                    for sub_key, sub_prop in option["properties"].items():
                        if "$ref" in sub_prop:
                            sub_section = resolve_ref(sub_prop["$ref"])
                            render_section(sub_section, responses, prefix=f"{sub_key}.")
                        elif sub_key != dep_key:
                            # Render direct properties
                            render_section({"properties": {sub_key: sub_prop}}, responses, prefix=f"{sub_key}.")
                    break

# Main app logic
st.title("🧠 AI System Risk Classification (EU AI Act)")
st.markdown("This tool helps classify the risk level of your AI system based on the EU AI Act. It follows a structured decision tree using your responses.")

section_keys = [k for k in schema["definitions"].keys() if not k.startswith("output")]
section_choice = st.selectbox("📂 Choose a section to evaluate:", section_keys)

if section_choice:
    st.header(f"Section: {section_choice}")
    responses = {}
    section_schema = schema["definitions"][section_choice]
    render_section(section_schema, responses)

    st.subheader("Collected Answers")
    st.json(responses)

    st.info("📝 Note: Risk classification logic output (e.g., `outputHigh`) is defined in your JSON, but applying that logic automatically requires a rules engine. Currently, this app collects structured answers — perfect for legal or compliance expert review.")

