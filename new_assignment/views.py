from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
"""
Task 1: Basic Bill Splitting
Create an endpoint to split a bill evenly among a group of users.

Endpoint: /split-evenly
Method: POST
Input: List of user IDs and total bill amount.
Output: Amount each user needs to pay.
"""
@csrf_exempt
def evenly_split(request):
    if request.method == "POST":
        data = json.loads(request.body)
        total = data.get('total') # Take int data
        peoples = data.get('peoples') # take num for length of peoples
        each_person_charges = int(total) / int(peoples)
        return JsonResponse({"Each Person Charges": each_person_charges})
# Example Json Body:
# {
#     "total": 1200,
#     "peoples": 15
# }
"""
Task 2: Uneven Bill Splitting
Create an endpoint to split a bill unevenly based on individual contributions.

Endpoint: /split-unevenly
Method: POST
Input: List of user IDs, their respective contributions, and the total bill amount. 
Output: Amount each user needs to pay or receive.
"""

@csrf_exempt
def split_unevenly(request):
    if request.method == "POST":
        # Parse the incoming JSON data
        data = json.loads(request.body)
        total_bill = data.get('total_bill')
        contributions = data.get('contributions')

        # Calculate the total contributions and number of users
        num_people = len(contributions)

        # Calculate each user's share of the bill
        result = {}
        for user_id, contribution in contributions.items():
            # Calculate how much each user owes or gets back
            difference = (int(total_bill) / int(num_people)) - contribution
            print(difference)
            result[user_id] = difference

        # Return the result as a JSON response
        return JsonResponse(result)

# Example Json Body Code:
# {
#     "total_bill": 120,
#     "contributions": {
#         "John": 50,
#         "Max": 30,
#         "Ellen": 40
#     }
# }
"""
Task 3: Including Tip and Tax
Create an endpoint to split a bill including tip and tax evenly among users.

Endpoint: /split-including-tip-tax
Method: POST
Input: List of user IDs, total bill amount, tip percentage, and tax percentage.
Output: Amount each user needs to pay including tip and tax.
"""
import json

# Function to calculate tip
def calculate_tip(price):
    return price * 0.05

# Function to calculate tax
def calculate_tax(price):
    return price * 0.10

# API view to calculate total price including tip and tax
@csrf_exempt  # Disable CSRF for testing via tools like Thunder Client/Postman
def add_tip_and_tax(request):
    if request.method == 'POST':

        data = json.loads(request.body)  # Parse JSON request body
        price = data.get('price')  # Get 'price' from the request
            
        tip = calculate_tip(price)
        tax = calculate_tax(price)
        total_price = price + tip + tax
        
        return JsonResponse({"total_price": total_price}) 
# Example Json Body Code: 
# {
#   "price": 100
# }

"""
Task 4: Handling Discounts
Create an endpoint to apply a discount to the total bill before splitting it evenly among users.

Endpoint: /split-with-discount
Method: POST
Input: List of user IDs, total bill amount, and discount percentage.
Output: Amount each user needs to pay after discount.
"""
def calculate_discount(price):
    return price * 0.20

@csrf_exempt
def add_discount_and_split(request):
    if request.method == "POST":
        # Parse the incoming JSON data
        data = json.loads(request.body)
        price = data.get('price')  # Get 'price' from the request
        users = data.get('users')   # Write the num of person in integer
        total = price - calculate_discount(price) 
        user_costs = total / users
        return JsonResponse({"total_per_user": user_costs})
# Example code json body:
# {
#   "price":8500,
#   "users":5
# }


"""
Task 5: Advanced Bill Splitting with Shared Items
Create an endpoint to split a bill where some items are shared among certain users.

Endpoint: /split-with-shared-items
Method: POST
Input: List of user IDs, list of items with prices, and list of user IDs for each shared item.
Output: Amount each user needs to pay.
"""
@csrf_exempt
def split_with_shared_items(request):
    if request.method == "POST":
        # Parse the incoming JSON data
        data = json.loads(request.body)
        items = data.get('items', [])

        # Initialize a dictionary to store the total cost for each user
        user_costs = {}

        # Loop through each item to calculate cost per user
        for item in items:
            price = item.get('item_price', 0)
            users_sharing = item.get('share_with', [])
            share_per_user = price / len(users_sharing) if users_sharing else 0

            # Distribute the cost to each user
            for user in users_sharing:
                if user not in user_costs:
                    user_costs[user] = 0
                user_costs[user] += share_per_user

        # Return the result as a JSON response
        return JsonResponse({"total_per_user": user_costs})

# {
#   "user_ids": ["user1", "user2", "user3", "user4"],
#   "items": [
#     {
#       "item_name": "Pizza",
#       "item_price": 1500,
#       "share_with": ["user1", "user2", "user3"]
#     },
#     {
#       "item_name": "Pasta",
#       "item_price": 1500,
#       "share_with": ["user2", "user4"]
#     },
#     {
#       "item_name": "Drinks",
#       "item_price": 300,
#       "share_with": ["user1", "user3", "user4"]
#     }
#   ]
# }
