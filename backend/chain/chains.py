# 문서 검색
from langchain import hub
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI()
# chain 생성
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
class RAGChain():
    def __init__(self, retriever) -> None:
        self.retriever = retriever
        self.prompt = hub.pull("rlm/rag-prompt")
        self.llm = llm
        self.chain = (
            {"context" : retriever | format_docs, "question" : RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    def run(self, query):
        return self.chain.invoke(query)

# 대화 추출 chain
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
class ConversationChain():
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=DocumentPage)
        self.prompt = PromptTemplate(
            template = "Iwill tell you the summary of the novel.\n\nsummary : {summary}and I will tell you the content of the novel.\n\n content : {page}\nNow, extract all the dialogue so that the speaker can reveal the content of the novel. {format_instructions}Excluding the description of the situation, only the conversation content enclosed in double quotation marks is extracted. We need to provide information about who the speaker is.",
            input_variables=["summary", "page"],
            partial_variables={"format_instructions" : self.parser.get_format_instructions()}
        )
        self.llm = llm
        self.prompt_and_llm = self.prompt | self.llm
    def run(self, summary, doc):
        output = self.prompt_and_llm.invoke({"summary" : summary, "page" : doc})
        
        documentPage = self.parser.invoke(output)
        return documentPage.conversations
    
from langchain.chains.summarize import load_summarize_chain
summarize_chain = load_summarize_chain(llm, chain_type="refine")
