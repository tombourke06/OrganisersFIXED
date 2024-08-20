from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Database configuration
USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'contactpage'

app = Flask(__name__, template_folder="website/templates", static_folder="website/static")

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
# Disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set the secret key for session management
app.config['SECRET_KEY'] = 'root'
# Initialize the SQLAlchemy object with the app
db = SQLAlchemy(app)


# Define the User model
class Contact(db.Model):
    __tablename__ = 'contactpage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    message = db.Column(db.Text(), nullable=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message


class Order(db.Model):
    __tablename__ = 'organs'
    id = db.Column(db.Integer, primary_key=True)
    organ = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)

    def __init__(self, organ, weight, height, color):
        self.organ = organ
        self.weight = weight
        self.height = height
        self.color = color


class User(db.Model):
    # Name of the table in the database
    __tablename__ = 'signin'
    # Primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Column for the first name, cannot be null
    fName = db.Column(db.String(40), nullable=False)
    lName = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)

    # Constructor to initialize the User object
    def __init__(self, fName, lName, username, email, password):
        self.fName = fName
        self.lName = lName
        self.username = username
        self.email = email
        self.password = password


# Define the route for the home page
@app.route('/')
def index():
    return render_template('HomePage.html')


# Define the route for the booking page
@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/3D Organisers - order now')
def order():
    return render_template('ordernow.html')


@app.route('/3D Organisers - merch')
def merch():
    return render_template('merch.html')


@app.route('/3D Organisers - termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')


@app.route('/3D Organisers - purchase')
def purchase():
    return render_template('purchase.html')


@app.route('/3D Organisers - heart')
def heart():
    return render_template('heart.html')


@app.route('/3D Organisers - lungs')
def lungs():
    return render_template('lungs.html')


@app.route('/3D Organisers - liver')
def liver():
    return render_template('liver.html')


@app.route('/3D Organisers - pancreas')
def pancreas():
    return render_template('pancreas.html')


@app.route('/3D Organisers - kidney')
def kidney():
    return render_template('kidney.html')


@app.route('/3D Organisers - bladder')
def bladder():
    return render_template('bladder.html')


@app.route('/3D Organisers - Cart')
def cart():
    return render_template('Your_Cart.html')


@app.route('/3D Organisers - Products')
def products():
    return render_template('organ_options.html')


@app.route('/3-D Organisers - about us')
def about_us():
    return render_template('aboutus.html')


@app.route('/Navigation Bar')
def navigation_bar():
    return render_template('NavBar.html')


@app.route('/3-D Organisers - Contact Us')
def contact():
    return render_template('contactinfo.html')


@app.route('/3-D Organisers - purchases')
def purchases():
    return render_template('purchases.html')


@app.route('/3-D Organisers - thankyouPurchases')
def thankyouPurchases():
    return render_template('thankyouPurchases.html')


@app.route('/3-D Organisers - Contact Thank you')
def thankyou():
    return render_template('thankyou.html')


@app.route('/Register & Login')
def signin():
    return render_template('signin.html')


# Define the route to handle form submission
@app.route('/enter-details', methods=['POST'])
def enter_details():
    # Retrieve the name, email, and message from the form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create a new User object with the form data
    new_user = Contact(name=name, email=email, message=message)

    try:
        # Attempt to add the new User object to the database
        db.session.add(new_user)
        db.session.commit()
        print('Details entered successfully!')
    except Exception as e:
        # If an error occurs, roll back the transaction
        db.session.rollback()
        print(f'An error occurred: {e}')

    # Redirect to the booking page after form submission
    return redirect(url_for('thankyou'))


# Define the route to handle form submission
@app.route('/ordernow', methods=['POST'])
def ordernow():
    organ = request.form.get('organ')
    weight = request.form.get('weight')
    height = request.form.get('height')
    color = request.form.get('color')

    # Create a new User object with the form data
    new_order = Order(organ=organ, weight=weight, height=height, color=color)

    try:
        # Attempt to add the new User object to the database
        db.session.add(new_order)
        db.session.commit()
        print('Details entered successfully!')
    except Exception as e:
        # If an error occurs, roll back the transaction
        db.session.rollback()
        print(f'An error occurred: {e}')

    return render_template(
            "Your_Cart.html",
        organ=organ,
        weight=weight,
        height=height,
        color=color
    )


# Redirect to the booking page after form submission
@app.route('/signup', methods=['POST'])
def signup():
    # Retrieve the first name and last name from the form data
    fName = request.form.get('fName')
    lName = request.form.get('lName')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new User object with the form data
    new_name = User(fName=fName, lName=lName, username=username, email=email, password=password)

    try:
        # Attempt to add the new User object to the database
        db.session.add(new_name)
        # Commit the transaction
        db.session.commit()
        print('Name entered successfully!')
    except Exception as e:
        # If an error occurs, roll back the transaction
        db.session.rollback()
        print('An error occurred while booking the class.')

    # Redirect to the booking page after form submission
    return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True)
