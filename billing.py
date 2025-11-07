#-----------------------BACKEND CODE-------------------------

import csv
import mysql.connector as mys
from datetime import datetime
import discounts
import os


#SERVER CONNECTION -----------------------------
def set_up():
    mycon = mys.connect(host="localhost", user="root", passwd="1234")
    mycursor = mycon.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS company")
    mycon.close()
    mycon = mys.connect(host="localhost", user="root", passwd="1234", database="company")
    mycursor = mycon.cursor()
    mycursor.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(10) NOT NULL,
        product_name VARCHAR(50),
        product_price DECIMAL,
        PRIMARY KEY(product_id)
    )''')
    mycon.close()

# Create all_bills.csv if it doesn’t exist
if not os.path.exists("all_bills.csv"):
    with open("all_bills.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Bill File", "Date", "Time", "Sr. No.", "Product Name", "Quantity", "Price"])


def edit_bill(bill_name, info, op):
    global current_date, current_time   
    
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    with open(bill_name, mode='a') as bill:
        wo = csv.writer(bill)
        if op == 0:
            wo.writerow(info)
            with open("all_bills.csv", mode='a', newline='') as allbills:
                writer = csv.writer(allbills)
                writer.writerow([bill_name, current_date, current_time] + info)
        elif op == 1:
            date = info[0]
            time = info[1]
            wo.writerow(["Date:", " ", date, " "])
            wo.writerow(["Time:", " ", time, " "])
            wo.writerow([" ", " ", " ", " "])
            wo.writerow(["Sr. no.", "product name", "quantity", "price"])
        elif op == 2:
            Amount, total, payment_method = info
            wo.writerow([" ", " ", " ", " "])
            wo.writerow(["Total:", " ", Amount, " "])
            wo.writerow(["After Discount:", " ", total, " "])
            wo.writerow(["Payment Method:", " ", payment_method, " "])



def get(mycon, mycursor, product_id):
    query = "SELECT * FROM products WHERE product_id='{}'".format(product_id)
    mycursor.execute(query)
    data = mycursor.fetchone()
    return data if data else " "

#Main Bill Generator Function-----------------
def billing(mycon, mycursor):
    global current_date, current_time
    t = str(datetime.today())
    bill_name = t[:10] + "_" + t[11:13] + "-" + t[14:16] + "-" + t[17:19] + ".csv"
    f = t[:19]
    l = f.split()
    edit_bill(bill_name, l, 1)
    sr_no = 1
    amount = 0
    while True:
        product_id = input("Enter Product ID: ")
        data = get(mycon, mycursor, product_id)
        if data == " ":
            print("Product not in database")
        else:
            product_name = data[1]
            print(product_name)
            quantity = float(input("Enter quantity: "))
            product_price = data[2]
            total_price = float(product_price) * quantity
            print("Price =", total_price)
            bill_record = [sr_no, product_name, quantity, total_price]
            edit_bill(bill_name, bill_record, 0)
            amount += total_price
            sr_no += 1
        o = input('''Press any key to bill more products
Enter 0 to end billing''')
        if o == '0':
            break
        
    membership = input("Enter membership level:").lower()
    amount = discounts.get_discounted_price(membership, amount)

    global payment_method
    payment_method = input("Enter payment method (Cash/Card/UPI): ").upper()

    print("Total=", amount)
    edit_bill(bill_name, [amount, payment_method], 2)

#Add product function----------------------
def enter_product(mycon, mycursor):
    while True:
        product_id = input("Enter Product ID: ")
        data = get(mycon, mycursor, product_id)
        if data != " ":
            print("Product already in database")
            continue
        else:
            break
    product_name = input("Enter product name: ")
    
    while True:
        product_price = input("Enter product price: ")
        if product_price:
            try:
                product_price = float(product_price) 
                break
            except:
                print("Invalid price. Please enter a numeric value.")
        else:
            print("Product price cannot be empty")
    query = "INSERT INTO products (product_id, product_name, product_price) VALUES ('{}', '{}', {})".format(product_id, product_name, product_price)
    mycursor.execute(query)
    mycon.commit()
    print("New product saved")

def show_inventory(mycursor):
    mycursor.execute("SELECT * FROM products")
    data = mycursor.fetchall()
    print("\nCurrent Inventory:")
    print("-"*50)
    for row in data:
        print(f"ID: {row[0]} | Name: {row[1]} | Price: ₹{row[2]}")
    print("-"*50)


def update_price(mycon, mycursor):
    while True:
        product_id = input("Enter Product ID: ")
        data = get(mycon, mycursor, product_id)
        if data == " ":
            print("Product not in database")
        else:
            break
    product_price = float(input("Enter new product price: "))
    query = "UPDATE products SET product_price={} WHERE product_id='{}'".format(product_price, product_id)
    mycursor.execute(query)
    mycon.commit()
    print("Product price updated")


if __name__ == "__main__":
    set_up()

    mycon = mys.connect(host="localhost", user="root", passwd="1234", database="company")
    mycursor = mycon.cursor()

    while True:
        o = input('''Choice          Action
1            Start billing
2            Edit inventory
3            End program
-->''')
        if o == '1':
            billing(mycon, mycursor)
        elif o == '2':
            while True:
                o = input('''Choice          Action
1            Enter new product
2            Show inventory
3            Update product price
4            Close inventory
-->''')
                if o == '1':
                    enter_product(mycon, mycursor)
                elif o == '2':
                    show_inventory(mycursor)
                elif o == '3':
                    update_price(mycon, mycursor)
                elif o == '4':
                    break
                else:
                    print("Invalid choice")
        elif o == '3':
            break
        else:
            print("Invalid choice")
