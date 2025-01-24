import logging
from database import Database  # Import the Database class

# Configure logging for better visibility of the process
logging.basicConfig(level=logging.DEBUG)

def main():
    """ Build the database and demonstrate its usage """
    db = Database()
    
    try:
        # Build the database (downloads, processes, and stores data)
        db._build_database()
        print("Database built successfully!")
        
        # Check the number of entries in the database
        print(f"Number of CWE entries in the database: {db.count}")
        
        # Example: Get details for a specific CWE (e.g., CWE-15)
        cwe = db.get(15)
        if cwe:
            print(f"\nDetails of CWE-15:\n{cwe}")
        else:
            print("CWE-15 not found in the database.")

        # Example: Get the top 25 weaknesses
        top_25 = db.get_top_25()
        print(f"\nTop 25 Weaknesses:\n{top_25}")

    except Exception as e:
        logging.error(f"Error during database build or usage: {e}")

if __name__ == "__main__":
    main()