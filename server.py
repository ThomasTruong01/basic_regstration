from flask import Flask, render_template, redirect, flash, request
from mysqlconnection import MySQLConnection
from validate_email import validate_email


app = Flask(__name__)
app.secret_key = 'shhdonttellanyone'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    is_valid = True
    if len(request.form['fName']) < 1:
        flash("Please enter in your First Name")
    elif not request.form['fName'].isalpha():
        is_valid = False
        flash('First Name is not a valid entry')

    if len(request.form['lName']) < 1:
        flash("Please enter in your Last Name")
    elif not request.form['lName'].isalpha():
        is_valid = False
        flash('Last Name is not a valid entry')

    if not validate_email(request.form['email']):
        is_valid = False
        flash('Please enter in a valid email.')

    SpecialSym = ['$', '@', '#', '%']
    if len(request.form['pw1']) < 5:
        flash("Please enter a password with 5 or more characters")
        is_valid = False
    elif request.form['pw1'] != request.form['pw2']:
        flash('Your passwords does not match')
    elif len(request.form['pw1']) < 6:
        flash('length should be at least 6')
        is_valid = False
    elif len(request.form['pw1']) > 20:
        flash('length should be not be greater than 8')
        is_valid = False
    elif not any(char.isdigit() for char in request.form['pw1']):
        flash('Password should have at least one numeral')
        is_valid = False
    elif not any(char.isupper() for char in request.form['pw1']):
        flash('Password should have at least one uppercase letter')
        is_valid = False
    elif not any(char.islower() for char in request.form['pw1']):
        flash('Password should have at least one lowercase letter')
        is_valid = False
    elif not any(char in SpecialSym for char in request.form['pw1']):
        flash('Password should have at least one of the symbols $@#')
        is_valid = False

    if is_valid:
        mySql = MySQLConnection('basic_regstration')
        query = 'INSERT INTO users (first_name, last_name, email, password, created_on, updated_on) ' +\
            'VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s,now(),now())'
        data = {'fn': request.form['fName'], 'ln': request.form['lName'],
                'em': request.form['email'], 'pw': request.form['pw1']}
        mySql.query_db(query, data)
        flash('User created!')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
