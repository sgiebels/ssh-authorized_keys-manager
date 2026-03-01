# Reference:
# - https://github.com/PrettyPrinted/youtube_video_code/tree/master/2025/05/15/How%20to%20Use%20SQLAlchemy%20in%202025
# Video: https://youtu.be/Y-TxICRUy_k
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
import os
from pathlib import Path
# https://realpython.com/python-pathlib/
#from os import path

from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import create_engine, String, Text, select, ForeignKey, DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, relationship

from sqlalchemy.sql import text
from sqlalchemy.sql.expression import literal

#engine = create_engine("sqlite:///db.sqlite3")
# Instead of using a fixed, hardcoded filename, let the SQLite database filename depend on the name of this .py file:
#sqlite_filename = os.path.splitext(os.path.basename(__file__))[0] + '.db'
#For modern Python versions (3.4+), Path(__file__).name should be more idiomatic. Also, Path(__file__).stem gives you the script name without the .py extension
#sqlite_filename = os.path.dirname(os.path.realpath) / '_' + Path(__file__).stem + '.db'

# Python Pathlib - https://realpython.com/python-pathlib/
#print(f"You can find me here: {Path(__file__).parent}!")
#sqlite_filename = Path(__file__).parent / ('_' + Path(__file__).stem + '.db')
sqlite_database_file = Path(__file__).parent.joinpath('_' + Path(__file__).stem + '.db')
#print(type(sqlite_filename), sqlite_filename)

if sqlite_database_file.exists():
    sqlite_database_file.unlink()

#if os.path.isfile(sqlite_filename):
#    os.remove(sqlite_filename)
from sqlalchemy.engine import URL
connect_url = URL.create('sqlite', database = str(sqlite_database_file))
engine = create_engine(connect_url)

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(30))
    host: Mapped[str] = mapped_column(String(30))
#?how to use 'Boolean'?:
# https://docs.sqlalchemy.org/en/20/core/types.html
#    is_owned_hardware: Mapped[int] = mapped_column(Int())
#    use_become: Mapped[bool] = mapped_column( ??
    def __repr__(self):
#        return f"SELF: Account(id={self.id}, name={self.user}@{self.host})"
        return f"account={self.user}@{self.host})"

class PubKey(Base):
    __tablename__ = "pubkey"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(30))
    host: Mapped[str] = mapped_column(String(30))
# ssh public key string length in bytes
# https://stackoverflow.com/questions/39068473/what-is-the-maximum-length-of-private-and-public-rsa-keys
# For OpenSSL and RSA, your RSA keys are limited to 16K at generation. (=bits), conversion to 
# TODO/TBD: what is the maximum lenght of a base64 encoded public ssh key in bytes
    pubkey: Mapped[str] = mapped_column(String(1000))
#    creation_date: Mapped[str] = mapped_column(String(1000))
#    is_tpm
#        is_tpm BOOLEAN,
    comment: Mapped[str]
#    comment: Mapped[str | None]
  # = mapped_column(String(200))
#        last_applied_to_account_date INTEGER,
#    last_login: Mapped[Optional[datetime]]
#    posts: Mapped[list["Post"]] = relationship(back_populates="user")
#    content: Mapped[str] = mapped_column(Text)
#    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#    user: Mapped["User"] = relationship(back_populates="posts")
    def __repr__(self):
#        return f"SELF: PubKey(id={self.id}, title={self.user}@{self.host})"
        return f"pubkey_{self.pubkey}_for_{self.user}@{self.host})"

class Authorization(Base):
    __tablename__ = "authorization"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    pubkey_id: Mapped[int] = mapped_column(ForeignKey('pubkey.id'))
    is_authorized: Mapped[int]
    account: Mapped["Account"] = relationship()
    pubkey: Mapped["PubKey"] = relationship()
#    notes: Mapped[List["Note"]] = relationship(back_populates="note")
    notes: Mapped[List["Note"]] = relationship(back_populates="authorization")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_modified: Mapped[Optional[datetime]]

    def __repr__(self):
#        return f"SELF: Authorization(id={self.id}, account_id={self.account_id}, pubkey_id={self.pubkey_id})"
        return f"auth_pubkey_id={self.pubkey_id}_on_account_id={self.account_id}_is_{self.is_authorized}"

class Note(Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    authorization_id: Mapped[int] = mapped_column(ForeignKey('authorization.id'))
    authorization: Mapped["Authorization"] = relationship(back_populates="notes")
#int] = mapped_column(ForeignKey('authorization.id'))
# List[]: https://youtu.be/T5n1UMD2c1w?si=FPQu-bhPCoJ5K4bK&t=797


Base.metadata.create_all(engine)

with Session(engine) as session:
    session.execute(text("PRAGMA foreigh_keys = ON;"))

    laptop_account = Account(user="myusername", host="laptop")
    server_account = Account(user="myusername", host="server")
    laptop_pubkey = PubKey(user="myusername", host="laptop", pubkey="ssh-rsa .. for myusername@laptop", comment="myusername@laptop_2026-02-27")
    server_pubkey = PubKey(user="myusername", host="server", pubkey="ssh-rsa .. for myusername@server", comment="myusername@server_2026-02-27")
    session.add(laptop_account)
    session.add(server_account)
    session.add(laptop_pubkey)
    session.add(server_pubkey)
    session.add(Account(user="myusername", host="nas"))
    session.commit()

    query = session.query(Account, PubKey).join(PubKey, literal(value=True))
    print("\nMy Join Query: ",str(query),'\n')
    query = session.query(Account, PubKey).join(PubKey, literal(value=True)).all()
    print("My Join Query.all() Result: ",str(query))

    one = Authorization(account_id = 1, pubkey_id = 1, is_authorized=1)
    two = Authorization(account_id = 1, pubkey_id = 2, is_authorized=2)
    session.add(one)
    session.add(two)
    session.commit()
#    result = session.query(Account)
#    print("My Account Query: ",str(result))
#    result = session.query(PubKey)
#    print("My Pubkey Query: ",str(result))
#    stmt = select(Post).where(Post.user == anthony).order_by(Post.id.de>
#    posts = session.scalars(stmt).all()
#    for post in posts:
#        print(post)
#        print(f"  {post.user}")
#https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.join

    # How to perform a left join in SQLALchemy? - https://stackoverflow.com/questions/39619353/how-to-perform-a-left-join-in-sqlalchemy
    # https://docs.sqlalchemy.org/en/20/orm/
    # sqlalchemy 2.0 join multiple columns
    # https://stackoverflow.com/questions/51164849/sqlalchemy-join-syntax-using-multiple-column-names
    print()
    query = session.query(Account, PubKey). \
     join(PubKey, literal(value=True)). \
      join(Authorization, (Authorization.account_id == Account.id) & (Authorization.pubkey_id == PubKey.id), isouter=True). \
       all()
#    query = session.query(Account, PubKey).join(PubKey, literal(value=True)).join(Authorization, (Authorization.account_id == Account.id) & (Authorization.pubkey_id == PubKey.id), isouter=False).all()
    print("2nd Join Query.all() Result: ",str(query))

#    query = session.query(Authorization). \
#     join(Account, PubKey). \
#     join(PubKey, literal(value=True)). \
#      join(Authorization, (Authorization.account_id == Account.id) & (Authorization.pubkey_id == PubKey.id), isouter=True). \
#       all()
#employees = session.query(Employee).all()
#for e in employees:
#    print(f"{e.name}, ${e.salary:.2f}")
    print(session.query(Authorization))
    auths = session.query(Authorization)
#    auths = session.query(Authorization).all()
    for auth in auths:
#        print(f"#{auth.id}:{auth.pubkey_id.}*{auth.account_id}, {auth.is_authorized}")
        print(f"#{auth.id}:Pubkey {auth.pubkey.user}@{auth.pubkey.host} IS {auth.is_authorized} ON {auth.account.user}@{auth.account.host}")
