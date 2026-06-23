from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(30))

    email: Mapped[str]

    password: Mapped[str] = mapped_column(String[8])

    total_games: Mapped[int] = mapped_column(default=0)

    total_wins: Mapped[int] = mapped_column(default=0)

    total_loses: Mapped[int] = mapped_column(default=0)

    total_draws: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    
