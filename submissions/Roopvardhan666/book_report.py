import csv
from collections import Counter
import requests

BASE_URL = "https://api.studiotypo.xyz"


def generate_book_report():
  try:
    # Pass limit=100 to fetch the full order book
    response = requests.get(
        f"{BASE_URL}/book", params={"limit": 100}, timeout=10
    )
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Network error while fetching order book: {e}")
    return

  data = response.json()
  orders = data.get("orders", [])
  total_orders = len(orders)

  # 1. Count orders with status "ready"
  ready_count = sum(1 for order in orders if order.get("status") == "ready")

  # 2. Find most frequently ordered drink
  drinks = [order.get("drink") for order in orders if order.get("drink")]
  drink_counts = Counter(drinks)
  most_common_drink, most_common_count = drink_counts.most_common(1)[0]

  # 3. Print the required metrics
  print("=== BOOK REPORT ===")
  print(f"Total orders in book: {total_orders}")
  print(f"Orders with status 'ready': {ready_count}")
  print(f"Most ordered drink: {most_common_drink} ({most_common_count} times)")

  # 4. Write records to orders.csv
  fieldnames = ["id", "drink", "size", "sugar", "name", "status"]
  with open("orders.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for order in orders:
      row = {field: order.get(field, "") for field in fieldnames}
      writer.writerow(row)

  print(f"\nSuccessfully exported {total_orders} orders to orders.csv")


if __name__ == "__main__":
  generate_book_report()
