import requests
import csv
from collections import Counter

# 1. Fetch the data
url = "https://api.studiotypo.xyz/book"
all_orders = []

while url:
    print(f"Fetching from: {url}")
    response = requests.get(url, timeout=10) # Remember the timeout!
    data = response.json()
    
    # Assuming the API returns something like: {"orders": [...], "next": "url_for_next_page"}
    # You MUST print(data) on your first run to see exactly what the keys are!
    # Update 'orders' and 'next' based on what you actually see in the JSON.
    all_orders.extend(data.get('orders', []))
    
    # Update the url to the next page. If it doesn't exist, this becomes None and the loop breaks.
    url = data.get('next') 

# 2. Write to CSV
with open('orders.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'drink', 'size', 'sugar', 'name', 'status'])
    writer.writeheader()
    for order in all_orders:
        # We only want to write these specific fields.
        writer.writerow({
            'id': order.get('id'),
            'drink': order.get('drink'),
            'size': order.get('size'),
            'sugar': order.get('sugar'),
            'name': order.get('name'),
            'status': order.get('status')
        })

# 3. Calculate the three numbers
total_orders = len(all_orders)
ready_orders = sum(1 for order in all_orders if order.get('status') == 'ready')

# Count drinks to find the most popular
drinks = [order.get('drink') for order in all_orders]
most_common_drink, drink_count = Counter(drinks).most_common(1)[0]

print(f"Total orders: {total_orders}")
print(f"Ready orders: {ready_orders}")
print(f"Most ordered drink: {most_common_drink} ({drink_count} times)")