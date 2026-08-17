import requests
import csv

API_URL = "https://api.studiotypo.xyz"
API_KEY = "dataeko-2026"
SEAT = "seat-10"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def get_seat_orders():
    response = requests.get(
        f"{API_URL}/orders?seat={SEAT}",
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    return data["orders"]


def delete_order(order_id):
    response = requests.delete(
        f"{API_URL}/orders/{order_id}",
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()


def create_order(drink, size, sugar, name):
    payload = {
        "drink": drink,
        "size": size,
        "sugar": sugar,
        "name": name,
        "seat": SEAT
    }

    response = requests.post(
        f"{API_URL}/orders",
        headers=HEADERS,
        json=payload,
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def update_order(order_id, updates):
    response = requests.patch(
        f"{API_URL}/orders/{order_id}",
        headers=HEADERS,
        json=updates,
        timeout=10
    )
    response.raise_for_status()

    return response.json()


try:
    # --------------------------------------------------
    # Step 0 — Clear the seat
    # --------------------------------------------------
    print(f"Clearing {SEAT}...")

    existing_orders = get_seat_orders()

    for order in existing_orders:
        delete_order(order["id"])
        print(f"Deleted order {order['id']}")

    # --------------------------------------------------
    # Step 1 — Anita
    # --------------------------------------------------
    print("Creating Anita's order...")

    anita = create_order(
        drink="latte",
        size="medium",
        sugar=2,
        name="Anita"
    )

    anita_id = anita["id"]

    update_order(anita_id, {"status": "brewing"})
    update_order(anita_id, {"status": "ready"})

    print(f"Anita's order {anita_id} is ready.")

    # --------------------------------------------------
    # Step 2 — Bharat changes to Chandni's order
    # --------------------------------------------------
    print("Creating Bharat's order...")

    bharat = create_order(
        drink="espresso",
        size="small",
        sugar=3,
        name="Bharat"
    )

    bharat_id = bharat["id"]

    print(f"Changing order {bharat_id} to Chandni's order...")

    update_order(
        bharat_id,
        {
            "drink": "mocha",
            "size": "large",
            "name": "Chandni",
            "status": "pending"
        }
    )

    # --------------------------------------------------
    # Step 3 — Dev walks out
    # --------------------------------------------------
    print("Creating Dev's order...")

    dev = create_order(
        drink="americano",
        size="large",
        sugar=0,
        name="Dev"
    )

    dev_id = dev["id"]

    print(f"Deleting Dev's order {dev_id}...")
    delete_order(dev_id)

    # --------------------------------------------------
    # Step 4 — Get final seat state
    # --------------------------------------------------
    final_orders = get_seat_orders()

    # --------------------------------------------------
    # Write seat.csv
    # --------------------------------------------------
    with open("seat.csv", "w", newline="") as csvfile:
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
            csvfile,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()

        for order in final_orders:
            order["seat"] = SEAT
            writer.writerow(order)

    print()
    print("Final orders:", len(final_orders))

    for order in final_orders:
        print(
            order["id"],
            order["drink"],
            order["size"],
            order["sugar"],
            order["name"],
            order["status"]
        )

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    print("Response:", getattr(e.response, "text", "No response body"))
