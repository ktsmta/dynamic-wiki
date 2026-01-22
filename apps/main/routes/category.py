from flask import render_template
from collections import defaultdict
from apps.main import main_bp
from apps.models import *
from apps import db

# All
@main_bp.route('/')
def category_all():
    # 1) 全カテゴリを一括取得（N+1回避のため、ここで全部取ってツリー化）
    rows = (
        Category.query
        .order_by(Category.name.asc())
        .all()
    )

    # 2) parent_id -> [children...] の隣接リスト
    children_map = defaultdict(list)
    roots = []
    for c in rows:
        if c.parent_id is None:
            roots.append(c)
        else:
            children_map[c.parent_id].append(c)

    # 3) 再帰で「children」属性を動的に付けてツリー化
    def attach(node):
        kids = children_map.get(node.id, [])
        # 表示順を安定させたい場合（nameでソート）
        kids.sort(key=lambda x: (x.name or "").lower())
        node.children = kids
        for k in kids:
            attach(k)

    for r in roots:
        attach(r)

    return render_template(
        "category/category_all.html",
        categories=roots,
    )

# detail
@main_bp.route('/<slug>')
def category_detail(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()

    # 子・スレッド・wikiは現状どおり
    children = category.children
    latest_threads = (
        Thread.query
        .filter_by(category_id=category.id)
        .order_by(Thread.created_at.desc())
        .limit(5)
        .all()
    )
    wiki = category.wiki

    # ✅ パンくず：親がなくなるまで辿る（無限ループ防止付き）
    crumbs = []
    cur = category
    seen = set()
    while cur is not None:
        # 何らかのデータ不整合（循環参照）に備えて保険
        if cur.id in seen:
            break
        seen.add(cur.id)

        crumbs.append(cur)   # 末端→親方向に積む
        cur = cur.parent

    crumbs.reverse()         # 親→末端にする

    return render_template(
        "category/category_detail.html",
        category=category,
        children=children,
        latest_threads=latest_threads,
        wiki=wiki,
        crumbs=crumbs,        # ✅ 追加
    )