# ============================================================
# SGSI KPIs (CANONICAL)
# ============================================================
c.execute("""
CREATE TABLE IF NOT EXISTS sgsi_kpis (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    kpi_date TEXT NOT NULL,
    kpi_name TEXT NOT NULL,
    kpi_value REAL NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
)
""")

