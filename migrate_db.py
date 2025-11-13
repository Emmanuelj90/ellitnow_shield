import sqlite3

conn = sqlite3.connect("tenants.db")
c = conn.cursor()

for column in ["parent_tenant_id", "logo_url", "primary_color"]:
    try:
        c.execute(f"ALTER TABLE tenants ADD COLUMN {column} TEXT")
    except sqlite3.OperationalError:
        pass  # Ya existe

conn.commit()
conn.close()
print("✅ Migración completada. Estructura actualizada.")
