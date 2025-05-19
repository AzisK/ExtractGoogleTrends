import duckdb

from core.google_trends import DB_DIR, DB_PATH, DB_TABLE


def migrate():
    sql_script_path = DB_DIR / 'create_table.sql'
    print(f"Running migration from {sql_script_path} to {DB_PATH}")

    with duckdb.connect(DB_PATH) as conn:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()

        print(f'Executing query:\n{sql_script}')
        conn.execute(sql_script)

        result = conn.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{DB_TABLE}'").fetchall()
        if result:
            print(f"Migration successful: {DB_TABLE} table created/verified")
        else:
            print(f"Migration failed: {DB_TABLE} table not found")


if __name__ == "__main__":
    migrate()
