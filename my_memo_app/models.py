from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Memo(db.Model):
    __tablename__ = 'memos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)