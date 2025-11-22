import bcrypt
import os

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except ValueError:
        print("Error: Invalid hash format.")
        return False

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
        
    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username = line.strip().split(',')[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False
    except IndexError:
        print(f"Warning: Skipping corrupted line in {USER_DATA_FILE}")
        
    return False

def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
        
    hashed_password = hash_password(password)
    
    try:
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{username},{hashed_password}\n")
        print(f"Success: User '{username}' registered successfully!")
        return True
    except IOError as e:
        print(f"Error: Could not write to user file. {e}")
        return False

def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered. Please register an account.")
        return False

    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                try:
                    stored_username, stored_hash = line.strip().split(',', 1)
                    
                    if stored_username == username:
                        if verify_password(password, stored_hash):
                            print(f"Success: Welcome, {username}!")
                            return True
                        else:
                            print("Error: Invalid password.")
                            return False
                except ValueError:
                    print(f"Warning: Skipping corrupted line in {USER_DATA_FILE}")
                    continue

    except FileNotFoundError:
        print("Error: User data file not found.")
        return False
    except IOError as e:
        print(f"Error: Could not read user file. {e}")
        return False

    print("Error: Username not found.")
    return False

def validate_username(username):
    if not (3 <= len(username) <= 20):
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum():
        return False, "Username must be alphanumeric (letters and numbers only)."
    return True, ""

def validate_password(password):
    if not (6 <= len(password) <= 50):
        return False, "Password must be between 6 and 50 characters."
    # Use built-in functions instead of regex
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""

def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n [1] Register a new user")
    print(" [2] Login")
    print(" [3] Exit")
    print("-"*50)

def main():
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
            
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()