import json
from openai import OpenAI, AsyncOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
import os
from .gpt_tools import *

load_dotenv()  # This loads the environment variables from the .env file


# Initialize the gpt 

GPT_MODEL = "gpt-4o-mini"
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
  )

# GPT Completion request
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature = 0.2,
            top_p = 0.2,
            max_tokens = 300,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    




async def gpt_completion(messages, tools):
  # First define the assistant

  chat_response = chat_completion_request(
    messages, tools=tools
  )

  # Then get the response based on input
  completion  = await chat_response
  assistant_message = completion.choices[0].message

  # Check if there are any tool calls, if so run them

  if(assistant_message.tool_calls):

    for tool_call in assistant_message.tool_calls:


        function = tool_call.function

        # Which function call was invoked
        function_called = tool_call.function

        # Extracting the arguments
        function_args  = json.loads(function_called.arguments)

        # Function names

        available_functions = {
            "add_option_position_to_portfolio": add_option_position_to_portfolio,
            "get_portfolio_delta": get_portfolio_delta,
            "get_portfolio_gamma": get_portfolio_gamma,
            "get_portfolio_value": get_portfolio_value,
            "get_portfolio_value_plot": get_portfolio_value_plot,
            "get_portfolio_description":get_portfolio_description,
            "add_straddle_position_to_portfolio":add_straddle_position_to_portfolio,
            "add_strangle_position_to_portfolio":add_strangle_position_to_portfolio,
            "add_call_spread_to_portfolio":add_call_spread_to_portfolio,
            "add_put_spread_to_portfolio":add_put_spread_to_portfolio,
            "add_butterfly_to_portfolio":add_butterfly_to_portfolio,
            "empty_portfolio":empty_portfolio, 

        }


        fuction_to_call = available_functions[function_called.name]

        print("Called function:", function_called.name)
        print("With arguements")
        print(function_args)
        content = fuction_to_call(*list(function_args .values()))
        print("Received content"+content)

       

        messages.append({
            "tool_call_id": tool_call.id,
            "role": "function",
            "name": function.name,
            "content": content,
        })

        if(function_called.name)=="add_straddle_position_to_portfolio":
           break




    # Now we need to run the response again to give the info to the chatbot
    result = await gpt_completion(messages, tools)
    return result

  else:
    return assistant_message.content
