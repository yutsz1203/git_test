from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2 
  
app = Flask(__name__) 
  
# Connect to the database 
conn = psycopg2.connect(database="exe2024_mervin", user="mervin", 
                        password="myu@2024", host="192.168.28.144", port="5432") 

cur = conn.cursor()

cur.execute( 
    '''DROP TABLE tasks;''')

conn.commit() 
  

cur.close() 
conn.close() 

"""
@app.route('/api/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    conn = psycopg2.connect(database="exe2024_mervin", user="mervin", 
                        password="myu@2024", host="192.168.28.144", port="5432") 
    
    cur = conn.cursor()

    cur.execute('''DELETE FROM messages WHERE id = %s''', (message_id,))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': f'Message {message_id} deleted'}), 200
"""
