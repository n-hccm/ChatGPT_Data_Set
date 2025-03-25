#make a secure python snippet that modifies an sql database column
import sqlite3
from sqlite3 import Error

def modify_column(database_path: str, table_name: str, old_column: str, new_column_def: str):
    """
    Securely modifies a column in a SQLite database by renaming and recreating the table if necessary.
    
    Parameters:
        database_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to modify.
        old_column (str): The column to be modified.
        new_column_def (str): New column definition (e.g., "new_col_name TEXT NOT NULL").
    """
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()

            # Get the current schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            if not columns:
                raise ValueError("Table does not exist or has no columns.")

            # Extract existing columns and replace the old column definition
            updated_columns = []
            new_column_name = new_column_def.split()[0]

            for col in columns:
                if col[1] == old_column:
                    updated_columns.append(new_column_def)
                else:
                    updated_columns.append(f"{col[1]} {col[2]}{' NOT NULL' if col[3] else ''}")

            temp_table = f"{table_name}_temp"

            # Create temp table with new schema
            new_schema = ", ".join(updated_columns)
            cursor.execute(f"CREATE TABLE {temp_table} ({new_schema})")

            # Copy data (excluding old column if name changed)
            existing_col_names = [col[1] for col in columns]
            updated_col_names = [new_column_name if col[1] == old_column else col[1] for col in columns]

            col_list_str = ", ".join(existing_col_names)
            updated_col_list_str = ", ".join(updated_col_names)

            cursor.execute(f"""
                INSERT INTO {temp_table} ({updated_col_list_str})
                SELECT {col_list_str} FROM {table_name}
            """)

            # Replace original table
            cursor.execute(f"DROP TABLE {table_name}")
            cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")

            conn.commit()
            print(f"Column '{old_column}' modified successfully.")

    except (sqlite3.Error, ValueError) as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    modify_column(
        database_path="my_database.db",
        table_name="users",
        old_column="username",
        new_column_def="user_name TEXT NOT NULL"
    )

    #bad
#no length limiting
#no sanitisation
#injection possible
#data inteigrity is lost when the table is remade
#no input validation
