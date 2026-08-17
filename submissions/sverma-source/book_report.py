import requests
import csv
from collections import Counter

API_URL = "https://api.studiotypo.xyz"

try:
    # --------------------------------------------------
    # 1. Get first 50 orders
    # --------------------------------------------------
    response = requests.get(
        f"{API_URL}/book?limit=50&offset=0",
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    orders = data["orders"]

    # --------------------------------------------------
    # 2. Get second 50 orders
    # --------------------------------------------------
    response2 = requests.get(
        f"{API_URL}/book?limit=50&offset=50",
        timeout=10
    )
    response2.raise_for_status()

    data2 = response2.json()
    second_orders = data2["orders"]

    # --------------------------------------------------
    # 3. Combine both pages
    # --------------------------------------------------
    all_orders = orders + second_orders

    # --------------------------------------------------
    # 4. Create orders.csv
    # --------------------------------------------------
    with open("orders.csv", "w", newline="") as csvfile:
        fieldnames = ["id", "drink", "size", "sugar", "name", "status"]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(all_orders)

    # --------------------------------------------------
    # 5. Count ready orders
    # --------------------------------------------------
    ready_orders = [
        order for order in all_orders
        if order["status"] == "ready"
    ]

    # --------------------------------------------------
    # 6. Find most ordered drink
    # --------------------------------------------------
    drink_counts = Counter(
        order["drink"] for order in all_orders
    )

    most_ordered_drink, most_ordered_count = drink_counts.most_common(1)[0]

    # --------------------------------------------------
    # 7. Print results
    # --------------------------------------------------
    print("First page:", len(orders))
    print("Second page:", len(second_orders))
    print("Total orders:", len(all_orders))
    print("Ready orders:", len(ready_orders))
    print("Most ordered drink:", most_ordered_drink)
    print("Most ordered drink count:", most_ordered_count)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
