import json
import os
from datetime import datetime

# Path where user-specific JSON files will be stored
USER_DB_PATH = "user_data"

# Ensure the directory exists
os.makedirs(USER_DB_PATH, exist_ok=True)

def load_user_data(user_id):
    """
    Load the user data from their specific JSON file.
    If the file does not exist, return an empty dictionary.
    """
    user_file = os.path.join(USER_DB_PATH, f"{user_id}.json")
    if os.path.exists(user_file):
        try:
            with open(user_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If file exists but is corrupted, reset it
            return {}
    return {}

def save_user_data(user_id, data):
    """
    Save the user data to their specific JSON file.
    Creates or overwrites the file with the provided data.
    """
    user_file = os.path.join(USER_DB_PATH, f"{user_id}.json")
    with open(user_file, "w") as file:
        json.dump(data, file, indent=4)

def add_user_to_database(user):
    """
    Add a new user to their own JSON file.
    Returns True if a new user is added, False if the user already exists.
    """
    user_id = str(user.id)
    if not os.path.exists(os.path.join(USER_DB_PATH, f"{user_id}.json")):
        user_data = {
            "username": user.username,
            "name": user.full_name,
            "date_joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": 1,
            "inventory": [],
            "started_prologue": False,
            "completed_prologue": False,
        }
        save_user_data(user_id, user_data)
        return True  # New user added
    return False  # User already exists

def update_user_progress(user_id, started=False, completed=False):
    """
    Update the user's progress in their own JSON file.
    Updates 'started_prologue' and/or 'completed_prologue' as specified.
    """
    user_data = load_user_data(user_id)

    if started:
        user_data["started_prologue"] = True
    if completed:
        user_data["completed_prologue"] = True

    save_user_data(user_id, user_data)

def check_user_progress(user_id):
    """
    Check if the user has started or completed the prologue.
    Returns a tuple: (started_prologue, completed_prologue)
    """
    user_data = load_user_data(user_id)
    return (
        user_data.get("started_prologue", False),
        user_data.get("completed_prologue", False),
    )

def update_user_level(user_id, level_increment=1):
    """
    Increment the user's level by the specified amount.
    If the user data does not exist, it creates the data with default values.
    """
    user_data = load_user_data(user_id)
    user_data["level"] = user_data.get("level", 1) + level_increment
    save_user_data(user_id, user_data)

def add_to_inventory(user_id, item):
    """
    Add an item to the user's inventory.
    If the user data does not exist, it creates the data with default values.
    """
    user_data = load_user_data(user_id)
    inventory = user_data.get("inventory", [])
    inventory.append(item)
    user_data["inventory"] = inventory
    save_user_data(user_id, user_data)

def get_user_inventory(user_id):
    """
    Retrieve the user's inventory.
    Returns an empty list if the user does not have an inventory.
    """
    user_data = load_user_data(user_id)
    return user_data.get("inventory", [])

def reset_user_data(user_id):
    """
    Reset a user's data to the default structure.
    Useful for testing or reinitializing a user's progress.
    """
    user_file = os.path.join(USER_DB_PATH, f"{user_id}.json")
    user_data = {
        "username": None,
        "name": None,
        "date_joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": 1,
        "inventory": [],
        "started_prologue": False,
        "completed_prologue": False,
    }
    save_user_data(user_id, user_data)