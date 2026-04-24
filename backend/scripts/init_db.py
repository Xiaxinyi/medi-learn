import sys
sys.path.insert(0, '/Users/shirley/Dev/xxy/backend')

from app.database import engine, Base
from app.models import *

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
