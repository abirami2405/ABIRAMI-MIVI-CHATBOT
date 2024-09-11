from flask import render_template, request, jsonify, session
from app import app, mongo
from pymongo import MongoClient

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()  # Get email and password from form
        email = data.get('email')
        password = data.get('password')
        
        # Check if user exists in the database
        user = mongo.db.users.find_one({"email": email})
        if user and user.get('password') == password:
            # If login successful, store email in the session
            session['email'] = email  # Store email in session (flask session)
            return jsonify({"status": "success", "redirect": "/dashboard"}), 200
        else:
            return jsonify({"message": "Invalid credentials. Please try again."}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.get_json()
        # Process the data and store it in MongoDB
        mongo.db.users.insert_one(user_data)
        return jsonify({"message": "Registration successful!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/dashboard')
def dashboard():
    email = session.get('email')  # Retrieve email from session
    if not email:
        return render_template('/login')  # Redirect to login if no session

    # Render dashboard HTML (with email for JavaScript to fetch data)
    return render_template('dashboard.html', email=email)
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    try:
        user_email = request.args.get('email')  # Retrieve email from the query parameter
        if not user_email:
            return jsonify({"message": "Email parameter is missing"}), 400
        
        # Fetch user data from MongoDB
        user = mongo.db.users.find_one({"email": user_email})
        
        if user:
            user_data = {
                "name": user.get('name'),
                "age": user.get('age'),
                "height": user.get('height'),
                "weight": user.get('weight'),
                "bloodGroup": user.get('bloodGroup'),
                "isDiabetic": user.get('isDiabetic'),
                "bp": user.get('bp'),
                "medicalHistory": user.get('medicalHistory')
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
