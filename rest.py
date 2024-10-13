from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_manager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hello:1@localhost/flask3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False)  

    def to_dict(self):
        return {
            'id': self.id, 
            "username": self.username, 
            "password": self.password, 
            'profile':self.profile.to_dict() if self.profile else None
        }


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    about = db.Column(db.String(500), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  
    user = db.relationship('User', back_populates='profile')  

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age, "about":self.about}



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),unique=True)
    text = db.Column(db.String(80),unique=True)

    def to_dict(self):
        return {"id":self.id, "title":self.title,"text":self.text}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route("/article/", methods=['GET'])
def get_article():
    articles = Article.query.all()
    return [article.to_dict() for article in articles]


@app.route("/register/", methods=['POST'])
def register():
    data = request.json

    username = data['username']
    password = data['password']
    try:
        check_data = User.query.filter_by(username=username).first()
    except Exception as error:
        print(error)

    if check_data:
        return {"error":"already exists"},400
    
    if not username and not password:
        return {"error":"this fields are required"}

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return {"register":"success"},201
    

@app.route("/login/", methods=['POST'])
def login():
    data = request.json

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return {"message":"login"},201
    
    return {"error":"user already exists"},400


@app.route("/logout/", methods=['POST'])
@login_required
def logout():
    logout_user()
    return {"message":"logout"}


@app.route('/user/', methods=['GET'])
@login_required
def get_profile():
    return jsonify({'message':current_user.username})


@app.route("/get_user/<int:id>/", methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    return {"error":"not found"}, 404


@app.route("/get_users/", methods=['GET'])
def get_user_list():
    user = User.query.all()
    return jsonify([user.to_dict() for user in user]),200


@app.route("/create_profile/", methods=['POST'])
def create_profile():
    data = request.json

    user_id = data['user_id']
    name = data['name']
    about = data['about']
    age = data['age']


    profile = Profile(user_id=user_id, name=name, about=about, age=age)
    db.session.add(profile)
    db.session.commit()

    return jsonify(profile.to_dict())


@app.route("/update_profile/<int:id>/", methods=['PUT'])
def update_profile():
    data = request.json
    
    profile = Profile.query.get(id)

    if not profile:
        return {'message':'not found'},404
    
    elif profile.user_id !=  current_user.user_id:
        return {"error": "permissions is required"}
    
    elif "name" in data:
        profile.name = data['name']
    elif 'age' in data:
        profile.age = data['age']
    elif 'about' in data:
        profile.about = data['about']

    db.session.add(profile)
    db.session.commit()

    return {"message": "updated"},201


@app.route("/delete_profile/<int:id>/", methods=['DELETE'])
def delete_profile(id):
    profile = Profile.query.get(id)

    if not profile:
        return {"error":"not found"},404

    elif profile.user_id !=  current_user.user_id:
        return {"error": "permissions is required"}
    
    db.session.delete(profile)
    db.session.commit()
    
    return {"message":"deleted"},204   


# @app.route("/create_post/", methods=['POST'])
# def create_post():
#     data = request.json
#     user_id = data['user_id']
#     title = data['title']
#     desc = data['desc']

#     user = User.query.get(user_id)
#     if not user and not user.profile:
#         return {"error":"no profile"}
    
#     post = Post(title=title, desc=desc, profile_id=user.profile.id)
#     db.session.add(post)
#     db.session.commit()


@app.route("/add_post/", methods=['POST'])
def create_post():
    data = request.json
    title = data['title']
    text = data['text']
    article = Article(title=title,text=text)
    
    if not text and not title:
        return {"error": "fields are required"}
    
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_dict())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
