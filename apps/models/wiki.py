import uuid
from datetime import datetime, timezone
from apps import db

class Wiki(db.Model):
    __tablename__ = "wikis"

    # 主キー (UUID)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    # カテゴリID（外部キー）
    category_id = db.Column(db.String(36), db.ForeignKey("categories.id"), unique=True, nullable=False)

    # Wiki本文（まとめ・要約）
    content = db.Column(db.Text, nullable=False)

    # 更新日時
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    # Categoriesテーブルとのリレーション
    category = db.relationship("Category", back_populates="wiki")

    def __repr__(self):
        return f"<Wiki of Category: {self.category.name}>"
