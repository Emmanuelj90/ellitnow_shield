import sqlite3, secrets, hashlib, uuid

DB_PATH = "tenants.db"
EMAIL = "emmanuelj90@gmail.com"
NAME = "Ellit Super Admin"


def ensure_tables_and_columns():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Crear tablas si no existen
    c.execute("""CREATE TABLE IF NOT EXISTS tenants (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    active INTEGER,
                    created_at TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS tenant_api_keys (
                    tenant_id TEXT,
                    key_fingerprint TEXT,
                    key_hash TEXT
                )""")
    conn.commit()

    # Verificar si existe la columna 'predictive'
    c.execute("PRAGMA table_info(tenants)")
    columns = [col[1] for col in c.fetchall()]
    if "predictive" not in columns:
        try:
            c.execute("ALTER TABLE tenants ADD COLUMN predictive INTEGER DEFAULT 1")
            conn.commit()
            print("🧩 Columna 'predictive' añadida a la tabla tenants.")
        except Exception as e:
            print("⚠️ No se pudo añadir la columna 'predictive':", e)

    conn.close()


def generate_api_key(name, email):
    ensure_tables_and_columns()
    tenant_id = str(uuid.uuid4())
    api_key = "sk_ellit_" + secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tenants WHERE email = ?", (email,))
    c.execute(
        "INSERT INTO tenants (id, name, email, active, predictive, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",
        (tenant_id, name, email, 1, 1),
    )
    c.execute(
        "INSERT INTO tenant_api_keys (tenant_id, key_fingerprint, key_hash) VALUES (?, ?, ?)",
        (tenant_id, api_key[:8], key_hash),
    )
    conn.commit()
    conn.close()
    return api_key


if __name__ == "__main__":
    key = generate_api_key(NAME, EMAIL)
    print("\n✅ NUEVA SUPER ADMIN KEY (guárdala en tu secrets.toml):\n")
    print(key)
    print("\nCopia esta clave y pégala en tu archivo .streamlit/secrets.toml reemplazando la antigua.\n")

