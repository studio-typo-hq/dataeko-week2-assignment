import requests
import csv
seat = "seat-07"
def get_seat_orders():
    try:
        response = requests.get(
            f"https://api.studiotypo.xyz/orders",
            params={"seat": seat},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print("API RESPONSE:")
        print(data)
        return data["orders"]

    except requests.exceptions.RequestException as error:
        print(f"Could not get seat orders: {error}")
        return None

def delete_order(order_id):
    try:
        response = requests.delete(
            f"https://api.studiotypo.xyz/orders/{order_id}",
            headers = {"X-API-Key": "dataeko-2026"},
            timeout = 10
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print(f"Can not delete ordeer {order_id} : {error}")

def create_order(drink, size, sugar, name):
    try:
        response = requests.post(
            f"https://api.studiotypo.xyz/orders",
            json={
                "drink": drink,
                "size": size,
                "sugar": sugar,
                "name": name,
                "seat": seat
            },
            headers={"X-API-Key": "dataeko-2026"},
            timeout=10
        )
        response.raise_for_status()
        order = response.json()
        print(f"Created order {order['id']}")
        return order

    except requests.exceptions.RequestException as error:
        print(f"Could not create order: {error}")
        return None

def update_order(order_id, updates):
    try:
        response = requests.patch(
            f"https://api.studiotypo.xyz/orders/{order_id}",
            json=updates,
            headers={"X-API-Key": "dataeko-2026"},
            timeout=10
        )

        response.raise_for_status()
        print(f"Updated order {order_id}")
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Could not update order {order_id}: {error}")
        return None

def write_seat_csv(orders):
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


def main():

    orders = get_seat_orders()
    if orders is None:
        return

    for order in orders:
        delete_order(order["id"])

    # Anita orders latte
    order = create_order(
        "latte",
        "medium",
        2,
        "Anita"
    )
    if order is None:
        return
    
    order_id = order["id"]
    update_order(
        order_id,
        {"status": "brewing"}
    )
    update_order(
        order_id,
        {"status": "ready"}
    )

    # Bharat changes the order
    order = create_order(
        "espresso",
        "small",
        3,
        "Bharat"
    )
    if order is None:
        return

    order_id = order["id"]

    update_order(
        order_id,
        {
            "drink": "mocha",
            "size": "large",
            "sugar": 3,
            "name": "Chandni",
            "status": "pending"
        }
    )

    # Dev walks out
    order = create_order(
        "americano",
        "large",
        0,
        "Dev"
    )
    if order is None:
        return
    
    delete_order(order["id"])

    # Save final seat state
    orders = get_seat_orders()
    if orders is None:
        return

    write_seat_csv(orders)
    print(f"Final orders on {seat}: {len(orders)}")


if __name__ == "__main__":
    main()