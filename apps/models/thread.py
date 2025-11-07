import uuid
from datetime import datetime, timezone
from apps import db

class Thread(db.Model):
    __tablename__ = "threads"

    # 主キー (UUID)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    # タイトル
    title = db.Column(db.String(100), nullable=False)

    # カテゴリID (外部キー)
    category_id = db.Column(db.String(36), db.ForeignKey("categories.id"), nullable=False)

    # 作成日時
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # 更新日時
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )


    # categoriesテーブルとのリレーション
    category = db.relationship("Category", back_populates="threads")

    # postsテーブルとのリレーション
    posts = db.relationship("Post", back_populates="thread", cascade="all, delete")

    def __repr__(self):
        return f"<Thread {self.title}>"
