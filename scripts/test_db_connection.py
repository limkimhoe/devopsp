import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_connection():
    """Tests the connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        print("Connection to the database was successful!")
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The psycopg2 library might not be installed by default.
    # Let's ensure it's installed before running the test.
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 is not installed. Please install it by running:")
        print("pip install psycopg2-binary")
        exit(1)
    
    test_connection()
