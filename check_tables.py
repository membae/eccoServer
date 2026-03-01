from sqlalchemy import create_engine, inspect

# Your Render External Database URL
DATABASE_URL = "postgresql://ecoserver_user:tSDVlZa8oHyT93fMDmWCDqI70d1kWpTi@dpg-d6i3367gi27c73875nm0-a.oregon-postgres.render.com:5432/ecoserver"

# Create engine
engine = create_engine(DATABASE_URL)

# Use inspector to get table names
inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tables in database:", tables)