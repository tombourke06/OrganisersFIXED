from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Database configuration test
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


class Contact(db.Model):
    __tablename__ = 'contactpage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message


class Organ(db.Model):
    __tablename__ = 'organs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organ = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Text, nullable=False)
    height = db.Column(db.Text, nullable=False)
    colour = db.Column(db.Text, nullable=False)

    orders = db.relationship('Order', back_populates='organ', cascade="all, delete-orphan")

    def __init__(self, organ, weight, height, colour):
        self.organ = organ
        self.weight = weight
        self.height = height
        self.colour = colour


class User(db.Model):
    __tablename__ = 'signin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fName = db.Column(db.Text, nullable=False)
    lName = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    orders = db.relationship('Order', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, fName, lName, username, email, password):
        self.fName = fName
        self.lName = lName
        self.username = username
        self.email = email
        self.password = password


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    signin_id = db.Column(db.Integer, db.ForeignKey('signin.id'), nullable=False)
    organ_id = db.Column(db.Integer, db.ForeignKey('organs.id'), nullable=False)
    email = db.Column(db.Text, nullable=False)
    organ_name = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Text, nullable=False)
    height = db.Column(db.Text, nullable=False)
    colour = db.Column(db.Text, nullable=False)

    user = db.relationship('User', back_populates='orders')
    organ = db.relationship('Organ', back_populates='orders')

    def __init__(self, signin_id, organ_id, email, organ_name, weight, height, colour):
        self.signin_id = signin_id
        self.organ_id = organ_id
        self.email = email
        self.organ_name = organ_name
        self.weight = weight
        self.height = height
        self.colour = colour

# Define the route for the home page
@app.route('/')
def index():
    return render_template('HomePage.html')


# Define the route for the booking page
@app.route('/booking')
def booking():
    return render_template('BookingCalendar.html')


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

@app.route('/Login')
def sign_in():
    return render_template('signin.html')


@app.route('/Signin')
def sign_up():
    return render_template('signup.html')




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
    signin_id = session.get('signin_id')

    if not signin_id:
        print('User not logged in.')
        return redirect(url_for('signin'))

    organ_name = request.form.get('organ_name')
    weight = request.form.get('weight')
    height = request.form.get('height')
    colour = request.form.get('colour')

    organ = Organ.query.filter_by(organ=organ_name).first()

    if not organ:
        print('Organ not found.')
        return redirect(url_for('products'))

    organ_id = organ.id

    user = User.query.get(signin_id)
    if not user:
        print('User not found.')
        return redirect(url_for('signin'))

    email = user.email

    new_order = Order(
        signin_id=signin_id,
        organ_id=organ_id,
        email=email,
        organ_name=organ_name,
        weight=weight,
        height=height,
        colour=colour
    )

    try:
        db.session.add(new_order)
        db.session.commit()
        print('Order placed successfully!')
        return render_template(
            "Your_Cart.html",
            organ_name=organ_name,
            weight=weight,
            height=height,
            colour=colour
        )
    except Exception as e:
        db.session.rollback()
        print(f'An error occurred: {e}')
        return redirect(url_for('products'))


@app.route('/Login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(
            (User.username == username_or_email) |
            (User.email == username_or_email)
        ).first()

        if user and user.password == password:
            session['signin_id'] = user.id
            session['username'] = user.username
            print('You have successfully logged in!')
            return redirect(url_for('index'))
        else:
            print('Invalid username/email or password.')
            return redirect(url_for('signin'))

    return render_template('signin.html')


@app.route('/signup', methods=['POST'])
def signup():
    fName = request.form.get('fName')
    lName = request.form.get('lName')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(fName=fName, lName=lName, username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        print('User registered successfully!')
        return redirect(url_for('products'))
    except Exception as e:
        db.session.rollback()
        print(f'An error occurred: {e}')
        return redirect(url_for('signup'))


if __name__ == '__main__':
    app.run(debug=True)
