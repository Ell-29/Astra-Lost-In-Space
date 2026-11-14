from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import duckdb
from typing import Optional

app = FastAPI(title="Fire Data API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    """Create database connection"""
    return duckdb.connect('fires.duckdb', read_only=False)

@app.get("/health")
def health():
    """Check if API is running"""
    return {"status": "ok", "message": "API is running"}

@app.get("/api/summary")
def get_summary():
    """Get database summary"""
    db = get_db()
    
    all_fires_count = db.execute("SELECT COUNT(*) FROM all_fires").fetchone()[0]
    monthly_count = db.execute("SELECT COUNT(*) FROM monthly_activity").fetchone()[0]
    
    return {
        "all_fires_records": all_fires_count,
        "monthly_activity_records": monthly_count,
        "total_records": all_fires_count + monthly_count
    }

@app.get("/api/tables")
def list_tables():
    """List all tables in database"""
    db = get_db()
    tables = db.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
    ).fetchall()
    return {"tables": [t[0] for t in tables]}

@app.get("/api/data")
def get_data(limit: int = Query(10, ge=1, le=1000)):
    """Get fire data with limit"""
    db = get_db()
    result = db.execute(f"SELECT * FROM all_fires LIMIT {limit}").fetchall()
    columns = [desc[0] for desc in db.description]
    
    return {
        "columns": columns,
        "data": result,
        "count": len(result)
    }

@app.get("/api/query")
def query(sql: str = Query(...)):
    """Run custom SQL query (SELECT only)"""
    if not sql.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries allowed"}
    
    db = get_db()
    try:
        result = db.execute(sql).fetchall()
        return {
            "query": sql,
            "results": result,
            "count": len(result)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/statistics")
def get_statistics():
    """Get statistics from database"""
    db = get_db()
    
    stats = db.execute("""
        SELECT 
            COUNT(*) as total_fires,
            AVG(confidence) as avg_confidence,
            MAX(brightness) as max_brightness,
            MIN(brightness) as min_brightness,
            COUNT(DISTINCT region) as unique_regions
        FROM all_fires
    """).fetchone()
    
    return {
        "total_fires": stats[0],
        "avg_confidence": round(stats[1], 2) if stats[1] else 0,
        "max_brightness": round(stats[2], 2) if stats[2] else 0,
        "min_brightness": round(stats[3], 2) if stats[3] else 0,
        "unique_regions": stats[4]
    }

@app.get("/api/monthly-activity")
def get_monthly_activity():
    """Get monthly activity summary"""
    db = get_db()
    result = db.execute("SELECT * FROM monthly_activity ORDER BY month DESC").fetchall()
    columns = [desc[0] for desc in db.description]
    
    return {
        "columns": columns,
        "data": result,
        "count": len(result)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
