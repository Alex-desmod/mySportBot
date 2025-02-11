from datetime import datetime
from sqlalchemy import Integer, BigInteger, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))


class Cycling(Base):
    __tablename__ = 'cycling'

    eventId: Mapped[int]
    name: Mapped[str] = mapped_column(String(50))
    dateFrom: Mapped[datetime]
    dateTo: Mapped[datetime]
    url: Mapped[str] = mapped_column(String(50), nullable=True)
    location: Mapped[str] = mapped_column(String(20))
    location_code: Mapped[str] = mapped_column(String(5))
    winner: Mapped[str] = mapped_column(String(25), nullable=True)


class Athletics(Base):
    __tablename__ = 'athletics'

    eventId: Mapped[int]
    name: Mapped[str] = mapped_column(String(50))
    dateFrom: Mapped[datetime]
    dateTo: Mapped[datetime]
    url: Mapped[str] = mapped_column(String(50), nullable=True)
    location: Mapped[str] = mapped_column(String(20))
    location_code: Mapped[str] = mapped_column(String(5))
    winners: Mapped[str] = mapped_column(String(25), nullable=True)


async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
