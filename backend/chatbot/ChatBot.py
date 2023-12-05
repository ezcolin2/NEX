from model.model import *
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from agent.agents import *
from agent.Image import *
class ChatBot:
    def __init__(self, id, retriever, novel_name) -> None:
        character = NovelCharacter.objects.get(id=id)
        self.name = character.name # 등장 인물 이름
        self.novel_name = novel_name
        self.appearance = character.appearance # 등장 인물 묘사
        self.conversatioins = '\n'.join(character.conversations) # 등장 인물 발화 내용
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.search_agent = get_search_agent(retriever)
        self.conversation_prompt =ChatPromptTemplate(
            messages=[
                # SystemMessagePromptTemplate.from_template(
                #     f"""I'll give you a new personality. You have the name \"{self.name}\" and I will tell you various sentences. 
                #     These sentences are what a person named \"{self.name}\" said. 
                #     You can learn the tone of these sentences and use that tone.
                #     {self.conversatioins}
                #     The sentences I just gave you are the ones you should imitate. 
                #     You just need to learn this way of speaking. 
                #     And let’s have a conversation with me based on this tone. 
                #     Once again, I'm not telling you to say the sentences I gave you. 
                #     The idea is to have a conversation with me using the tone of that sentence."""
                # ),
                MessagesPlaceholder(variable_name="chat_history"),
                # HumanMessagePromptTemplate.from_template("I'll show you the information. \n\n{question}And use the sentence information I gave you to imitate this person's speaking style."),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        ) # 등장 인물의 말투를 흉내내도록 하는 prompt
        self.conversation_chain = LLMChain(llm=ChatOpenAI(), prompt=self.conversation_prompt, verbose=True, memory=self.memory)

        
    def chat(self, query):
        search_result = self.search_agent.invoke({"input" : f"{self.novel_name}이라는 소설에서 {query}"})['output']
        template = """
        I'll show you the information. \n\n"""+search_result+"""
        I'll give you a new personality. You have the name \""""+self.name+"""\" and I will tell you various sentences. 
        These sentences are what a person named \""""+self.name+"""\" said. 
        You can learn the tone of these sentences and use that tone.
        """+self.conversatioins+"""
        The sentences I just gave you are the ones you should imitate. 
        You just need to learn this way of speaking. 
        And let’s have a conversation with me based on this tone. 
        Once again, I'm not telling you to say the sentences I gave you. 
        The idea is to have a conversation with me using the tone of that sentence.
        Now answer the query"""+query+"""
        You have to imitate sentences i gave you.            
        """
        # res = self.conversation_chain({"question" :  f"information : {search_result}\n Now anaswer the query : {query}"})
        res = self.conversation_chain({"question" :  template})
        url = image_generate("다음 인물을 그려줘."+self.appearance)
        print(url)
        print(res)
        return res['text'], url
        