import requests
import csv

BASE_URL = "https://api.studiotypo.xyz/book"
OUTPUT_FILE = "submissions/alagwal-droid/orders.csv"


def get_orders(offset):
    try:
        response = requests.get(
            BASE_URL,
            params={"limit": 50, "offset": offset},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
        return None


def main():
    all_orders = []

    first_page = get_orders(0)

    if first_page is None:
        return

    all_orders.extend(first_page["orders"])

    total = first_page["total"]
    limit = first_page["limit"]

    offset = limit

    while offset < total:
        page = get_orders(offset)

        if page is None:
            return

        all_orders.extend(page["orders"])
        offset = offset + limit

    # Write all orders to CSV
    with open(OUTPUT_FILE, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "id",
            "drink",
            "size",
            "sugar",
            "name",
            "status"
        ])

        for order in all_orders:
            writer.writerow([
                order["id"],
                order["drink"],
                order["size"],
                order["sugar"],
                order["name"],
                order["status"]
            ])

    # Count ready orders
    ready_count = 0

    for order in all_orders:
        if order["status"] == "ready":
            ready_count = ready_count + 1

    # Count drinks
    drink_counts = {}

    for order in all_orders:
        drink = order["drink"]

        if drink in drink_counts:
            drink_counts[drink] = drink_counts[drink] + 1
        else:
            drink_counts[drink] = 1

    most_ordered_drink = ""
    most_ordered_count = 0

    for drink in drink_counts:
        if drink_counts[drink] > most_ordered_count:
            most_ordered_drink = drink
            most_ordered_count = drink_counts[drink]

    print("Total orders:", len(all_orders))
    print("Ready orders:", ready_count)
    print(
        "Most ordered drink:",
        most_ordered_drink,
        "-",
        most_ordered_count,
        "times"
    )


main()