# test_snowflake_connect_verbose.py
import os
import traceback
import logging
import snowflake.connector
from dotenv import load_dotenv

# Logging for debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# also enable the snowflake logger
logging.getLogger("snowflake.connector").setLevel(logging.DEBUG)

load_dotenv()

SF_USER = os.getenv("SF_USER")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_ACCOUNT = os.getenv("SF_ACCOUNT")
SF_DATABASE = os.getenv("SF_DATABASE")
SF_SCHEMA = os.getenv("SF_SCHEMA", "PUBLIC")
SF_WAREHOUSE = os.getenv("SF_WAREHOUSE")
SF_ROLE = os.getenv("SF_ROLE")

HTTP_PROXY = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
HTTPS_PROXY = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")

print("=== Snowflake verbose connect test ===")
print("User:", SF_USER)
print("Account (from .env):", SF_ACCOUNT)
print("Database/Schema/Warehouse/Role:", SF_DATABASE, SF_SCHEMA, SF_WAREHOUSE, SF_ROLE)
print("HTTP_PROXY:", HTTP_PROXY)
print("HTTPS_PROXY:", HTTPS_PROXY)
print("-" * 60)

variants = [SF_ACCOUNT]
if SF_ACCOUNT and not SF_ACCOUNT.endswith(".aws"):
    variants.append(SF_ACCOUNT + ".aws")
if SF_ACCOUNT and SF_ACCOUNT.endswith(".aws"):
    variants.append(SF_ACCOUNT[:-4])
variants = list(dict.fromkeys([v for v in variants if v]))

def try_connect(acc, use_proxy=False):
    print(f"\nTrying account='{acc}' proxy={use_proxy}")
    try:
        conn_args = dict(
            user=SF_USER,
            password=SF_PASSWORD,
            account=acc,
            warehouse=SF_WAREHOUSE,
            database=SF_DATABASE,
            schema=SF_SCHEMA,
            role=SF_ROLE,
            login_timeout=30,
        )

        # If told to use proxy, try to read host/port from HTTPS_PROXY HTTP(S) env var
        if use_proxy and (HTTPS_PROXY or HTTP_PROXY):
            proxy = HTTPS_PROXY or HTTP_PROXY
            # proxy likely in form http://host:port or host:port
            proxy = proxy.replace("http://", "").replace("https://", "")
            if "@" in proxy:
                # remove credentials if any (user:pass@host:port)
                proxy = proxy.split("@", 1)[1]
            parts = proxy.split(":")
            if len(parts) >= 2:
                proxy_host = parts[0]
                try:
                    proxy_port = int(parts[1])
                except ValueError:
                    proxy_port = None
                # these params are supported by snowflake.connector.connect
                conn_args.update({
                    "proxy_host": proxy_host,
                    "proxy_port": proxy_port,
                })
                print("Using proxy_host/proxy_port:", proxy_host, proxy_port)
            else:
                print("Proxy string not parseable:", proxy)

        # attempt connection
        conn = snowflake.connector.connect(**conn_args)
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();")
        print("=== CONNECTED SUCCESSFULLY ===")
        for row in cur:
            print("CURRENT_ACCOUNT:", row[0])
            print("CURRENT_REGION:", row[1])
            print("CURRENT_ROLE:", row[2])
            print("CURRENT_WAREHOUSE:", row[3])
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Connection FAILED:", repr(e))
        traceback.print_exc()
        return False

# Try normal connection first, then try with proxy (if proxy env exists)
for acc in variants:
    ok = try_connect(acc, use_proxy=False)
    if ok:
        break
    # if proxies are present, try via proxy
    if (HTTP_PROXY or HTTPS_PROXY):
        if try_connect(acc, use_proxy=True):
            break
else:
    print("\nAll attempts failed. See debug logs above for more details.")
    print("If you are behind a corporate network that inspects SSL / uses a proxy, try connecting from a mobile hotspot.")
    print("Also confirm your SF_USER/SF_PASSWORD are valid for non-SSO login (not Okta/SSO).")
