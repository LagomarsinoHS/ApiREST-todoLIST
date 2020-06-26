from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Tarea(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), nullable=False, unique=True)
    task = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "userName": self.userName,
            "task": self.task
        }

