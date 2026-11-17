"""
Battery arbitrage: a battery can charge once and discharge once per day.
Find the best time to charge (buy) and then discharge (sell) to make the most profit.
"""

prices = [52, 48, 45, 41, 39, 44, 60, 85, 92, 78, 65, 58, 55, 61, 70, 98, 110, 95, 72, 60]


def best_trade_brute_force(prices: list[float]) -> tuple[int, int, float]:
    """O(n²) time: try every pair"""
    best = (0, 0, 0.0)
    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):
            profit = prices[sell] - prices[buy]
            if profit > best[2]:
                best = (buy, sell, profit)
    return best


def best_trade(prices: list[float], efficiency: float = 1.0) -> tuple[int, int, float]:
    """O(n) time, O(1) space: one pass, remembering the cheapest price so far"""
    best = (0, 0, 0.0)
    cheapest_index = 0
    for i, price in enumerate(prices):
        if price < prices[cheapest_index]:
            cheapest_index = i
        # We pay for 1 unit of energy but can only sell `efficiency` units back
        profit = price * efficiency - prices[cheapest_index]
        if profit > best[2]:
            best = (cheapest_index, i, profit)
    return best


assert best_trade_brute_force(prices) == best_trade(prices)
assert best_trade([100, 90, 80]) == (0, 0, 0.0)  # Prices only fall: don't trade

buy, sell, profit = best_trade(prices)
print(f"Charge at slot {buy} (£{prices[buy]}), discharge at slot {sell} (£{prices[sell]}): £{profit}/MWh")

buy, sell, profit = best_trade(prices, efficiency=0.9)
print(f"With 90% efficiency: £{profit:.1f}/MWh")
