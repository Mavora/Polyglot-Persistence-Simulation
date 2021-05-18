
# Imports 
import uuid
import sqlite3
import pickledb
from termcolor import colored
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId


print(colored("\nStarting up ...\n","green"))



# To break chain of loops 
break_chain = False



temp_cat = []



# ##########################
# ##### Database stuff #####
# ##########################



# ###################
# ## Relational DB ##
# ###################
def start_program():
    global conn
    global cur
    try:  # If database already exists
        with open('memory') as f:
            f.close()
            
        conn = sqlite3.connect("memory")  # Connect to DB
        cur = conn.cursor()  # Create cursor

    except:  # If database doesnt exist
        conn = sqlite3.connect("memory")  # Create DB
        cur = conn.cursor()  # Create cursor
        sql_script = open('sql_file.sql', 'r')
        cur.executescript(sql_script.read())
        sql_script.close()
        conn.commit()
    get_categories()


def get_categories():
    global cat_list
    cat_list = []
    for i in cur.execute("SELECT category FROM product"):
        if i not in temp_cat:
            temp_cat.append(i)
    for i in temp_cat:
        j = "".join(i)
        cat_list.append(j)
        cat_list = list(dict.fromkeys(cat_list))



# ###################
# ## PickleDB #######
# ###################

db = pickledb.load('shopping_cart.db', False)

unique_id = str(uuid.uuid4())

#Create a dictionary with name unique_id
db.dcreate(unique_id)


# ###################
# ## MongoDB ########
# ###################

client = MongoClient()
mdb = client.orders
orders = mdb.orders



# #####################
# ##### Main menu #####
# #####################


def menu():
    while True:
        print("\n"
              "\n\033[4mMain menu\033[0m"
              "\n"
              "\n1: Frontend"
              "\n2: Backend"
              "\n0: Exit")
        choice = input("\n"
                       "\nEnter number: ")
        if choice == "1":
            print("\n"
                  "\n"+colored("Going to Frontend ...","green"),
                  "\n")
            frontend()
        elif choice == "2":
            print("\n"
                  "\n"+colored("Going to backend ...","green"),
                  "\n")
            backend()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Goodbye","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")



# ####################
# ##### Frontend #####
# ####################

def frontend():
    while True:
        global break_chain
        break_chain = False
        print("\n"
              "\n\033[4mFrontend menu\033[0m"
              "\n"
              "\n1: View products"
              "\n2: View shopping cart"
              "\n0: Back")
        choice = input("\n"
                       "\nEnter number: ")
        if choice == "1":
            print("\n"
                  "\n"+colored("Going to category selection ...","green"),
                  "\n")
            category_selection()
        elif choice == "2":
            print("\n"
                  "\n"+colored("Going to shopping cart ...","green"),
                  "\n")
            view_shopping_cart()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def category_selection():
    while True:
        print("\n"
              "\n\033[4mSelect category\033[0m"
              "\n"
              "\nCategories: \n")
        for i in cat_list:
            print(i)
        print("\n0: Back")
        global category
        category = input("\nEnter category (case sensitive): ")

        if category == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        elif category in cat_list:
            print("\n"
                  "\n"+colored("Going to {} ...".format(category),"green"),
                  "\n")  
            product_selection(category)
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def product_selection(category):
    while True:

        print("\n"
              "\n\033[4mSelect product\033[0m"
              "\n")
        id_list = []
        columns = [["ID", "Name", "Category", "Year", "Quantity", "Price"]]
        for row in cur.execute("SELECT * FROM product WHERE category = '{}'".format(category)):
            columns.append(list(row))

        for i in columns:
            print("{:<0}{:<10}{:<15}{:<15}{:<15}{:<15}{:<15}".format(i[0],":",i[1],i[2],i[3],i[4],i[5]))
            if str(i[0]).isdigit():
                id_list.append(str(i[0]))

        print("{:<10} Back".format("0:"))
        product = input("\nEnter product ID: ")

        if product == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        elif product in id_list:

            for i in cur.execute("SELECT product_name FROM product WHERE product_id = '{}'".format(product)):
                prod_name = i
            print("\n"
                  "\n"+colored("Going to {} ...".format(prod_name[0]),"green"),
                  "\n")
            product_menu(product)
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def product_menu(product):
    while True:

        print("\033[4mProduct:\033[0m\n")
        for i in cur.execute("SELECT * FROM product WHERE product_id = '{}'".format(product)):
            product_info=list(i)
            

        print("{:<10}{}".format("ID:",product_info[0]),
              "\n{:<10}{}".format("Name:",product_info[1]),
              "\n{:<10}{}".format("Category:",product_info[2]),
              "\n{:<10}{}".format("Year:",product_info[3]),
              "\n{:<10}{}".format("Quantity:",product_info[4]),
              "\n{:<10}{}".format("Price:",product_info[5]),)
        
        
        print("\n1: Add to shopping cart"
              "\n0: Back")
        choice = input("\nEnter number: ")
        if choice == "1":
            if product_info[4] == 0:
                print("\n"
                      "\n"+colored("This product is out of stock","red"),
                      "\n")
                break

            else:
            
                if db.dexists(unique_id,product):
                    print("\n"
                          "\n"+colored("Product already in shopping cart","red"),
                          "\n")
                    break
                else:
                    print("\n"
                          "\n"+colored("{} has been added to the shopping cart ...".format(product_info[1]),"green"),
                          "\n")
                    
                    product_id = "{}".format(product_info[0])
                    product_inf = {"ID":str(product_info[0]),
                                   "Name":(product_info[1]),
                                   "Price":(product_info[5]),
                                   "Quantity":(1),
                                   "Available":product_info[4]
                                   }
                    add_to_cart(product_id, product_inf)
                    break
        
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def add_to_cart(product_id, product_inf):
    product_pair = (product_id, product_inf)
    db.dadd(unique_id, product_pair)


def view_shopping_cart():
    print("\n"
          "\n\033[4mShopping cart\033[0m"
          "\n")
    global total
    total = 0
    #Create a dict for the values
    if len(db.dgetall(unique_id)) == 0:
        print(colored("Shopping cart is empty","red"))
    elif len(db.dgetall(unique_id)) != 0:
        get_all_dict = db.dgetall(unique_id)
        #Print the values
        for i in get_all_dict.values():
            for j,k in i.items():
                print(j,":",k)
            print("")
            total += int(i["Price"])*int(i["Quantity"])
    
        
        print("Total price: ", total)
            
        print("\n1: Checkout"
              "\n2: Remove product"
              "\n3: Edit quantity"
              "\n4: Delete shopping cart"
              "\n0: Back")
        choice = input("\nEnter number: ")
        if choice == "1":
            checkout()
    
        elif choice == "2":
            print("")
            for i in get_all_dict.values():
                for j,k in i.items():
                    print(j,":",k)
                print("")
            print("0: Back")
            delete_id = input("Enter ID to delete: ")
            if delete_id == "0":
                print("\n"
                      "\n"+colored("Going back ...","green"),
                      "\n")
            elif delete_id != "0":
                if delete_id in db.dkeys(unique_id):
                    remove_from_cart(delete_id)
                else:
                    print("\n"
                          "\n"+colored("Product with ID {} not in cart".format(delete_id),"red"),
                          "\n")


        elif choice == "3":
    
            print("")
            for i in get_all_dict.values():
                for j,k in i.items():
                    print(j,":",k)
                print("")
            id_to_change = input("Enter product ID to change quantity: ")

            if id_to_change in db.dkeys(unique_id):
                dict_to_change = get_all_dict[id_to_change]
                new_quantity = int(input("Enter new quantity: "))
                if new_quantity == 0:
                    remove_from_cart(id_to_change)
                elif new_quantity <= int(dict_to_change["Available"]):
    
                    change_quantity(id_to_change,new_quantity)
    
                elif new_quantity > int(dict_to_change["Available"]):
                    print(colored("Only {} available in stock".format(dict_to_change["Available"]),"red"))

                else:
                    print("\n"
                          "\n"+colored("Invalid input","red"),
                          "\n")
            else:
                print("\n"
                      "\n"+colored("Product with ID {} not in cart".format(id_to_change),"red"),
                      "\n")
            
        elif choice == "4":
            delete_cart()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def change_quantity(id_to_change,new_quantity):
    try:
        get_all_dict = db.dgetall(unique_id)
        dict_to_change = get_all_dict[id_to_change]
        dict_to_change["Quantity"] = new_quantity
        print(colored("Quantity updated","green"))
    except:
        print(colored("Something went wrong, did you type the correct ID? ","red"))
    view_shopping_cart()


def delete_cart():
    db.drem(unique_id)
    db.dcreate(unique_id)
    view_shopping_cart()


def remove_from_cart(product):
    try:
        db.dpop(unique_id,product)
        print(colored("Product removed from cart","green"))
    except:
        print(colored("Something went wrong, did you type the correct ID? ","red"))
    view_shopping_cart()


def checkout():
    while True:
        if break_chain:
            break
        print("\n"
              "\n\033[4mCheckout\033[0m"
              "\n"
              "\nYou have these products in your shopping cart")
        global total
        total = 0
            #Create a dict for the values
        if len(db.dgetall(unique_id)) == 0:
            print(colored("Shopping cart is empty","red"))
        elif len(db.dgetall(unique_id)) != 0:
            get_all_dict = db.dgetall(unique_id)
            #Print the values
            for i in get_all_dict.values():
                for j,k in i.items():
                    print(j,":",k)
                print("")
                total += int(i["Price"])*int(i["Quantity"])
            
                
            print("Total price: ", total,
                  "\n"
                  "\n1: Next step"
                  "\n0: Back")
        
        choice = input("\nEnter number: ")

        if choice == "1":
            print("\n"
                  "\n"+colored("Going to customer information ...","green"),
                  "\n")
            customer_registration()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def customer_registration():
    while True:
        if break_chain:
            break
        
        print("\n"
              "\n\033[4mCustomer information\033[0m"
              "\n")
        print("1: Already registered"
              "\n2: New customer"
              "\n0: Back")
        choice = input("Enter number: ")
        if choice == "1":
            while True:
                if break_chain:
                    break
                email = input("Enter email address: ")
                customer = {}
                for i in cur.execute("SELECT * FROM customer WHERE email = '{}'".format(email)):
                    customer_tuple = i
                try:
                    if customer_tuple:
                        customer = {"Customer ID":customer_tuple[0],
                                    "First name":customer_tuple[1],
                                    "Last name":customer_tuple[2],
                                    "Address":customer_tuple[3],
                                    "Email":customer_tuple[4],}
                        print("\nCustomer information: "
                              "\n"
                              "\nCustomer ID: ", customer["Customer ID"],
                              "\nFirst name: ", customer["First name"],
                              "\nLast name: ", customer["Last name"],
                              "\nAddress: ", customer["Address"],
                              "\nEmail: ", customer["Email"],)
                        while True:
                            if break_chain:
                                break
                            correct = input("0: Back"
                                            "\nPress enter to place order: ")
                            if correct == "0":
                                break
                            else:
                                place_order(email)
                except:
                    print("\n"
                          "\n"+colored("Email not found in database, please register","red"),
                          "\n")

        
        elif choice == "2":
            print("\n"
                  "\n\033[4mCustomer registration\033[0m"
                  "\n")
            customer = {}
            while True:
                if break_chain:
                    break
                first_name = input("0: Back"
                                   "\nEnter first name: ")
                if first_name == "0":
                    break
                
                while True:
                    if break_chain:
                        break
                    last_name = input("0: Back"
                                      "\nEnter last name: ")
                    if last_name == "0":
                        break
                    
                    while True:
                        if break_chain:
                            break
                        address = input("0: Back"
                                        "\nEnter address: ")
                        if address == "0":
                            break
                        
                        while True:
                            if break_chain:
                                break
                            email = input("0: Back"
                                          "\nEnter email: ")
                            if email == "0":
                                break
                            
                            while True:
                                if break_chain:
                                    break
                                correct = input("0: Back"
                                                "\nPress enter to place order: ")
                                if correct == "0":
                                    break
                                else:
                                
                                    cur.execute("")
                                    cur.execute("insert into customer (first_name, last_name, address, email) values ("
                                                "'{}', '{}', '{}', '{}')".format(first_name,last_name,address,email))
                                    conn.commit()
                                    for i in cur.execute("SELECT * FROM customer WHERE email = '{}'".format(email)):
                                        customer_tuple = i
                                    
                                    customer = {"Customer ID":customer_tuple[0],
                                                "First name":customer_tuple[1],
                                                "Last name":customer_tuple[2],
                                                "Address":customer_tuple[3],
                                                "Email":customer_tuple[4],}
                                    print("\nCustomer information: "
                                          "\n"
                                          "\nCustomer ID: ", customer["Customer ID"],
                                          "\nFirst name: ", customer["First name"],
                                          "\nLast name: ", customer["Last name"],
                                          "\nAddress: ", customer["Address"],
                                          "\nEmail: ", customer["Email"],)

                                    place_order(email)
                         
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")
        


def place_order(email):
    global total

    
    document={"Total": total, "Open":1}
    
    
    for i in cur.execute("SELECT * FROM customer WHERE email = '{}'".format(email)):
        customer_tuple = i
        customer = {"Customer ID":customer_tuple[0],
                    "First name":customer_tuple[1],
                    "Last name":customer_tuple[2],
                    "Address":customer_tuple[3],
                    "Email":customer_tuple[4],}
    document.update(customer)
    
    id_quant = {}  # used to update quantity
    cart = db.dgetall(unique_id)
    for k,v in cart.items():
        id_quant.update({v["ID"] : v["Quantity"]})
        del v["Available"]  # This is only needed when viewing the shopping cart 
        v["Product ID"] = v["ID"]  # 
        del v["ID"]
        v = [v]
    
    document.update(cart)
    
    orders.insert_one(document)  # placing order 
    for i,q in id_quant.items():  # Updating quantity
        cur.execute("UPDATE product SET quantity = quantity - '{}' WHERE product_id='{}'".format(q, i))
        conn.commit()

    db.drem(unique_id)
    db.dcreate(unique_id)
    global break_chain
    break_chain = True



# ###################
# ##### Backend #####
# ###################

def backend():
    while True:
        print("\n"
              "\n\033[4mBackend menu\033[0m"
              "\n"
              "\n1: Orders"
              "\n2: Products"
              "\n0: Back")
        choice = input("Enter number: ")
        if choice == "1":
            print("\n"
                  "\n"+colored("Going to orders menu ...","green"),
                  "\n")
            orders_menu()
        elif choice == "2":
            print("\n"
                  "\n"+colored("Going to products ...","green"),
                  "\n")
            product_backend_menu()
        elif choice == "0":
            "\n"
            "\n"+colored("Going back ...","green"),
            "\n"
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def orders_menu():
    while True:
        print("\n"
              "\n\033[4mOrders menu\033[0m"
              "\n"
              "\n1: Open Orders"
              "\n2: Closed Orders"
              "\n0: Back")
        choice = input("Enter number: ")
        if choice == "1":
            print("\n"
                  "\n"+colored("Going to open orders ...","green"),
                  "\n")
            open_orders()
        elif choice == "2":
            print("\n"
                  "\n"+colored("Going to closed orders ...","green"),
                  "\n")
            closed_orders()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def open_orders():
    while True:
        print("\n"
              "\n\033[4mOpen orders\033[0m"
              "\n"
              "\nOrders:")
        for i in orders.find({"Open":1}):
            pprint.pprint(i)
        print("\n0: Back")
        order = input("Enter ID: ")
        if order == "0":
            print(""
                  "\n"+colored("Going back ...","green"),
                  "")
            break
        elif order:
            close_open_order(order)


def close_open_order(order):
    while True:
        print("\n"
              "\n\033[4mOrder details\033[0m"
              "\n"
              "\nOrder: ")
        pprint.pprint(orders.find_one({"_id": ObjectId(order)}))
        print("\n1: Close order"
              "\n0: Back")
        choice = input("Enter number: ")
        if choice == "1":
            orders.update_one({"_id": ObjectId(order)},{ "$set": { "Open": 0 } })
            print("\n"
                  "\n"+colored("Order has been closed, going back to open orders ...","green"),  # Close order ############
                  "\n")
            break
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def closed_orders():
    while True:
        print("\n"
              "\n\033[4mClosed orders\033[0m"
              "\n"
              "\nOrders:")
        for i in orders.find({"Open":0}):
            pprint.pprint(i)
        print("\n0: Back")
        order = input("Enter order: ")
        if order == "0":
            print(""
                  "\n"+colored("Going back ...","green"),
                  "")
            break
        elif order:
            closed_order(order)


def closed_order(order):
    while True:
        print("\n"
              "\n\033[4mOrder details\033[0m"
              "\n"
              "\nOrder: ")
        for i in orders.find({"Open":0}):
            pprint.pprint(i)
        print("\n0: Back")
        choice = input("Press enter to go back: ")
        if choice:
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break


def product_backend_menu():
    while True:
        print("\n"
              "\n\033[4mProduct menu\033[0m"
              "\n"
              "\n1: Add product"
              "\n2: View products"

              "\n0: Back")
        choice = input("Enter number: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            view_category()
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")



def add_product():
    while True:
        print("\n\033[4mAdd product\033[0m"
              "\n"
              "\nEnter 0 to go back ")

        product_name = input("Enter product name: ")
        if product_name == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        category = input("Enter category: ")
        if category == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        elif category not in cat_list:
            cat_list.append(category)
        prod_year = input("Enter production year: ")
        if prod_year == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        quantity = input("Enter quantity: ")
        if quantity == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        price = input("Enter price: ")
        if price == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break

        elif (product_name and category and prod_year and quantity and price):
            print("\n\033[4mProduct information:\033[0m")
            print("\nProduct name: ", product_name, 
                  "\nCategory: ", category, 
                  "\nProduction year: ", prod_year, 
                  "\nQuantity: ", quantity, 
                  "\nPrice: ", price)
            correct = input("Enter 1 if the information is correct, or 0 to try again: ")
            if correct == "1":
                cur.execute("insert into product (product_name, category, prod_year, quantity, price) values ("
                    "'{}', '{}', '{}', '{}', '{}')".format(product_name,category,prod_year,quantity,price))
                conn.commit()
                print("\n"+colored("Product has been added","green"))
            
            elif correct == "0":
                print("\n"
                      "\n"+colored("Going back ...","green"),
                      "\n")
            else:
                print("\n"
                      "\n"+colored("Invalid input","red"),
                      "\n")
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")



def view_category():
    while True:

        print("\n"
              "\n\033[4mSelect category\033[0m"
              "\n"
              "\nCategories: \n")
        for i in cat_list:
            print(i)
        print("\n0: Back")
        global cat
        cat = input("\nEnter category (case sensitive): ")

        if cat == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        elif cat in cat_list:
            print("\n"
                  "\n"+colored("Going to {} ...".format(cat),"green"),
                  "\n")  
            view_products(cat)
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def view_products(cat):
    while True:


        id_list = []
        global columns
        columns = [["ID", "Name", "Category", "Year", "Quantity", "Price"]]
        for row in cur.execute("SELECT * FROM product WHERE category = '{}'".format(cat)):
            columns.append(list(row))
        if len(columns)<2:  # If the category is empty, delete category and go back to category selection
            cat_list.remove(cat)
            break
        print("\n"
              "\n\033[4mSelect product\033[0m"
              "\n")
        for i in columns:

            print("{:<0}{:<10}{:<15}{:<15}{:<15}{:<15}{:<15}".format(i[0],":",i[1],i[2],i[3],i[4],i[5]))
            if str(i[0]).isdigit():
                id_list.append(str(i[0]))

        print("{:<10} Back".format("0:"))
        product = input("\nEnter product ID: ")

        if product == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        elif product in id_list:
            print("\n"
                  "\n"+colored("Going to {} ...".format(product),"green"),
                  "\n")
            product_options(product)
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")

def product_options(product):
    while True:

        print("\n"
              "\n\033[4mProduct:\033[0m"
              "\n")
        for i in cur.execute("SELECT * FROM product WHERE product_id = '{}'".format(product)):
            #print(i)
            product_info=list(i)

        #print(product_info)
        print("Product ID: {}".format(product_info[0]),
              "\nProduct name: {}".format(product_info[1]),
              "\nCategory: {}".format(product_info[2]),
              "\nProduction year: {}".format(product_info[3]),
              "\nQuantity: {}".format(product_info[4]),
              "\nPrice: {}".format(product_info[5]))

        print("\n1: Delete product"
              "\n2: Edit price"
              "\n3: Edit quantity"
              "\n0: Back")
        choice = input("\nEnter number: ")
        
        if choice == "1":
            remove_product(product)
            break
        
        elif choice == "2":
            print("\nCurrent price:\t",product_info[5])
            print("x: Back")
            new_price = input("Enter new price: ")
            if new_price == "x":
                print("\n"
                      "\n"+colored("Going back ...","green"),
                      "\n")
                break
            elif new_price.isdigit():
                method = "price"
                edit_product(method, product, new_price)
        
        elif choice == "3":
            print("\nCurrent quantity:\t",product_info[4])
            print("x: Back")
            new_quantity = input("Enter new quantity: ")
            if new_quantity == "x":
                print("\n"
                      "\n"+colored("Going back ...","green"),
                      "\n")
                break
            elif new_quantity.isdigit():
                method = "quantity"
                edit_product(method, product, new_quantity)
        
        
        elif choice == "0":
            print("\n"
                  "\n"+colored("Going back ...","green"),
                  "\n")
            break
        else:
            print("\n"
                  "\n"+colored("Invalid input","red"),
                  "\n")


def remove_product(product):
    cur.execute("DELETE FROM product WHERE product_id='{}'".format(product))
    conn.commit()
    get_categories()
    print("\n"+colored("Product has been deleted ...","green"))


def edit_product(method, product, value):
    if method == "price":
        cur.execute("UPDATE product SET price='{}' WHERE product_id='{}'".format(value, product))
        conn.commit()
        print("\n"+colored("Price has been updated\nNew price: {}".format(value),"green"))

    elif method == "quantity":
        cur.execute("UPDATE product SET quantity='{}' WHERE product_id='{}'".format(value, product))
        conn.commit()
        print("\n"+colored("Quantity has been updated\nNew quantity: {}".format(value),"green"))
    else:
        print("\n"
              "\n"+colored("Invalid input","red"),
              "\n")
    

start_program()

menu()



