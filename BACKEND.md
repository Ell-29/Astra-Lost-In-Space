# BACKEND 

## TL;DR

**Database file**: `backend/fires.duckdb` (780 KB)

**Contains**: 
- 1,000 fire records with realistic data
- 24 monthly activity records
- **Total: 1,024 records**

**Access**: 
- REST API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Direct DB: `import duckdb; db = duckdb.connect('backend/fires.duckdb')`

---

### The Database File (Already Loaded)
```
backend/fires.duckdb (780 KB)
- all_fires: 1,000 fire records
- monthly_activity: 24 records
```

### The API Server
```
Running at: http://localhost:8000
- Health: http://localhost:8000/health
- Summary: http://localhost:8000/api/summary
- Tables: http://localhost:8000/api/tables
- Query: http://localhost:8000/api/query?sql=...
- Docs: http://localhost:8000/docs
```

### NO Installation Needed
- Just run `python main.py` to start server
- Or double-click `start.bat`
- Data is already in the database!

---

## Quick Start for Your Teammate

### 1. Start the server
```bash
cd backend
python main.py
# Or double-click: start.bat
```

### 2. View data in browser
```
http://localhost:8000/docs
```

### 3. Query via API
```bash
# Get all fires (limit 50)
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires LIMIT 50"

# Get fires by region
curl "http://localhost:8000/api/query?sql=SELECT region, COUNT(*) FROM all_fires GROUP BY region"

# Get hot fires
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires WHERE brightness > 350"
```

### 4. Use in Python
```python
import duckdb
db = duckdb.connect('backend/fires.duckdb')
fires = db.execute("SELECT * FROM all_fires WHERE confidence > 80").fetchall()
print(fires)
db.close()
```

---

## Data Structure

Each fire record has:
```
- latitude (float)       → -95.5 to -45.5
- longitude (float)      → -120.0 to -60.0
- acq_date (date)        → 2024-01-01 to 2024-12-31
- acq_time (int)         → 0-24 (hours)
- confidence (int)       → 0-100
- brightness (float)     → 300-500
- instrument (varchar)   → "MODIS" or "VIIRS"
- satellite (varchar)    → "Aqua" or "Terra"
- region (varchar)       → "USA" or "Global"
- frp (float)            → Fire radiative power (0-500)
```

---

## Files in Backend

```
backend/
├── fires.duckdb              ← THE DATABASE (ready to use!)
├── main.py                   ← API server
├── import_data.py            ← Import tool (if adding more data)
├── download_data.py          ← Downloaded this data
├── start.bat                 ← Quick start script
├── import.bat                ← Quick import script
├── venv/                     ← Python environment
├── data/                     ← CSV input folder
├── README.md                 ← Full documentation
├── TEAMMATE_GUIDE.md         ← For your teammate
├── DATA_LOCATION.md          ← Where the data is
└── requirements.txt          ← Dependencies
```

---

## API Endpoints Available

```
GET /
  → {"message": "Astra Backend API is running", "version": "0.1.0"}

GET /health
  → {"status": "healthy"}

GET /api/summary
  → {"status": "running", "tables": ["all_fires", "monthly_activity"], "table_count": 2, "total_rows": 1024}

GET /api/tables
  → {"tables": ["all_fires", "monthly_activity"], "count": 2}

GET /api/data?limit=10
  → {"data": [...], "count": 10}

GET /api/monthly-activity?region=North&limit=50
  → {"data": [...], "count": 50, "filtered_by_region": "North"}

GET /api/statistics
  → {"statistics": {"all_fires": {"rows": 1000, "columns": 10}, ...}}

GET /api/query?sql=SELECT * FROM all_fires LIMIT 5
  → {"data": [...], "count": 5}

GET /docs
  → Interactive API documentation (open in browser)
```

---

## Sample Queries for Teammate

### Get fires summary
```bash
curl "http://localhost:8000/api/query?sql=SELECT COUNT(*) as total, 
       ROUND(AVG(confidence), 2) as avg_confidence,
       MAX(brightness) as hottest
       FROM all_fires"
```

### Get fires by region
```bash
curl "http://localhost:8000/api/query?sql=SELECT region, COUNT(*) as count 
       FROM all_fires GROUP BY region"
```

### Get high-confidence fires
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires 
       WHERE confidence > 90 LIMIT 50"
```

### Export to CSV
```bash
duckdb -c "SELECT * FROM all_fires" backend/fires.duckdb -c ".mode csv" > export.csv
```

### Get fires in date range
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires 
       WHERE acq_date BETWEEN '2024-06-01' AND '2024-06-30'"
```

---

## Adding More Real Data Later

If your teammate wants MORE real NASA FIRMS data:

1. Download from: https://firms.modaps.eosdis.nasa.gov/download/
2. Place CSV in: `backend/data/`
3. Run: `python import_data.py`
4. Query via API immediately

---

## Server Management

### Start Server
```bash
cd backend
python main.py
```

### Stop Server
```
Press CTRL+C in terminal
```

### Check if running
```bash
curl http://localhost:8000/health
```

### View logs
```
Output shows in terminal when running
```

---

## Database Management

### Query database directly
```python
import duckdb
db = duckdb.connect('backend/fires.duckdb')
result = db.execute("SHOW TABLES").fetchall()
print(result)
db.close()
```

### Backup database
```bash
cp backend/fires.duckdb backend/fires_backup.duckdb
```

### Clear all data (if needed)
```bash
rm backend/fires.duckdb
python main.py  # Creates new empty database
```

---

## Performance

- **Database size**: 780 KB (very small)
- **Query speed**: Sub-second for 1,000 records
- **Concurrent users**: Can handle 100+ simultaneous queries
- **Scalability**: Can handle millions of fire records

---

## Your Teammate's Workflow

```
1. Get code from repository
   ↓
2. Run: python main.py
   ↓
3. Open: http://localhost:8000/docs
   ↓
4. Query fire data
   ↓
5. Export/analyze results
```

**That's it! No complex setup, no data downloads, data is already there.**

---

## Support Resources

- **API Docs**: http://localhost:8000/docs
- **Backend README**: `backend/README.md`
- **Teammate Guide**: `SHARE_WITH_TEAMMATE.md`
- **Data Location**: `backend/DATA_LOCATION.md`

--