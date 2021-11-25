from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import shortuuid
from random import randint
app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://ujypevobdznoejre:0f8Z8R1fpniQ0GkOxeYK@bs4ttoxa3uefryx7uje7-mysql.services.clever-cloud.com:3306/bs4ttoxa3uefryx7uje7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class inscrit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.String(100))
    number = db.Column(db.String(100))
    num = db.Column(db.String(100))
    def __init__(self, username, lastname, age, number,num):

        self.username = username
        self.lastname = lastname
        self.age = age
        self.number = number
        self.num = num

#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = inscrit.query.all()

    return render_template("index.html", etudiant=all_data)


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':

        username = request.form['username']
        lastname = request.form['lastname']
        age = request.form['age']
        number = request.form['number']
        num=shortuuid.ShortUUID().random(length=10)
        user =inscrit.query.filter_by(number=number).first()
    if  not user:
        my_data = inscrit(username, lastname, age, number,num)
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully with number :  "+"  "+num)
        return redirect(url_for('Index'))
    else:
      flash("existe")
      return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        data = inscrit.query.get(request.form.get('id'))

        data.username = request.form['username']
        data.lastname = request.form['lastname']
        data.age = request.form['age']
        data.number = request.form['number']
        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = inscrit.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Index'))

 
@app.route('/search', methods = ['GET', 'POST']) 
def search():
   if request.method == 'POST':
       print('post method') 
       form =request.form
       search_value=form['search']
       
       search="%{}%".format(search_value)
      
       resultat=inscrit.query.filter(inscrit.num.like(search)).all()
       
       return render_template('index.html',etudiant=resultat)
   else:
     return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
