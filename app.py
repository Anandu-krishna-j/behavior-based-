from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pickle
import os
import sklearn

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f'<User {self.email},{self.password}>'


@app.route('/',methods=['POST','GET'])
def LoginSection():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        data = User.query.filter_by(email=email,password=password).all()
        if data:
            return redirect(url_for('HomeSection'))
    return render_template('index.html')


@app.route('/register',methods=['POST','GET'])
def RegisterSection():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        retypepassword = request.form.get('retypepassword')
        filterEmail = User.query.filter_by(email = email).all()
        print(filterEmail,"Filter Email")
        if filterEmail:
            return render_template('register.html',status='Email Already Registered')
        elif password==retypepassword:
            data = User(
                       email= email, 
                       password=password)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('LoginSection'))
           

    return render_template('register.html',status='')


@app.route('/home',methods=['POST','GET'])
def HomeSection():
    if request.method=='POST':
        on_min_ts = int(request.form.get('on_min_ts'))
        on_max_ts = int(request.form.get('on_max_ts'))
        on_mode_ts = int(request.form.get('on_mode_ts'))
        on_mean_ts = int(request.form.get('on_mean_ts'))
        off_min_ts = int(request.form.get('off_min_ts'))
        off_max_ts = int(request.form.get('off_max_ts'))
        off_mode_ts = int(request.form.get('off_mode_ts'))
        off_mean_ts = int(request.form.get('off_mean_ts'))
        pc_count = int(request.form.get('pc_count'))
        o = int(request.form.get('o'))
        c = int(request.form.get('c'))
        e = int(request.form.get('e'))
        a = int(request.form.get('a'))
        n = int(request.form.get('n'))

        # file = open('mymodel', 'r')
        loaded_model = pickle.load(open("mymodel", 'rb'))
        # model = pickle.load(file)
        loaded_model
        # data = all_parameters_input.head(1)
        data = [[on_min_ts,on_max_ts,on_mode_ts,on_mean_ts,off_min_ts,off_max_ts,off_mode_ts,off_mean_ts,pc_count,o,c,e,a,n]]
        print(data)
        all_parameters_ascore = loaded_model.decision_function(data)
        all_parameters_ascore[:10]
        if all_parameters_ascore[:10]<0:
            return render_template('result.html',data='Outlier')
        else:
            return render_template('result.html',data='Normal')
        print(all_parameters_ascore[:10])

    return render_template("homepage.html")


@app.route('/result',methods=['POST','GET'])
def Result():
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True)
    
