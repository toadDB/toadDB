# ToadDB Database Management System

ToadDB is a simple database management system implemented in Python, using SQLite as the underlying database engine. This system allows for versatile data handling, including creating tables, inserting data, fetching data, and closing connections.

## Features

- **Table Creation**: Easily create tables in the database with specified columns.
- **Data Insertion**: Insert data into the tables seamlessly.
- **Data Retrieval**: Fetch data from the tables with optional filtering conditions.
- **Connection Management**: Close the database connection when done.

## Usage

1. **Initialization**: Initialize the `DatabaseManager` class with the name of the SQLite database file.
2. **Table Creation**: Use the `create_table` method to create tables with specified columns.
3. **Data Insertion**: Insert data into the tables using the `insert_data` method.
4. **Data Retrieval**: Fetch data from the tables with optional filtering conditions using the `fetch_data` method.
5. **Connection Closing**: Close the database connection when finished with the `close_connection` method.

## Example

```python
if __name__ == "__main__":
    try:
        db_manager = DatabaseManager("my_database.db")
        
        # Create a table
        db_manager.create_table("students", ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"])
        
        # Insert data
        db_manager.insert_data("students", (1, "Alice", 25))
        db_manager.insert_data("students", (2, "Bob", 22))
        
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
