import streamlit as st
import pandas as pd
import sqlite3
import random

conn = sqlite3.connect("book_data.db", check_same_thread=False)
c = conn.cursor()

st.set_page_config(layout="wide", page_title='The Book Hive')

st.sidebar.title("The Book Hive.")

if 'start' not in st.session_state:
    st.session_state['start'] = 101
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'password' not in st.session_state:
    st.session_state['password'] = ""
if 'add_to_cart' not in st.session_state:
    st.session_state['add_to_cart'] = []
if 'test' not in st.session_state:
    st.session_state['test'] = 1


def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')


def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, 
    C_Number) VALUES(?,?,?,?,?)''', (Cname, Cpass, Cemail, Cstate, Cnumber))
    conn.commit()


def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data


def customer_update(Cemail, Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''',
              (Cnumber, Cemail,))
    conn.commit()


def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()


def book_update(b_publisher, b_id):
    c.execute(''' UPDATE Books SET B_Publisher = ? WHERE B_id = ?''',
              (b_publisher, b_id))  # CHANGE
    conn.commit()


def book_delete(bid):
    c.execute(''' DELETE FROM Books WHERE B_id = ?''', (bid,))
    conn.commit()


def books_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Books (
    B_id INT PRIMARY KEY NOT NULL,
    B_Name VARCHAR(100) NOT NULL,
    B_Author VARCHAR(100) NOT NULL,
    B_YOP VARCHAR(4) NOT NULL,
    B_Publisher VARCHAR(100) NOT NULL,
    B_img_thumb VARCHAR(255) NOT NULL,
    B_quantity INT NOT NULL,
    B_Price DECIMAL(10,2) NOT NULL
);
                ''')


def book_add_data(bname, bauthor, byop, bpublisher, bid, b_img, b_quantity,
                  b_price):
    try:
        # Read the binary data from the file object
        b_img_data = b_img.read()

        # Insert the data into the database
        c.execute(
            '''INSERT INTO Books (B_Name, B_Author, B_YOP, B_Publisher, 
            B_id, B_img, B_quantity, B_Price) VALUES (?, ?, ?, ?, ?, ?, ?, 
            ?)''',
            (bname, bauthor, byop, bpublisher, bid, b_img_data, b_quantity,
             b_price))
        conn.commit()
        print("Book added successfully.")

    except sqlite3.Error as e:
        print("Error adding book:", e)
        # Rollback the transaction in case of error
        conn.rollback()


def book_view_all_data():
    c.execute('SELECT * FROM Books')
    book_data = c.fetchall()
    return book_data


def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')


def order_delete(Oid):
    print(Oid)
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))
    conn.commit()


def order_add_data(O_Name, O_Items, O_Qty, O_id):
    c.execute(
        '''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
        (O_Name, O_Items, O_Qty, O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?', (customername,))
    order_data = c.fetchall()
    return order_data


def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data


def admin():
    st.title("The Book Hive Admin Dashboard")
    menu1 = ["", "Book Inventory", "Customers", "Orders"]
    choice1 = st.selectbox("Access database for: ", menu1)

    if choice1 == "Book Inventory":

        menu1 = ["", "Add", "View", "Update", "Delete"]
        choice1 = st.selectbox("CRUD Operation: ", menu1)
        if choice1 == "Add":

            st.subheader("Add Books")

            b_name = st.text_input("Book Name")
            b_author = st.text_input("Book Author")
            b_yop = st.text_input("Book Year of Publishing")
            b_publisher = st.text_input("Book Publisher")
            b_id = st.text_input("Book ID")
            b_quantity = st.text_input("Book Quantity")
            b_price = st.text_input("Book Price")
            b_img = st.file_uploader("Book Image")

            if st.button("Add Book to Inventory"):
                book_add_data(b_name, b_author, b_yop,
                              b_publisher, b_id, b_img, b_quantity, b_price)
                st.success("Successfully Added Data")
        if choice1 == "View":
            st.subheader("Book Details")
            book_result = book_view_all_data()
            # st.write(drug_result)
            with st.expander("View All Book Data"):
                book_clean_df = pd.DataFrame(book_result,
                                             columns=["Book Name", "Author",
                                                      "Year of Publishing",
                                                      "Publisher", "ID",
                                                      "Image", "Quantity",
                                                      "Price"])
                book_clean_df = book_clean_df.drop(columns=['Image'])
                st.dataframe(book_clean_df)
            with st.expander("View Book Quantity"):
                book_name_quantity_df = \
                    book_clean_df[['Book Name', 'Quantity']]

                st.dataframe(book_name_quantity_df)
        if choice1 == 'Update':
            st.subheader("Update Books Details")
            b_id = st.text_input("Book ID")
            b_publisher = st.text_input("Book Publisher")
            if st.button(label='Update'):
                book_update(b_publisher, b_id)
                st.success("Successfully Updated Data!")

        if choice1 == 'Delete':
            st.subheader("Delete Books")
            bid = st.text_input("Book ID")
            if st.button(label="Delete"):
                book_delete(bid)
                st.success("Successfully Deleted Data!")

    elif choice1 == "Customers":

        menu1 = ["", "View", "Update", "Delete"]
        choice1 = st.selectbox("CRUD Operation: ", menu1)
        if choice1 == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            # st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result,
                                             columns=["Name", "Password",
                                                      "Email-ID", "Area",
                                                      "Number"])
                st.dataframe(cust_clean_df)

        if choice1 == 'Update':
            st.subheader("Update Customer Details")
            cust_email1 = st.text_input("Email")
            cust_number1 = st.text_input("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email1, cust_number1)
                st.success('Customer Data Updated Successfully!')

        if choice1 == 'Delete':
            st.subheader("Delete Customer")
            cust_email1 = st.text_input("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email1)
                st.success('Customer Data Deleted Successfully!')

    elif choice1 == "Orders":

        menu1 = ["View"]
        choice1 = st.selectbox("View Customer Orders:", menu1)
        if choice1 == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            # st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result,
                                              columns=["Name", "Items", "Qty",
                                                       "ID"])
                st.dataframe(order_clean_df)


def getAuthenticate(username1, password1):
    try:
        c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?',
                  (username1,))
        cust_password11 = c.fetchall()
        if cust_password11[0][0] == password1:
            return True
        else:
            st.sidebar.warning('Invalid username or password.')
            return False
    except IndexError:
        if username1 != "" and password1 != "":
            st.sidebar.warning('Invalid username or password.')


def initialAuthenticate(username1, password1):
    try:
        c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?',
                  (username1,))
        cust_password11 = c.fetchall()
        if cust_password11[0][0] == password1:
            return True
        else:
            return False
    except IndexError:
        return False


def customer(usernamec, passwordc):
    if getAuthenticate(usernamec, passwordc):
        st.session_state['start'] = 103
        st.session_state['test'] = 0
        st.sidebar.divider()
        st.toast("Successfully logged in!")
        st.title("Welcome to The Book Hive!")
        st.session_state['username'] = usernamec
        st.session_state['password'] = password
        st.subheader("Your Order Details")
        order_result = order_view_data(usernamec)

        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result,
                                          columns=["Name", "Items", "Qty",
                                                   "ID"])
            st.dataframe(order_clean_df)
            cancel = st.selectbox("Cancel order: ", order_clean_df["ID"])
            if st.button("Cancel selected order"):
                order_delete(cancel)
                st.experimental_rerun()

        book_result = book_view_all_data()
        st.subheader("Books in Stock:")

        num_columns = 3

        st.sidebar.subheader("Cart: ")

        for i in range(0, len(book_result), num_columns):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                if i + j < len(book_result):
                    col = cols[j]
                    book_index = i + j  # Unique identifier for each book
                    col.image(book_result[book_index][-3], width=250)
                    col.write(book_result[book_index][1])
                    with col:
                        st.write(f"Rs. {book_result[book_index][-1]}")
                        if st.button("Add to cart", key=book_index):
                            st.session_state['add_to_cart'].append(book_index)
                            st.toast("Book added to cart!")
        total = 0
        titles = ""
        counter = 0
        if st.session_state['add_to_cart']:
            for book_index in st.session_state['add_to_cart']:
                book_title = book_result[book_index][1]
                titles += book_title
                book_price = book_result[book_index][-1]
                total += book_price
                counter += 1
                st.sidebar.info(f"{book_title}: Rs. {book_price}")
            st.sidebar.write(f"TOTAL: Rs. {total}")
            cols1, cols2 = st.sidebar.columns(2)
            with cols1:
                if st.sidebar.button(f"Buy now."):
                    st.session_state['start'] = 1
                    st.session_state['add_to_cart'] = []
                    O_id = st.session_state['username'] + "#O" + str(
                        random.randint(0, 1000000))
                    order_add_data(st.session_state['username'], titles,
                                   counter,
                                   O_id)
                    st.experimental_rerun()
            with cols2:
                if st.sidebar.button("Clear cart."):
                    st.session_state['add_to_cart'] = []
                    st.experimental_rerun()
        else:
            st.sidebar.info('Cart is empty!')
        if st.session_state['start'] == 1:
            st.sidebar.success('Purchase successful!')
            st.session_state['start'] = 2


if __name__ == '__main__':
    books_create_table()
    cust_create_table()
    order_create_table()

    menu = ["Login", "Sign Up", "Admin Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if not initialAuthenticate(st.session_state['username'], st.session_state['password']):
        if st.session_state['test'] == 1:
            book_result = book_view_all_data()
            st.subheader("Books in Stock:")
            st.write("Sign in to purchase!")
            num_columns = 3

            st.sidebar.subheader("Cart: ")

            for i in range(0, len(book_result), num_columns):
                cols = st.columns(num_columns)
                for j in range(num_columns):
                    if i + j < len(book_result):
                        col = cols[j]
                        book_index = i + j  # Unique identifier for each book
                        col.image(book_result[book_index][-3], width=250)
                        col.write(book_result[book_index][1])
                        with col:
                            st.write(f"Rs. {book_result[book_index][-1]}")

    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button(label="Login") and st.session_state[
            'start'] == 101:
            st.session_state['start'] = 102
            customer(username, password)
            st.experimental_rerun()
        else:
            customer(st.session_state['username'],
                     st.session_state['password'])

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password',
                                       key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_input("Email ID")
        with col2:
            cust_area = st.text_input("State")
        with col3:
            cust_number = st.text_input("Phone Number")

        if st.button("Sign Up"):
            if cust_password == cust_password1:
                try:
                    customer_add_data(cust_name, cust_password, cust_email,
                                      cust_area, cust_number, )
                    st.success("Account Created! Please login.")
                except sqlite3.IntegrityError:
                    st.warning('Account with this email exists!')

            else:
                st.warning('Passwords do not match!')
    elif choice == "Admin Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        b1 = st.sidebar.button('Login')
        if (b1 and username == 'admin' and password == 'admin') or (
                username == 'admin' and password == 'admin'):
            admin()
        elif username != '' and password != '':
            st.sidebar.warning('Invalid admin credentials.')

st.sidebar.divider()
with st.sidebar.expander("About"):
    st.write(
        "The Book Hive is a mini project that was developed to implement "
        "various DBMS (Database Management Systems) concepts."
        "This project was developed by Yohan Vergis Vinu (RA2111003010417)."
    )
