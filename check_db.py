import sqlite3

# Connect to the database
conn = sqlite3.connect('snapcalorie.db')
c = conn.cursor()

# Get all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("Tables:", tables)

# Get structure of users table
c.execute("PRAGMA table_info(users)")
users_table = c.fetchall()
print("Users table:", users_table)

# Get structure of food_logs table
c.execute("PRAGMA table_info(food_logs)")
food_logs_table = c.fetchall()
print("Food logs table:", food_logs_table)

# Check if there are any users
c.execute("SELECT * FROM users")
users = c.fetchall()
print("Users:", users)

# Check if there are any food logs
c.execute("SELECT * FROM food_logs")
food_logs = c.fetchall()
print("Food logs:", food_logs)

conn.close()