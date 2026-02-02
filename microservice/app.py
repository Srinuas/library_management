from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = "secret_key_for_flash_messages"  # Flash messages pani cheyyadaniki

# --- Existing Routes (Home/Login etc unte ikkada untayi) ---
# Example Home Route
@app.route('/')
def home():
    return "<h1>Welcome to Digital Library</h1><a href='/mybooks'>Go to My Books</a>"

# --- My Books Route ---
@app.route('/mybooks')
def my_books():
    user_id = 1  # Hardcoded for testing (Session unte session['user_id'] vadu)
    
    # Borrow Service nundi data techukuntunnam
    try:
        # Note: Docker Swarm lo service name 'borrow_service'
        response = requests.get(f"http://borrow_service:5003/mybooks/{user_id}")
        if response.status_code == 200:
            books = response.json()
        else:
            books = []
            flash("Could not fetch books.", "warning")
    except Exception as e:
        books = []
        flash(f"Error connecting to service: {str(e)}", "danger")

    return render_template('borrow.html', books=books)

# --- Return Book Route (NEWLY ADDED) ---
@app.route("/return_book/<int:book_id>", methods=["POST"])
def return_book_route(book_id):
    user_id = 1  # Hardcoded for testing
    
    try:
        # Borrow Service ki DELETE request pampisthunnam
        response = requests.post("http://borrow_service:5003/return", json={
            "user_id": user_id,
            "book_id": book_id
        })
        
        if response.status_code == 200:
            flash("Book returned successfully!", "success")
        else:
            flash("Failed to return book. Try again.", "danger")
    except Exception as e:
        flash(f"Service unavailable: {str(e)}", "danger")
        
    # Malli My Books page ki redirect chesthunnam
    return redirect(url_for('my_books'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
