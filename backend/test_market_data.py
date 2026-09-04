from services.market_data import get_market_data


# Test 1: Existing stock
result = get_market_data("TCS")
print("Test 1:", result)


# Test 2: Lowercase symbol
result = get_market_data("infy")
print("Test 2:", result)


# Test 3: Unknown stock
result = get_market_data("ABC")
print("Test 3:", result)