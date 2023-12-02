from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from model.model import *
from chromadb.utils import embedding_functions
import os 

import logging
import chromadb
from chromadb.config import Settings
# PydanticOutputParser를 위한 클래스 정의
# class Character(BaseModel):
#     speaker:str = Field(description="Name of the character")
#     utterance:str = Field(description="What this character said directly")
# class DocumentPage(BaseModel):
#     conversations : list[Character] = Field(description="Order of conversations")
# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 100,
    length_function = len,
    is_separator_regex = False,
    separators=["\n\n", "\n", "\"", " ", ""] # 대화가 잘리는 것을 막기위해 쌍따옴표를 separator로 추가
)
# chroma client
chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
# chat model
llm = ChatOpenAI()
def document_load_and_split(uuid):
    # 데이터베이스에서 document 정보 가져옴
    novel = Novel.objects.filter(uuid=uuid)
    print(novel[0].url)
    collection = chroma_client.get_or_create_collection(name=uuid, embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key = os.getenv("OPENAI_API_KEY")
    ))
    if collection.count() == 0:
        logging.info("document 저장 시작")
        # document loader
        loader = UnstructuredPDFLoader('./documents/{}.{}'.format(novel[0].uuid, novel[0].url.rsplit('.', 1)[1].lower()))

        # split
        data = loader.load()
        documents = text_splitter.split_documents(data)
        print(documents[1])
        ids = [str(i) for i in range(len(documents))]
        for doc, doc_id in zip(documents, ids):
            collection.add(documents=str(doc), ids=doc_id)
        # collection.add(documents=documents, ids=ids)
        # database
    else:
        logging.info("이미 저장되어 있습니다.")