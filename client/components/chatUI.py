import streamlit as st
from utils.api import ask_question

def render_chat():
    st.subheader("💬 Chat with your documents")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        # Use a specific display method to avoid truncation
        st.chat_message(msg["role"]).code(msg["content"], language='python') # You can change the language, or omit it.

    # Input and response
    user_input = st.chat_input("Type your question here...")
    if user_input:
        # **CORRECTED:** Use a code block to display the full user input
        st.chat_message("user").code(user_input, language='python')
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = ask_question(user_input)
        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])
            
            st.chat_message("assistant").markdown(answer)
            if sources:
                st.markdown("📄 **Sources:**")
                for src in sources:
                    st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.text}")


# import streamlit as st
# from utils.api import ask_question

   
# def render_chat():
#     st.subheader("💬 Chat with your documents")

#     # Add a clear button
#     if st.button("Clear Chat"):
#         st.session_state.messages = []
#         st.rerun()

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # ... rest of your code

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Render existing chat history
#     for msg in st.session_state.messages:
#         # Display the content as markdown to ensure all text is rendered
#         st.chat_message(msg["role"]).markdown(msg["content"])

#     # Input and response
#     user_input = st.chat_input("Type your question here...")
#     if user_input:
#         # **CORRECTED:** Display the full user input without truncation
#         st.chat_message("user").markdown(user_input)
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         response = ask_question(user_input)
#         if response.status_code == 200:
#             data = response.json()
#             answer = data["response"]
#             sources = data.get("sources", [])
            
#             st.chat_message("assistant").markdown(answer)
#             if sources:
#                 st.markdown("📄 **Sources:**")
#                 # The set() function has been removed from this part as it's for the backend
#                 for src in sources:
#                     st.markdown(f"- `{src}`")
#             st.session_state.messages.append({"role": "assistant", "content": answer})
#         else:
#             st.error(f"Error: {response.text}")