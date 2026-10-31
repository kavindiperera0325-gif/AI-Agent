
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Company Smart Assistant Agent",
    page_icon="🤖"
)

st.title("🤖 Company Productivity & Policy Agent")

st.write(
    "Ask me anything about company leave policies, "
    "working hours, or IT guidelines!"
)

api_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

company_knowledge = """
- Working Hours: 9:00 AM to 5:00 PM, Monday to Friday.
  Core hours are 10:00 AM to 3:00 PM.

- Hybrid Policy: Employees can work remotely up to
  2 days per week with manager approval.

- Leave Policy: 14 days of annual leave and 7 days
  of casual leave per year. Requests must be submitted
  3 days in advance via the HR portal.

- IT Support: For hardware issues, email
  support@company.com or message the #it-help
  channel on Slack.
"""

if api_key:
    client = Groq(api_key=api_key)

    user_query = st.chat_input(
        "Ask a question about company policies..."
    )

    if user_query:
        with st.chat_message("user"):
            st.write(user_query)

        system_prompt = f"""
        You are a helpful internal corporate assistant.

        Use ONLY the following company knowledge base
        to answer questions accurately.

        If the answer is not available, say you don't know
        and advise the employee to contact HR.

        Knowledge Base:
        {company_knowledge}
        """

        with st.chat_message("assistant"):
            with st.spinner("Agent is checking company policies..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ],
                    temperature=0.3,
                )

                answer = response.choices[0].message.content
                st.write(answer)

else:
    st.info("🔑 Please enter your Groq API key in the sidebar.")
