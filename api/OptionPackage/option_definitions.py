# Start with the Vanilla options class

from .OptionBaseClass import Option
import numpy as np
from scipy.stats import norm

class VanillaOption(Option):
    def __init__(self, S0, K, T, r, sigma, option_type="call", ticker=None):
        super().__init__(S0, K, T, r, sigma, ticker)
        self.option_type = option_type

    def price(self):
        if self.option_type == "call":
            return self.S0 * self.N(self.d1()) - self.K * np.exp(-self.r * self.T) * self.N(self.d2())
        elif self.option_type == "put":
            return self.K * np.exp(-self.r * self.T) * self.N(-self.d2()) - self.S0 * self.N(-self.d1())
        else:
            raise ValueError("Invalid option type")

    def delta(self):
        if self.option_type == "call":
            return self.N(self.d1())
        elif self.option_type == "put":
            return self.N(self.d1()) - 1

    def theta(self):
        if self.option_type == "call":
            return (-self.S0 * self.N_prime(self.d1()) * self.sigma / (2 * np.sqrt(self.T))
                    - self.r * self.K * np.exp(-self.r * self.T) * self.N(self.d2()))
        elif self.option_type == "put":
            return (-self.S0 * self.N_prime(self.d1()) * self.sigma / (2 * np.sqrt(self.T))
                    + self.r * self.K * np.exp(-self.r * self.T) * self.N(-self.d2()))

    def rho(self):
        if self.option_type == "call":
            return self.K * self.T * np.exp(-self.r * self.T) * self.N(self.d2())
        elif self.option_type == "put":
            return -self.K * self.T * np.exp(-self.r * self.T) * self.N(-self.d2())

    def payoff(self, S):
        if self.option_type == "call":
            return np.maximum(S - self.K, 0)
        elif self.option_type == "put":
            return np.maximum(self.K - S, 0)
        else:
            raise ValueError("Invalid option type")












class BarrierOption(VanillaOption):
    def __init__(self, S0, K, T, r, sigma, H, barrier_type, option_type="call", ticker=None):
        super().__init__(S0, K, T, r, sigma, option_type, ticker)
        self.H = H
        self.barrier_type = barrier_type

    def price(self):
        q = 0  # Assuming no dividend for simplicity
        gamma = (self.r - q + 0.5 * self.sigma ** 2) / self.sigma ** 2
        eta = np.log((self.H ** 2) / (self.S0 * self.K)) / (self.sigma * np.sqrt(self.T)) + gamma * self.sigma * np.sqrt(self.T)
        nu = np.log(self.S0 / self.H) / (self.sigma * np.sqrt(self.T)) + gamma * self.sigma * np.sqrt(self.T)
        lmbda = np.log(self.H / self.S0) / (self.sigma * np.sqrt(self.T)) + gamma * self.sigma * np.sqrt(self.T)

        vanilla_price = super().price()

        if self.H < self.K:
            if self.barrier_type == "down-and-in" and self.option_type == "call":
                return (self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(eta)
                        - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(eta - self.sigma * np.sqrt(self.T)))
            elif self.barrier_type == "down-and-out" and self.option_type == "call":
                di_call = (self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(eta)
                          - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(eta - self.sigma * np.sqrt(self.T)))
                return vanilla_price - di_call
            elif self.barrier_type == "up-and-in" and self.option_type == "call":
                return vanilla_price
            elif self.barrier_type == "up-and-out" and self.option_type == "call":
                return 0
            elif self.barrier_type == "down-and-in" and self.option_type == "put":
                return (- self.S0 * np.exp(-q * self.T) * self.N(-nu) + self.K * np.exp(-self.r * self.T) * self.N(-nu + self.sigma * np.sqrt(self.T))
                        + self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * (self.N(eta) - self.N(lmbda))
                        - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * (self.N(eta - self.sigma * np.sqrt(self.T)) - self.N(lmbda - self.sigma * np.sqrt(self.T))))
            elif self.barrier_type == "down-and-out" and self.option_type == "put":
                di_put = (- self.S0 * np.exp(-q * self.T) * self.N(-nu) + self.K * np.exp(-self.r * self.T) * self.N(-nu + self.sigma * np.sqrt(self.T))
                          + self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * (self.N(eta) - self.N(lmbda))
                          - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * (self.N(eta - self.sigma * np.sqrt(self.T)) - self.N(lmbda - self.sigma * np.sqrt(self.T))))
                return vanilla_price - di_put
            elif self.barrier_type == "up-and-in" and self.option_type == "put":
                uo_put = (- self.S0 * np.exp(-q * self.T) * self.N(-nu) + self.K * np.exp(-self.r * self.T) * self.N(-nu + self.sigma * np.sqrt(self.T))
                          + self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(-lmbda)
                          - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(-lmbda + self.sigma * np.sqrt(self.T)))
                return vanilla_price - uo_put
            elif self.barrier_type == "up-and-out" and self.option_type == "put":
                if self.H <= self.S0:
                    return vanilla_price
                else:
                    return (- self.S0 * np.exp(-q * self.T) * self.N(-nu) + self.K * np.exp(-self.r * self.T) * self.N(-nu + self.sigma * np.sqrt(self.T))
                            + self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(-lmbda)
                            - self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(-lmbda + self.sigma * np.sqrt(self.T)))
        elif self.H >= self.K:
            if self.barrier_type == "down-and-in" and self.option_type == "call":
                return vanilla_price
            elif self.barrier_type == "down-and-out" and self.option_type == "call":
                return 0
            elif self.barrier_type == "up-and-in" and self.option_type == "call":
                return (self.S0 * np.exp(-q * self.T) * self.N(nu) - self.K * np.exp(-self.r * self.T) * self.N(nu - self.sigma * np.sqrt(self.T))
                        - self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * (self.N(-eta) - self.N(-lmbda))
                        + self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * (self.N(-eta + self.sigma * np.sqrt(self.T)) - self.N(-lmbda + self.sigma * np.sqrt(self.T))))
            elif self.barrier_type == "up-and-out" and self.option_type == "call":
                ui_call = (self.S0 * np.exp(-q * self.T) * self.N(nu) - self.K * np.exp(-self.r * self.T) * self.N(nu - self.sigma * np.sqrt(self.T))
                          - self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * (self.N(-eta) - self.N(-lmbda))
                          + self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * (self.N(-eta + self.sigma * np.sqrt(self.T)) - self.N(-lmbda + self.sigma * np.sqrt(self.T))))
                return vanilla_price - ui_call
            elif self.barrier_type == "down-and-in" and self.option_type == "put":
                return vanilla_price
            elif self.barrier_type == "down-and-out" and self.option_type == "put":
                return 0
            elif self.barrier_type == "up-and-in" and self.option_type == "put":
                return (- self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(-eta)
                        + self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(-eta + self.sigma * np.sqrt(self.T)))
            elif self.barrier_type == "up-and-out" and self.option_type == "put":
                ui_put = (- self.S0 * np.exp(-q * self.T) * (self.H / self.S0) ** (2 * gamma) * self.N(-eta)
                          + self.K * np.exp(-self.r * self.T) * (self.H / self.S0) ** (2 * gamma - 2) * self.N(-eta + self.sigma * np.sqrt(self.T)))
                return vanilla_price - ui_put

    def delta(self):
        delta_S = 0.01
        price_up = BarrierOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        price_down = BarrierOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        return (price_up - price_down) / (2 * delta_S)

    def gamma(self):
        delta_S = 0.01
        price_up = BarrierOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        price = self.price()
        price_down = BarrierOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        return (price_up - 2 * price + price_down) / (delta_S ** 2)

    def vega(self):
        delta_sigma = 0.01  # 1% change in volatility
        price_up = BarrierOption(self.S0, self.K, self.T, self.r, self.sigma + delta_sigma, self.H, self.barrier_type, self.option_type).price()
        price_down = BarrierOption(self.S0, self.K, self.T, self.r, self.sigma - delta_sigma, self.H, self.barrier_type, self.option_type).price()
        return (price_up - price_down) / 2

    def theta(self):
        delta_T = 1/365  # One day
        price_down = BarrierOption(self.S0, self.K, self.T - delta_T, self.r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        return -(self.price() - price_down)  # Note the negative sign

    def rho(self):
        delta_r = 0.01  # 1% change in interest rate
        price_up = BarrierOption(self.S0, self.K, self.T, self.r + delta_r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        price_down = BarrierOption(self.S0, self.K, self.T, self.r - delta_r, self.sigma, self.H, self.barrier_type, self.option_type).price()
        return (price_up - price_down) / 2


    def payoff(self, S_T, S_path=None):
        if S_path is None:
            S_path = [self.S0, S_T]
        
        barrier_hit = self.is_barrier_hit(S_path)
        
        if self.option_type == "call":
            vanilla_payoff = max(S_T - self.K, 0)
        elif self.option_type == "put":
            vanilla_payoff = max(self.K - S_T, 0)
        else:
            raise ValueError("Invalid option type")

        if self.barrier_type.startswith("down-and-in") or self.barrier_type.startswith("up-and-in"):
            return vanilla_payoff if barrier_hit else 0
        elif self.barrier_type.startswith("down-and-out") or self.barrier_type.startswith("up-and-out"):
            return vanilla_payoff if not barrier_hit else 0
        else:
            raise ValueError("Invalid barrier type")

    def is_barrier_hit(self, S_path):
        if self.barrier_type.startswith("down"):
            return any(S <= self.H for S in S_path)
        elif self.barrier_type.startswith("up"):
            return any(S >= self.H for S in S_path)
        else:
            raise ValueError("Invalid barrier type")








class AsianOption:
    def __init__(self, S0, K, T, r, sigma, option_type="call", asian_type="geometric", ticker=None):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.Nt = T*252  # Number of trading days until maturity
        self.option_type = option_type.lower()
        self.asian_type = asian_type.lower()
        self.ticker = ticker

    def price(self):
        if self.asian_type == "geometric":
            return self.geometric_asian_option_price()
        else:
            raise ValueError("Only geometric Asian options are currently supported")

    def geometric_asian_option_price(self):
        adj_sigma = self.sigma * np.sqrt((2 * self.Nt + 1) / (6 * (self.Nt + 1)))
        rho = 0.5 * (self.r - (self.sigma ** 2) * 0.5 + adj_sigma ** 2)
        d1 = (np.log(self.S0 / self.K) + (rho + 0.5 * adj_sigma ** 2) * self.T) / (adj_sigma * np.sqrt(self.T))
        d2 = (np.log(self.S0 / self.K) + (rho - 0.5 * adj_sigma ** 2) * self.T) / (adj_sigma * np.sqrt(self.T))

        if self.option_type == "call":
            price = np.exp(-self.r * self.T) * (self.S0 * np.exp(rho * self.T) * norm.cdf(d1) - self.K * norm.cdf(d2))
        elif self.option_type == "put":
            price = np.exp(-self.r * self.T) * (self.K * norm.cdf(-d2) - self.S0 * np.exp(rho * self.T) * norm.cdf(-d1))
        else:
            raise ValueError("Invalid option type")

        return price

    def delta(self):
        delta_S = 0.01
        price_up = AsianOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.option_type, self.asian_type).price()
        price_down = AsianOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.option_type, self.asian_type).price()
        return (price_up - price_down) / (2 * delta_S)

    def gamma(self):
        delta_S = 0.01
        price_up = AsianOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.option_type, self.asian_type).price()
        price = self.price()
        price_down = AsianOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.option_type, self.asian_type).price()
        return (price_up - 2 * price + price_down) / (delta_S ** 2)

    def vega(self):
        delta_sigma = 0.01
        price_up = AsianOption(self.S0, self.K, self.T, self.r, self.sigma + delta_sigma, self.option_type, self.asian_type).price()
        price_down = AsianOption(self.S0, self.K, self.T, self.r, self.sigma - delta_sigma, self.option_type, self.asian_type).price()
        return (price_up - price_down) / 2

    def theta(self):
        delta_T = 1/365
        price_down = AsianOption(self.S0, self.K, self.T - delta_T, self.r, self.sigma, self.option_type, self.asian_type).price()
        return -(self.price() - price_down)

    def rho(self):
        delta_r = 0.01
        price_up = AsianOption(self.S0, self.K, self.T, self.r + delta_r, self.sigma, self.option_type, self.asian_type).price()
        price_down = AsianOption(self.S0, self.K, self.T, self.r - delta_r, self.sigma, self.option_type, self.asian_type).price()
        return (price_up - price_down) / 2

    def payoff(self, S_T, S_path=None):
        if S_path is None:
            S_path = [self.S0, S_T]
        
        if self.asian_type == "geometric":
            average_price = np.exp(np.mean(np.log(S_path)))
        else:
            average_price = np.mean(S_path)

        if self.option_type == "call":
            return max(average_price - self.K, 0)
        elif self.option_type == "put":
            return max(self.K - average_price, 0)
        else:
            raise ValueError("Invalid option type")
        






class AmericanOption(Option):
    def __init__(self, S0, K, T, r, sigma, option_type='call'):
        super().__init__(S0, K, T, r, sigma)
        self.N = 300  # Number of steps in the binomial tree
        self.option_type = option_type  # 'call' or 'put'

    def binomial_tree_pricing(self):
        dt = self.T / self.N  # Length of one time step
        u = np.exp(self.sigma * np.sqrt(dt))  # Up factor
        d = 1 / u  # Down factor
        p = (np.exp(self.r * dt) - d) / (u - d)  # Risk-neutral probability

        # Initialize the stock price tree
        stock_price_tree = np.zeros((self.N+1, self.N+1))
        for i in range(self.N+1):
            for j in range(i+1):
                stock_price_tree[j, i] = self.S0 * (u ** (i - j)) * (d ** j)

        # Initialize the option value tree
        option_value_tree = np.zeros((self.N+1, self.N+1))
        if self.option_type == 'call':
            option_value_tree[:, self.N] = np.maximum(stock_price_tree[:, self.N] - self.K, 0)
        else:
            option_value_tree[:, self.N] = np.maximum(self.K - stock_price_tree[:, self.N], 0)

        # Fill the tree backwards
        for i in range(self.N-1, -1, -1):
            for j in range(i+1):
                hold = np.exp(-self.r * dt) * (p * option_value_tree[j, i+1] + (1 - p) * option_value_tree[j+1, i+1])
                exercise = self.K - stock_price_tree[j, i] if self.option_type == 'put' else stock_price_tree[j, i] - self.K
                option_value_tree[j, i] = max(hold, exercise)

        return option_value_tree[0, 0]

    def price(self):
        return self.binomial_tree_pricing()

    # Implementing Greek calculations
    def delta(self):
        delta_S = 0.01
        price_up = AmericanOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.option_type).price()
        price_down = AmericanOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.option_type).price()
        return (price_up - price_down) / (2 * delta_S)

    def gamma(self):
        delta_S = 0.01
        price_up = AmericanOption(self.S0 + delta_S, self.K, self.T, self.r, self.sigma, self.option_type).price()
        price = self.price()
        price_down = AmericanOption(self.S0 - delta_S, self.K, self.T, self.r, self.sigma, self.option_type).price()
        return (price_up - 2 * price + price_down) / (delta_S ** 2)

    def vega(self):
        delta_sigma = 0.01  # 1% change in volatility
        price_up = AmericanOption(self.S0, self.K, self.T, self.r, self.sigma + delta_sigma, self.option_type).price()
        price_down = AmericanOption(self.S0, self.K, self.T, self.r, self.sigma - delta_sigma, self.option_type).price()
        return (price_up - price_down) / 2

    def theta(self):
        delta_T = 1/365  # One day
        price_down = AmericanOption(self.S0, self.K, self.T - delta_T, self.r, self.sigma, self.option_type).price()
        return -(self.price() - price_down)  # Note the negative sign

    def rho(self):
        delta_r = 0.01  # 1% change in interest rate
        price_up = AmericanOption(self.S0, self.K, self.T, self.r + delta_r, self.sigma, self.option_type).price()
        price_down = AmericanOption(self.S0, self.K, self.T, self.r - delta_r, self.sigma, self.option_type).price()
        return (price_up - price_down) / 2
