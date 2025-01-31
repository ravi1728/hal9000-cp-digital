from config import POSTGRE_DATABASE
import psycopg2
from psycopg2.extras import DictCursor


def get_db_connection():
    """Establish a new database connection."""
    return psycopg2.connect(**POSTGRE_DATABASE)

def find_rows(tablename, filters):
    """
    Find rows in the given table that match the filter conditions.
    Args:
        tablename (str): The name of the table.
        filters (dict): A dictionary where keys are column names and values are the values to filter by.

    Returns:
        list: A list of matching rows as dictionaries.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)

    where_clause = " AND ".join(f"{key} = %s" for key in filters.keys())
    values = list(filters.values())

    sql = f"SELECT * FROM {tablename} WHERE {where_clause};"
    
    try:
        cur.execute(sql, values)
        results = cur.fetchall()
        return [dict(row) for row in results]
    finally:
        cur.close()
        conn.close()

def create_or_update_row(tablename, data, primary_keys):
    """
    Insert a row if it doesn't exist, otherwise update it.

    Args:
        tablename (str): The name of the table.
        data (dict): The data to insert or update.
        primary_keys (list): List of column names that act as primary keys.

    Returns:
        None
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the row already exists
    filters = {key: data[key] for key in primary_keys}
    existing_rows = find_rows(tablename, filters)

    if existing_rows:
        if len(data) == len(primary_keys):
            pass
        else:
            # If row exists, update it
            set_clause = ", ".join(f"{key} = %s" for key in data.keys() if key not in primary_keys)
            where_clause = " AND ".join(f"{key} = %s" for key in primary_keys)
            values = list(data.values()) + [data[key] for key in primary_keys]

            update_sql = f"UPDATE {tablename} SET {set_clause} WHERE {where_clause};"
            cur.execute(update_sql, values)
    else:
        # If row doesn't exist, insert it
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        insert_sql = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders});"
        cur.execute(insert_sql, list(data.values()))

    conn.commit()
    cur.close()
    conn.close()

    return find_rows(tablename, filters)[0]
