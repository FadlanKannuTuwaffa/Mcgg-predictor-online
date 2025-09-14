# helper to create an admin user locally
from app.db import engine, init_db
from app.models import User
from app.auth import hash_password
from sqlmodel import Session

init_db()
username = input('admin username: ')
pw = input('admin password: ')
with Session(engine) as s:
    u = User(username=username, password_hash=hash_password(pw), is_admin=True, active=True)
    s.add(u); s.commit()
    print('admin created')
