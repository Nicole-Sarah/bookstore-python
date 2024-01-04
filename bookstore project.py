import sqlite3
import tkinter as tk
from tkinter import messagebox

connection = sqlite3.connect('bookstore_final.db')
c = connection.cursor()
app = tk.Tk()
app.title("Bookstore Management Database")


c.execute("""CREATE TABLE IF NOT EXISTS author ( 
author_id INTEGER PRIMARY KEY,
author_firstname TEXT,
author_lastname TEXT)""")

#duplicates 

multiple_authors = [(1,'Rowling','J.K.'),
(2,'Collins','Suzanne'), (3,'Beaton','Kate'),
(4,'Telgemeier','Raina'), (5,'Tolkien','J.R.R.'),
(6,'King','Stephen'), (7,'Shinkai','Makoto'),
(8,'Horikoshi','Kohei'), (9,'Darwin','Charles'),
(10,'Hawking','Stephen'), (11,'Gries','Paul'),
(12, 'Campbell', 'Jennifer'),  (13,'Montojo','Jason'),
(14,'May','Kyla'),(15,'Arakawa', 'Hiromu'),
(16,'Oda','Eiichiro'),(17,'Fujimoto','Tatsuki'),
(18,'Dami','Elisabetta'),(19,'Kinney','Jeff'),
(20,'Green','John'),(21,'Bloom','Judy'),
(22,'Baker','Chandler'),(23,'King','Wesley'),
(24,'Light','Alex'),(25,'Haig','Matt')]

c.executemany("INSERT or IGNORE INTO author VALUES(?,?,?)",multiple_authors)

#Order all authors in alpebetical order by last name
c.execute("""SELECT author_firstname,author_lastname
FROM author
ORDER BY author_lastname ASC""")

c.execute("""DROP TABLE IF EXISTS books""")

c.execute("""CREATE TABLE IF NOT EXISTS books ( 
book_id INTEGER PRIMARY KEY,
book_title TEXT,
genre TEXT,
cover_type TEXT,
price NUMERIC)""")



c.execute("""ALTER TABLE books
           ADD COLUMN published_year INTEGER DEFAULT 0""")
c.execute("""ALTER TABLE books
           ADD COLUMN cost FLOAT DEFAULT 0""")


multiple_books = [(1,'The Lord of the Rings:The Fellowship of the Ring',\
'fantasy','paperback', 18.50), 
(2,'The Lord of the Rings: The Two Towers','fantasy','paperback',18.50), (3,'The Lord of the Rings:The Return of the King','fantasy','paperback',18.50),
(4,'Holly','horror','paperback',25.99), (5,'The Shining','horror','paperback',17.99),
(6,'Smile','comedy','paperback',15.50), (7,'A Brief History of Time','paperback','science',19.99),
(8,'Upside of Falling','romance','paperback',16.99), (9,'The Origin of Species:150th Anniversary Edition','science','paperback',9.00),
(10,'Practical Programming','education','hardcover',75.00), (11,'SuperFudge',"children's literature",'paperback',15.99),
(12, "Pug's Snow Day","children's literature",'hardcover',25.99), (13,'Ducks: Two Years in the Oil Sands','comic','paperbook',16.99),
(14,'Diary of a Wimpy Kid:Rodrick Rules',"children's literature",'paperback',18.99),(15,'Fullmetal Alchemist VI','manga','paperback',16.99),
(16,'One Piece VI','manga','paperback',15.50),(17,'Chainsaw man VI','manga','paperback',16.99),
(18,'Paws off, Cheddarface',"children's literature",'paperback',12.99),(19,'The Kingdom of Fantasy',"children's literature",'hardcover',18.99),
(20,'The Fault In Our Stars','romance','paperback',16.80),(21,'Paper Towns','young adult','paperback',15.99),
(22,'Hello(From Here)','romance','paperback',16.99),(23,'My Hero Academia VI','manga','paperback',15.99),(24,'My Hero Academia VII','manga','paperback',15.99),(25,'The Humans','comedy','paperback',15.00),(26,'Chainsaw man VII','manga','paperback',15.99),(26,"Harry Potter and the Sorcerer's Stone",'fantasy','paperback',15.00),(27,'Chainsaw man VIII','manga','paperback',15.90),(28,'Harry Potter and the Chamber of Secrets','fantasy','paperback',15.00),(29,'Harry Potter and the Prisoner of Azkaben','fantasy','paperback',15.00),(30,'Harry Potter and the Goblet of Fire','fantasy','paperback',15.00),(31,'The Hunger Games','fantasy','hardcover',26.00)]

c.executemany("INSERT or IGNORE INTO books ('book_id','book_title','genre','cover_type','price') VALUES(?,?,?,?,?)",multiple_books)





update_info = "UPDATE books SET published_year = ?,cost = ? WHERE book_id = ?"

years_for_books = {
    1: (1954,14.50),
    2: (1954,14.50),
    3: (1955,14.50),
    4:(2023,18.85),
    5:(1977,12.99),
    6:(2010,18.99),
    7:(1988,22.85),
    8:(2020,17.99),
    9:(2003,15.25),
    10:(2017,55.78),
    11:(1980,13.99),
    12:(2019,23.85),
    13:(2022,14.20),
    14:(2008,15.55),
    15:(2002,12.75),
    16:(1997,10.99),
    17:(2019,14.59),
    18:(2000,9.60),
    19:(2003,14.55),
    20:(2012,15.99),
    21:(2008,12.47),
    22:(2021,12.25),
    23:(2014,10.25),
    24:(2015,14.80),
    25:(2013,13.00),
    26:(1997,12.89),
    27:(2019,13.50),
    28:(1998,13.50),
    29:(1999,14.00),
    30:(2000,14.00),
    31:(2008,21.20)
}

for book_id, (year,cost) in years_for_books.items():
    c.execute(update_info, (year,cost, book_id))



#A customer asked for all books written by J.K. Rowling, lets 


#Find all books that are hardcover published after 2010
c.execute("""SELECT book_id,book_title
FROM books 
WHERE cover_type='hardcover' 
   AND published_year>2010""")

c.execute("""DROP TABLE IF EXISTS accessories""")
c.execute("""CREATE TABLE IF NOT EXISTS accessories ( 
item_id INTEGER,
item TEXT,
price NUMERIC,
cost NUMERIC)""")

#Find the average price of all books in the romance genre 
c.execute("""SELECT genre, AVG(books.price) AS average_book_price
FROM books
GROUP BY genre
HAVING genre='romance'""")






multiple_items=[(31,'bookmark', 2.50,1.00),(32,'bookmark', 2.50,1.00),(33,'water bottle',6.00,4.25),(34,'ballpoint pen',1.99,0.50)\
                ,(35,'greeting card',3.00,1.00),(36,'puzzle',5.99,2.50),(37,'notebook',3.50,2.00)]
                


c.executemany("INSERT or IGNORE INTO accessories VALUES(?,?,?,?)",multiple_items)


#DElete duplicates so accessories are unique 

c.execute("""DELETE FROM accessories
WHERE item_id NOT IN (
    SELECT MIN(item_id)
    FROM accessories
    GROUP BY TRIM(UPPER(item))
);""")




#show how many copies of each book there is, take id of primary key like tabe storage number of copies and book id create  a table to show parent child relatonships foreign key, 

c.execute("""DROP TABLE IF EXISTS customers""")
#this is parent table
c.execute("""CREATE TABLE IF NOT EXISTS customers ( 
cust_id INTEGER PRIMARY KEY,
cust_name TEXT,
num_books INTEGER,
num_accessories INTEGER,
regular_status BOOLEAN CHECK (regular_status IN (0, 1)))""")   


c.execute("""DROP TABLE IF EXISTS books_bought""")
c.execute("""CREATE TABLE IF NOT EXISTS books_bought (
cust_id INTEGER,
book_id INTEGER,
book_title TEXT,
FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
FOREIGN KEY (book_id) REFERENCES books(book_id))
""")

the_customers = [('Jim','Chainsaw man VII','greeting card',1,1,1),
('Pam',('The Humans', "Pug's Snow Day"),3,2,0,1), (3,'Beaton','Kate'),
(4,'Telgemeier','Raina'), (5,'Tolkien','J.R.R.'),
(6,'King','Stephen'), (7,'Shinkai','Makoto'),
(8,'Horikoshi','Kohei'), (9,'Darwin','Charles'),
(10,'Hawking','Stephen'), (11,'Gries','Paul'),
(12, 'Campbell', 'Jennifer'), (13,'Montojo','Jason'),
(14,'May','Kyla'),(15,'Arakawa', 'Hiromu'),
(16,'Oda','Eiichiro'),(17,'Fujimoto','Tatsuki'),
(18,'Dami','Elisabetta'),(19,'Kinney','Jeff'),
(20,'Green','John'),(21,'Bloom','Judy'),
(22,'Baker','Chandler'),(23,'King','Wesley'),
(24,'Light','Alex'),(25,'Haig','Matt')]

c.execute("""INSERT INTO customers (cust_name, num_books, num_accessories, regular_status) VALUES ('Pam', 2, 0, 1)""")
c.execute("""INSERT INTO customers (cust_name, num_books, num_accessories, regular_status) VALUES ('Jim', 1, 2, 1)""")
c.execute("""INSERT INTO customers (cust_name, num_books, num_accessories, regular_status) VALUES ('Dwight', 1, 0, 0)""")
c.execute("""INSERT INTO customers (cust_name, num_books, num_accessories, regular_status) VALUES ('Kevin', 0, 2, 0)""")

c.execute("""INSERT INTO books_bought (cust_id,book_id, book_title) VALUES
    (3, 30, 'Harry Potter and the Goblet of Fire')""")
c.execute("""INSERT INTO books_bought (cust_id, book_id, book_title) VALUES
    (2, 17, 'Chainsaw man VI')""")

c.execute("""INSERT INTO books_bought (cust_id, book_id, book_title) VALUES
    (1, 25, 'The Humans')""")
c.execute("""INSERT INTO books_bought (cust_id, book_id, book_title) VALUES (1, 12, "Pug's Snow Day")""")

c.execute("""DROP TABLE IF EXISTS accessories_bought""")
c.execute("""CREATE TABLE IF NOT EXISTS accessories_bought (
    cust_id INTEGER,
    accessory_id INTEGER,
    accessory_item TEXT,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
    FOREIGN KEY (accessory_id) REFERENCES accessories(item_id))"""
)

c.execute("""INSERT INTO accessories_bought (cust_id, accessory_id, accessory_item) VALUES
    (2, 35, 'greeting card'),
    (2, 37, 'notebook')
""")

c.execute("""INSERT INTO accessories_bought (cust_id, accessory_id, accessory_item) VALUES
    (4, 33, 'water bottle'),
    (4, 34, 'ballpoint pen')
""")

#Let's calculate what each customer paid for accessories-left join 


c.execute("""SELECT
    customers.cust_id,
    customers.cust_name,
    SUM(accessories.price) AS total_price
FROM
    customers
LEFT JOIN
    accessories_bought ON customers.cust_id = accessories_bought.cust_id
LEFT JOIN
    accessories ON accessories_bought.accessory_id = accessories.item_id
GROUP BY
    customers.cust_id, customers.cust_name""")

c.execute("""SELECT
    customers.cust_id,
    customers.cust_name,
    SUM(books.price) AS total_price
FROM
    customers
LEFT JOIN
    books_bought ON customers.cust_id = books_bought.cust_id
LEFT JOIN
    books ON books_bought.book_id = books.book_id
GROUP BY
    customers.cust_id, customers.cust_name""")

#customers who bought both books and accessories_JIM 

c.execute("""SELECT customers.cust_id,customers.cust_name,accessories_bought.accessory_item,books_bought.book_title 
FROM customers
INNER JOIN 
books_bought
ON customers.cust_id=books_bought.cust_id
INNER JOIN
accessories_bought
ON accessories_bought.cust_id=books_bought.cust_id""")

#calculate the total price paid per customer including HST 

#Looking at the customers table, Pam bought 2 books and no accessories.


c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    SUM(books.price)*1.13 AS total_price
FROM
    customers
LEFT JOIN
    books_bought ON customers.cust_id = books_bought.cust_id
LEFT JOIN
    books ON books_bought.book_id = books.book_id
    WHERE cust_name='Pam'""")
total_price_pam=c.fetchone()[2]
print(total_price_pam)

#Looking at the customers table, Dwight bought 1 book and no accessories.
c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    SUM(books.price)*1.13 AS total_price
FROM
    customers
LEFT JOIN
    books_bought ON customers.cust_id = books_bought.cust_id
LEFT JOIN
    books ON books_bought.book_id = books.book_id
    WHERE cust_name='Dwight'""")
total_price_dwight=c.fetchone()[2]
print(total_price_dwight)

#Looking at the customers table, Kevin bought no books and 2 accessories.
c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    SUM(accessories.price)*1.13 AS total_price
FROM
    customers
LEFT JOIN
    accessories_bought ON customers.cust_id = accessories_bought.cust_id
LEFT JOIN
    accessories ON accessories_bought.accessory_id = accessories.item_id
    WHERE cust_name='Kevin'""")
total_price_kevin=c.fetchone()[2]
print(total_price_kevin)
#Looking at the customers table, Jim bought 1 book and 2 accessories.
price_accessories=c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    SUM(books.price) AS total_price
FROM
    customers
LEFT JOIN
    books_bought ON customers.cust_id = books_bought.cust_id
LEFT JOIN
    books ON books_bought.book_id = books.book_id
    WHERE cust_name='Jim'""")

price_books=c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    SUM(accessories.price) AS total_price
FROM
    customers
LEFT JOIN
    accessories_bought ON customers.cust_id = accessories_bought.cust_id
LEFT JOIN
    accessories ON accessories_bought.accessory_id = accessories.item_id
    WHERE cust_name='Jim'""")

result=c.fetchone()


#a
c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    COALESCE(SUM(books.price), 0) AS total_books_price
FROM
    customers
LEFT JOIN
    books_bought ON customers.cust_id = books_bought.cust_id
LEFT JOIN
    books ON books_bought.book_id = books.book_id
WHERE cust_name='Jim'
GROUP BY customers.cust_id, customers.cust_name
""")

# Fetch the result
books_result = c.fetchone()


# Query to get the total amount spent on accessories by Jim
c.execute("""SELECT customers.cust_id,
    customers.cust_name,
    COALESCE(SUM(accessories.price), 0) AS total_accessories_price
FROM
    customers
LEFT JOIN
    accessories_bought ON customers.cust_id = accessories_bought.cust_id
LEFT JOIN
    accessories ON accessories_bought.accessory_id = accessories.item_id
WHERE cust_name='Jim'
GROUP BY customers.cust_id, customers.cust_name
""")

# Fetch the result
accessories_result = c.fetchone()
print(accessories_result)

# Combine the results
total_books_price = books_result[2] 
total_accessories_price = accessories_result[2] 
total_price_jim= (total_books_price + total_accessories_price)*1.13

# Print or use the total price
print("Total amount spent by Jim:", total_price_jim)

#Create table of total amount paid 

#total cost of books bought 

c.execute("""SELECT SUM(books.cost) AS total_bookcost
FROM books
INNER JOIN 
books_bought 
ON books.book_id=books_bought.book_id""")
books_cost=c.fetchone()[0]
print(books_cost)

#total cost of accessories bought
c.execute("""SELECT SUM(accessories.cost) AS total_accessorycost
FROM accessories
INNER JOIN 
accessories_bought 
ON accessories.item_id=accessories_bought.accessory_id""")
accessory_cost=c.fetchone()[0]
print(accessory_cost)

#total costs of books and accessories 
total_costs=books_cost+accessory_cost
print(total_costs)

#total amount paid by all customers 
total_amount_paid=total_price_pam+total_price_dwight+total_price_kevin+total_price_jim
print(total_amount_paid)

#total profit generated from books and accessories bought
total_profit=total_amount_paid-total_costs
print(total_profit)






def show_total_costs():
    c.execute("SELECT SUM(cost) FROM books UNION ALL SELECT SUM(cost) FROM accessories")
    total_costs = c.fetchone()[0]
    messagebox.showinfo("Total Costs", f"Total Costs: {total_costs}")

def show_total_profits():
    # Assume total_amount_paid and total_costs are available
    total_profit = total_amount_paid - total_costs
    messagebox.showinfo("Total Profits", f"Total Profits: {total_profit}")
def show_total_costs():
    messagebox.showinfo("Total Costs", f"Total Costs: {total_costs}")



# Create buttons for total costs and profits
btn_show_total_costs = tk.Button(app, text="Show Total Costs", command=show_total_costs)
btn_show_total_costs.pack()

btn_show_total_profits = tk.Button(app, text="Show Total Profits", command=show_total_profits)
btn_show_total_profits.pack()



# Run the application loop
app.mainloop()


connection.commit()
connection.close()




