import pyodbc
from fastapi import FastAPI
import time

app = FastAPI()

# Set up database connection details
server = "your-server-name.database.windows.net"
database = "your-database-name"
username = "your-username"
password = "your-password"
driver = "{ODBC Driver 17 for SQL Server}"

# Database connection function
def get_db_connection():
    try:
        connection = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.get("/ping/")
async def ping():
    return {"status": f"All good! {time.time()})"}

# API endpoint to fetch data from the Azure SQL database
@app.get("/verify/")
async def read_items():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}

    cursor = conn.cursor()
    try:
        # Example SQL query
        cursor.execute("SELECT TOP 10 * FROM Items")
        rows = cursor.fetchall()
        
        # Convert SQL rows to list of dictionaries
        items = [{"id": row[0], "name": row[1]} for row in rows]
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
