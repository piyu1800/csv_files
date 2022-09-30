from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from os.path import join , dirname, realpath
import mysql.connector
app = Flask(__name__)

app.config["DEBUG"] = True


UPLOAD_FOLDER='static/files'
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

mydb= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pk_123456",
    database="students"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename !='':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return redirect(url_for('index'))

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['Name','Mobile','Address', 'Education']
      print('column Name:', col_names)

      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      print('CSV Data:', csvData)
      # Loop through the Rows
      for i,row in csvData.iterrows():
        sql =  "INSERT INTO addresses (Name, Mobile, Address , Education) VALUES (%s, %s, %s, %s)"
        print('SQL:',sql)
        value = (row['Name'], row['Mobile'], row['Address'], row['Education'])
        print('values:',value)
        mycursor.execute(sql, value, if_exists='append')
        mydb.commit()
        print(i,row['Name'],row['Mobile'],row['Address'],row['Education'])


if (__name__ == "__main__"):
     app.run(port = 5000)