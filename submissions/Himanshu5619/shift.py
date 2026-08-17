import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-05"

HEADERS = {
    "X-API-Key": "dataeko-2026",
    "Content-Type": "application/json"
}


def get_seat_orders():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"seat": SEAT},
        timeout=10
    )

    response.raise_for_status()

    return response.json()["orders"]


def delete_order(order_id):
    response = requests.delete(
        f"{BASE_URL}/orders/{order_id}",
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()


def create_order(drink, size, sugar, name):
    response = requests.post(
        f"{BASE_URL}/orders",
        headers=HEADERS,
        json={
            "drink": drink,
            "size": size,
            "sugar": sugar,
            "name": name,
            "seat": SEAT
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def update_order(order_id, data):
    response = requests.patch(
        f"{BASE_URL}/orders/{order_id}",
        headers=HEADERS,
        json=data,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def main():

    # Step 0 - clear the seat

    try:
        orders = get_seat_orders()

        print("Orders before clearing:", len(orders))

        for order in orders:
            delete_order(order["id"])

        print("Step 0 complete - seat cleared")

    except requests.exceptions.RequestException as e:
        print("Step 0 failed:", e)
        return


    # Step 1 - Anita

    try:
        order = create_order(
            "latte",
            "medium",
            2,
            "Anita"
        )

        order_id = order["id"]

        print("Anita order created:", order_id)

        update_order(
            order_id,
            {"status": "brewing"}
        )

        print("Anita order is brewing")

        update_order(
            order_id,
            {"status": "ready"}
        )

        print("Anita order is ready")

    except requests.exceptions.RequestException as e:
        print("Step 1 failed:", e)
        return


    # Step 2 - Bharat changes completely

    try:
        order = create_order(
            "espresso",
            "small",
            3,
            "Bharat"
        )

        order_id = order["id"]

        print("Bharat order created:", order_id)

        update_order(
            order_id,
            {
                "drink": "mocha",
                "size": "large",
                "name": "Chandni",
                "status": "pending"
            }
        )

        print("Bharat order changed to Chandni's mocha")

    except requests.exceptions.RequestException as e:
        print("Step 2 failed:", e)
        return


    # Step 3 - Dev leaves

    try:
        order = create_order(
            "americano",
            "large",
            0,
            "Dev"
        )

        order_id = order["id"]

        print("Dev order created:", order_id)

        delete_order(order_id)

        print("Dev order deleted")

    except requests.exceptions.RequestException as e:
        print("Step 3 failed:", e)
        return


    # Step 4 - save final state

    try:
        orders = get_seat_orders()

        print("Final orders:", len(orders))

        with open(
            "submissions/Himanshu5619/seat.csv",
            "w",
            newline=""
        ) as file:

            fieldnames = [
                "seat",
                "id",
                "drink",
                "size",
                "sugar",
                "name",
                "status"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for order in orders:
                writer.writerow({
                    "seat": SEAT,
                    "id": order["id"],
                    "drink": order["drink"],
                    "size": order["size"],
                    "sugar": order["sugar"],
                    "name": order["name"],
                    "status": order["status"]
                })

        print("Step 4 complete - seat.csv created")

    except requests.exceptions.RequestException as e:
        print("Step 4 failed:", e)
        return


main()
