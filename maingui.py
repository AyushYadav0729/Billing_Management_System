import customtkinter as ctk
import billing  
import billgui
import inventory_gui
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

billing.set_up()
mycon = billing.mys.connect(host="localhost", user="root", passwd="1234", database="company")
mycursor = mycon.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

main = ctk.CTk()
main.title("Billing System")
main.geometry("500x400")

title = ctk.CTkLabel(main, text="🏪 Billing Management System", font=("Arial Rounded MT Bold", 24))
title.pack(pady=40)

def open_billing_window():
    main.withdraw()  # hide main window
    import billgui
    billgui.open_billing_gui(main, mycon, mycursor)

def open_inventory_window():
    import inventory_gui
    inventory_gui.open_inventory_window(main)

def exit_app():
    mycon.close()
    main.destroy()

# --- Buttons ---
billing_btn = ctk.CTkButton(main, text="🧾 Billing", width=200, height=50, font=("Arial", 18),
                             command=open_billing_window)
billing_btn.pack(pady=10)

inventory_btn = ctk.CTkButton(main, text="📦 Inventory", width=200, height=50, font=("Arial", 18),
                               command=open_inventory_window)
inventory_btn.pack(pady=10)
exit_btn = ctk.CTkButton(main, text="Exit", width=200, height=50, font=("Arial", 18),
                         command=exit_app)
exit_btn.pack(pady=30)
main.mainloop()
