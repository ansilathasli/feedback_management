import sqlite3
import getpass
from datetime import datetime
conn = sqlite3.connect("product_feedback2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        is_admin BOOLEAN
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        price REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        product_id INTEGER,
                        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                        comment TEXT,
                        date_submitted DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(user_id),
                        FOREIGN KEY(product_id) REFERENCES products(product_id))''')

# cursor.execute("INSERT INTO  users (name, email, password, is_admin) VALUES (?, ?, ?, true)", ("admin", "admin@gmail.com", "admin@123"))

conn.commit()


def view_customer():
    print("\n---------------------- All customer ------------------")
    cursor.execute("SELECT user_id,  name, email FROM users where is_admin=false")
    customers = cursor.fetchall()
    if not customers:
        print("No customers found😐.")
        return
    
    for customer in customers:
        print(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}")

def update_customer():
    id = int(input("👉 Enter your customer ID to update: "))
    name = input("👉 Enter new customer name: ")
    email = input("👉 Enter new email : ")

    cursor.execute('''
        UPDATE users SET name = ?, email = ? WHERE user_id = ?
    ''', (name,email, id))
    print('Customer Updated') 
    conn.commit()

def delete_customer():
    id = int(input("👉 Enter your customer ID to delete: "))
    choose = input("Are you sure you want to delete? (y/n): ")
    if choose.lower() == 'y':
         cursor.execute('''
            DELETE FROM users WHERE  user_id = ?
            ''', (id,))
         print('Customer Deleted😊') 
    else:
             print("customer NOT deleted😐")
    conn.commit()

def customer_menu(customer_id, is_admin):
     while True:
        print("\n ----------- 🙍‍♂️ Customer MENU ----------")
        print("1.🙍‍♂️ Add customers")
        print("1.👁️ view all customers")
        print("2.🙍 Update Customers")
        print("3.❌ Delete Customer")
        print("4.🔙 Back to Main Menu")
        try:
            ch = int(input("👉 Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if ch==1:
            print("already logged in")
        elif ch == 2:
            update_customer()    
        elif ch == 3:
            update_customer()
        elif ch == 4:
            delete_customer()
        elif ch ==5:
            
            break
        else:
            print("❌Invalid choice. Please try again.") 

#product management


def add_product():
    name=input("👉 Enter Product Name : ")
    category=input("👉 Enter Category : ")
    try:
         price=int(input("👉 Enter price : "))
    except ValueError:
        print("❌Invalid price entered.😐")
        return
    cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", (name, category, price))
    print("product added😊")
    conn.commit()

def view_all_products():
    print("\n-------------- All products -------------")
    cursor.execute("SELECT product_id, name, category,price FROM products")
    products = cursor.fetchall()
    if not products:
        print("No products found😐.")
        return
    
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, category: {product[2]},price: {product[3]}")

def delete_product():
    id = int(input("👉 Enter your product ID to delete: "))
    choose = input("Are you sure you want to delete? (y/n): ")
    if choose.lower() == 'y':
         cursor.execute('''
            DELETE FROM products WHERE  product_id = ?
            ''', ( id,))
         print('Product deleted😊') 
    else:
             print("product NOT deleted😐")
    conn.commit()

def update_product(): 
    id = int(input("👉 Enter your product ID to update: "))
    name = input("👉 Enter new product name: ")
    category = input("👉 Enter new category : ")
    price = input("👉 Enter new price : ")

    cursor.execute('''
        UPDATE products SET name = ?, category = ?,price = ?
        WHERE product_id = ?
    ''', (name,category,price, id))
    print('Product Updated') 
    conn.commit()

def product_menu(customer_id, is_admin):
     while True:
        print("\n ------------📦Product MENU-----------")
        print("1.📦Add product")
        print("2.👁️ View all Products")
        print("3.📦 Update Products")
        print("4.❌ Delete Product")
        print("5.🔙 Back to Main Menu")
        try:
            ch = int(input("👉 Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if ch == 1:
            add_product()
        elif ch==2:
            view_all_products()
        elif ch == 3:
            update_product()
        elif ch == 4:
            delete_product()
        elif ch == 5:
             
            break
        else:
            print("❌Invalid choice. Please try again.") 


#feedback management

def submit_feedback(user_id, is_admin): 
    if is_admin:
        print("No provision to add feedback ⚠️")
        return  
    cursor.execute("SELECT product_id, name FROM products")
    products = cursor.fetchall()
    if not products:
        print("No products found. Add products first.🫤")
        return
    print("-----------Available products:📦---------")
    for product in products:
        print(f"{product[0]} - {product[1]}")

    try:
        product_id = int(input("👉 Enter the product ID you want to give feedback for: "))
        rating = int(input("Enter rating (1 to 5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("❌Invalid input.😐")
        return

    comment = input("Enter your comment: ")

    cursor.execute("INSERT INTO feedback (user_id, product_id, rating, comment) VALUES (?, ?, ?, ?)",
                   (user_id, product_id, rating, comment))
    conn.commit()
    print("Feedback Submitted Successfully.😊")



def view_all_feedback(user_id, is_admin):
    if is_admin:
        cursor.execute('''SELECT f.feedback_id, c.name, p.name, f.rating, f.comment, f.date_submitted
                        FROM feedback f
                        JOIN users c ON f.user_id = c.user_id
                        JOIN products p ON f.product_id = p.product_id''')
        rows = cursor.fetchall()
        print("\n--------- All Feedback📝 -------")
        for row in rows:
            print(f"ID: {row[0]}, Customer: {row[1]}, Product: {row[2]}, Rating: {row[3]}, Comment: {row[4]}, Date: {row[5]}")
    else:
        cursor.execute(f'''SELECT f.feedback_id, p.name, f.rating, f.comment, f.date_submitted
                        FROM feedback f
                        JOIN users c ON f.user_id = c.user_id
                        JOIN products p ON f.product_id = p.product_id
                        where f.user_id = {user_id}''')
        rows = cursor.fetchall()
        print("\n-----------All Feedback📝 ------------")
        for row in rows:
            print(f"ID: {row[0]}, Product: {row[1]}, Rating: {row[2]}, Comment: {row[3]}, Date: {row[4]}")


def update_feedback(user_id, is_admin):
    try:
        feedback_id = int(input("👉 Enter feedback ID to update: "))
    except ValueError:
        print("❌Invalid feedback ID.😐")
        return

    if is_admin:
        cursor.execute(f"SELECT * FROM feedback WHERE feedback_id = {feedback_id}")
        if not cursor.fetchone():
            print("Feedback ID not found.😐")
            return
    else:
        cursor.execute(f"SELECT * FROM feedback WHERE feedback_id = {feedback_id} and user_id = {user_id}")
        if not cursor.fetchone():
            print("Access Denied❌")
            return


    try:
        new_rating = int(input("Enter new rating (1 to 5): "))
        if new_rating < 1 or new_rating > 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("❌ Invalid rating.😐")
        return

    new_comment = input("Enter new comment: ")

    cursor.execute("UPDATE feedback SET rating = ?, comment = ? WHERE feedback_id = ?",
                   (new_rating, new_comment, feedback_id))
    conn.commit()
    print("Feedback updated successfully.😊")



def delete_feedback(user_id, is_admin):
    feedback_id=int(input("👉 Enter The Feedback ID you want to Delete"))
    if is_admin:
        cursor.execute("DELETE FROM feedback WHERE feedback_id=?", (feedback_id,))
    else:
        cursor.execute(f"DELETE FROM feedback WHERE feedback_id={feedback_id} and user_id = {user_id}")
    conn.commit()
    print("Feedback Deleted.😊")

def feedback_menu(customer_id, is_admin):
    while True:
        print("\n ------------📝FEEDBACK MENU--------------")
        print("1.📝 Submit Feedback")
        print("2.👁️ View All Feedback")
        print("3.🆕 Update Feedback")
        print("4.❌ Delete Feedback")
        print("5.🔙 Back to Main Menu")
        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if ch == 1:
            submit_feedback(customer_id, is_admin)
        elif ch==2:
            view_all_feedback(customer_id, is_admin)
        elif ch == 3:
            update_feedback(customer_id, is_admin)
        elif ch == 4:
            delete_feedback(customer_id, is_admin)
           
        elif ch ==5:
             
            break
        else:
            print("❌ Invalid input. Please try again.")  

#register
    
def register(is_admin=False):
    print("\n---------- USER Registration --------")
    name = input("Enter User Name🙍: ")
    email = input("Enter User Email (will be used for login)📧: ")
    password = input("Enter User Password🔑: ")

    try:
        cursor.execute("INSERT INTO  users (name, email, password, is_admin) VALUES (?, ?, ?, ?)", (name, email, password, is_admin))
        conn.commit()
        print("Registration successful!😊")
    except sqlite3.IntegrityError:
        print("Email already registered.")

#login
        
def login():
    print("\n-------- User Login ---------")
    email = input("Enter User Email📧: ")
    password = input("Enter User Password🔑: ")

    cursor.execute("SELECT user_id,is_admin, name FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    if user:
        print(f"🔓Login successful. Welcome, {user[2]}!😊")
        customer_id = user[0]
        is_admin = user[1]
        if customer_id:
                next_menu(customer_id, is_admin)
        return   
    else:
        print("❌ Invalid login.😐")
        return None
def next_menu(customer_id, is_admin):
    while True:
        if is_admin:
            print("\n--------Please select--------- ")
            print("1.📦 Product Management")
            print("2.📝 Feedback Management")
            print("3.🧑‍💻 Add New Admin")
            print("4.🔒 Logout")

            try:
                ch = int(input("👉 Enter your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            

            
            if ch==1:
                product_menu(customer_id, is_admin) 
            elif ch==2:
                feedback_menu(customer_id, is_admin) 
            elif ch==3:
                register(is_admin)    
            elif ch == 4:
                print("❌Exiting program.")
                break
            else:
                print("❌ Invalid input.. Please try again.")   
        else:
            print("\n --------Please select--------- ")
            print(" 1. 👁️ View Products")
            print("2. 📝Feedback Menu")
            print("3. 🔒Logout")

            try:
                ch = int(input("👉Enter your choice: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if ch==1:
                view_all_products()
            elif ch==2:
                feedback_menu(customer_id, is_admin) 
            elif ch == 3:
                print("❌ Logging out .")
                break
            else:
                print("❌ Invalid input. Please try again.")   

def forgot_password():
    email = input("👉 Enter your registered email: ")
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if not result:
        print("No account found with that email.")
        return
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    if new_password != confirm_password:
        print("Passwords do not match.")
        return
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    conn.commit()
    print("Password reset successfully! ✅")         
        
#main 
                            
def main():
    while True:
       print("\n--------MAIN MENUE----------")
       print("1.🔓 Login              ")
       print("2.📝 Register           ") 
       print("3.🔐 Forgot Password           ")              
       print("4.❌ Exit               ")
       print("------------------------------")
       try:
            ch = int(input("👉 Enter Your Choice: "))
       except ValueError:
            print("Please Enter a Valid Number.")
            continue
       if ch == 1:    
            
            should_exit = login()
            if should_exit:
                break
       elif ch == 2:
            register()
       elif ch == 3:
            forgot_password()     

       elif ch == 4:
            print("❌Exiting Program.")
            break
       else:
            print("❌ Invalid input.. Please Try again.")


main()

    
