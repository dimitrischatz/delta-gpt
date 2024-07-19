from quart import Quart, request, jsonify
from quart_cors import cors
import json
from . import config
from .OptionPackage.OptionPortfolioClass import OptionPortfolio
from .gpt_completion import gpt_completion
from .gpt_tools import tools

app = Quart(__name__)
cors(app)  # Enable CORS for all routes


@app.route('/')
def home():
    return "Delta GPT API is live!!"



@app.route('/deltagpt_api', methods=['POST'])
async def deltagpt_api():
    # Fetch the data from the request
    data = await request.get_json()
    messages = data.get('messages', [])
    portfolio_json = data.get('portfolio', [])
    message = messages[-1]["content"]

    # Initialize the portfolio and reset the plot
    config.portfolio = OptionPortfolio(portfolio_json)
    config.plots = []

    # Fetch the response
    response_text = await gpt_completion(messages, tools)
    messages.append({"role": "system", "content": response_text})

    # Get the updated portfolio json
    portfolio_response = config.portfolio.dictionary

    #return jsonify(text=response_text, messages=messages, portfolio=portfolio_response, plot=json.loads(config.plots) if config.plots else None)
    return jsonify(text=response_text, messages=messages, portfolio=portfolio_response, plots=config.plots or None)


@app.after_request
def apply_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == '__main__':
    app.run(debug=False)
