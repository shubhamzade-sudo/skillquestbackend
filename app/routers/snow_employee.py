# app/routers/snow_employee.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
import snowflake.connector
import os

# import global settings instance
from app.core.settings import settings

router = APIRouter(prefix="/snow", tags=["Snowflake"])

# --- Config (read from app.core.settings, fallback to env/defaults) ---
def _s(name: str, default: Optional[str] = None) -> Optional[str]:
    # settings uses snake_case attribute names
    val = getattr(settings, name.lower(), None)
    if val:
        return val
    # fallback to environment variable (in case)
    return os.getenv(name.upper(), default)

SNOWFLAKE_USER = _s("snowflake_user")
SNOWFLAKE_PASSWORD = _s("snowflake_password")
SNOWFLAKE_ACCOUNT = _s("snowflake_account")
SNOWFLAKE_ROLE = _s("snowflake_role", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = _s("snowflake_warehouse", "COMPUTE_WH")
SNOWFLAKE_DATABASE = _s("snowflake_database", "SKILL_QUEST")
SNOWFLAKE_SCHEMA = _s("snowflake_schema", "DEV")

# --- Helper: connect ---
def get_connection():
    if not (SNOWFLAKE_USER and SNOWFLAKE_PASSWORD and SNOWFLAKE_ACCOUNT):
        raise RuntimeError("Snowflake credentials not configured. Check .env and Settings.")
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
            if isinstance(val, Decimal):
                d[col] = float(val)
            else:
                d[col] = val
        out.append(d)
    return out

# -------------------------
# Pydantic models
# -------------------------
class EmployeeIn(BaseModel):
    employee_id: Optional[int] = None
    name: str
    email: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None

class JDIn(BaseModel):
    # frontend-supplied REQ id (optional). Keep int if you want numeric-only.
    jd_id: Optional[int] = None
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
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
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
        # return latest row (ordered by first column)
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

        # If frontend supplies jd_id (numeric), we insert it; otherwise rely on autoincrement
        if payload.jd_id is not None:
            insert_sql = """
            INSERT INTO JD_MASTER
            (jd_id, title, description, required_skills, preferred_skills, 
             experience_min, experience_max, location, status, model_status, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp())
            """
            cur.execute(insert_sql, (
                int(payload.jd_id),
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
            # fetch by provided jd_id
            cur.execute("SELECT * FROM JD_MASTER WHERE jd_id = %s", (int(payload.jd_id),))
        else:
            # insert without jd_id (auto-incremented by Snowflake)
            insert_sql = """
            INSERT INTO JD_MASTER
            (title, description, required_skills, preferred_skills, 
             experience_min, experience_max, location, status, model_status, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp())
            """
            cur.execute(insert_sql, (
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
            # fetch last inserted row (highest jd_id)
            cur.execute("SELECT * FROM JD_MASTER ORDER BY jd_id DESC LIMIT 1")

        cols = [c[0] for c in cur.description]
        row = cur.fetchone()
        return {"jd": dict(zip(cols, row))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
