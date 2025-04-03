# client/components/chat.py

import asyncio

from client.agent import ReactAgent
from client.external.streamlit import st


def chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        st.session_state.agent = ReactAgent()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        print(f"Prompt: {prompt}")
        st.session_state.messages.append({"role": "human", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = asyncio.run(
                    st.session_state.agent.get_agent_response(prompt)
                )
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
