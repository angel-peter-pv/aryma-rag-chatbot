#Uses retrieved website content to generate a grounded answer

from typing import Dict, List
from graph.state import RAGState,ChatMessage
from generation.answer_generation import AnswerGenerator

# node that generates an answer from retrieved documents
def generate_node(state:RAGState)->Dict[str,object]:
    user_query=state["user_query"]
    retrieved_docs=state["retrieved_docs"]
    chat_history=state["chat_history"]

    #take only recent chat history
    recent_history = chat_history[-10:]
    formatted_history= "\n".join(f"{msg['role'].capitalize()}: {msg['content']}"
                                 for msg in recent_history)
    

    generator=AnswerGenerator()
    result=generator.generate_answer(query=user_query, documents=retrieved_docs, chat_history=formatted_history)
    answer=result["answer"]
    sources=result["sources"]

    #to update chat history with the question and answer 
    updated_chat_history:List[ChatMessage]=chat_history+[{"role":"user","content":user_query},
                                                         {"role":"assistant","content":answer}]
    
    return {"answer":answer,"sources":sources,"chat_history":updated_chat_history}





if __name__ == "__main__":

    test_state: RAGState = {
        "user_query": "What does Aryma Labs do?",
        "retrieved_docs": [
            {
                "text": "Aryma Labs is a global partner helping enterprises improve marketing ROI using data science.",
                "url": "https://arymalabs.com/",
            }
        ],
        "answer": "",
        "sources": [],
        "chat_history": [],
    }

    output = generate_node(test_state)

    print("Answer:", output["answer"])
    print("Sources:", output["sources"])