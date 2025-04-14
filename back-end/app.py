from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/products', methods=['GET'])
def get_products():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Missing required fields (name, price)'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)",
            (data['name'], data['price'], data.get('description', None))
        )
        connection.commit()
        product_id = cursor.lastrowid
        cursor.close()
        connection.close()

        return jsonify({
            'id': product_id,
            'name': data['name'],
            'price': data['price'],
            'description': data.get('description')
        }), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        updates = []
        values = []
        if 'name' in data:
            updates.append("name = %s")
            values.append(data['name'])
        if 'price' in data:
            updates.append("price = %s")
            values.append(data['price'])
        if 'description' in data:
            updates.append("description = %s")
            values.append(data['description'])

        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        values.append(id)
        cursor.execute(query, tuple(values))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Product updated successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)