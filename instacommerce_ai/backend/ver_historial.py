from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///db.sqlite3")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM historial_conversaciones ORDER BY timestamp DESC"))
    for row in result.fetchall():
        print(dict(row))