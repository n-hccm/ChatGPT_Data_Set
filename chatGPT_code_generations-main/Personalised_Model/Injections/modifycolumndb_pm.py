#make a python snippet that modifies an sql database column
import sqlite3
import os

def modify_column(database_path, table_name, old_column, new_column, new_type):
    """
    Modifies a column name and/or type in an SQLite database table securely.

    Args:
        database_path (str): Path to the SQLite database file.
        table_name (str): Name of the table.
        old_column (str): Current name of the column to modify.
        new_column (str): New column name.
        new_type (str): New column data type.
    """
    if not os.path.isfile(database_path):
        raise FileNotFoundError(f"Database file not found at: {database_path}")
    
    # Basic validation of identifiers to prevent SQL injection
    def is_valid_identifier(name):
        return name.isidentifier() and not name.lower() in {"select", "from", "where", "table", "drop", "delete"}

    if not all(map(is_valid_identifier, [table_name, old_column, new_column])):
        raise ValueError("Invalid table or column name provided.")
    
    # Connect to database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Begin transaction
        cursor.execute("BEGIN TRANSACTION;")
        
        # Get existing table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()

        new_columns = []
        for col in columns_info:
            col_name, col_type = col[1], col[2]
            if col_name == old_column:
                col_name = new_column
                col_type = new_type
            new_columns.append((col_name, col_type))

        # Create a temporary table with modified column
        columns_sql = ", ".join(f"{name} {dtype}" for name, dtype in new_columns)
        temp_table = f"{table_name}_temp"
        cursor.execute(f"CREATE TABLE {temp_table} ({columns_sql});")

        # Copy data from old table to new table
        old_column_names = ", ".join(col[1] for col in columns_info)
        new_column_names = ", ".join(name for name, _ in new_columns)
        cursor.execute(f"INSERT INTO {temp_table} ({new_column_names}) SELECT {old_column_names} FROM {table_name};")

        # Replace old table
        cursor.execute(f"DROP TABLE {table_name};")
        cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name};")

        conn.commit()
        print("Column modified successfully.")
    except sqlite3.DatabaseError as e:
        conn.rollback()
        print(f"Database error occurred: {e}")
    finally:
        conn.close()

# Example usage
# modify_column("example.db", "users", "age", "user_age", "INTEGER")

#bad
#does not filter out all keywords / input sanitisation issues
#needs to make sure columns are ordered correctly.
#no backups / repudation
#deadlock possible
