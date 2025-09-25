import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='skillquest',
    password='Skillquest@123',
    account='KYSHCAK-SZC76532',   # <-- replace <region> with yours, e.g. ap-south-1
    warehouse='COMPUTE_WH',        # use your warehouse
    database='SKILL_QUEST',
    schema='DEV',
    role='ACCOUNTADMIN'
)

# Create cursor
cur = conn.cursor()

try:
    # Run query
    cur.execute("SELECT * FROM EMPLOYEE_MASTER LIMIT 10;")
    
    # Fetch results
    rows = cur.fetchall()
    for row in rows:
        print(row)

finally:
    cur.close()
    conn.close()
