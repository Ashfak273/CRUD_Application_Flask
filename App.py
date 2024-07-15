from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os


# App Configuration
app = Flask(__name__)

# Secret key for flash messaes
app.secret_key = "flash_message"


# MySQL connection using FLASK Framework
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapplication'
mysql = MySQL(app)


# app photo configuration path
app.config['UPLOAD_FOLDER'] = 'C:/Users/mzaah/Desktop/My_Files/UNI_Doc/FocalID/Project1_CRUD_APP/photo'


# function to save the photo
def save_photo(photo, user_id):
    if photo:
        filename = secure_filename(photo.filename)
        filename = f"{user_id}.{filename.split('.')[-1]}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(file_path)
        return filename
    return None


# Get all data in UI
@app.route('/')
@app.route('/home')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users = data)


# Retrive all data by API
@app.route('/users_data', methods=['GET'])
def users_data():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        user_list = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'age': row[3], 'address': row[4], 'description': row[5], 'photo': row[6]} for row in data]

        return jsonify(users=user_list)


#  Collect Data from UI
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        #  form submission
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        address = request.form.get('address')
        description = request.form.get('description')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, age, address, description) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, age, address, description))
        mysql.connection.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

        photo = request.files['photo']
        filename = save_photo(photo, user_id)

        cur.execute("UPDATE users SET photo = %s WHERE id = %s", (filename, user_id))
        mysql.connection.commit()

        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))


# Collect Data from API
@app.route('/insert_data', methods=['POST'])
def insert_data():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        address = request.form.get('address')
        description = request.form.get('description')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, age, address, description) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, age, address, description))
        mysql.connection.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

        photo = request.files['photo']
        filename = save_photo(photo, user_id)

        cur.execute("UPDATE users SET photo = %s WHERE id = %s", (filename, user_id))
        mysql.connection.commit()

        inserted_data = {
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'address': address,
            'description': description,
            'photo': filename
        }
        return jsonify(inserted_data)


# Update Data from Form UI
@app.route('/update', methods=['POST','PUT'])
def update():
    if request.method == 'PUT' or 'POST':
        # HTML form Data for update
        id_data = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        address = request.form['address']
        description = request.form['description']

        # existing photo
        cur = mysql.connection.cursor()
        cur.execute("SELECT photo FROM users WHERE id = %s", (id_data,))
        existing_photo = cur.fetchone()[0]

        # if new pho uploaded
        if 'photo' in request.files:
            new_photo = request.files['photo']
            if new_photo:
                if existing_photo:
                    # delete existing photo
                    existing_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_photo)
                    if os.path.exists(existing_photo_path):
                        os.remove(existing_photo_path)

                # get new pho filename
                new_filename = save_photo(new_photo, id_data)
                # update user record
                cur.execute("""
                UPDATE users
                SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s, photo=%s
                WHERE id=%s
                """, (first_name, last_name, age, address, description, new_filename, id_data))

            else:
                # no new photo
                cur.execute("""
                     UPDATE users
                     SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s
                     WHERE id=%s
                 """, (first_name, last_name, age, address, description, id_data))

        else:
            # no new photo
            cur.execute("""
                     UPDATE users
                     SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s
                     WHERE id=%s
                 """, (first_name, last_name, age, address, description, id_data))

        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))


# Update Data from Form API
@app.route('/update_data', methods=['PUT'])
def update_data():
    if request.method == 'PUT':
        # HTML form Data for update
        id_data = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        address = request.form['address']
        description = request.form['description']

        # existing photo
        cur = mysql.connection.cursor()
        cur.execute("SELECT photo FROM users WHERE id = %s", (id_data,))
        existing_photo = cur.fetchone()[0]

        # if new pho uploaded
        if 'photo' in request.files:
            new_photo = request.files['photo']
            if new_photo:
                if existing_photo:
                    # delete existing photo
                    existing_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_photo)
                    if os.path.exists(existing_photo_path):
                        os.remove(existing_photo_path)

                # get new pho filename
                new_filename = save_photo(new_photo, id_data)
                # update user record
                cur.execute("""
                UPDATE users
                SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s, photo=%s
                WHERE id=%s
                """, (first_name, last_name, age, address, description, new_filename, id_data))

                inserted_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'address': address,
                    'description': description,
                    'photo': new_filename
                }

            else:
                # no new photo
                cur.execute("""
                     UPDATE users
                     SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s
                     WHERE id=%s
                 """, (first_name, last_name, age, address, description, id_data))

                inserted_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'address': address,
                    'description': description,
                    'photo': existing_photo
                }

        else:
            # no new photo
            cur.execute("""
                     UPDATE users
                     SET first_name=%s, last_name=%s, age=%s, address=%s, description=%s
                     WHERE id=%s
                 """, (first_name, last_name, age, address, description, id_data))

            inserted_data = {
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'address': address,
                'description': description,
                'photo': existing_photo
            }

        flash("Data Updated Successfully")
        mysql.connection.commit()
        return jsonify(inserted_data)


# Delete a Data from UI
@app.route('/delete/<string:id_data>', methods = ['POST', 'GET'] )
def delete(id_data):

    cur = mysql.connection.cursor()
    cur.execute("SELECT photo FROM users WHERE id = %s", (id_data,))
    existing_photo = cur.fetchone()[0]
    # delete existing photo
    existing_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_photo)
    if os.path.exists(existing_photo_path):
        os.remove(existing_photo_path)

    # delete data now
    cur.execute("DELETE FROM users WHERE id=%s", (id_data,))

    flash("Data deleted Successfully")
    mysql.connection.commit()
    return redirect(url_for('Index'))


# Delete user data from API
@app.route('/delete_user/<string:id_data>', methods=['DELETE'])
def delete_user(id_data):
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()

        cur.execute("SELECT photo FROM users WHERE id = %s", (id_data,))
        existing_photo = cur.fetchone()[0]
        # delete existing photo
        existing_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_photo)
        if os.path.exists(existing_photo_path):
            os.remove(existing_photo_path)

        # Now delete data
        cur.execute("DELETE FROM users WHERE id=%s", (id_data,))
        flash("Data deleted Successfully")
        mysql.connection.commit()

        # check
        if cur.rowcount >0:
            response = {
                'status': 'success',
                'message': f'Data with ID {id_data} deleted successfully.'
            }
        else:
            response = {
                'status': 'error',
                'message': f'No Data found with ID {id_data}.'
            }
        cur.close()
        return jsonify(response)


# Now run your server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(3000), debug=True)
    #  while developing webapp place debug =True & remove while deploy
