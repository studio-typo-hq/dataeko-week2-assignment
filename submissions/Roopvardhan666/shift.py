import csv
import requests

BASE_URL = "https://api.studiotypo.xyz"
MY_SEAT = "seat-08"

HEADERS = {
    "X-API-Key": "dataeko-2026",
    "Content-Type": "application/json",
}


def clear_seat():
  """Step 0: Clear all existing orders for seat-08 to ensure idempotency."""
  print(f"--- Step 0: Clearing existing orders for {MY_SEAT} ---")
  try:
    res = requests.get(f"{BASE_URL}/orders?seat={MY_SEAT}", timeout=10)
    res.raise_for_status()
    data = res.json()
    orders = data if isinstance(data, list) else data.get("orders", [])

    for order in orders:
      order_id = order["id"]
      del_res = requests.delete(
          f"{BASE_URL}/orders/{order_id}", headers=HEADERS, timeout=10
      )
      del_res.raise_for_status()
      print(f"  Deleted leftover order ID: {order_id}")

    print(f"Cleared {len(orders)} previous order(s).\n")
  except requests.exceptions.RequestException as e:
    print(f"Error during seat cleanup: {e}")
    raise


def work_shift():
  # Start clean
  clear_seat()

  try:
    # -------------------------------------------------------------
    # Step 1: Anita orders a Latte -> brewing -> ready
    # -------------------------------------------------------------
    print("--- Step 1: Anita's Order ---")
    anita_payload = {
        "drink": "latte",
        "size": "medium",
        "sugar": 2,
        "name": "Anita",
        "seat": MY_SEAT,
    }
    res_1 = requests.post(
        f"{BASE_URL}/orders",
        json=anita_payload,
        headers=HEADERS,
        timeout=10,
    )
    res_1.raise_for_status()
    order_1_id = res_1.json().get("id") or res_1.json().get("order", {}).get(
        "id"
    )
    print(f"  Created Anita's order (ID: {order_1_id})")

    # Update to brewing
    requests.patch(
        f"{BASE_URL}/orders/{order_1_id}",
        json={"status": "brewing"},
        headers=HEADERS,
        timeout=10,
    ).raise_for_status()
    print("  Status updated -> brewing")

    # Update to ready
    requests.patch(
        f"{BASE_URL}/orders/{order_1_id}",
        json={"status": "ready"},
        headers=HEADERS,
        timeout=10,
    ).raise_for_status()
    print("  Status updated -> ready\n")

    # -------------------------------------------------------------
    # Step 2: Bharat orders Espresso -> Changes mind to Chandni's Large Mocha
    # -------------------------------------------------------------
    print("--- Step 2: Bharat -> Chandni Mind Change ---")
    bharat_payload = {
        "drink": "espresso",
        "size": "small",
        "sugar": 3,
        "name": "Bharat",
        "seat": MY_SEAT,
    }
    res_2 = requests.post(
        f"{BASE_URL}/orders",
        json=bharat_payload,
        headers=HEADERS,
        timeout=10,
    )
    res_2.raise_for_status()
    order_2_id = res_2.json().get("id") or res_2.json().get("order", {}).get(
        "id"
    )
    print(f"  Created initial order for Bharat (ID: {order_2_id})")

    # Update the same order ID to Chandni's large mocha
    chandni_update = {
        "drink": "mocha",
        "size": "large",
        "sugar": 0,
        "name": "Chandni",
    }
    requests.patch(
        f"{BASE_URL}/orders/{order_2_id}",
        json=chandni_update,
        headers=HEADERS,
        timeout=10,
    ).raise_for_status()
    print(
        f"  Order ID {order_2_id} mutated to large mocha under name 'Chandni'\n"
    )

    # -------------------------------------------------------------
    # Step 3: Dev orders Americano -> Walks out (Delete)
    # -------------------------------------------------------------
    print("--- Step 3: Dev Orders and Leaves ---")
    dev_payload = {
        "drink": "americano",
        "size": "large",
        "sugar": 0,
        "name": "Dev",
        "seat": MY_SEAT,
    }
    res_3 = requests.post(
        f"{BASE_URL}/orders", json=dev_payload, headers=HEADERS, timeout=10
    )
    res_3.raise_for_status()
    order_3_id = res_3.json().get("id") or res_3.json().get("order", {}).get(
        "id"
    )
    print(f"  Created Dev's order (ID: {order_3_id})")

    # Delete order
    requests.delete(
        f"{BASE_URL}/orders/{order_3_id}", headers=HEADERS, timeout=10
    ).raise_for_status()
    print(f"  Deleted Dev's order (ID: {order_3_id})\n")

    # -------------------------------------------------------------
    # Step 4: Record final seat state to seat.csv
    # -------------------------------------------------------------
    print(f"--- Step 4: Exporting Final Seat State for {MY_SEAT} ---")
    final_res = requests.get(f"{BASE_URL}/orders?seat={MY_SEAT}", timeout=10)
    final_res.raise_for_status()
    final_data = final_res.json()
    final_orders = (
        final_data
        if isinstance(final_data, list)
        else final_data.get("orders", [])
    )

    print(f"Total orders remaining on {MY_SEAT}: {len(final_orders)}")

    # Write seat.csv with 'seat' at the front
    fieldnames = ["seat", "id", "drink", "size", "sugar", "name", "status"]
    with open("seat.csv", mode="w", newline="", encoding="utf-8") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for order in final_orders:
        row = {
            "seat": order.get("seat", MY_SEAT),
            "id": order.get("id", ""),
            "drink": order.get("drink", ""),
            "size": order.get("size", ""),
            "sugar": order.get("sugar", ""),
            "name": order.get("name", ""),
            "status": order.get("status", ""),
        }
        writer.writerow(row)

    print("Saved seat.csv successfully.")

  except requests.exceptions.RequestException as e:
    print(f"\n[ERROR] An API error occurred: {e}")
    if hasattr(e, "response") and e.response is not None:
      print(f"HTTP Status: {e.response.status_code}")
      print(f"Server Message: {e.response.text}")


if __name__ == "__main__":
  work_shift()
