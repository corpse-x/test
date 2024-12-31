import psycopg2
from psycopg2.extras import Json
from datetime import datetime

# PostgreSQL connection string
DB_URL = "postgresql://postgres:WUcp0oe6jS5DtnUY@tastelessly-delicate-moccasin.data-1.use1.tembo.io:5432/postgres"

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(DB_URL)

def add_user_to_database(user):
    """
    Add a new user to the PostgreSQL database.
    Returns True if a new user is added, False if the user already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (user_id, username, full_name, date_joined)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING;
        """, (user.id, user.username, user.full_name, datetime.now()))
        conn.commit()
        return cursor.rowcount > 0  # True if a new row was inserted
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_user_progress(user_id, started=False, completed=False):
    """
    Update the user's progress in the PostgreSQL database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if started:
            cursor.execute("UPDATE users SET started_prologue = TRUE WHERE user_id = %s", (user_id,))
        if completed:
            cursor.execute("UPDATE users SET completed_prologue = TRUE WHERE user_id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error updating progress: {e}")
    finally:
        cursor.close()
        conn.close()

def check_user_progress(user_id):
    """
    Check if the user has started or completed the prologue.
    Returns a tuple: (started_prologue, completed_prologue)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT started_prologue, completed_prologue FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]
        return False, False
    except Exception as e:
        print(f"Error checking progress: {e}")
        return False, False
    finally:
        cursor.close()
        conn.close()

def update_user_level(user_id, level_increment=1):
    """
    Increment the user's level by the specified amount.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET level = level + %s WHERE user_id = %s", (level_increment, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating user level: {e}")
    finally:
        cursor.close()
        conn.close()

def add_to_inventory(user_id, item):
    """
    Add an item to the user's inventory.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT inventory FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            inventory = result[0] if result[0] else []
            inventory.append(item)
            cursor.execute("UPDATE users SET inventory = %s WHERE user_id = %s", (Json(inventory), user_id))
            conn.commit()
    except Exception as e:
        print(f"Error updating inventory: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_inventory(user_id):
    """
    Retrieve the user's inventory.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT inventory FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result and result[0]:
            return result[0]
        return []
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def reset_user_data(user_id):
    """
    Reset a user's data to default values in the PostgreSQL database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET level = 1, inventory = %s, started_prologue = FALSE, completed_prologue = FALSE
            WHERE user_id = %s
        """, (Json([]), user_id))
        conn.commit()
    except Exception as e:
        print(f"Error resetting user data: {e}")
    finally:
        cursor.close()
        conn.close()
