liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def calculate_swap_amount(x, y, delta_x):
    """Calculate the amount of token y received for delta_x amount of token x."""
    new_x = x + delta_x
    new_y = (x * y) / new_x
    return new_x, new_y

def update_liquidity(token_from, token_to, new_x, new_y, liquidity):
    """Update the liquidity pool after a swap."""
    liquidity_copy = liquidity.copy()
    liquidity_copy[(token_from, token_to)] = (new_x, new_y)
    return liquidity_copy

def find_arbitrage_path(start_token, current_token, balance, path, visited, liquidity):
    # print(f"Path: {'->'.join(path)}, {current_token} balance={balance}")
    # print(f"liquidity: {liquidity}")
    if current_token == start_token and len(path) > 1:
        if balance > 20:
            print(f"Path: {'->'.join(path)}, {start_token} balance={balance}")
            return True
        return False

    for (token_from, token_to), (x, y) in liquidity.items():
        if (token_from, token_to) in visited or (token_to, token_from) in visited:
            continue

        if token_from == current_token:
            new_x, new_y = calculate_swap_amount(x, y, balance)
            new_balance = y - new_y
            new_liquidity = update_liquidity(token_from, token_to, new_x, new_y, liquidity)
            if find_arbitrage_path(start_token, token_to, new_balance, path + [token_to], visited + [(token_from, token_to)], new_liquidity):
                return True
        elif token_to == current_token:
            new_y, new_x  = calculate_swap_amount(y, x, balance)
            new_balance = x - new_x
            new_liquidity = update_liquidity(token_from, token_to, new_x, new_y, liquidity)
            if find_arbitrage_path(start_token, token_from, new_balance, path + [token_from], visited + [(token_to, token_from)], new_liquidity):
                return True
    return False

# Initial token and balance
start_token = "tokenB"
initial_balance = 5

# Start the search for an arbitrage path
find_arbitrage_path(start_token, start_token, initial_balance, [start_token], [], liquidity)
