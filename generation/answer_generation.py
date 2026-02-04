import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AnswerGenerator:
    def __init__(self,model="gpt-4o-mini"):
        self.model=model
        self.client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    #to build a single context string from retrieved doc chunks
    def _build_context(self,documents:List[Dict])-> str:
        context_blocks= []

        for doc in documents:
            text=doc.get("text","")
            url=doc.get("url","")
            block=f"Source: {url}\nContent: {text}"
            context_blocks.append(block)
        return "\n\n".join(context_blocks)

    # Generate an answer based only on retrieved documents
    def generate_answer(self,query:str,documents:List[Dict],chat_history: str = "")->Dict:
        if not documents:
            return{"answer":"I dont know based on the website","sources":[]}
        context=self._build_context(documents)

        system_prompt = (
                            "You are a factual assistant. "
                            "Answer the user's question using the provided website context. "
                            "You may use the conversation history ONLY to understand followup questions or references like 'that', 'they', or 'this'. "
                            "You may infer or synthesize answers if the conclusion can be reasonably derived from multiple parts of the provided context. "
                            "Do NOT use any external knowledge or assumptions."
                            "If the user asks about the conversation itself, summarize based on the conversation history, not the website."
                            "If the answer cannot be reasonably inferred from the content, say: "
                            "I don't know based on the website."
                        )

        
        user_prompt=f"""
                        You are given website content below.

                        Use ONLY this content to answer the question.
                        If the answer is not in the content, respond with:
                        "I don't know based on the website."

                        Conversation so far:
                        {chat_history}
                        
                        Website Content:
                        {context}
                        
                        Question:
                        {query}

                        Answer:
                        """
        
        response=self.client.chat.completions.create(model=self.model,
                                                    messages=  [{"role":"system","content":system_prompt},
                                                                {"role":"user","content":user_prompt}],
                                                    temperature=0)
                                                    
        answer_text=response.choices[0].message.content.strip()
        # to collect all url from retrieved docs 
        sources=list({doc.get("url") for doc in documents if doc.get("url")})
    
        return {"answer":answer_text,"sources":sources}









if __name__ == "__main__":
    retrieved_docs = [
        {
            "url": "https://arymalabs.com/",
            "text": (
                "Aryma Labs is a global partner helping enterprises "
                "improve marketing ROI using data science."
            ),
        }
    ]

    generator = AnswerGenerator()
    query = "What does Aryma Labs do?"
    result = generator.generate_answer(query, retrieved_docs)

    print("\nAnswer:\n")
    print(result["answer"])
    print("\nSources:")
    for src in result["sources"]:
        print(src)



        
        

                             