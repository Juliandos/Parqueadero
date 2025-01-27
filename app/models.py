from app import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
with app.app_context():
    db.create_all()  # Crear la base de datos si no existe

    new_user = User(username='JulianO', email='juliano@gmail.com')
    db.session.add(new_user)
    db.session.commit()
    print(f"Usuario creado: {new_user}")
    users = User.query.all()
    print("Todos los usuarios:")
    print(users)