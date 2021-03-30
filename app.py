from flask import Flask, request, jsonify
from utils import connection

app = Flask(__name__)

@app.route('/co')
def method_name():
   return 'hello world!'

@app.route('/post', methods=['POST'])
def method_conn():
  conn, cur = connection()
  data_json = request.get_json()
  
  i_d = data_json['id']
  firstname = data_json['firstname']
  lastname = data_json['lastname']
  email = data_json['email']
  pass_word = data_json['password']

  select_query = 'select email_id from details where email_id=%s;'
  valu_qur = (email,)
  cur.execute(select_query, valu_qur)
  email_data = cur.fetchall()
  print(email_data)
  print(email)

   

  if len(email_data) == 0 :
     cur_query = 'insert into details(usr_id, first_name, last_name, email_id, pass_word) values(%s, %s, %s, %s, %s);'
     qur_values = (i_d, firstname, lastname, email, pass_word)
     cur.execute(cur_query, qur_values)
     conn.commit()
     print('data is sent')
     return jsonify(message='data sent')

  else:
     print('email is already exixts')
     return jsonify(message='email is already exists')
conn, cur = connection()
@app.route('/<int:data>/<pass_word>', methods=['GET', 'DELETE', 'PATCH'])
def methods_types(data,pass_word):
   if request.method == 'GET':
      qur_data = 'select * from details where usr_id=%s;'
      v_qu = (data,)
     
      cur.execute(qur_data,v_qu)
      cur_data = cur.fetchall()
      for data in cur_data:
         t=dict(data)
         k_v={str(i):str(j) for i,j in t.items()}
         print(k_v)
         return str(k_v)

   if request.method == 'PATCH':
      qur_data = 'update details set pass_word=%s where usr_id=%s;'
      v_qur = (pass_word,data)
      cur.execute(qur_data,v_qur)
      conn.commit()
      return 'data updated'

   if request.method == 'DELETE':
      qur_data='delete from details where usr_id=%s;'
      v_qu = (data,)
      cur.execute(qur_data,v_qu)
      conn.commit()
      
      return 'successfully deleted'

  

@app.route('/<int:use_id>/<int:new_id>/<firstname>/<lastname>/<email>/<pass_word>', methods=['PUT'])
def method_put(use_id,new_id,firstname,lastname,email,pass_word):
   if request.method == 'PUT':
      qur_data = '''update details set usr_id=%s, first_name=%s,
                     last_name=%s, email_id=%s, pass_word=%s
                     where usr_id=%s;'''
      v_qu =(new_id,firstname,lastname,email,pass_word,use_id)

      cur.execute(qur_data,v_qu)
      conn.commit()

      return 'data fully updated'

cur.close()
conn.close()
  

if __name__ == '__main__':
    app.run(debug=True, port=5001)