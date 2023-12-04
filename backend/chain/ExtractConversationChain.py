from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from model.model import *
from chromadb.utils import embedding_functions
import os 

import logging
import chromadb
from chromadb.config import Settings

# embedding function 정의
embedding_function = OpenAIEmbeddings()

# PydanticOutputParser를 위한 클래스 정의
# class Character(BaseModel):
#     speaker:str = Field(description="Name of the character")
#     utterance:str = Field(description="What this character said directly")
# class DocumentPage(BaseModel):
#     conversations : list[Character] = Field(description="Order of conversations")
# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex = False,
    separators=["\n\n", "\n", "\"", " ", ""] # 대화가 잘리는 것을 막기위해 쌍따옴표를 separator로 추가
)
# chroma client
chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
# from llamaapi import LlamaAPI
# from langchain_experimental.llms import ChatLlamaAPI

# llama = LlamaAPI(os.getenv("LLAMA_API_KEY"))
# llm = ChatLlamaAPI(client=llama)
def document_load_and_split(uuid):
    # 데이터베이스에서 document 정보 가져옴
    novel = Novel.objects.filter(uuid=uuid)
    print(novel[0].url)
    collection = chroma_client.get_or_create_collection(name=uuid, embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        # api_key = os.getenv("OPENAI_API_KEY")
        api_key = "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"
    ))
    db = Chroma(
        client = chroma_client,
        collection_name=uuid,
        embedding_function = OpenAIEmbeddings(api_key = "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")
    )
    # collection = chroma_client.get_or_create_collection(name=uuid, embedding_function=OpenAIEmbeddings)
    print(collection.count())
    if collection.count() == 0:
        logging.info("document 저장 시작")
        # document loader
        loader = UnstructuredPDFLoader('./documents/{}.{}'.format(novel[0].uuid, novel[0].url.rsplit('.', 1)[1].lower()))

        # split
        data = loader.load()
        documents = text_splitter.split_documents(data)
        print(documents[1])
        for idx, doc in enumerate(documents):
            collection.add(documents=doc.page_content, ids=[str(idx)], metadatas=doc.metadata)
        # collection.add(documents=documents, ids=ids)
        # database
    else:
        logging.info("이미 저장되어 있습니다.")
    return collection, db
        
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from collections import defaultdict
from typing import List
class Character(BaseModel):
    speaker:str = Field(description="Name of the character")
    utterance:str = Field(description="What this character said directly")
class DocumentPage(BaseModel):
    conversations : List[Character] = Field(description="Utterances of the character")
parser = PydanticOutputParser(pydantic_object=DocumentPage)
prompt = PromptTemplate(
    template = "I will tell you the content of the novel.\n\n content : {page}\nNow, extract all the dialogue so that the speaker can reveal the content of the novel. {format_instructions}Excluding the description of the situation, only the conversation content enclosed in double quotation marks is extracted. We need to provide information about who the speaker is.",
    input_variables=["page"],
    partial_variables={"format_instructions" : parser.get_format_instructions()}

)
# chat model
llm = ChatOpenAI(api_key="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")
prompt_and_model = prompt | llm

# 문서 검색
from langchain import hub
prompt = hub.pull("rlm/rag-prompt") # rag prompt 가져오기
# chain 생성
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
def extract_conversation(collection, db):
    length = collection.count() # 길이
    res = collection.get(
        ids=[str(i) for i in range(length)]
    )
    print(res)
    docs = res['documents']
    # for doc in docs:  
    #     output = prompt_and_model.invoke({"page" : doc})
    #     print(output)
    #     documentPage = parser.invoke(output)
    #     conversations = documentPage.conversations
    #     print(conversations)
    #     # speaker 정보 추출
    #     speakers = set(character.speaker for character in conversations)

    #     # 각 speaker에 대한 utterance 리스트 구성
    #     utterances_dict = {speaker: [] for speaker in speakers}
    #     for character in conversations:
    #         if character.speaker:
    #             utterances_dict[character.speaker].append(character.utterance)
    #     # 발화의 개수가 10개 이상인 것만 남김
    #     utterances_dict = {speaker: utterances for speaker, utterances in utterances_dict.items() if len(utterances) >= 10}
    retriever = db.as_retriever()
    rag_chain = (
    {"context" : retriever | format_docs, "question" : RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
    res = rag_chain.invoke("동광학교가 뭐야?")
    print(res)
    # return utterances_dict

                