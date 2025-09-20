# scripts/check_table.py
from sqlalchemy import create_engine, inspect
from app.core.settings import settings

def check_table():
    engine = create_engine(settings.database_url, future=True)
    inspector = inspect(engine)

    schema = "public"
    tables = inspector.get_table_names(schema=schema)

    print("Connected to:", settings.database_url)
    print(f"Tables in schema '{schema}': {tables}")

    if "jd_master" in tables:
        print("✅ Table jd_master exists")
    else:
        print("❌ Table jd_master does NOT exist")

if __name__ == "__main__":
    check_table()
