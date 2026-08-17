import csv
import requests

BASE_URL = "https://api.studiotypo.xyz"
SEAT = "seat-09"


def fetch_all_orders():
    """/book is paginated — 'total' can be bigger than the 'orders' list
    returned in a single page. Keep paging with offset until we've
    collected as many orders as 'total' says exist."""
    orders = []
    offset = 0
    total = None

    while True:
        try:
            r = requests.get(
                f"{BASE_URL}/book",
                params={"limit": 50, "offset": offset},
                timeout=10,
            )
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
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

    if total is not None and len(orders) != total:
        print(f"Warning: expected {total} orders but only collected {len(orders)}.")

    return orders


def write_csv(orders):
    with open("orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "drink", "size", "sugar", "name", "status"])
        for o in orders:
            writer.writerow([o["id"], o["drink"], o["size"], o["sugar"], o["name"], o["status"]])


def summarize(orders):
    total_orders = len(orders)
    ready_orders = sum(1 for o in orders if o["status"] == "ready")

    drink_counts = {}
    for o in orders:
        drink_counts[o["drink"]] = drink_counts.get(o["drink"], 0) + 1
    top_drink, top_count = max(drink_counts.items(), key=lambda kv: kv[1])

    return total_orders, ready_orders, top_drink, top_count


def main():
    orders = fetch_all_orders()
    write_csv(orders)

    total_orders, ready_orders, top_drink, top_count = summarize(orders)

    print(f"Total orders: {total_orders}")
    print(f"Ready orders: {ready_orders}")
    print(f"Most ordered drink: {top_drink} ({top_count} times)")

    with open("ANSWERS.md", "w") as f:
        f.write("# Week 2 assignment — answers\n\n")
        f.write(f"**Seat:** {SEAT}\n\n")
        f.write("## Part 1 — order book\n\n")
        f.write(f"- Total orders in the book: {total_orders}\n")
        f.write(f"- Orders with status 'ready': {ready_orders}\n")
        f.write(f"- Most ordered drink: {top_drink} ({top_count} times)\n\n")
        f.write("## What surprised me\n\n")
        f.write(
            "The /book endpoint is paginated — it only returns 50 orders per "
            "call even though `total` says 100, so book_report.py has to page "
            "through it with `offset` until it's collected all of them.\n"
        )


if __name__ == "__main__":
    main()