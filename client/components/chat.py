# client/components/chat.py


from client.agent import ReactAgent
from client.external.streamlit import st


async def chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        st.session_state.agent = ReactAgent()

    if "last_message" not in st.session_state:
        st.session_state.last_message = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                message_placeholder = st.empty()
                message_placeholder.markdown("🤔 Thinking...")

                stream = await st.session_state.agent.get_agent_response(prompt)
                response_content = ""

                async for chunk in stream:
                    if (
                        isinstance(chunk, tuple)
                        and chunk[0] == "values"
                        and chunk[-1] is not None
                    ):
                        print("=====")
                        print(chunk)
                        print("=====")

                        messages = chunk[1].get("messages", [])  # We get the messages
                        for message in messages:
                            if (
                                hasattr(message, "content")
                                and message.content
                                and message.__class__.__name__ == "AIMessage"
                            ):
                                new_content = message.content
                                if new_content != response_content:
                                    response_content = new_content
                                    if (
                                        response_content
                                        != st.session_state.last_message
                                    ):
                                        message_placeholder.markdown(response_content)
                                        st.session_state.last_message = response_content

                st.session_state.messages.append(
                    {"role": "assistant", "content": response_content}
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
