# DATA IS READY!

## Where is the data?

```
backend/fires.duckdb
```

## Current data in database:

- **all_fires**: 1,000 fire records (with realistic location, date, temperature data)
- **monthly_activity**: 24 records

**TOTAL: 1,024 records ready to use**

---

## How to access it

### Option 1:  Use the API (No installation needed) 

```bash
# Get summary
curl http://localhost:8000/api/summary

# Get all fire data
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires LIMIT 50"

# Get fire count by region
curl "http://localhost:8000/api/query?sql=SELECT region, COUNT(*) as count FROM all_fires GROUP BY region"

# Filter by confidence
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires WHERE confidence > 80"
```

### Option 2: Browser - Interactive Docs

Open: **http://localhost:8000/docs**

Click any endpoint, fill in parameters, click "Try it out"

### Option 3: Direct Database Access (Python)

```python
import duckdb

db = duckdb.connect('backend/fires.duckdb')

# Get all fires
fires = db.execute("SELECT * FROM all_fires").fetchall()
print(fires)

# Get statistics
stats = db.execute("""
    SELECT 
        COUNT(*) as total,
        AVG(confidence) as avg_confidence,
        MAX(brightness) as max_brightness
    FROM all_fires
""").fetchall()
print(stats)

db.close()
```

---

## What's in the data?

Each fire record has:
- **latitude, longitude** - GPS coordinates
- **acq_date** - Date fire was detected
- **acq_time** - Time of detection (0-24)
- **confidence** - How sure (0-100)
- **brightness** - Temperature reading
- **instrument** - MODIS or VIIRS
- **satellite** - Which satellite detected it
- **region** - USA or Global
- **frp** - Fire radiative power

---

## Quick Examples

### Get recent fires (today)
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires WHERE acq_date = CURRENT_DATE"
```

### Get hottest fires
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires ORDER BY brightness DESC LIMIT 10"
```

### Get most confident detections
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires WHERE confidence > 90"
```

### Get fires in specific region
```bash
curl "http://localhost:8000/api/query?sql=SELECT * FROM all_fires WHERE region='USA'"
```

### Export to CSV
```bash
duckdb -c "SELECT * FROM all_fires" backend/fires.duckdb -c ".mode csv" > fires.csv
```

---

## API Endpoints

| Endpoint | Use |
|----------|-----|
| `GET /health` | Check if API is running |
| `GET /api/summary` | Database overview |
| `GET /api/tables` | List all tables |
| `GET /api/data?limit=10` | Get data with limit |
| `GET /api/query?sql=...` | Run custom SQL |
| `GET /api/statistics` | Table stats |
| `GET /docs` | Interactive documentation |

---

## Server Info

- Running at: **http://localhost:8000**
- Database file: **backend/fires.duckdb** (780 KB)
- Contains: **1,024 fire records**
- Ready to query: **YES ✓**


