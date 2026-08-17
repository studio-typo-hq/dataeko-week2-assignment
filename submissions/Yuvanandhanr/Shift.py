import requests
import csv

BASE_URL = "https://api.studiotypo.xyz" 
MY_SEAT = "seat-11" 

headers = {
    "X-API-Key": "dataeko-2026",
    "Content-Type": "application/json"
}

def safe_request(method, url, **kwargs):
    """A helper function to satisfy the try/except requirement and avoid crashing."""
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status() 
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if response is not None:
            print("Hint from API:", response.text)
        return None


print("Step 0: Clearing seat...")
seat_orders_url = f"{BASE_URL}/orders?seat={MY_SEAT}" 
response = safe_request("GET", seat_orders_url)
if response:
    for order in response.json().get('orders', []): # Adjust 'orders' based on actual API response
        safe_request("DELETE", f"{BASE_URL}/orders/{order['id']}", headers=headers)

print("Step 1: Anita's Latte...")
payload_1 = {"drink": "latte", "size": "medium", "sugar": 2, "name": "Anita", "seat": MY_SEAT}
res_1 = safe_request("POST", f"{BASE_URL}/orders", json=payload_1, headers=headers)
if res_1:
    order_id = res_1.json()['id']
    safe_request("PATCH", f"{BASE_URL}/orders/{order_id}", json={"status": "brewing"}, headers=headers)
    safe_request("PATCH", f"{BASE_URL}/orders/{order_id}", json={"status": "ready"}, headers=headers)

print("Step 2: Bharat -> Chandni...")
payload_2 = {"drink": "espresso", "size": "small", "sugar": 3, "name": "Bharat", "seat": MY_SEAT}
res_2 = safe_request("POST", f"{BASE_URL}/orders", json=payload_2, headers=headers)
if res_2:
    order_id = res_2.json()['id']
    new_payload = {"drink": "mocha", "size": "large", "sugar": 0, "name": "Chandni", "seat": MY_SEAT}
    safe_request("PUT", f"{BASE_URL}/orders/{order_id}", json=new_payload, headers=headers)

print("Step 3: Dev walks out...")
payload_3 = {"drink": "americano", "size": "large", "sugar": 0, "name": "Dev", "seat": MY_SEAT}
res_3 = safe_request("POST", f"{BASE_URL}/orders", json=payload_3, headers=headers)
if res_3:
    order_id = res_3.json()['id']
    safe_request("DELETE", f"{BASE_URL}/orders/{order_id}", headers=headers)

print("Step 4: Writing seat.csv...")
final_orders_res = safe_request("GET", seat_orders_url)
if final_orders_res:
    final_orders = final_orders_res.json().get('orders', [])
    with open('seat.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['seat', 'id', 'drink', 'size', 'sugar', 'name', 'status'])
        writer.writeheader()
        for order in final_orders:
            writer.writerow({
                'seat': MY_SEAT,
                'id': order.get('id'),
                'drink': order.get('drink'),
                'size': order.get('size'),
                'sugar': order.get('sugar'),
                'name': order.get('name'),
                'status': order.get('status')
            })
print("Shift complete!")