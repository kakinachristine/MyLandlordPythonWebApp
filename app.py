import os

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database import Users, House
from os import path
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = "bnvsdnvsfvdvkvnjvdvdkbvdsc"


@app.route('/', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        jina = request.form["x"]
        arafa = request.form["y"]
        siri = request.form["z"]
        encrypted_password = generate_password_hash(siri)
        Users.create(name=jina, email=arafa, password=encrypted_password)
        flash("User registered successfully")
    return render_template("Register.html")
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["y"]
        password = request.form["z"]
        try:
            user = Users.get(Users.email == email)
            encrypted_password = user.password
            if check_password_hash(encrypted_password, password):
                flash("User logged in successfully")
                session["logged_in"] = True
                session["name"] = user.name
                session['id'] = user.id
                return redirect(url_for("home"))
        except Users.DoesNotExist:
            flash("wrong username or password")
    return render_template("login.html")
@app.route('/home')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users = Users.select()
    return render_template("home.html", users=users)

@app.route('/logout')
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("logged_in",None)
    return redirect(url_for("login"))
@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    users = Users.select()
    return render_template('users.html',users = users)

@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = Users.get(Users.id == id)
    if request.method == "POST":
        updatedName = request.form["x"]
        updatedEmail = request.form["y"]
        updatedPassword = request.form["z"]
        encryptedPassword = generate_password_hash(updatedPassword)
        user.name = updatedName
        user.email = updatedEmail
        user.password = encryptedPassword
        user.save()
        flash("User update successfully")
        return redirect(url_for("home"))
    return render_template("update.html", user=user)
@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    flash("user deleted successfully")
    return redirect(url_for("home"))
# @app.route('/addhouse',methods=['GET','POST'])
# def index():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     if request.method == "POST":
#         houseName = request.form["houseName"]
#         price = request.form["price"]
#         description = request.form["description"]
#         address = request.form["address"]
#         county = request.form["county"]
#         subCounty = request.form["subCounty"]
#         file = request.files['image']
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(path.dirname(path.realpath(__file__))+"/static/images", filename))
#         id = session['id']
#         House.create(houseName = houseName ,price = price, description = description, image = file.filename,address = address,county = county , subCounty = subCounty)
#         flash("House posted Successfully")
#         flash("House "+houseName)
#     return render_template("addhouses.html")


@app.route('/addhouse',methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        houseName = request.form["houseName"]
        contacts = request.form["contacts"]
        address = request.form["address"]
        county = request.form["county"]
        subCounty = request.form["subCounty"]
        description = request.form["description"]
        price = request.form["price"]
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(path.dirname(path.realpath(__file__))+"/static/images", filename))
        # file2 = request.files['image2']
        # filename2 = secure_filename(file2.filename)
        # file2.save(os.path.join(path.dirname(path.realpath(__file__)) + "/static/images", filename2))
        # file3 = request.files['image3']
        # filename3 = secure_filename(file3.filename)
        # file3.save(os.path.join(path.dirname(path.realpath(__file__)) + "/static/images", filename3))
        # file4 = request.files['image4']
        # filename4 = secure_filename(file4.filename)
        # file4.save(os.path.join(path.dirname(path.realpath(__file__)) + "/static/images", filename4))
        # file5 = request.files['image5']
        # filename5 = secure_filename(file5.filename)
        # file5.save(os.path.join(path.dirname(path.realpath(__file__)) + "/static/images", filename5))
        id = session['id']
        House.create(houseName=houseName,price=price,description=description,address=address,
                                county=county,subCounty=subCounty,image=filename,contacts = contacts
                                )
        flash("House posted Successfully")
    return render_template("addhouse.html")
@app.route('/view')
def view():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    houses = House.select()
    return render_template('viewhouses.html',houses = houses)
@app.route('/viewhouse/<int:id>')
def viewhouse(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    house = House.get(House.id == id)
    return render_template('viewhouseimage.html',house = house)

@app.route('/deletehouse/<int:id>')
def delete2(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    House.delete().where(House.id == id).execute()
    flash("user deleted successfully")
    return redirect(url_for("home"))

@app.route('/updatehouse/<int:id>',methods=["POST","GET"])
def update2(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    house = House.get(House.id == id)
    if request.method == "POST":
        updatedHouseName = request.form["houseName"]
        updatedContact = request.form["contacts"]
        updatedAddress = request.form["address"]
        updatedCounty = request.form["county"]
        updatedSubCounty = request.form["subCounty"]
        updatedDescription = request.form["description"]
        updatedPrice = request.form["price"]
        updatedFile = request.files['image']
        filename = secure_filename(updatedFile .filename)
        updatedFile .save(os.path.join(path.dirname(path.realpath(__file__)) + "/static/images", filename))
        house.houseName = updatedHouseName
        house.contact = updatedContact
        house.address = updatedAddress
        house.county = updatedCounty
        house.subCounty = updatedSubCounty
        house.description = updatedDescription
        house.price = updatedPrice
        house.image = updatedFile
        flash("User update successfully")
        return redirect(url_for("home"))
    return render_template("update2.html", house = house)



if __name__ == '__main__':
    app.run()
