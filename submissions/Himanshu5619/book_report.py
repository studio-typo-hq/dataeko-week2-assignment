import requests
import csv

URL = "https://api.studiotypo.xyz/book"
OUTPUT = "submissions/Himanshu5619/orders.csv"

all_orders = []

try:
    # Get first 50 orders
    response = requests.get(
        URL,
        params={"limit": 50, "offset": 0},
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    total = data["total"]

    all_orders.extend(data["orders"])

    # Get the remaining orders
    if len(all_orders) < total:
        response = requests.get(
            URL,
            params={"limit": 50, "offset": 50},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        all_orders.extend(data["orders"])

    # Write all orders to CSV
    with open(OUTPUT, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "drink",
                "size",
                "sugar",
                "name",
                "status"
            ]
        )

        writer.writeheader()

        for order in all_orders:
            writer.writerow({
                "id": order["id"],
                "drink": order["drink"],
                "size": order["size"],
                "sugar": order["sugar"],
                "name": order["name"],
                "status": order["status"]
            })

    # Count ready orders
    ready_count = 0

    # Count drinks
    drink_counts = {}

    for order in all_orders:

        if order["status"] == "ready":
            ready_count += 1

        drink = order["drink"]

        if drink not in drink_counts:
            drink_counts[drink] = 0

        drink_counts[drink] += 1

    most_ordered_drink = max(
        drink_counts,
        key=drink_counts.get
    )

    most_ordered_count = drink_counts[
        most_ordered_drink
    ]

    print("Total orders:", len(all_orders))
    print("Ready orders:", ready_count)
    print(
        "Most ordered drink:",
        most_ordered_drink,
        most_ordered_count
    )

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
