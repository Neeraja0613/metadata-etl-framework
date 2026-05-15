import psycopg2, json, time, requests, pandas as pd
import networkx as nx
from datetime import datetime
import os

print("🚀 Orchestrator started...")

# Retry DB connection
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        print("✅ Connected to DB")
        break
    except Exception as e:
        print("⏳ Waiting for DB...", e)
        time.sleep(3)


def fetch_pipelines():
    cur = conn.cursor()
    cur.execute("SELECT * FROM etl_control WHERE is_active=true")
    rows = cur.fetchall()
    cur.close()
    print(f"📌 Pipelines fetched: {len(rows)}")
    return rows


def build_graph(pipelines):
    G = nx.DiGraph()
    for p in pipelines:
        name = p[1]
        deps = p[7]
        G.add_node(name)
        if deps:
            for d in deps:
                G.add_edge(d, name)
    return G


def extract(p):
    source_type = p[2]
    options = p[3]

    print(f"📥 Extracting from {source_type}")

    if source_type == 'csv':
        return pd.read_csv(options['path'])

    if source_type == 'db':
        return pd.read_sql(f"SELECT * FROM {options['table']}", conn)

    if source_type == 'api':
        cur = conn.cursor()
        cur.execute("SELECT watermark_value FROM etl_watermarks WHERE pipeline_name=%s", (p[1],))
        result = cur.fetchone()
        cur.close()

        if result:
            url = options['url'] + f"?since={result[0]}"
        else:
            url = options['url']

        return pd.DataFrame(requests.get(url).json())

def load(df, table, load_type):
    cur = conn.cursor()

    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (data JSONB)")

    if load_type == 'full':
        cur.execute(f"TRUNCATE {table}")

    for _, row in df.iterrows():
        cur.execute(f"INSERT INTO {table} VALUES (%s)", [json.dumps(row.to_dict(), default=str)])

    conn.commit()
    cur.close()

    print(f"📤 Loaded {len(df)} rows into {table}")


def run():
    print("🔄 Running pipeline cycle...")

    pipelines = fetch_pipelines()
    G = build_graph(pipelines)

    # REMOVE cycle pipelines ONLY
    if not nx.is_directed_acyclic_graph(G):
        print("ERROR: Cycle detected in dependency graph")
        return
    
    order = list(nx.topological_sort(G))
    print("➡️ Execution order:", order)

    for name in order:
        p = next(x for x in pipelines if x[1] == name)

        start = datetime.now()

        try:
            df = extract(p)
            load(df, p[4], p[5])
            status = "SUCCESS"
            rows = len(df)
            err = None
            if p[5] == 'incremental' and rows > 0:
                max_val = df[p[6]].max()

                cur = conn.cursor()
                cur.execute("""
                INSERT INTO etl_watermarks(pipeline_name, watermark_value)
                VALUES (%s,%s)
                ON CONFLICT (pipeline_name)
                DO UPDATE SET watermark_value = EXCLUDED.watermark_value
                """, (name, str(max_val)))
                conn.commit()
                cur.close()
        except Exception as e:
            print("❌ Error:", e)
            status = "FAILED"
            rows = 0
            err = str(e)

        cur = conn.cursor()
        cur.execute("""
        INSERT INTO etl_audit_log
        (pipeline_name,start_time,end_time,status,rows_read,rows_written,error_message)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (name, start, datetime.now(), status, rows, rows, err))
        conn.commit()
        cur.close()

        print(f"✅ {name} -> {status}")


while True:
    run()
    time.sleep(20)