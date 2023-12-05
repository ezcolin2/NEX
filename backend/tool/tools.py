from langchain.utilities import SerpAPIWrapper
from langchain.tools import tool
from chain.chains import *
# 소설에서 검색 후 만족스러운 답을 얻지 못했을 때 구글에서 검색
@tool("search-google")
def search_google(novel_name:str, query : str) -> str:
    """When you search in a novel and the result comes up saying you don't know, search on Google."""
    search = SerpAPIWrapper()
    result = search.run(query)
    return result

