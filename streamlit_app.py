import streamlit as st

from graph.state import RAGState
from graph.rag_graph import build_rag_graph

#pg config
st.set_page_config(page_title="Aryma Labs RAG Chatbot",layout="centered")
st.title("Aryma Labs RAG Chatbot")
st.write("Ask questions based on content from arymalabs.com")

#graph
if "rag_graph" not in st.session_state:
    st.session_state.rag_graph = build_rag_graph()

#session state
if "rag_state" not in st.session_state:
    st.session_state.rag_state ={"user_query":"",
                                "retrieved_docs":[],
                                "answer":"",
                                "sources":[],
                                "chat_history":[]}  
    
#to show chat history
for message in st.session_state.rag_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# chat input
user_input= st.chat_input("Ask a question about Aryma Labs")


if user_input:
    #show user input
    with st.chat_message("user"):
        st.markdown(user_input)

    #update state
    st.session_state.rag_state["user_query"]=user_input

    #running rag
    st.session_state.rag_state=st.session_state.rag_graph.invoke(st.session_state.rag_state)

    #showing assistant's answer
    with st.chat_message("assistant"):
        st.markdown(st.session_state.rag_state["answer"])

        if st.session_state.rag_state["sources"]:
            st.markdown("**Sources:**")
            for src in st.session_state.rag_state["sources"]:
                st.markdown(f"- {src}")

