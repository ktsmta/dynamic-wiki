import uuid
from datetime import datetime, timezone
from apps import db

class Post(db.Model):
    __tablename__ = "posts"

    # 主キー (UUID)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    # スレッドID（外部キー）
    thread_id = db.Column(db.String(36), db.ForeignKey("threads.id"), nullable=False)

    # 親ポスト
    parent_id = db.Column(db.String(36), db.ForeignKey("posts.id"), nullable=True)

    # 本文
    content = db.Column(db.Text, nullable=False)

    # 作成日時
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # 更新日時
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )


    # 自己参照リレーション
    parent = db.relationship(
        "Post", remote_side=[id],
        backref=db.backref("replies", cascade="all, delete-orphan")
    )

    # threadsテーブルとのリレーション
    thread = db.relationship("Thread", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id}>"
