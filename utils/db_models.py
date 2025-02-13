from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from pathlib import Path
import os

class Base(DeclarativeBase):
    pass

class Quotes(Base):
    __tablename__ = "quotes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quote: Mapped[str] = mapped_column()
    widget_shown: Mapped[bool] = mapped_column(default=False)
    vid_shown: Mapped[bool] = mapped_column()

class GoodQuotes(Base):
    __tablename__ = "goodquotes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column()
    quote: Mapped[str] = mapped_column()
    widget_shown: Mapped[bool] = mapped_column(default=False)
    vid_shown: Mapped[bool] = mapped_column()
    page: Mapped[int] = mapped_column()

# create a folder for db
db_path = Path(__file__).parent.parent / "db"
if not db_path.exists():
    os.makedirs(db_path, exist_ok=True)

ENGINE = create_engine(f"sqlite:///{str(db_path)}/quotes.db")