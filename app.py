from models import Base, engine, session, Product
import time
import csv
import datetime


def menu():
    while True:
        choice = input("""***** PRODUCT DATABASE *****\n
            \r\tv: View details of a single product
            \r\ta: Add a new product
            \r\tb: Backup current database
            \r\tq: Exit
        \nWhat would you like to do?
        \rChoose an option: """)
        if choice.lower() in ["v", "a", "b", "q"]:
            return choice.lower()
        else:
            input("Invalid input. Your input should be an element from the list given -> [v, a, b, q]. \n"
                  "Press enter to try again. ")


def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        headers = next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name,
                                      product_price=product_price,
                                      product_quantity=product_quantity,
                                      date_updated=date_updated)
                session.add(new_product)
        session.commit()


def clean_price(price_str):
    split_price = price_str.split("$")
    try:
        if not price_str.startswith("$"):
            raise ValueError("Pricing error! we only accept $ pricing. Please try again. ")
        price = float(split_price[1])
    except ValueError:
        input("Price error. Valid price format should be like this (Ex: $5.99). Press enter to try again. ")
        return
    else:
        return int(price * 100)


def clean_quantity(quantity_str):
    try:
        quantity = int(quantity_str)
    except ValueError:
        input("Quantity error. Quantity should be an integer. Press enter to try again. ")
        return
    else:
        return quantity


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input("Date error. Valid date format should be like this (Ex: 01/23/2001). Press enter to try again. ")
        return
    else:
        return return_date


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input("ID error. ID should be a number. Press enter to try again. ")
        return
    else:
        if product_id in options:
            return product_id
        else:
            print(f"Your input id is out of options. Please try again. ")
            return


def view_product_detail():
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    while id_error:
        id_choice = input(f"ID options: {id_options}. \nEnter a product id: ")
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
            id_error = False
    the_product = session.query(Product).filter(Product.product_id == id_choice).first()
    print(f"\nPRODUCT DETAILS:"
          f"\n\tID: {the_product.product_id}"
          f"\n\tName: {the_product.product_name}"
          f"\n\tPrice: {the_product.product_price}"
          f"\n\tQuantity: {the_product.product_quantity}"
          f"\n\tUpdated: {the_product.date_updated}\n")
    time.sleep(1)


def add_product():
    print("\nTo add a new product we need some product info. ")
    product_name = input("Name: ")
    price_error = True
    while price_error:
        product_price = input("Price (Ex: $4.30): ")
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False

    quantity_error = True
    while quantity_error:
        product_quantity = input("Quantity (Ex: 97): ")
        product_quantity = clean_quantity(product_quantity)
        if type(product_quantity) == int:
            quantity_error = False

    date_error = True
    while date_error:
        date_updated = input("Updated (Ex: 11/1/2018): ")
        date_updated = clean_date(date_updated)
        if type(date_updated) == datetime.date:
            date_error = False

    new_product = Product(product_name=product_name,
                          product_price=product_price,
                          product_quantity=product_quantity,
                          date_updated=date_updated)
    product_in_db = session.query(Product).filter(Product.product_name == new_product.product_name).one_or_none()
    if product_in_db == None:
        session.add(new_product)
        session.commit()
        print(f"Successfully added a new product. Added new product: {new_product}")
        time.sleep(1)
    else:
        new_product = session.query(Product)
        return add_product()


def handle_backup():
    with open("new_inventory.csv", "a") as csvfile:
        header = ["Name", "Price", "Quantity", "Updated"]
        writer = csv.writer(csvfile)
        writer.writerow(header)
        products = session.query(Product)
        for product in products:
            data = [product.product_name, product.product_price, product.product_quantity, product.date_updated]
            writer.writerow(data)
        print("Successfully new backup csv file created. ")
        time.sleep(1)


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            view_product_detail()
            input("Press ENTER to return to main menu. ")
            print("")
        elif choice == "a":
            add_product()
            input("Press ENTER to return to main menu. ")
            print("")
        elif choice == "b":
            handle_backup()
            input("Press ENTER to return to main menu. ")
            print("")
        else:
            print("Goodbye and thanks for you consideration. ")
            exit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

