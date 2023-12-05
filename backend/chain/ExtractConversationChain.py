from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from model.model import *
from chromadb.utils import embedding_functions
from chain.chains import *
from agent.agents import *
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
conversation_chain = ConversationChain()

def document_load_and_split(uuid):
    # 데이터베이스에서 document 정보 가져옴
    novel = Novel.objects.filter(uuid=uuid)[0]
    print(novel.url)
    collection = chroma_client.get_or_create_collection(name=uuid, embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key = os.getenv("OPENAI_API_KEY")
    ))
    db = Chroma(
        client = chroma_client,
        collection_name=uuid,
        embedding_function = OpenAIEmbeddings(api_key = os.getenv("OPENAI_API_KEY"))
    )
    # collection = chroma_client.get_or_create_collection(name=uuid, embedding_function=OpenAIEmbeddings)
    print(collection.count())
    if collection.count() == 0:
        logging.info("document 저장 시작")
        # document loader
        loader = UnstructuredPDFLoader('./documents/{}.{}'.format(novel.uuid, novel.url.rsplit('.', 1)[1].lower()))

        # split
        data = loader.load()
        documents = text_splitter.split_documents(data)
        # 문서 요약 및 저장
        summarization = summarize_chain.run(documents)
        novel.summary = summarization
        novel.save()
        print(documents[1])
        for idx, doc in enumerate(documents):
            collection.add(documents=doc.page_content, ids=[str(idx)], metadatas=doc.metadata)
        # collection.add(documents=documents, ids=ids)
        # database
    else:
        logging.info("이미 저장되어 있습니다.")
        
    # 전처리 시작
    print('소설 전처리 시작')
    res = collection.get(
        ids=[str(i) for i in range(collection.count())]
    )
    print(res)
    docs = res['documents']
    conversations = []
    for doc in docs:  
        try:
            print(novel.summary)
            conversation = conversation_chain.run(novel.summary, doc)
            print(conversation)
            conversations += conversation
        except Exception as e:
            print(e)
            break
    # speaker 정보 추출
    speakers = set(character.speaker for character in conversations)

    # 각 speaker에 대한 utterance 리스트 구성
    utterances_dict = {speaker: [] for speaker in speakers}
    for character in conversations:
        if character.speaker:
            utterances_dict[character.speaker].append(character.utterance)
    # 발화의 개수가 2개 이상인 것만 남김
    utterances_dict = {speaker: utterances for speaker, utterances in utterances_dict.items() if len(utterances) >= 3}
    
    # 발화자의 정보를 담음
    for speaker, utterances in utterances_dict.items():
        
        retriever = db.as_retriever()
        agent = get_search_agent(retriever)
        result = agent.invoke({"input" : f"\"{novel.name}\"이라는 소설에 등장하는 \"{speaker}\"라는 인물의 겉모습을 알려줘."})
        novel_character = NovelCharacter(name=speaker, appearance=result['output'], conversations=utterances, novel=novel)
        novel_character.save()
        # res = agent.invoke({"input" : "\"운수 좋은 날\"이라는 소설에 등장하는 김 첨지가 아내에게 화를 낼 때의 심정은 어떨까?"})
        # return utterances_dict
        


# # 문서 검색
# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt") # rag prompt 가져오기
# # chain 생성
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import RunnablePassthrough
# conversation_chain = ConversationChain()
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)
# def extract_conversation(collection, db, name):
#     length = collection.count() # 길이
#     res = collection.get(
#         ids=[str(i) for i in range(length)]
#     )
#     print(res)
#     docs = res['documents']
#     conversations = []
#     for doc in docs:  
#         conversations.append(conversation_chain.run(doc))
#     # speaker 정보 추출
#     speakers = set(character.speaker for character in conversations)

#     # 각 speaker에 대한 utterance 리스트 구성
#     utterances_dict = {speaker: [] for speaker in speakers}
#     for character in conversations:
#         if character.speaker:
#             utterances_dict[character.speaker].append(character.utterance)
#     # 발화의 개수가 10개 이상인 것만 남김
#     utterances_dict = {speaker: utterances for speaker, utterances in utterances_dict.items() if len(utterances) >= 10}
    
#     # 발화자의 정보를 담음
#     for speaker, utterances in utterances_dict.items():
        
#         retriever = db.as_retriever()
#         agent = get_search_agent(retriever)
#         appearance = agent.invoke({"input" : f"\"{name}\"이라는 소설에 등장하는 \"{speaker}\"라는 인물의 겉모습을 알려줘."})
#         Character(name=speaker, appearance=appearance, conversations=utterances, )
#         # res = agent.invoke({"input" : "\"운수 좋은 날\"이라는 소설에 등장하는 김 첨지가 아내에게 화를 낼 때의 심정은 어떨까?"})
#         # return utterances_dict

                