from tool.tools import *
from langchain.tools import Tool
from chain.chains import *
from langchain.agents import AgentExecutor
from langchain.schema.runnable.passthrough import RunnablePassthrough
from langchain.schema.runnable import RunnableLambda
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from operator import itemgetter
def get_search_agent(retriever):
    # 가장 먼저 소설에서 검색하고 원하는 정보를 얻지 못했을 경우에 구글에 검색하는 agent
    rag_chain = RAGChain(retriever)
    tools = [
        Tool.from_function(
            func=rag_chain.run,
            name="search-in-the-document",
            description="Search in the document."
        ), # 문서 검색 tool
        search_google # 구글 검색 tool
    ]
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "First, search in the document, and if you get an answer saying you don't know, search on Google.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"), # 중간 과정 전달
    ]
)
    llm = ChatOpenAI()
    chat_model_tools = llm.bind(functions = [format_tool_to_openai_function(t) for t in tools])
    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=RunnableLambda(
                itemgetter('intermediate_steps')
            )
            | format_to_openai_functions
        )
        | prompt
        | chat_model_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor