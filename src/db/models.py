from sqlalchemy import String, Integer
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column
)


class Base(DeclarativeBase):
    pass


class WordCount(Base):
    __tablename__ = "word_count"
    word: Mapped[str] = mapped_column(String(100), primary_key=True)
    url_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(500))
    count: Mapped[int] = mapped_column(Integer)
