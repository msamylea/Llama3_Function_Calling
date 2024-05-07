# Llama3 Function Calling


Demonstrates calling functions using Llama 3 with Ollama through utilization of LangChain OllamaFunctions.  The functions are basic, but the model does identify which function to call appropriately and returns the correct results.
The LangChain documentation on OllamaFunctions is pretty unclear and missing some of the key elements needed to make it work.

- After you use model.invoke, the return you get is not the final result.  It's JSON that contains the arguments you need for the next step (which is left out of LangChain documentation).
- You next need to extract your function_call and additional arguments (if any) that will be passed into the function call before calling the function.
- For example, if your function is "def call_next():" and you gave it the same name in model.bind_tools , you can extract that from  result = model.invoke with result.additional_kwargs['function_call'].
  - In my code, this results in : {'name': 'get_stock_price', 'arguments': '{"stock_ticker": "AAPL"}'}
- From there, I load that into an arguments variable with json.loads(function_call[arguments]) to extract the actual arguments
- Then I use my functions mapping to determine which function is which (can be used if your name is different than function_name).
- Code shows both direct function invocation and also use of a RunnableLambda in case you need to async

- Note: The model "l3custom" is just llama3:latest via Ollama with a Modelfile that ends with PARAMETER stop Human: PARAMETER stop Assistant:

  

