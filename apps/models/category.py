import uuid
from datetime import datetime, timezone

from apps.models.wiki import Wiki
from apps import db

from sqlalchemy import event
from sqlalchemy.orm import validates, Session
import re

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



    # slug制約
    @validates('slug')
    def validate_slug(self, key, slug):
        if not re.match(r"^[a-zA-Z0-9-]+$", slug):
            raise ValueError('slug には半角英数字とハイフンのみ使用できます。')
        return slug
    
    # 識別の為
    def __repr__(self):
        return self.slug

    # 親参照リレーション
    parent = db.relationship(
        'Category',
        back_populates='children',
        remote_side=[id],
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


@event.listens_for(Category, "after_insert")
def create_wiki_for_category(mapper, connection, target):
    """
    Category が新規作成された際に、対応する Wiki レコードを1件自動生成する。
    """

    # SQLAlchemy ORM セッションを生成（connection に紐づくセッション）
    session = Session(bind=connection)

    # Wiki を生成（content は nullable=True のため空で可）
    new_wiki = Wiki(
        category_id=target.id,
        content="",   # 初期本文は空。将来的にAI等で更新可能。
    )

    # セッションに追加してコミット
    session.add(new_wiki)
    session.commit()