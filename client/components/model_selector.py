# client/components/model_selector.py

from client.external.streamlit import st


def model_selector():
    option_map = {
        "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet",
        "gpt-4o-mini": "GPT 4o Mini",
        "gpt-4o": "GPT 4o",
    }

    selection = st.pills(
        "Choose a Model",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
    )

    st.write(
        f"Your selected option: {None if selection is None else option_map[selection]}"
    )
