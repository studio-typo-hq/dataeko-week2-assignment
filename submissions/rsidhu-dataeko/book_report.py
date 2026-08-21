import requests
import csv


API_URL = "https://api.studiotypo.xyz"
X_API_Key = "dataeko-2026"

def get_book():
    try:
        response = requests.get(
            f"{API_URL}/book",
            # header={"X-API-Key": "dataeko-2026"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Could not fetch the order book: {error}")
        return None


def main():
    data = get_book()

    if data is None:
        return

    orders = data["orders"]

    with open("orders.csv", "w", newline="") as file:
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
                "status": order["status"]
            })

    total_orders = len(orders)

    ready_orders = 0

    drink_counts = {}

    for order in orders:
        if order["status"] == "ready":
            ready_orders += 1

        drink = order["drink"]

        if drink not in drink_counts:
            drink_counts[drink] = 0

        drink_counts[drink] += 1

    most_ordered_drink = max(
        drink_counts,
        key=drink_counts.get
    )

    most_ordered_count = drink_counts[most_ordered_drink]

    print(f"Orders in book: {total_orders}")
    print(f"Ready orders: {ready_orders}")
    print(
        f"Most ordered drink: "
        f"{most_ordered_drink} ({most_ordered_count})"
    )


if __name__ == "__main__":
    main()