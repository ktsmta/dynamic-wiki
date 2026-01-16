import uuid
from datetime import datetime, timezone
from apps import db

class Thread(db.Model):
    __tablename__ = "threads"

    # 主キー (UUID)
    id = db.Column(
        db.String(36),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    # カテゴリID (外部キー)
    category_id = db.Column(
        db.String(36),
        db.ForeignKey("categories.id"),
        nullable=False,
    )

    # 作成者
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
    )

    # タイトル
    title = db.Column(
        db.String(100),
        nullable=False,
    )

    # スレッド種別 (質問/議論)
    thread_type = db.Column(
        db.String(100),
        nullable=True,
    )

    # post数
    post_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
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



    # categoriesテーブルとのリレーション
    category = db.relationship(
        "Category",
        back_populates="threads",
    )

    # postsテーブルとのリレーション
    posts = db.relationship(
        "Post",
        back_populates="thread",
    )

    # usersテーブルとのリレーション
    user = db.relationship(
        "User",
        back_populates="threads",
    )