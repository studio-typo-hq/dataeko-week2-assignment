import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-06"

def create_order(drink, size, sugar, name):
 import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-06"

HEADERS = {
    "X-API-Key": "dataeko-2026",
    "Content-Type": "application/json"
}


def get_seat_orders():
    try:
        response = requests.get(
            f"{BASE_URL}/orders",
            params={"seat": SEAT},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Get orders failed: {e}")
        return []

    return response.json()["orders"]


def clear_seat():
    orders = get_seat_orders()

    for order in orders:
        order_id = order["id"]

        try:
            response = requests.delete(
                f"{BASE_URL}/orders/{order_id}",
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Delete order {order_id} failed: {e}")
            continue

        print(f"Deleted existing order {order_id}")


def create_order(drink, size, sugar, name):
    payload = {
        "drink": drink,
        "size": size,
        "sugar": sugar,
        "name": name,
        "seat": SEAT
    }

    try:
        response = requests.post(
            f"{BASE_URL}/orders",
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Create order failed: {e}")
        return None

    order = response.json()

    print(f"Created order {order['id']}")

    return order


def update_order(order_id, updates):
    try:
        response = requests.patch(
            f"{BASE_URL}/orders/{order_id}",
            headers=HEADERS,
            json=updates,
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Update order {order_id} failed: {e}")
        return None

    order = response.json()

    print(f"Updated order {order_id}: {order}")

    return order


def delete_order(order_id):
    try:
        response = requests.delete(
            f"{BASE_URL}/orders/{order_id}",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Delete order {order_id} failed: {e}")
        return False

    print(f"Deleted order {order_id}")

    return True


def write_seat_csv(orders):
    with open(
        "submissions/chettuprasanna/seat.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "seat",
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
                "seat": order["seat"],
                "id": order["id"],
                "drink": order["drink"],
                "size": order["size"],
                "sugar": order["sugar"],
                "name": order["name"],
                "status": order["status"]
            })


# STEP 0 — Clear our seat

clear_seat()


 STEP 1 — Anita orders a latte

anita = create_order(
    "latte",
    "medium",
    2,
    "Anita"
)

if anita:
    anita_id = anita["id"]

    update_order(
        anita_id,
        {"status": "brewing"}
    )

    update_order(
        anita_id,
        {"status": "ready"}
    )


 STEP 2 — Bharat changes his order completely

bharat = create_order(
    "espresso",
    "small",
    3,
    "Bharat"
)

if bharat:
    bharat_id = bharat["id"]

    update_order(
        bharat_id,
        {
            "drink": "mocha",
            "size": "large",
            "name": "Chandni",
            "status": "pending"
        }
    )


 STEP 3 — Dev walks out

dev = create_order(
    "americano",
    "large",
    0,
    "Dev"
)

if dev:
    dev_id = dev["id"]

    delete_order(dev_id)


# STEP 4 — Get final orders and write seat.csv

final_orders = get_seat_orders()

print(f"Final orders on {SEAT}: {len(final_orders)}")

write_seat_csv(final_orders)

print("Created seat.csv")
