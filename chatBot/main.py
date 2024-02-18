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


os.environ["OPENAI_API_KEY"] = "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"

chat = ChatOpenAI(openai_api_key="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")

with open('courseCatalog.txt', "r") as file:
    text = file.read()

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 512,
    chunk_overlap = 0,
    length_function = count_tokens,
    is_separator_regex = False
)

chunks = text_splitter.create_documents([text])

embeddings = OpenAIEmbeddings()

db = FAISS.from_documents(chunks, embeddings)

#INSERT QUESTION HERE

chain = load_qa_chain(OpenAI(temperature = 0), chain_type = "stuff")

query = "What will I learn in CSS 101?"
docs = db.similarity_search(query)
docs[0]

chain.run(input_documents = docs, question = query)

messages = [
    SystemMessage(content="You're a helpful assistant tasked with helping users identify university course details and prerequisites."),
    HumanMessage(content="What is your purpose?")
]

myGPT = ConversationalRetrievalChain.from_llm(OpenAI(temperature = 0.1), db.as_retriever())

chat_history = []

while query.lower() != 'exit':
    print("Type EXIT to stop, otherwise ask a question.")
    query = input()
    result = myGPT({"question": query, "chat_history": chat_history})
    chat_history.append(query, result['answer'])

print("Exiting Application.")

