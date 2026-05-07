from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    event_type: Mapped[str] = mapped_column(String, index=True)
    entity_type: Mapped[str] = mapped_column(String, index=True)
    entity_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    message: Mapped[str] = mapped_column(String)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_ts: Mapped[int] = mapped_column(Integer, index=True)
