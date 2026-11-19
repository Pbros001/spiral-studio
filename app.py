import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request, send_file, url_for, flash, redirect
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError

from typography_engine import save_png

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
OUTPUT_DIR = ROOT / "static" / "generated"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"}
MAX_UPLOAD_MB = 12

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-local-development-key")
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    result_image = None
    download_url = None
    entered_text = "the"
    selected_width = 1800

    if request.method == "POST":
        uploaded = request.files.get("image")
        entered_text = request.form.get("phrase", "the").strip()
        try:
            selected_width = int(request.form.get("width", "1800"))
        except ValueError:
            selected_width = 1800

        if not uploaded or not uploaded.filename:
            flash("Please choose an image first.", "error")
            return render_template("index.html", result_image=None, download_url=None,
                                   phrase=entered_text, width=selected_width)
        if not allowed_file(uploaded.filename):
            flash("Unsupported file type. Please upload JPG, PNG, WEBP, BMP or TIFF.", "error")
            return render_template("index.html", result_image=None, download_url=None,
                                   phrase=entered_text, width=selected_width)
        if not entered_text:
            flash("Please enter the text you want to repeat.", "error")
            return render_template("index.html", result_image=None, download_url=None,
                                   phrase=entered_text, width=selected_width)
        if len(entered_text) > 80:
            flash("Please keep the repeated text to 80 characters or fewer.", "error")
            return render_template("index.html", result_image=None, download_url=None,
                                   phrase=entered_text, width=selected_width)
        if selected_width not in (1200, 1800, 2600):
            selected_width = 1800

        safe_name = secure_filename(uploaded.filename)
        token = uuid.uuid4().hex
        input_path = UPLOAD_DIR / f"{token}_{safe_name}"
        output_name = f"{token}_spiral.png"
        output_path = OUTPUT_DIR / output_name
        uploaded.save(input_path)

        try:
            # Verify the uploaded file is a readable image before processing.
            with Image.open(input_path) as check:
                check.verify()
            save_png(str(input_path), str(output_path), width=selected_width, text=entered_text)
            result_image = url_for("static", filename=f"generated/{output_name}")
            download_url = url_for("download_file", filename=output_name)
            flash("Your spiral typography artwork is ready.", "success")
        except (OSError, ValueError, UnidentifiedImageError) as exc:
            output_path.unlink(missing_ok=True)
            flash(f"Could not process this image: {exc}", "error")
        finally:
            input_path.unlink(missing_ok=True)

    return render_template("index.html", result_image=result_image,
                           download_url=download_url, phrase=entered_text,
                           width=selected_width)


@app.route("/download/<filename>")
def download_file(filename):
    # Only allow generated PNG names, not arbitrary filesystem paths.
    if not filename.endswith("_spiral.png") or "/" in filename or "\\" in filename:
        return "File not found", 404
    path = OUTPUT_DIR / filename
    if not path.is_file():
        return "File not found", 404
    return send_file(path, as_attachment=True, download_name="spiral-typography.png")


@app.errorhandler(413)
def too_large(_error):
    flash(f"Image is too large. Maximum upload size is {MAX_UPLOAD_MB} MB.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
