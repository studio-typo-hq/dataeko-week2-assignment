import requests
import csv

BASE_URL = "https://api.studiotypo.xyz"
API_KEY = "dataeko-2026"
SEAT = "seat-02"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def get_seat_orders():
    response = requests.get(
        f"{BASE_URL}/orders",
        params={"seat": SEAT},
        timeout=10
    )

    if not response.ok:
        print("GET failed:")
        print(response.text)
        response.raise_for_status()

    return response.json()["orders"]


def delete_order(order_id):
    response = requests.delete(
        f"{BASE_URL}/orders/{order_id}",
        headers=HEADERS,
        timeout=10
    )

    if not response.ok:
        print(f"DELETE failed for order {order_id}:")
        print(response.text)
        response.raise_for_status()

    print(f"Deleted order {order_id}")


def create_order(drink, size, sugar, name):
    data = {
        "drink": drink,
        "size": size,
        "sugar": sugar,
        "name": name,
        "seat": SEAT
    }

    response = requests.post(
        f"{BASE_URL}/orders",
        headers=HEADERS,
        json=data,
        timeout=10
    )

    if not response.ok:
        print("POST failed:")
        print(response.text)
        response.raise_for_status()

    order = response.json()
    print(f"Created order {order['id']}")
    return order


def update_order(order_id, data):
    response = requests.patch(
        f"{BASE_URL}/orders/{order_id}",
        headers=HEADERS,
        json=data,
        timeout=10
    )

    if not response.ok:
        print(f"PATCH failed for order {order_id}:")
        print(response.text)
        response.raise_for_status()

    order = response.json()
    print(f"Updated order {order_id}")
    return order


try:
    # Step 0 — clear seat-02
    print("Step 0: Clearing seat-02")

    existing_orders = get_seat_orders()

    for order in existing_orders:
        delete_order(order["id"])

    # Step 1 — Anita orders a latte
    print("\nStep 1: Anita's latte")

    anita = create_order(
        drink="latte",
        size="medium",
        sugar=2,
        name="Anita"
    )

    anita_id = anita["id"]

    update_order(
        anita_id,
        {"status": "brewing"}
    )

    update_order(
        anita_id,
        {"status": "ready"}
    )

    # Step 2 — Bharat changes his mind
    print("\nStep 2: Bharat's order")

    bharat = create_order(
        drink="espresso",
        size="small",
        sugar=3,
        name="Bharat"
    )

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

    # Step 3 — Dev walks out
    print("\nStep 3: Dev's order")

    dev = create_order(
        drink="americano",
        size="large",
        sugar=0,
        name="Dev"
    )

    delete_order(dev["id"])

    # Step 4 — write final state to seat.csv
    print("\nStep 4: Final seat state")

    final_orders = get_seat_orders()

    with open("seat.csv", "w", newline="") as file:
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

        for order in final_orders:
            writer.writerow({
                "seat": order["seat"],
                "id": order["id"],
                "drink": order["drink"],
                "size": order["size"],
                "sugar": order["sugar"],
                "name": order["name"],
                "status": order["status"]
            })

    print(f"\nFinal orders on {SEAT}: {len(final_orders)}")

    for order in final_orders:
        print(
            order["id"],
            order["drink"],
            order["size"],
            order["sugar"],
            order["name"],
            order["status"]
        )

    if len(final_orders) != 2:
        raise RuntimeError(
            f"Expected exactly 2 orders, but found {len(final_orders)}"
        )

    print("\nSUCCESS: seat-02 has exactly 2 orders.")

except requests.exceptions.RequestException as error:
    print("\nAPI request failed:")
    print(error)
