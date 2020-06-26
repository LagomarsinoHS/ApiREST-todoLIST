from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Tarea
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///BD_Local.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/BD_Local'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)


@app.route("/todos/user/", methods=["GET"])
@app.route("/todos/user/<user>", methods=["GET", "DELETE", "POST", "PUT"])
def main(user=None):

    ############ G E T ###########
    if request.method == "GET":
        if user is None:
            todosUsuarios = Tarea.query.all()
            if todosUsuarios:
                todosUsuarios = list(
                    map(lambda usuario: usuario.userName, todosUsuarios))
                return jsonify(todosUsuarios), 200
            else:
                return jsonify({"Msg": "No hay usuarios actualmente"})

        else:
            usuario = Tarea.query.filter(Tarea.userName.ilike(f"{user}")).first()
            if usuario:
                return jsonify(json.loads(usuario.task)), 200 #Loads es para transformar de json a diccionario python, sino en el insomnia se ve mal
            else:
                return jsonify({"msg": "No existe el usuario buscado"})


###################################################################################
############ P O S T ###########
    if request.method == "POST":
        valorEntrante = request.get_json()

        tarea = Tarea()
        tarea.userName = user
        tarea.task = json.dumps(valorEntrante)
        db.session.add(tarea)
        db.session.commit()
        return jsonify({"Msg": "Usuario creado"}),201

###################################################################################
############ P U T ###########

    if request.method == "PUT":
        valorEntrante = request.get_json()
        tareaUser = Tarea.query.filter(Tarea.userName.ilike(f"%{user}")).first()

        if tareaUser:
            tareaUser.task = json.dumps(valorEntrante)
            db.session.commit()
            return jsonify({"Msg": f"Lista con {len(valorEntrante)} fue guardada"})
        else:
            return jsonify({"msg": "No existe ese usuario"})


###################################################################################
############ D E L E T E ###########
    if request.method == "DELETE":
        if user:
            userNameBD = Tarea.query.filter(
                Tarea.userName.ilike(f"%{user}")).first()
            if userNameBD:
                db.session.delete(userNameBD)
                db.session.commit()
                return jsonify({"Msg": f"Usuario {userNameBD.userName} eliminado"})
            else:
                return jsonify({"Msg": f"No se pudo eliminar a {user}"})


if __name__ == "__main__":
    manager.run()
