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
    

def get_portfolio_description():
    return config.portfolio.describe_portfolio()




# Functions to add spreads

def add_straddle_position_to_portfolio(strike_price, quantity, position, underlying_ticker):
        if(position == 'long'):
             call_position_direction = 'long'
             put_position_direction = 'long'
        
        else:
             call_position_direction = 'short'
             put_position_direction = 'short'


        call_pos_dict = {
            'option_flavour': "vanilla",
            'option_type': "call",
            'strike_price': strike_price,
            'quantity': quantity,
            'position': call_position_direction,
            'underlying_ticker': underlying_ticker,
            "barrier_level":None,
            "barrier_type":None,
        }

        put_pos_dict = {
            'option_flavour': "vanilla",
            'option_type': "put",
            'strike_price': strike_price,
            'quantity': quantity,
            'position': call_position_direction,
            'underlying_ticker': underlying_ticker,
            "barrier_level":None,
            "barrier_type":None,
        }

        config.portfolio.dictionary.append(call_pos_dict)
        config.portfolio.dictionary.append(put_pos_dict)
             
        # Create a call option
        call_option = VanillaOption(S0=None, K=strike_price, T=1, r=0.05, sigma=None, option_type='call', ticker=underlying_ticker)
        call_position = OptionPosition(call_option, call_position_direction, quantity)
        config.portfolio.add_position(call_position)
        
        # Create a put option
        put_option = VanillaOption(S0=None, K=strike_price, T=1, r=0.05, sigma=None, option_type='put', ticker=underlying_ticker)
        put_position = OptionPosition(put_option, put_position_direction, quantity)
        config.portfolio.add_position(put_position)

        # Logging message
        return f"Added {quantity} {position} straddle position with {underlying_ticker} underlying and strike {strike_price} to the portfolio."


def add_strangle_position_to_portfolio(higher_strike_price, lower_strike_price, quantity, position, underlying_ticker):
    if position == 'long':
        call_position_direction = 'long'
        put_position_direction = 'long'
    else:
        call_position_direction = 'short'
        put_position_direction = 'short'


    call_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "call",
        'strike_price': higher_strike_price,
        'quantity': quantity,
        'position': call_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level":None,
        "barrier_type":None,
    }

    put_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "put",
        'strike_price': lower_strike_price,
        'quantity': quantity,
        'position': call_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level":None,
        "barrier_type":None,
    }

    config.portfolio.dictionary.append(call_pos_dict)
    config.portfolio.dictionary.append(put_pos_dict)


    # Create a call option at a higher strike price
    call_option = VanillaOption(S0=None, K=higher_strike_price, T=1, r=0.05, sigma=None, option_type='call', ticker=underlying_ticker)
    call_position = OptionPosition(call_option, call_position_direction, quantity)
    config.portfolio.add_position(call_position)
    
    # Create a put option at a lower strike price
    put_option = VanillaOption(S0=None, K=lower_strike_price, T=1, r=0.05, sigma=None, option_type='put', ticker=underlying_ticker)
    put_position = OptionPosition(put_option, put_position_direction, quantity)
    config.portfolio.add_position(put_position)

    # Logging message
    return f"Added {quantity} {position} strangle position with {underlying_ticker} underlying and lower strike of {lower_strike_price} and higher strike of {higher_strike_price} to the portfolio."


def add_call_spread_to_portfolio(lower_strike_price, higher_strike_price, quantity, spread_type, underlying_ticker):
    if spread_type == 'bull':
        long_strike_price = lower_strike_price
        short_strike_price = higher_strike_price
        long_position_direction = 'long'
        short_position_direction = 'short'
    elif spread_type == 'bear':
        long_strike_price = higher_strike_price
        short_strike_price = lower_strike_price
        long_position_direction = 'long'
        short_position_direction = 'short'
    else:
        return "Invalid spread type. Choose 'bull' or 'bear'."

    # Dictionary for long position
    long_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "call",
        'strike_price': long_strike_price,
        'quantity': quantity,
        'position': long_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Dictionary for short position
    short_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "call",
        'strike_price': short_strike_price,
        'quantity': quantity,
        'position': short_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Adding option dictionaries to the portfolio list
    config.portfolio.dictionary.append(long_pos_dict)
    config.portfolio.dictionary.append(short_pos_dict)

    # Create long position call option
    long_call_option = VanillaOption(S0=None, K=long_strike_price, T=1, r=0.05, sigma=None, option_type='call', ticker=underlying_ticker)
    long_call_position = OptionPosition(long_call_option, long_position_direction, quantity)
    config.portfolio.add_position(long_call_position)

    # Create short position call option
    short_call_option = VanillaOption(S0=None, K=short_strike_price, T=1, r=0.05, sigma=None, option_type='call', ticker=underlying_ticker)
    short_call_position = OptionPosition(short_call_option, short_position_direction, quantity)
    config.portfolio.add_position(short_call_position)

    return f"Added {quantity} {spread_type} call spread with {underlying_ticker} underlying, lower strike of {lower_strike_price}, and higher strike of {higher_strike_price} to the portfolio."


def add_put_spread_to_portfolio(lower_strike_price, higher_strike_price, quantity, spread_type, underlying_ticker):
    if spread_type == 'bull':
        long_strike_price = lower_strike_price
        short_strike_price = higher_strike_price
        long_position_direction = 'long'
        short_position_direction = 'short'
    elif spread_type == 'bear':
        long_strike_price = higher_strike_price
        short_strike_price = lower_strike_price
        long_position_direction = 'long'
        short_position_direction = 'short'
    else:
        return "Invalid spread type. Choose 'bull' or 'bear'."

    # Dictionary for long position
    long_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "put",
        'strike_price': long_strike_price,
        'quantity': quantity,
        'position': long_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Dictionary for short position
    short_pos_dict = {
        'option_flavour': "vanilla",
        'option_type': "put",
        'strike_price': short_strike_price,
        'quantity': quantity,
        'position': short_position_direction,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Adding option dictionaries to the portfolio list
    config.portfolio.dictionary.append(long_pos_dict)
    config.portfolio.dictionary.append(short_pos_dict)

    # Create long position put option
    long_put_option = VanillaOption(S0=None, K=long_strike_price, T=1, r=0.05, sigma=None, option_type='put', ticker=underlying_ticker)
    long_put_position = OptionPosition(long_put_option, long_position_direction, quantity)
    config.portfolio.add_position(long_put_position)

    # Create short position put option
    short_put_option = VanillaOption(S0=None, K=short_strike_price, T=1, r=0.05, sigma=None, option_type='put', ticker=underlying_ticker)
    short_put_position = OptionPosition(short_put_option, short_position_direction, quantity)
    config.portfolio.add_position(short_put_position)

    return f"Added {quantity} {spread_type} put spread with {underlying_ticker} underlying, lower strike of {lower_strike_price}, and higher strike of {higher_strike_price} to the portfolio."


def add_butterfly_to_portfolio(lower_strike, middle_strike, higher_strike, quantity, option_type, underlying_ticker, position='long'):
    if option_type not in ['call', 'put']:
        return "Invalid option type. Choose 'call' or 'put'."
    if position not in ['long', 'short']:
        return "Invalid position. Choose 'long' or 'short'."

    # Determine positions based on long or short butterfly
    outer_position = 'long' if position == 'long' else 'short'
    middle_position = 'short' if position == 'long' else 'long'

    # Lower strike position
    lower_dict = {
        'option_flavour': "vanilla",
        'option_type': option_type,
        'strike_price': lower_strike,
        'quantity': quantity,
        'position': outer_position,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Middle strike position (double quantity)
    middle_dict = {
        'option_flavour': "vanilla",
        'option_type': option_type,
        'strike_price': middle_strike,
        'quantity': 2 * quantity,
        'position': middle_position,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Higher strike position
    higher_dict = {
        'option_flavour': "vanilla",
        'option_type': option_type,
        'strike_price': higher_strike,
        'quantity': quantity,
        'position': outer_position,
        'underlying_ticker': underlying_ticker,
        "barrier_level": None,
        "barrier_type": None,
    }

    # Adding option dictionaries to the portfolio list
    config.portfolio.dictionary.extend([lower_dict, middle_dict, higher_dict])

    # Create and add options to the portfolio
    lower_option = VanillaOption(S0=None, K=lower_strike, T=1, r=0.05, sigma=None, option_type=option_type, ticker=underlying_ticker)
    lower_position = OptionPosition(lower_option, outer_position, quantity)
    config.portfolio.add_position(lower_position)

    middle_option = VanillaOption(S0=None, K=middle_strike, T=1, r=0.05, sigma=None, option_type=option_type, ticker=underlying_ticker)
    middle_position = OptionPosition(middle_option, middle_position, 2 * quantity)
    config.portfolio.add_position(middle_position)

    higher_option = VanillaOption(S0=None, K=higher_strike, T=1, r=0.05, sigma=None, option_type=option_type, ticker=underlying_ticker)
    higher_position = OptionPosition(higher_option, outer_position, quantity)
    config.portfolio.add_position(higher_position)

    return f"Added {quantity} {position} {option_type} butterfly spread with {underlying_ticker} underlying, strikes at {lower_strike}, {middle_strike}, and {higher_strike} to the portfolio."


def empty_portfolio():
     return config.portfolio.empty_portfolio()


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
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_description",
            "description": "Get a detailed description of the option portfolio."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_straddle_position_to_portfolio",
            "description": "Adds a straddle position to the portfolio based on specified parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "strike_price": {
                        "type": "number",
                        "description": "The strike price of the straddle"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of straddles to be added to the portfolio"
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
                },
                "required": ["strike_price", "quantity", "position", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_strangle_position_to_portfolio",
            "description": "Adds a straddle position to the portfolio based on specified parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "higher_strike_price": {
                        "type": "number",
                        "description": "The higher strike price of the strangle (call option)"
                    },
                     "lower_strike_price": {
                        "type": "number",
                        "description": "The lower strike price of the strangle (put option)"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of straddles to be added to the portfolio"
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
                },
                "required": ["strike_price", "quantity", "position", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_call_spread_to_portfolio",
            "description": "Adds a call spread position to the portfolio based on specified parameters, which can be configured as either a bull or bear call spread.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lower_strike_price": {
                        "type": "number",
                        "description": "The lower strike price of the call option; for a bull spread this is the strike price of the long position, and for a bear spread this is the strike price of the short position."
                    },
                    "higher_strike_price": {
                        "type": "number",
                        "description": "The higher strike price of the call option; for a bull spread this is the strike price of the short position, and for a bear spread this is the strike price of the long position."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of call spreads to be added to the portfolio"
                    },
                    "spread_type": {
                        "type": "string",
                        "enum": ["bull", "bear"],
                        "description": "The type of call spread, either 'bull' for a bullish outlook or 'bear' for a bearish outlook."
                    },
                    "underlying_ticker": {
                        "type": "string",
                        "description": "The ticker symbol of the underlying asset."
                    }
                },
                "required": ["lower_strike_price", "higher_strike_price", "quantity", "spread_type", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_put_spread_to_portfolio",
            "description": "Adds a put spread position to the portfolio based on specified parameters, which can be configured as either a bull or bear put spread.",
            "parameters": {
                "type": "object",
                "properties": {
                        "lower_strike_price": {
                        "type": "number",
                        "description": "The lower strike price of the put option; for a bull spread this is the strike price of the short position, and for a bear spread this is the strike price of the long position."
                    },
                        "higher_strike_price": {
                        "type": "number",
                        "description": "The higher strike price of the put option; for a bull spread this is the strike price of the long position, and for a bear spread this is the strike price of the short position."
                    },
                        "quantity": {
                        "type": "integer",
                        "description": "The number of put spreads to be added to the portfolio"
                    },
                        "spread_type": {
                        "type": "string",
                        "enum": ["bull", "bear"],
                        "description": "The type of put spread, either 'bull' for a bullish outlook or 'bear' for a bearish outlook."
                    },
                        "underlying_ticker": {
                        "type": "string",
                        "description": "The ticker symbol of the underlying asset."
                    }
                },
                "required": ["lower_strike_price", "higher_strike_price", "quantity", "spread_type", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_butterfly_to_portfolio",
            "description": "Adds a butterfly spread position to the portfolio based on specified parameters. This can be either a call or put butterfly spread.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lower_strike_price": {
                        "type": "number",
                        "description": "The lowest strike price of the three options in the butterfly spread. This is a long position."
                    },
                    "middle_strike_price": {
                        "type": "number",
                        "description": "The middle strike price of the three options in the butterfly spread. This is a short position with double the quantity of the others."
                    },
                    "higher_strike_price": {
                        "type": "number",
                        "description": "The highest strike price of the three options in the butterfly spread. This is a long position."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of butterfly spreads to be added to the portfolio. Note that the middle strike will have double this quantity."
                    },
                    "option_type": {
                        "type": "string",
                        "enum": ["call", "put"],
                        "description": "The type of options used in the butterfly spread, either 'call' for a call butterfly or 'put' for a put butterfly."
                    },
                    "underlying_ticker": {
                        "type": "string",
                        "description": "The ticker symbol of the underlying asset."
                    },
                    "position": {
                        "type": "string",
                        "enum": ["long", "short"],
                        "description": "The position type"
                    },
                },
                "required": ["lower_strike_price", "middle_strike_price", "higher_strike_price", "quantity", "option_type", "underlying_ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "empty_portfolio",
            "description": "Empty the portfolio"
        }
    },
    
]



