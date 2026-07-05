import streamlit as st
from openai import OpenAI

FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal:qa-testcase-generator:DdkyUZ2Y"

system_message = (
    "You are a QA test case generation assistant. "
    "Given a software requirement, generate concise, structured test cases. "
    "Use markdown table format with columns: TC ID, Scenario, Category, Steps, Expected Result."
)

st.set_page_config(
    page_title="AI-Powered Test Case Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("AI-Powered Test Case Generator")
st.write(
    "This Streamlit application uses a fine-tuned OpenAI model to generate "
    "structured QA test cases from software requirements."
)

st.sidebar.header("Settings")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)

st.subheader("Enter Software Requirement")

sample_requirement = """Two-factor authentication feature:
After entering valid username and password, the user must enter a six-digit verification code.
Invalid code should show an error.
Expired code should be rejected.
After three invalid code attempts, verification should be blocked.
"""

requirement = st.text_area(
    "Requirement / Feature Description",
    value=sample_requirement,
    height=220
)

generate_button = st.button("Generate Test Cases")

if generate_button:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not requirement.strip():
        st.error("Please enter a software requirement.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            with st.spinner("Generating test cases using the fine-tuned model..."):
                response = client.chat.completions.create(
                    model=FINE_TUNED_MODEL,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": requirement}
                    ],
                    temperature=temperature
                )

            output = response.choices[0].message.content

            st.subheader("Generated Test Cases")
            st.markdown(output)

            st.download_button(
                label="Download Test Cases",
                data=output,
                file_name="generated_test_cases.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()

st.caption(
    "Roshan G C |DSC670 Milestone 4 | AI-Powered Test Case Generator"
)