import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-01"
OUTPUT_FILE = "submissions/alagwal-droid/seat.csv"

HEADERS = {
    "X-API-Key": "dataeko-2026",
    "Content-Type": "application/json"
}


def get_seat_orders():
    try:
        response = requests.get(
            BASE_URL + "/orders",
            params={"seat": SEAT},
            timeout=10
        )

        print("GET orders:", response.status_code)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        return data["orders"]

    except requests.exceptions.RequestException as error:
        print("GET request failed:", error)
        return []


def delete_order(order_id):
    try:
        response = requests.delete(
            BASE_URL + "/orders/" + str(order_id),
            headers=HEADERS,
            timeout=10
        )

        print("DELETE", order_id, ":", response.status_code)
        print(response.text)

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as error:
        print("DELETE request failed:", error)
        return False


def create_order(drink, size, sugar, name):
    try:
        data = {
            "drink": drink,
            "size": size,
            "sugar": sugar,
            "name": name,
            "seat": SEAT
        }

        response = requests.post(
            BASE_URL + "/orders",
            headers=HEADERS,
            json=data,
            timeout=10
        )

        print("POST:", response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        print("POST request failed:", error)
        return None


def update_order(order_id, data):
    try:
        response = requests.patch(
            BASE_URL + "/orders/" + str(order_id),
            headers=HEADERS,
            json=data,
            timeout=10
        )

        print("PATCH", order_id, ":", response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        print("PATCH request failed:", error)
        return None


def write_seat_csv(orders):
    with open(OUTPUT_FILE, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "seat",
            "id",
            "drink",
            "size",
            "sugar",
            "name",
            "status"
        ])

        for order in orders:
            writer.writerow([
                order["seat"],
                order["id"],
                order["drink"],
                order["size"],
                order["sugar"],
                order["name"],
                order["status"]
            ])


def main():

    # Step 0 - Clear our seat
    print("STEP 0 - Clearing seat-01")

    existing_orders = get_seat_orders()

    for order in existing_orders:
        delete_order(order["id"])

    # Step 1 - Anita
    print("STEP 1 - Anita")

    anita = create_order(
        "latte",
        "medium",
        2,
        "Anita"
    )

    if anita is None:
        return

    anita_id = anita["id"]

    update_order(
        anita_id,
        {"status": "brewing"}
    )

    update_order(
        anita_id,
        {"status": "ready"}
    )

    # Step 2 - Bharat changes completely to Chandni's order
    print("STEP 2 - Bharat -> Chandni")

    bharat = create_order(
        "espresso",
        "small",
        3,
        "Bharat"
    )

    if bharat is None:
        return

    bharat_id = bharat["id"]

    update_order(
        bharat_id,
        {
            "drink": "mocha",
            "size": "large",
            "sugar": 3,
            "name": "Chandni",
            "status": "pending"
        }
    )

    # Step 3 - Dev walks out
    print("STEP 3 - Dev")

    dev = create_order(
        "americano",
        "large",
        0,
        "Dev"
    )

    if dev is None:
        return

    dev_id = dev["id"]

    delete_order(dev_id)

    # Step 4 - Get final state
    print("STEP 4 - Final seat state")

    final_orders = get_seat_orders()

    write_seat_csv(final_orders)

    print("Final number of orders:", len(final_orders))

    for order in final_orders:
        print(
            order["id"],
            order["drink"],
            order["size"],
            order["sugar"],
            order["name"],
            order["status"]
        )


main()