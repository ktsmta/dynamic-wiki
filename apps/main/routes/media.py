import uuid
from datetime import datetime
from pathlib import Path

from flask import abort, current_app, jsonify, send_from_directory, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from apps.main import main_bp

ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def _ensure_inside(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except Exception:
        return False


@main_bp.route("/media/<path:filename>")
def media_serve(filename: str):
    upload_root = Path(current_app.instance_path) / "uploads"
    file_path = upload_root / filename

    if (not _ensure_inside(upload_root, file_path)) or (not file_path.is_file()):
        abort(404)

    return send_from_directory(upload_root, filename)


@main_bp.route("/media/upload", methods=["POST"])
@login_required
def media_upload():
    f = request.files.get("image")
    if not f or f.filename == "":
        return jsonify({"error": "no file"}), 400

    original = secure_filename(f.filename)
    ext = Path(original).suffix.lower()
    if ext not in ALLOWED_EXTS:
        return jsonify({"error": "unsupported file type"}), 400

    # instance/uploads/YYYY/MM/ に保存
    now = datetime.utcnow()
    upload_root = Path(current_app.instance_path) / "uploads"
    subdir = Path(str(now.year)) / f"{now.month:02d}"
    save_dir = upload_root / subdir
    save_dir.mkdir(parents=True, exist_ok=True)

    new_name = f"{uuid.uuid4().hex}{ext}"
    save_path = save_dir / new_name
    f.save(save_path)

    # main_bp は /c 配下なので /c/media/... を返す
    url = f"/c/media/{subdir.as_posix()}/{new_name}"

    return jsonify({"url": url})
