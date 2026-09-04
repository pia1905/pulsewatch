from services.change_engine import analyze_stock


# Test 1: Large price movement
result = analyze_stock(
    last_seen_price=1000,
    current_price=1050
)

print("Test 1:", result)


# Test 2: Small movement
result = analyze_stock(
    last_seen_price=1000,
    current_price=1005
)

print("Test 2:", result)


# Test 3: Medium movement
result = analyze_stock(
    last_seen_price=1000,
    current_price=1020
)

print("Test 3:", result)


# Test 4: Volume spike
result = analyze_stock(
    last_seen_price=1000,
    current_price=1008,
    volume_ratio=2.0
)

print("Test 4:", result)