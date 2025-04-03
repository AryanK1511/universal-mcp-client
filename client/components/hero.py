# client/components/hero.py

from client.external.streamlit import st


def hero():
    st.title("Universal MCP Client")
    st.markdown(
        "An Assistant that can hook up to any MCP servers and instantly start working with them."
    )
