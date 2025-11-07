import uuid
from datetime import datetime, timezone
from apps import db

class Category(db.Model):
    __tablename__ = "categories"

    # 主キー (UUID)
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    # 簡易識別子 (半角英数字制限有)
    slug = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    # 名前
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    # 親カテゴリ
    parent_id = db.Column(
        db.String(36),
        db.ForeignKey("categories.id"),
        nullable=True,
    )

    # 作成日時
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # 更新日時
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )



    # 親参照リレーション
    parent = db.relationship(
        'Category',
        back_populates='children',
        emote_side=[id],
    )

    # 子参照リレーション
    children = db.relationship(
        'Category',
        back_populates='parent',
    )

    # wikisテーブルとのリレーション
    wiki = db.relationship(
        "Wiki",
        back_populates="category",
        uselist=False,
    )

    # threadsテーブルとのリレーション
    threads = db.relationship(
        "Thread",
        back_populates="category",
    )