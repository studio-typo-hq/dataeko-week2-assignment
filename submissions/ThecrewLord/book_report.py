import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"


def get_orders(offset):
    response = requests.get(
        f"{BASE_URL}/book",
        params={"offset": offset, "limit": 50},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


try:
    first_page = get_orders(0)

    all_orders = first_page["orders"]
    total = first_page["total"]
    limit = first_page["limit"]

    offset = limit

    while len(all_orders) < total:
        page = get_orders(offset)
        all_orders.extend(page["orders"])
        offset += page["limit"]

    # Write orders.csv
    with open("submissions/ThecrewLord/orders.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "drink", "size", "sugar", "name", "status"]
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

    for order in all_orders:
        if order["status"] == "ready":
            ready_count += 1

    # Count drinks
    drink_counts = {}

    for order in all_orders:
        drink = order["drink"]

        if drink not in drink_counts:
            drink_counts[drink] = 0

        drink_counts[drink] += 1

    # Find most ordered drink
    most_ordered_drink = ""
    most_ordered_count = 0

    for drink in drink_counts:
        if drink_counts[drink] > most_ordered_count:
            most_ordered_drink = drink
            most_ordered_count = drink_counts[drink]

    print("Orders in book:", len(all_orders))
    print("Ready orders:", ready_count)
    print(
        "Most ordered drink:",
        most_ordered_drink,
        "-",
        most_ordered_count
    )

except requests.exceptions.RequestException as error:
    print("Request failed:", error)
