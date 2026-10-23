from flask import Flask, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.db import db
from config.settings import Config
from routes.analyze import analyze_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://"
    f"{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(analyze_bp)

@app.get("/health")
def get_health():
    return {"status": "Alive"}

@app.delete("/clear")
def clear():
    try:
        db.session.execute(text("TRUNCATE TABLE extracted_files, jobs;"))
        db.session.commit()
        return jsonify({"message": "Cleared Successfully"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=Config.PORT)
