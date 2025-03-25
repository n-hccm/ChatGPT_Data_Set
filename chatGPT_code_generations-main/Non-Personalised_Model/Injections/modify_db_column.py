#make a python snippet that modifies an sql database column
import sqlite3

# Database connection
db_name = "example.db"  # Replace with your DB name
table_name = "users"     # Replace with your table name
old_column = "age"        # Column to modify
new_column = "age_in_years"  # New column name
new_type = "INTEGER"     # New data type
#make a python snippet that modifies an sql database column
# Connect to the database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Rename column example (SQLite syntax)
try:
    cursor.execute(f"""
        ALTER TABLE {table_name} RENAME COLUMN {old_column} TO {new_column};
    """)
    print(f"Column '{old_column}' renamed to '{new_column}'")

    # Modify data type (SQLite requires creating a new table to modify types)
    cursor.execute(f"""
        CREATE TABLE new_{table_name} AS
        SELECT *, CAST({new_column} AS {new_type}) AS {new_column}_cast
        FROM {table_name};
    """)

    # Drop the old column and rename the cast column
    cursor.execute(f"""
        ALTER TABLE new_{table_name} RENAME COLUMN {new_column}_cast TO {new_column};
    """)
    
    # Replace the old table with the new one
    cursor.execute(f"DROP TABLE {table_name};")
    cursor.execute(f"ALTER TABLE new_{table_name} RENAME TO {table_name};")

    conn.commit()
    print("Column type modified successfully!")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.close()

#bad
#sql injections
#no parameterised queries
#no input validation
#no checks to see if columns exist
#data integrity is not maintained
#no roll backs, causes data inconsitency. 
