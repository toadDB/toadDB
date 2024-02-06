# This is simple code used as an example using SQLite as the database management system for versatile data handling.
# (c) toadDB 2024

import sqlite3
import logging

class DatabaseManager:
    def __init__(self, db_name):
        """
        Initialize the DatabaseManager class with the given database name.
        Establishes a connection to the SQLite database.
        
        Args:
            db_name (str): The name of the SQLite database file.
        """
        self._validate_db_name(db_name)
        try:
            self.conn = sqlite3.connect(db_name)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def _validate_db_name(self, db_name):
        if not isinstance(db_name, str):
            raise ValueError("Database name must be a string.")
        if not db_name.endswith('.db'):
            raise ValueError("Database name must end with '.db'.")

    def _validate_table_name(self, table_name):
        if not isinstance(table_name, str):
            raise ValueError("Table name must be a string.")
        if not table_name.isidentifier():
            raise ValueError("Table name must be a valid identifier.")

    def _validate_column_names(self, columns):
        for column in columns:
            if not isinstance(column, str):
                raise ValueError("Column names must be strings.")
            if not column.isidentifier():
                raise ValueError("Column name must be a valid identifier.")
    
    # Method to execute SQL queries
    def _execute_query(self, query, data=None):
        try:
            if data:
                self.cur.execute(query, data)
            else:
                self.cur.execute(query)
            self.conn.commit()
            return self.cur.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            raise
    
    def create_table(self, table_name, columns):
        """
        Create a new table in the database with the given name and columns.
        
        Args:
            table_name (str): The name of the table to be created.
            columns (list of str): The list of column definitions for the table.
        """
        self._validate_table_name(table_name)
        self._validate_column_names(columns)
        try:
            columns_str = ', '.join(columns)
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            self._execute_query(create_table_sql)
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
            raise
    
    def insert_data(self, table_name, data):
        """
        Insert data into the specified table.
        
        Args:
            table_name (str): The name of the table to insert data into.
            data (tuple): The data to be inserted into the table.
        """
        self._validate_table_name(table_name)
        try:
            placeholders = ', '.join(['?' for _ in range(len(data))])
            insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self._execute_query(insert_sql, data)
        except sqlite3.Error as e:
            logging.error(f"Error inserting data: {e}")
            raise
    
    def fetch_data(self, table_name, condition=None):
        """
        Fetch data from the specified table.
        
        Args:
            table_name (str): The name of the table to fetch data from.
            condition (str, optional): The condition to filter the fetched data.
        
        Returns:
            list of tuples: The fetched data from the table.
        """
        self._validate_table_name(table_name)
        try:
            if condition:
                fetch_sql = f"SELECT * FROM {table_name} WHERE {condition}"
            else:
                fetch_sql = f"SELECT * FROM {table_name}"
            return self._execute_query(fetch_sql)
        except sqlite3.Error as e:
            logging.error(f"Error fetching data: {e}")
            raise
    
    def close_connection(self):
        """
        Close the connection to the database.
        """
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logging.error(f"Error closing connection: {e}")
            raise

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Example usage:
if __name__ == "__main__":
    try:
        db_manager = DatabaseManager("my_database.db")
        
        # Create a table
        db_manager.create_table("students", ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"])
        
        # Insert data
        db_manager.insert_data("students", (1, "Alice", 25))
        db_manager.insert_data("students", (2, "Bob", 22))
        db_manager.insert_data("students", (3, "Justin", 18))
        db_manager.insert_data("students", (4, "Mike", 27))
        
        # Fetch data
        all_students = db_manager.fetch_data("students")
        print("All students:", all_students)
        
        # Fetch data with condition
        students_over_23 = db_manager.fetch_data("students", "age > 23")
        print("Students over 23:", students_over_23)
        
    except sqlite3.Error as e:
        logging.error(f"An SQLite error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        try:
            # Close connection
            db_manager.close_connection()
        except NameError:
            pass
