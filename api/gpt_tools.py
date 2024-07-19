import json
import numpy as np
from .OptionPackage.option_definitions import VanillaOption
from .OptionPackage.OptionPositionClass import OptionPosition
from . import config

response_json = {"message":None, "plot": None}


def add_option_position_to_portfolio(option_flavour, option_type, strike_price, quantity, position, underlying_ticker, barrier_level = None, barrier_type = None):
    """
    Add an option position to the portfolio.

    :param portfolio: The OptionPortfolio instance to which the position will be added
    :param option_flavour: The flavour/type of the option (e.g., "vanilla")
    :param option_type: The type of the option (e.g., "call" or "put")
    :param strike_price: The strike price of the option
    :param quantity: The number of option contracts
    :param position: The position type (e.g., "long" or "short")
    :param underlying_ticker: The ticker symbol of the underlying asset
    :return: A string describing the updated portfolio
    """

    pos_dict = {
        'option_flavour': option_flavour,
        'option_type': option_type,
        'strike_price': strike_price,
        'quantity': quantity,
        'position': position,
        'underlying_ticker': underlying_ticker,
        "barrier_level":barrier_level,
        "barrier_type":barrier_type,
    }
    

    response = config.portfolio.add_position_dict(pos_dict)
    return response
    


def get_portfolio_delta():
    """
    Calculate the delta of the portfolio.

    :param portfolio: The OptionPortfolio instance for which the delta will be calculated
    :return: The calculated delta
    """

    # Plot the value over S0
    plot_json = config.portfolio.plot_delta(return_html = True)

    config.plots.append(plot_json)

    return str(config.portfolio.total_delta())



def get_portfolio_gamma():
    """
    Calculate the gamma of the portfolio.

    :param portfolio: The OptionPortfolio instance for which the gamma will be calculated
    :return: The calculated gamma
    """

    # Plot the value over S0
    plot_json = config.portfolio.plot_gamma(return_html = True)

    config.plots.append(plot_json)


    return str(config.portfolio.total_gamma())



def get_portfolio_value():
    """
    Calculate the value of the portfolio.

    :param portfolio: The OptionPortfolio instance for which the value will be calculated
    :return: The calculated value
    """
    return str(config.portfolio.total_value())



def get_portfolio_value_plot():
    """
    Plot the payoff of the portfolio.

    :param portfolio: The OptionPortfolio instance for which the plot will be generated
    :return: A Plotly figure object representing the plot
    """

    # Plot the value over S0
    plot_json = config.portfolio.plot_value(return_html = True)

    config.plots.append(plot_json)

    return "The value plot of the portfolio is shown to the screen for the user"
    






# Now define the tool guidelines to be used by the GPT agent

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_option_position_to_portfolio",
            "description": "Adds an option position to the portfolio based on specified parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "option_flavour": {
                        "type": "string",
                        "enum": ["vanilla", "barrier", "asian"],
                        "description": "The flavour/type of the option"
                    },
                    "option_type": {
                        "type": "string",
                        "enum": ["call", "put"],
                        "description": "The type of the option"
                    },
                    "strike_price": {
                        "type": "number",
                        "description": "The strike price of the option"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of option contracts"
                    },
                    "position": {
                        "type": "string",
                        "enum": ["long", "short"],
                        "description": "The position type"
                    },
                    "underlying_ticker": {
                        "type": "string",
                        "description": "The ticker symbol of the underlying asset"
                    },
                    "barrier_level": {
                        "type": "number",
                        "description": "The price level of the barrier option (only used for barrier options)"
                    },
                    "barrier_type": {
                        "type": "string",
                        "enum": ["down-and-in", "down-and-out", "up-and-in", "up-and-out"],
                        "description": "The type of barrier option (only used for barrier options)"
                    },
                },
                "required": ["option_flavour", "option_type", "strike_price", "quantity", "position", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_delta",
            "description": "Calculates the delta of the portfolio."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_gamma",
            "description": "Calculates the gamma of the portfolio."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_value",
            "description": "Calculates the value of the portfolio."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_value_plot",
            "description": "Generates and displays a payoff plot for the portfolio."
        }
    }
]



