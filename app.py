from yahoo_fin import stock_info
import json
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from datetime import datetime

model=OllamaFunctions(model="l3custom", format="json")

def get_stock_price(stock_ticker: str) -> float:
    current_price = stock_info.get_live_price(stock_ticker)
    return current_price

def create_meeting(attendee, time):
    time = datetime.strptime(kwargs['time'], "%Y-%m-%dT%H:%M:%S")
    print(f"Scheduled a meeting with {attendee} at {time}")


tools = [
        { 
            "name": "get_stock_price",
            "description": "Get the current price of the given stock",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_ticker": {
                        "type": "string",
                        "description": "The stock ticker to pass into the function"
                    }
                },
                "required": ["stock_ticker"]
            }
        },
        {
            "name": "create_meeting",
            "description": "Schedule a meeting for the user with the specified details",
            "parameters": {
                "type": "object",
                "properties": {
                    "attendee": {
                        "type": "string",
                        "description": "The person to schedule the meeting with"
                    },
                    "time": {
                        "type": "datetime",
                        "description": "The date and time of the meeting"
                    }
                },
                "required": [
                    "attendee",
                    "time"
                ]
            },
        },
    ],

model = model.bind_tools(
    tools = [
        { 
            "name": "get_stock_price",
            "description": "Get the current price of the given stock",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_ticker": {
                        "type": "string",
                        "description": "The stock ticker to pass into the function"
                    }
                },
                "required": ["stock_ticker"]
            }
        },
        {
            "name": "create_meeting",
            "description": "Schedule a meeting for the user with the specified details",
            "parameters": {
                "type": "object",
                "properties": {
                    "attendee": {
                        "type": "string",
                        "description": "The person to schedule the meeting with"
                    },
                    "time": {
                        "type": "datetime",
                        "description": "The date and time of the meeting"
                    }
                },
                "required": [
                    "attendee",
                    "time"
                ]
            },
        },
    ],

)


functions = {
    "get_stock_price": get_stock_price,
    "create_meeting": create_meeting,
}


result = model.invoke("What is the current stock price of Apple (AAPL)?")
if result:
    runnable = RunnableLambda(get_stock_price)

    function_call = result.additional_kwargs['function_call']

    arguments = json.loads(function_call['arguments'])

    stock_ticker = arguments['stock_ticker']

    if isinstance(stock_ticker, str):
        price = runnable.invoke(stock_ticker)
        print("The current price is ", "$", round(price, 2))   
    else:
        price = runnable.map().invoke(stock_ticker)
        print("The current price is ", "$", round(price, 2))    

price = HumanMessage(content=price)   


kwargs = model.invoke("Schedule a meeting with John at 3:00PM tomorrow")
function_call = kwargs.additional_kwargs['function_call']
function_name = kwargs.additional_kwargs['function_call']['name']
kwargs = json.loads(kwargs.additional_kwargs['function_call']['arguments'])

function = functions[function_name]
function(**kwargs)