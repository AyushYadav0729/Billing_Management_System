import customtkinter as ctk
import mysql.connector as mys
from tkinter import messagebox

def open_inventory_window(main_window):

    main_window.withdraw()  

    try:
        mycon = mys.connect(host="localhost", user="root", passwd="1234", database="company")
        cursor = mycon.cursor()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to MySQL:\n{e}")
        return

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(10) PRIMARY KEY,
        product_name VARCHAR(50),
        product_price FLOAT,
        quantity INT
    )''')
    mycon.commit()

    window = ctk.CTk()
    window.title("Inventory Management")
    window.geometry("950x700+0+0")
    window.configure(fg_color="#1e1e1e")

    ctk.CTkLabel(window, text="Inventory Management", font=("Arial", 28, "bold")).pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(window, width=850, height=400, fg_color="#2b2b2b", corner_radius=10)
    scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    headers = ["Product ID", "Name", "Price", "Quantity"]
    for col, text in enumerate(headers):
        ctk.CTkLabel(scroll_frame, text=text, font=("Arial", 18, "bold")).grid(row=0, column=col, padx=15, pady=10)

    entry_rows = []

    def create_row(data):
        row_entries = []
        row_index = len(entry_rows) + 1

        id_entry = ctk.CTkEntry(scroll_frame, width=120, font=("Arial", 16))
        id_entry.insert(0, data[0])
        id_entry.configure(state="readonly")
        id_entry.grid(row=row_index, column=0, padx=10, pady=5)
        row_entries.append(id_entry)

        name_entry = ctk.CTkEntry(scroll_frame, width=200, font=("Arial", 16))
        name_entry.insert(0, data[1])
        name_entry.grid(row=row_index, column=1, padx=10, pady=5)
        row_entries.append(name_entry)

        price_entry = ctk.CTkEntry(scroll_frame, width=150, font=("Arial", 16))
        price_entry.insert(0, str(data[2]))
        price_entry.grid(row=row_index, column=2, padx=10, pady=5)
        row_entries.append(price_entry)

        qty_entry = ctk.CTkEntry(scroll_frame, width=150, font=("Arial", 16))
        qty_entry.insert(0, str(data[3]))
        qty_entry.grid(row=row_index, column=3, padx=10, pady=5)
        row_entries.append(qty_entry)

        entry_rows.append(row_entries)

    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        if not products:
            sample_data = [
                ("P001", "Chips", 20, 50),
                ("P002", "Soda", 30, 40),
                ("P003", "Chocolate", 25, 60)
            ]
            cursor.executemany("INSERT INTO products VALUES (%s,%s,%s,%s)", sample_data)
            mycon.commit()
            products = sample_data

        for item in products:
            create_row(item)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load data:\n{e}")

    def add_product():
        new_id = f"P{len(entry_rows) + 1:03}"
        create_row([new_id, "", "", ""])

    ctk.CTkButton(window, text="Add Product", font=("Arial", 18), command=add_product).pack(pady=10)

    def save_changes():
        try:
            for row in entry_rows:
                pid = row[0].get().strip()
                name = row[1].get().strip()
                price = row[2].get().strip()
                qty = row[3].get().strip()

                cursor.execute("SELECT COUNT(*) FROM products WHERE product_id=%s", (pid,))
                exists = cursor.fetchone()[0]

                if exists:
                    cursor.execute(
                        "UPDATE products SET product_name=%s, product_price=%s, quantity=%s WHERE product_id=%s",
                        (name, price, qty, pid)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO products (product_id, product_name, product_price, quantity) VALUES (%s, %s, %s, %s)",
                        (pid, name, price, qty)
                    )

            mycon.commit()
            messagebox.showinfo("✅ Success", "Products updated successfully!")

        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to update database:\n{e}")

    ctk.CTkButton(window, text="Save Changes", font=("Arial", 18), fg_color="green", command=save_changes).pack(pady=10)

    def close_window():
        try:
            cursor.close()
            mycon.close()
        except:
            pass
        window.destroy()
        main_window.deiconify()

    ctk.CTkButton(window, text="Back to Main", font=("Arial", 18), fg_color="#d9534f", command=close_window).pack(pady=10)

    window.mainloop()
