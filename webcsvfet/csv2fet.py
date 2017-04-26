import os, sys
from flask import Flask, request, redirect, Response, make_response,flash, render_template, session
import tempfile
from xml.etree import ElementTree as ET
sys.path.append("/home/asier/Hezkuntza/python-hezkuntza/python-fet/ordutegia")
import MendiFet as MF

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def process_file(file):
    # create a temporary directory using the context manager
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        file.save(os.path.join(tmpdirname, file.filename))
        a=MF.MendiFet()
        a.read_csv_data(os.path.join(tmpdirname, file.filename))
        a.set_hours(['08:30-9:25','09:25-10:20', '10:20-11:15','11:45-12:40','11:15-11:45', '11:45-12:40','12:40-13:35', '13:35-14:30', '14:30-15:20' ])
        a.set_days(['Astelehena', 'Asteartea', 'Asteazkena', 'Osteguna', 'Ostirala'])
        a.set_name('Mendillorri BHI')
        a.generate_from_raw_data()
        a.generate_teachers_from_activities()
        a.generate_subjects_from_activities()
        a.generate_rooms_from_activities()
        a.generate_buildings_from_rooms()
        a.create_groups_XML(a.generate_groups_from_activities())
        xml = ET.tostring(a.fetxml)                
        response = make_response(xml)
        response.headers["Content-Type"] = "text/xml; charset=utf-8"
        response.headers["Content-Disposition"] = "attachment; filename="+file.filename[:-3]+".fet"
        return response

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename[-4] != '.csv':
            flash('File is not *.csv')
            return redirect(request.url)
        if file:
            process_file(file)
    return render_template("index.html") 
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
    
    