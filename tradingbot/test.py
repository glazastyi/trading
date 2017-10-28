import support
import database
import config
import time
def get_successful_orders(orders):
    return_orders = [[],[]]
    for order in orders:
        type_of_order = order[:1]
        order_num = order[1:-1]
        info = support.get_data("/exchange/order", [("orderId", order_num)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])
        if quantity > 0.0:
            return_orders[type_of_order == "S"].append(order_num)
    return return_orders

def close_sell_orders(orders):
    for order in orders:
        info = support.get_data("/exchange/order", [("orderId", order[1:-1])])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])


        cond = float(info["price"]) / config.INCOME

        update_list = database.select(
            ["id", "purchased_quantity", "sold_quantity", "profit"],
            ["symbol == ", "purchase_price <= ", "result == "],
            ("'%s'" % symbol, cond, 0))

        print "here", update_list
        for el in update_list:
            balance = float(el[1]) - float(el[2])
            profit = float(el[3])
            print quantity, float(el[2]), profit, price
            if balance > quantity:
                database.update(["sold_quantity", "profit"],
                                (float(el[2]) + quantity,
                                 profit + quantity * price),
                                ["id == "], (el[0],))
            else:
                quantity -= balance
                database.update(
                    ["sold_quantity", "profit", "end_time", "result"],
                    (float(el[1]), profit + quantity * price, time.time(), 1),
                    ["id == "], (el[0],))

def close_buy_orders(orders):
    for order in orders:
        info = support.get_data("/exchange/order", [("orderId", order[1:-1])])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])
        database.insert(order[1:-1], time.time(), symbol, quantity, price)

def close_orders():
    with open("orders_buffer.txt", "r") as file:
        orders = file.readlines()

    successful_orders = get_successful_orders(orders)
    close_buy_orders(successful_orders[0])
    close_sell_orders(successful_orders[1])
