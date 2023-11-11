from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# 接続先DBの設定
DATABASE = 'sqlite:///circle.sqlite3'

# Engine の作成
Engine = create_engine(
  DATABASE,
  echo=False
)

def create_session() -> Session: 
  return Session(
    autocommit = False,
    autoflush = True,
    bind = Engine
  )
