from flask import Flask, request,jsonify
import json
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

#Do NOT put functions/statement outside functions

# Show your student ID
@app.route('/mystudentID/', methods=['GET'])
def my_student_id():    
    response={"studentID": "12345678G"}
    return jsonify(response), 200, {'Content-Type': 'application/json'}
 

if __name__ == '__main__':
   app.run()

