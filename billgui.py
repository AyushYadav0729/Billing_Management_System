import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import billing
import discounts

def open_billing_gui(main, mycon, mycursor):
    win = ctk.CTkToplevel()
    win.title("Billing Window")
    win.geometry("700x650")

    def add_product():
        pid = pid_entry.get().strip()
        qty = qty_entry.get().strip()

        if not pid or not qty:
            messagebox.showwarning("Input Error", "Please enter both Product ID and Quantity.")
            return
        
        try:
            qty = float(qty)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be numeric.")
            return
        

        data = billing.get(mycon, mycursor, pid)
        if data == " ":
            messagebox.showerror("Error", "Product not found in database.")
            return
        
        pname = data[1]
        price = float(data[2])
        total_price = price * qty
        total_amount[0] += total_price
        bill_data.append([len(bill_data)+1, pname, qty, total_price])
        items_box.insert("end", f"{pname} x{qty} = ₹{total_price}\n")
        total_label.configure(text=f"Total: ₹{total_amount[0]:.2f}")
        

        pid_entry.delete(0, "end")
        qty_entry.delete(0, "end")

    ctk.CTkLabel(win, text="🧾 Billing Section", font=("Arial Rounded MT Bold", 22)).pack(pady=15)

    # --- Product Entry Section ---
    frame = ctk.CTkFrame(win)
    frame.pack(pady=10)

    ctk.CTkLabel(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
    pid_entry = ctk.CTkEntry(frame, width=180)
    pid_entry.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
    qty_entry = ctk.CTkEntry(frame, width=180)
    qty_entry.grid(row=1, column=1, pady=5)
    ctk.CTkButton(frame, text="Add Product", width=150, command=add_product).grid(row=2 , column=1, pady=10)

    items_box = ctk.CTkTextbox(win, width=500, height=200)
    items_box.pack(pady=15)

    total_label = ctk.CTkLabel(win, text="Total: ₹0.00", font=("Arial", 16))
    total_label.pack(pady=5)

    discounts_label = ctk.CTkLabel(win, text="After Discount: ₹0.00", font=("Arial", 16))
    discounts_label.pack(pady=5)

    bill_data = []
    total_amount = [0]
   
    # --- Finalize and save bill ---
    def finalize_bill():
        if not bill_data:
            messagebox.showwarning("Empty Bill", "No products added yet!")
            return

        membership = ctk.CTkInputDialog(text="Enter membership level:", title="Membership").get_input()
        # --- Apply Discount ---
        discounted_value = discounts.get_discounted_price(membership, total_amount[0])

        # Handle different possible return types
        if isinstance(discounted_value, (tuple, list)):
            discounted_total = discounted_value[0]
        elif isinstance(discounted_value, (int, float)):
            discounted_total = discounted_value
        else:
            discounted_total = total_amount[0]  # fallback (no discount)

        # Update UI
        discounts_label.configure(text=f"After Discount: ₹{discounted_total:.2f}")
        payment = ctk.CTkInputDialog(text="Enter payment method (Cash/Card/UPI):", title="Payment").get_input()

        now = datetime.now()
        bill_name = now.strftime("%Y-%m-%d_%H-%M-%S.csv")

        # Save base bill info
        billing.edit_bill(bill_name, [now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")], 1)
        for rec in bill_data:
            billing.edit_bill(bill_name, rec, 0)

        # Save final bill details
        billing.edit_bill(bill_name, [total_amount[0], discounted_total, payment], 2)

        messagebox.showinfo("Bill Generated", f"Bill saved as {bill_name}")

        # Reset the UI for new bill
        items_box.delete("1.0", "end")
        total_label.configure(text="Total: ₹0.00")
        discounts_label.configure(text="After Discount: ₹0.00")
        bill_data.clear()
        total_amount[0] = 0


    def go_back():
        win.destroy()
        main.deiconify()

    ctk.CTkButton(win, text="Finalize Bill", width=200, command=finalize_bill).pack(pady=5)
    ctk.CTkButton(win, text="Back", width=200, command=go_back).pack(pady=20)
