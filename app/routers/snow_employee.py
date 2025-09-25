# app/routers/snow_employee.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from decimal import Decimal
import os
import snowflake.connector
import json

router = APIRouter(prefix="/snow", tags=["Snowflake"])

# --- Config (use env vars in production) ---
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "skillquest")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "Skillquest@123")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "KYSHCAK-SZC76532")  # replace with full locator if needed
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "SKILL_QUEST")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "DEV")

# --- Helper: connect ---
def get_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        client_session_keep_alive=True,
    )

# --- Helper: convert rows to json-serializable dicts ---
def rows_to_dicts(columns: List[str], rows: List[tuple]) -> List[dict]:
    out = []
    for r in rows:
        d = {}
        for i, col in enumerate(columns):
            val = r[i]
            # convert Decimal to float (or str if you want)
            if isinstance(val, Decimal):
                # If precision matters, consider str(val)
                d[col] = float(val)
            else:
                d[col] = val
        out.append(d)
    return out

# -------------------------
# Pydantic models
# -------------------------
class EmployeeIn(BaseModel):
    # adjust fields to match your EMPLOYEE_MASTER columns
    employee_id: Optional[int] = None
    name: str
    email: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None

class JDIn(BaseModel):
    jd_id: Optional[int] = None   # 👈 allow frontend to send jd_id
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    experience_min: Optional[Decimal] = None
    experience_max: Optional[Decimal] = None
    location: Optional[str] = None
    status: Optional[str] = None
    model_status: Optional[str] = None


# -------------------------
# EMPLOYEES endpoints
# -------------------------
@router.get("/employees")
def get_employees(limit: int = 50):
    """
    Get employees (limit default 50)
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        # use fully-qualified or rely on connection DB/SCHEMA
        cur.execute("SELECT * FROM EMPLOYEE_MASTER LIMIT %s", (limit,))
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return {"employees": rows_to_dicts(cols, rows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@router.post("/employees", status_code=201)
def create_employee(payload: EmployeeIn):
    """
    Insert a new employee. Adjust columns as per your EMPLOYEE_MASTER.
    This example assumes columns: name, email, designation, location
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        insert_sql = """
        INSERT INTO EMPLOYEE_MASTER (name, email, designation, location)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_sql, (
            payload.name,
            payload.email,
            payload.designation,
            payload.location
        ))

        # fetch the latest inserted row (autoincrement jd_id style)
        # Note: Snowflake doesn't provide a simple LAST_INSERT_ID; we query the recently inserted row.
        cur.execute("SELECT * FROM EMPLOYEE_MASTER ORDER BY 1 DESC LIMIT 1")
        cols = [c[0] for c in cur.description]
        row = cur.fetchone()
        return {"employee": rows_to_dicts(cols, [row])[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# -------------------------
# JD_MASTER endpoints
# -------------------------
@router.get("/jds")
def get_jds(limit: int = 50):
    """
    Return jd_master rows
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM JD_MASTER LIMIT %s", (limit,))
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return {"jds": rows_to_dicts(cols, rows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



@router.post("/jds", status_code=201)
def create_jd(payload: JDIn):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        insert_sql = """
        INSERT INTO JD_MASTER
        (jd_id, title, description, required_skills, preferred_skills, 
         experience_min, experience_max, location, status, model_status, updated_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp())
        """
        cur.execute(insert_sql, (
            payload.jd_id,
            payload.title,
            payload.description,
            payload.required_skills,
            payload.preferred_skills,
            payload.experience_min,
            payload.experience_max,
            payload.location,
            payload.status,
            payload.model_status
        ))

        # fetch just inserted row (by jd_id)
        cur.execute("SELECT * FROM JD_MASTER WHERE jd_id = %s", (payload.jd_id,))
        cols = [c[0] for c in cur.description]
        row = cur.fetchone()
        return {"jd": dict(zip(cols, row))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur: cur.close()
        if conn: conn.close()
