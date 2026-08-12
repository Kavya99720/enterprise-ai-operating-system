from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False,
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )