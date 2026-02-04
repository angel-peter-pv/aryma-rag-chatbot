#LangGraph RAG workflow

from langgraph.graph import StateGraph,END

from graph.state import RAGState
from graph.nodes.retriever_node import retrieve_node
from graph.nodes.generate_node import generate_node

def build_rag_graph():
    graph= StateGraph(RAGState)

    graph.add_node("retrieve",retrieve_node)
    graph.add_node("generate",generate_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve","generate")
    graph.add_edge("generate",END)

    return graph.compile()





