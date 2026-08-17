import requests
import csv

BASE_URL = "https://api.studiotypo.xyz/book"


def fetch_all_orders():
    orders = []
    offset = 0

    while True:
        try:
            response = requests.get(
                BASE_URL,
                params={"offset": offset},
                timeout=10
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []

        data = response.json()

        orders.extend(data["orders"])

        if len(orders) >= data["total"]:
            break

        offset += data["limit"]

    return orders


def write_orders_csv(orders):
    with open(
        "submissions/chaitna/orders.csv",
        "w",
        newline=""
    ) as file:

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

        for order in orders:
            writer.writerow({
                "id": order["id"],
                "drink": order["drink"],
                "size": order["size"],
                "sugar": order["sugar"],
                "name": order["name"],
                "status": order["status"],
            })


def print_report(orders):
    total_orders = len(orders)

    ready_orders = sum(
        1
        for order in orders
        if order["status"] == "ready"
    )

    drink_counts = {}

    for order in orders:
        drink = order["drink"]
        drink_counts[drink] = drink_counts.get(drink, 0) + 1

    most_ordered_drink = max(
        drink_counts,
        key=drink_counts.get
    )

    most_ordered_count = drink_counts[most_ordered_drink]

    print(f"Total orders: {total_orders}")
    print(f"Ready orders: {ready_orders}")
    print(
        f"Most ordered drink: "
        f"{most_ordered_drink} ({most_ordered_count})"
    )


orders = fetch_all_orders()

if orders:
    write_orders_csv(orders)
    print_report(orders)
