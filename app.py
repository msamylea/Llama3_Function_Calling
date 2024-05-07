from yahoo_fin import stock_info
import json
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.runnables import RunnableLambda
from datetime import datetime

model=OllamaFunctions(model="l3custom", format="json")

def get_stock_price(stock_ticker: str) -> float:
    current_price = stock_info.get_live_price(stock_ticker)
    print("The current price is ", "$", round(current_price, 2))

def create_meeting(attendee, time):
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    print(f"Scheduled a meeting with {attendee} on {time}")

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


def invoke_and_run(model, invoke_arg):
    result = model.invoke(invoke_arg)
    if result:
        function_call = result.additional_kwargs['function_call']
        print(function_call)
        function_name = function_call['name']
        arguments = json.loads(function_call['arguments'])
        function = functions[function_name]
        if function_name == 'get_stock_price':
            runnable = RunnableLambda(function)
            stock_ticker = arguments['stock_ticker']
            if isinstance(stock_ticker, str):
                runnable.invoke(stock_ticker)
            else:
                runnable.map().invoke(stock_ticker)
        else:
            if 'time' in arguments:
                if isinstance(arguments['time'], dict):
                    try:
                        arguments['time'] = arguments['time']['time']
                    except KeyError:
                        raise ValueError("The 'time' dictionary does not have a key named 'time'")
                elif not isinstance(arguments['time'], str):
                    raise ValueError("The 'time' value must be a string")
            function(**arguments)

invoke_and_run(model, "What is the current stock price of Apple (AAPL)?")
invoke_and_run(model, f"Today is {datetime.now()}. Schedule a meeting with John at 3:00PM tomorrow")
