import streamlit as st


def main():
    # Set the page layout to wide mode
    st.set_page_config(layout="wide")

    # Define the gray and white background colors
    gray_background = "background-color: #f0f0f0;"
    white_background = "background-color: #ffffff;"

    # Add a title and description at the top
    st.title("ChatGPT-like UI in Streamlit")
    st.write("An example of a ChatGPT-like UI with user input at the bottom.")

    # Create a container for the AI's response at the top
    answer_container = st.container()
    with answer_container:
        st.markdown(
            f'<div style="{white_background} padding: 10px; border-radius: 10px;">', unsafe_allow_html=True)
        st.text("AI's Response:")
        st.text("This is a sample answer from the AI.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Add a placeholder to push the user input box to the bottom
    st.empty()

    # Add a container for user input at the bottom
    user_input_container = st.container()
    with user_input_container:
        st.markdown(
            f'<div style="{gray_background} padding: 10px; border-radius: 10px;">', unsafe_allow_html=True)
        user_input = st.text_input("You:", key="user_input")
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
