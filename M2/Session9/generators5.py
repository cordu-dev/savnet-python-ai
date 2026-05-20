def coffee_orders():
    orders = ["Espresso", "Cappuccino", "Latte", "Tea"]

    for order in orders:
        yield order
        print(f"Barista finished the order: {order}")


for order in coffee_orders():
    print(f"Customer receives: {order}")

print("-" * 20)

orders_generator = coffee_orders()

print(orders_generator)
print(next(orders_generator))
print(next(orders_generator))
