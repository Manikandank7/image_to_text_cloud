from flask import *
from pytesseract import pytesseract
import cv2
import os
app = Flask(__name__)

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        for i in os.listdir(r"download"):
                os.remove(r"download\\"+i)
        pytesseract.tesseract_cmd = r"D:pytesseract\tesseract.exe"
        files = request.files.getlist('file')
        for file in files:
            file.save(os.path.join('upload', file.filename))
        for file in files:   
            img1=cv2.imread('upload/'+file.filename)
            text=pytesseract.image_to_string(img1,lang='eng',config='--psm 6')
            mode = 'a' if os.path.exists('download/download.txt') else 'w'
            with open('download/download.txt', mode) as f:
                f.write(text)
        for i in os.listdir(r"upload"):
                os.remove(r"upload\\"+i)
        return render_template("success.html", name = "Extraction completed")  

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "download/download.txt"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':  
    app.run(debug = True)  
