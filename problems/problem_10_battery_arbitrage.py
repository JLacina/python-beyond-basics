"""
Battery arbitrage: a battery can charge once and discharge once per day.
Given half-hourly electricity prices (£/MWh), find the best time to charge (buy)
and then discharge (sell) to make the most profit.
Charging must happen BEFORE discharging.

(This is the classic "best time to buy and sell stock" problem - aim for O(n).)
"""

prices = [52, 48, 45, 41, 39, 44, 60, 85, 92, 78, 65, 58, 55, 61, 70, 98, 110, 95, 72, 60]

# Todo: Write a brute-force O(n²) solution that checks every (buy, sell) pair

# Todo: Write an O(n) solution: track the lowest price seen so far as you loop

# Todo: Return (buy_index, sell_index, profit) and check both solutions agree

# Bonus: the battery has 90% round-trip efficiency - you only get 90% of the energy back.
#        How does that change the profit calculation?
