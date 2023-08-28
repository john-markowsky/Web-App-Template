import sys
print(sys.path)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database import ActiveHost, SessionLocal

# # Replace with your user ID and database URL
# user_id = 1
# DATABASE_URL = "sqlite:///./test.db"

# # Create a database session
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()

# # Define the list of active host IP addresses
# active_hosts = [
#     "192.168.1.1",
#     "192.168.1.11",
#     "192.168.1.15",
#     "192.168.1.32",
#     "192.168.1.44",
#     "192.168.1.133",
#     "192.168.1.168",
#     "192.168.1.198",
#     "192.168.1.230",
#     "192.168.1.254"
# ]

# # Insert the active host IP addresses into the ActiveHost table
# for ip_address in active_hosts:
#     active_host = ActiveHost(user_id=user_id, ip_address=ip_address)
#     db.add(active_host)

# # Commit the changes to the database
# db.commit()
# db.close()

# print("Active host IP addresses inserted into the database.")
