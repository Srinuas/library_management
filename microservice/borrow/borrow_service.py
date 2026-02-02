from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database Connection Logic
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "digital_library")
    )

# 1. Borrow Book API
@app.route("/borrow", methods=["POST"])
def borrow_book():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO borrow_records (user_id, book_id) VALUES (%s, %s)", 
                       (data["user_id"], data["book_id"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Book borrowed"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Return Book API (NEWLY ADDED)
@app.route("/return", methods=["POST"])
def return_book():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        # User ID mariyu Book ID match ayithene delete chesthundhi
        cursor.execute("DELETE FROM borrow_records WHERE user_id=%s AND book_id=%s", 
                       (data["user_id"], data["book_id"]))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Book returned successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Get My Books API (UPDATED)
@app.route("/mybooks/<int:user_id>", methods=["GET"])
def my_books(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # IMPORTANT: 'b.id as book_id' ani add chesanu. 
        # Idi lekapothe return cheyyadam kastam.
        cursor.execute("""
            SELECT b.id as book_id, b.title, b.author, br.borrow_date 
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.user_id=%s
        """, (user_id,))
        
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
