# Take the user query & retrieve relevant website content & store it in the state

from typing import Dict,List
from graph.state import RAGState,RetrievedDocuments
from retrieval.retriever import Retriever

FAISS_INDEX_PATH = "data/faiss/index.bin"
FAISS_METADATA_PATH = "data/faiss/metadata.json"


# LangGraph node that retrieves relevant website documents based on the current user query
def retrieve_node(state:RAGState)->Dict[str,List[RetrievedDocuments]]:
    user_query= state["user_query"]
    retriever= Retriever(index_path=FAISS_INDEX_PATH, metadata_path=FAISS_METADATA_PATH,)
    results =retriever.retrieve(user_query)
    retrieved_docs:List[RetrievedDocuments]=[]

    for item in results:
        retrieved_docs.append({"text":item["text"], "url": item["url"]})
    
    return {"retrieved_docs":retrieved_docs}





if __name__ == "__main__":

    test_state: RAGState = {
        "user_query": "What does Aryma Labs do?",
        "retrieved_docs": [],
        "answer": "",
        "sources": [],
        "chat_history": [],
    }

    output = retrieve_node(test_state)

    print(f"Retrieved {len(output['retrieved_docs'])} documents.")