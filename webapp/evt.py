import os
from flask import Flask, request, redirect, url_for, send_from_directory
import datetime
import teachereval


UPLOAD_FOLDER = '/home/asier/Hezkuntza/python-hezkuntza/python-fet/webapp/files'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def pt(sumdic):
    text = "<table class=\"table table-striped\"><tr><th>Dias completos</th><th>Profesores</th></tr>"
    for key in sumdic.keys():
        text += "<tr><td>"+ str(key) + "</td><td> " + str(sumdic[key]) + "</td></tr>"
    text += "</table>"
    return text

def secure_filename(filename):
    time = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    return (time + filename).replace(" ","")

def allowed_file(filename):
    return filename[-12:] == 'teachers.xml'

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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tdic, sumdic = teachereval.evaluate(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            teachereval.write(tdic,sumdic,os.path.join(app.config['UPLOAD_FOLDER'], filename[:-3]+"csv"))
            #return redirect(request.url) #redirect(url_for('uploaded_file',upload_file=filename))
            return '''
            <!DOCTYPE html>
            <html lang="es">
                <head>
                    <title>Evaluación de archivo</title>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
                </head>
                <body>
                    <div class="jumbotron">
                        <h1>Resultados de</h1>
                        <p>%s</p>
                    </div>
                    <div class="row">
                        <div class="col-md-4"></div>
                        <div class="col-md-4">%s</div>
                        <div class="col-md-4"></div>
                    </div>
                    <p><a class="label label-primary" href=/csv/%s target="_blank"  style="margin-right: 5px;">Descargar csv </a></p>
                    <h1>Sube un archivo teachers.xml</h1>
                    <form action="" method=post enctype=multipart/form-data>
                         <div class="row">
                            <div class="col-md-4"><input class="form-control" type=file name=file></div>
                            <div class="col-md-4"><input class="btn btn-default" type=submit value=Upload></div>
                            <div class="col-md-4"></div>
                        </div>
                    </form>
                </body>
            </html>
            '''%(filename,pt(sumdic),filename[:-3]+"csv")
    return '''
     <!DOCTYPE html>
    <html lang="es">
        <head>
            <title>Evaluar archivo fet</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        </head>
        <body>
            <div class="jumbotron">
                <h1>Sube un archivo teachers.xml</h1>
            </div>
            <form action="" method=post enctype=multipart/form-data>
                <div class="row">
                        <div class="col-md-4"><input class="form-control" type=file name=file></div>
                        <div class="col-md-4"><input class="btn btn-default" type=submit value=Upload></div>
                        <div class="col-md-4"></div>
                    </div>
                    
            </form>
        </body>
    </html>
    '''
    
@app.route('/csv/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    
    