from config import POSTGRE_DATABASE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_name = POSTGRE_DATABASE["name"]
user = POSTGRE_DATABASE['username']
password = POSTGRE_DATABASE['password']
host = POSTGRE_DATABASE['host']
db_url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine,
                            expire_on_commit=False)

def connect_to_db():
    print("connecting")
    session = SessionLocal()
    try:
        session.execute("SELECT 1")
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()

def create_or_update_row(tablename, data, primary_keys):
    session = SessionLocal()
    find_object = find_rows(tablename, primary_keys)[0]
    
    if find_object:
        for key, value in data.items():
            setattr(find_object, key, value)
    else:
        session.add(data)
    session.commit()
    session.close()
    return find_rows(tablename, primary_keys)[0]

def find_rows(tablename, dict):
    session = SessionLocal()
    find_object = session.query(tablename).filter_by(**dict).all()
    session.close()
    return find_object