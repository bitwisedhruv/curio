import asyncio
import json

# from logging import getLogger
from fastapi import FastAPI, WebSocket
from model.chatModel import ChatBody
from services.llm_service import LLMService
from services.sort_source_service import SortSourceService
from services.search_service import SearchSrervice

app = FastAPI()
search_service = SearchSrervice()
sortSourceService = SortSourceService()
llmService = LLMService()
# logger = getLogger(__name__)


# chat websocket
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await asyncio.sleep(0.1)
        data = await websocket.receive_json()
        query = data.get("query")
        search_results = search_service.web_search(query)
        sorted_results = sortSourceService.sort_sources(query, search_results)
        await asyncio.sleep(0.1)
        await websocket.send_json(
            {
                "type": "search_result",
                "data": sorted_results,
            }
        )
        for chunk in llmService.generate_response(query, sorted_results):
            await asyncio.sleep(0.1)
            await websocket.send_json(
                {
                    "type": "content",
                    "data": chunk,
                }
            )
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        await websocket.close()


# chat
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_results = search_service.web_search(body.query)
    sorted_results = sortSourceService.sort_sources(body.query, search_results)
    # print(sorted_results)
    response = llmService.generate_response(body.query, sorted_results)
    # return body.query
    return response
