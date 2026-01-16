import uuid
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # 主キー (UUID)
    id = db.Column(
        db.String(36),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    # メールアドレス
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # ユーザーネーム
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # ハッシュ化済みパスワード
    password_hash = db.Column(
        db.String(255),
        nullable=False,
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



    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    


    # threadsテーブルとのリレーション
    threads = db.relationship(
        "Thread",
        back_populates="user",
    )

    # postsテーブルとのリレーション
    posts = db.relationship(
        "Post",
        back_populates="user",
    )