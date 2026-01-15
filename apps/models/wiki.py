import uuid
from datetime import datetime, timezone
from apps import db

class Wiki(db.Model):
    __tablename__ = "wikis"

    # 主キー (UUID)
    id = db.Column(
        db.String(36),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    # カテゴリID（外部キー）
    category_id = db.Column(
        db.String(36),
        db.ForeignKey("categories.id"),
        unique=True,
        nullable=False,
    )

    # Wiki本文（まとめ・要約）
    content = db.Column(
        db.Text,
        nullable=True,
    )

    # 作成日時
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # 更新日時
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )



    # Categoriesテーブルとのリレーション
    category = db.relationship(
        "Category",
        back_populates="wiki",
        uselist=False,
    )