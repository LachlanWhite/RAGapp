# run
# export OPENAI_API_KEY="KEYHERE"

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
#from IPython.display import display
import ipywidgets as widgets
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import ContentStore

ContentS = ContentStore.ContentStore()

#os.environ["OPENAI_API_KEY"] = "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"

chat = ChatOpenAI(openai_api_key= os.getenv('OPENAI_API_KEY'))

with open('courseCatalog.txt', "r") as file:
    text = file.read()

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))



#chain = load_qa_chain(OpenAI(temperature = 0), chain_type = "stuff")

#INSERT QUESTION HERE
query = "What prerequisite classes do I need in order to take CSS 360?"
#docs = db.similarity_search(query)
#docs[0]

#chain.run(input_documents = docs, question = query)

messages = [
    SystemMessage(content=ContentS.createPrompt(query, 0.66)),
    HumanMessage(content=query)
]

myGPT = ConversationalRetrievalChain.from_llm(OpenAI(temperature = 0.1), db.as_retriever())

chat_history = []

while query.lower() != 'exit':
    print("Type EXIT to stop, otherwise ask a question.")
    query = input() 
    result = myGPT({"question": query, "chat_history": chat_history})
    chat_history.append(query, result['answer'])

print("Exiting Application.")

