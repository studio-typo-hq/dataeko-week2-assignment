import csv
import requests

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-09"
HEADERS = {"X-API-Key": "dataeko-2026", "Content-Type": "application/json"}


def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=10, **kwargs)
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None


def get_seat_orders():
    """/orders is a shared, live board across every seat. The ?seat= query
    param does NOT actually filter server-side (its 'filters' field comes
    back empty), so we fetch everything — paginating in case the board
    grows past one page — and filter down to our own seat ourselves."""
    orders = []
    offset = 0
    total = None

    while True:
        r = safe_request(
            "GET",
            f"{BASE_URL}/orders",
            headers=HEADERS,
            params={"limit": 50, "offset": offset},
        )
        if r is None:
            break
        data = r.json()
        total = data.get("total")
        page = data.get("orders", [])
        orders.extend(page)

        if not page:
            break
        offset += len(page)
        if total is not None and offset >= total:
            break

    return [o for o in orders if o.get("seat") == SEAT]


def clear_seat():
    for order in get_seat_orders():
        r = safe_request("DELETE", f"{BASE_URL}/orders/{order['id']}", headers=HEADERS)
        if r is not None:
            print(f"Cleared order {order['id']}: {r.status_code}")


def create_order(drink, size, sugar, name):
    payload = {"drink": drink, "size": size, "sugar": sugar, "name": name, "seat": SEAT}
    r = safe_request("POST", f"{BASE_URL}/orders", headers=HEADERS, json=payload)
    if r is None:
        return None
    body = r.json()
    print(f"Created order: {r.status_code} -> {body}")
    return body.get("id")


def patch_order(order_id, payload):
    r = safe_request("PATCH", f"{BASE_URL}/orders/{order_id}", headers=HEADERS, json=payload)
    if r is not None:
        print(f"Patched order {order_id}: {r.status_code}")


def delete_order(order_id):
    r = safe_request("DELETE", f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
    if r is not None:
        print(f"Deleted order {order_id}: {r.status_code}")


def write_seat_csv():
    orders = get_seat_orders()
    with open("seat.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seat", "id", "drink", "size", "sugar", "name", "status"])
        for o in orders:
            writer.writerow([SEAT, o["id"], o["drink"], o["size"], o["sugar"], o["name"], o["status"]])
    return orders


def main():
    # Step 0 — clear the seat first so this script is safe to run twice
    clear_seat()

    # Step 1 — Anita orders a latte, and we make it
    anita_id = create_order("latte", "medium", 2, "Anita")
    if anita_id is not None:
        patch_order(anita_id, {"status": "brewing"})
        patch_order(anita_id, {"status": "ready"})

    # Step 2 — Bharat orders an espresso, then changes their mind completely
    # before it's started. Sugar wasn't respecified, so it's left as-is —
    # only the fields that actually changed are patched.
    bharat_id = create_order("espresso", "small", 3, "Bharat")
    if bharat_id is not None:
        patch_order(bharat_id, {"drink": "mocha", "size": "large", "name": "Chandni"})

    # Step 3 — Dev orders an americano, then walks out before it's made
    dev_id = create_order("americano", "large", 0, "Dev")
    if dev_id is not None:
        delete_order(dev_id)

    # Step 4 — record where we ended up
    orders = write_seat_csv()
    print(f"Seat {SEAT} ends with {len(orders)} order(s) — expected 2.")


if __name__ == "__main__":
    main()