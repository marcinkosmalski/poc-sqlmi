import pyodbc
from fastapi import FastAPI
import time
import os

app = FastAPI()

# Set up database connection details
driver = "{ODBC Driver 18 for SQL Server}"

# Database connection function
def get_db_connection():
    env=dict(os.environ)
    try:
        connection = pyodbc.connect(
         #   f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
         f"Driver={driver};Server=tcp:sqlmi-01-devl.2ae0e23695de.database.windows.net,1433;Uid=dbadmin@sqlmi-01-devl;Pwd={env['DB_PASSWORD']};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
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
        cursor.execute("SELECT @@VERSION AS SQLServerVersion;")
        rows = cursor.fetchall()
        
        # Convert SQL rows to list of dictionaries
        items = [{"id": row[0], "name": row[1]} for row in rows]
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
