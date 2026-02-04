from typing import TypedDict, List

# website derived document used as factual evidence
class RetrievedDocuments(TypedDict):
    text:str
    url:str

# single conversational message used for short term context
class ChatMessage(TypedDict):
    role:str
    content:str

# langGraph state carrying query, retrieved evidence, answer, sources, and session memory
class RAGState(TypedDict):
    user_query:str
    retrieved_docs:List[RetrievedDocuments]
    answer:str
    sources:List[str]
    chat_history:List[ChatMessage]





if __name__ == "__main__":

    state: RAGState = {
        "user_query": "What services does Aryma Labs offer?",
        "retrieved_docs": [
            {
                "text": "Aryma Labs provides AI and data engineering services.",
                "url": "https://www.arymalabs.com/services"
            }
        ],
        "answer": "Aryma Labs provides AI and data engineering services.",
        "sources": ["https://www.arymalabs.com/services"],
        "chat_history": [
            {"role": "user", "content": "Tell me about Aryma Labs"},
            {"role": "assistant", "content": "Aryma Labs is an AI-focused company."}
        ],
    }

    print("RAGState schema test passed.")