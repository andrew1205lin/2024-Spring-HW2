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

def calculate_swap_amount(x, y, delta_y):
    """Calculate the amount of token x received for delta_y amount of token y."""
    return x - (x * y) / (y + delta_y)

def find_arbitrage_path(start_token, current_token, balance, path, visited):
    if current_token == start_token and len(path) > 1:
        if balance > 20:
            print(f"Path: {'->'.join(path)}, {start_token} balance={balance}")
            return True
        return False

    for (token_from, token_to), (x, y) in liquidity.items():
        if (token_from, token_to) in visited or (token_to, token_from) in visited:
            continue

        if token_from == current_token:
            new_balance = balance + calculate_swap_amount(x, y, balance)
            if find_arbitrage_path(start_token, token_to, new_balance, path + [token_to], visited + [(token_from, token_to)]):
                return True
        elif token_to == current_token:
            new_balance = balance + calculate_swap_amount(y, x, balance)
            if find_arbitrage_path(start_token, token_from, new_balance, path + [token_from], visited + [(token_to, token_from)]):
                return True
    return False

# Initial token and balance
start_token = "tokenB"
initial_balance = 5

# Start the search for an arbitrage path
find_arbitrage_path(start_token, start_token, initial_balance, [start_token], [])
