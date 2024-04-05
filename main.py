from mysql.connector import connect
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

#konek to DB
# try:
mydb = {
            'host' : os.environ.get('HOST'),
            'port' : os.environ.get('PORT'),
            'username' : os.environ.get('USER'),
            'password' : os.environ.get('PASSWORD'),
            'database' : os.environ.get('DB')
    }
#     print("Connection successful!")

# except mysql.connector.Error as err:
#     print("Connection failed:", err)

# message = [{'title':"Message one",
#             'content':"Content one"},
#             {'title':"Message two", 
#             'content':"Content two"},]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/deploy-clipper', methods=['GET', 'POST'])
def deploy_clipper():
    print(request)
    if request.method == 'GET':
        return render_template('clipper.html')
    else:
        source = request.form['source']
        # print(request.form)
        category = request.form["category"]
        clippername = request.form["clippername"]
        state_id = request.form["state_id"]
        tag_media = request.form["media_tag"]
        baselink = request.form["baselink"]

        #Konek to DB
        conn = connect(**mydb)
        cursor = conn.cursor()

        #insert to DB
        query = "INSERT INTO clippers (source, category, clippername, state_id, tag_media, baselink) VALUES (%s, %s, %s, %s, %s, %s)"

        values = (source, category, clippername, state_id, tag_media, baselink)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('deploy_clipper'))
    # return render_template('clipper.html')

@app.route('/deploy-media', methods=['GET', 'POST'])
def deploy_media():
    if request.method == "GET":
        return render_template('media.html')
    else:
        m_name = request.form["m_name"]
        m_displayName = request.form["m_displayName"]
        m_image = request.form["m_image"]
        m_link = request.form["m_link"]
        m_counter = request.form["m_counter"]
    # return render_template('media.html')
        
    conn=connect(**mydb)
    cursor=conn.cursor()

    query = "INSERT INTO media (m_name, m_displayName, m_image, m_link, m_counter) VALUES (%s, %s, %s, %s, %s)"

    values = (m_name, m_displayName, m_image, m_link, m_counter)
    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('deploy_media'))

@app.route('/upload-media', methods=['POST'])
def upload_media():
    file = request.files['file']
    df = pd.read_csv(file, delimiter=';')

    # print(df.columns)
    # column_names = df.columns.tolist()

    conn = connect(**mydb)
    cursor = conn.cursor()  

    for _,row in df.iterrows():
        # values = (row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], row[column_names[4]])
        # print (row) 
        query = "INSERT INTO media (m_name, m_displayName, m_image, m_link, m_counter) VALUES (%s, %s, %s, %s, %s)"
        values = (row['m_name'], row['m_displayName'], row['m_image'], row['m_link'], row['m_counter'])
        # print (row) 
        cursor.execute(query, values)
        # print(cursor.execute)

    conn.commit()
    cursor.close()
    conn.close()

    return 'Data berhasil di unggah'

@app.route('/upload-clipper', methods=['POST'])
def upload_clipper():
    file = request.files['file']
    df = pd.read_csv(file, delimiter=';')

    conn = connect(**mydb)
    cursor = conn.cursor()

    for _,row in df.iterrows():
        query = "INSERT INTO clippers (source, category, clippername, state_id, tag_media, baselink) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (row['source'], row['category'], row['clippername'], row['state_id'], row['tag_media'], row['baselink'])
        cursor.execute(query, values)
       
        conn.commit()
        cursor.close()
        conn.close()
    
    return 'Data berhasil di unggah'

if __name__ == "__main__":
    app.run(debug=True)