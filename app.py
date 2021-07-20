import easyocr
import re
from tkinter import *
from tkinter import filedialog as fd 
import tkinter as tk 
from PIL import ImageTk, Image
import os

from flask import Flask, app, jsonify, flash, send_file, request,url_for,redirect,abort
app = Flask(__name__)

@app.route('/')
def temp():
        return '''
    <!doctype html>
<title>Face Matching</title>
<h2>Select file(s) to upload</h2>
<h3>Steps to follow:\n1)Upload Aadhar\n2)Upload PAN\n3)Upload haarcascade file\n4) Capture photo of user<h3/>
    <form method="post" action="/">
        <input type="submit" value="Click Here to Start Matching!" name="action1"/>
    </form>
    '''  

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'Click Here to Start Matching!':
          root = Tk()
          filename = fd.askopenfilename()
          reader = easyocr.Reader(['en','hi'])
          result = reader.readtext(filename)#pan matching
          f=""

          for r in result:
            
            # print(r[1])
            if(len(re.findall("^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$",r[1]))!=0):
              print("UID: ", end=" ")
              print(re.findall("^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$",r[1]))
            f+=r[1]
            f+="\n"
          # print(f)
          p=re.findall("[(A-Z)+(0-9)]{10}",f)#PAN NUMBER FULL FINAL
          l=len(p)
          # print("PAN: ", end="")
          pan=p[l-1]
          panini=pan[:5]
          # print(panini)
          # print(pan)
          d=re.findall("[0-9]{2}/[0-9]{2}/[0-9]{4}",f)#DOB FULL FINAL
          dob=d[0]
          # print("DOB: ", end="")
          # print(dob)
          na=re.findall("[A-Z]+[""]+[A-Z]",f)
          t=[]
          for i in range(6,len(na)):
            if(na[i]!=panini and len(na[i])>2):
              t.append(na[i])
          # print(t)

          name=t[0]+" "+t[1]
          # print("Name: ", end="")
          # print(name)
          # nal=len(na)
          # father=na[nal-2]+" "+na[nal-1]
          # print("Father's Name: ", end="")
          # print(father)
          # name=na[nal-4]+" "+na[nal-3]
          # print("Name: ", end="")
          # print(name)
          
            
          # specify size of window.
          root.geometry("250x170")
            
          # Create text widget and specify size.
          T = Text(root, height = 5, width = 52)
            
          # Create label
          l = Label(root, text = "PAN CARD DETAILS")
          l.config(font =("Courier", 14))
            
          Fact ="PAN: "+pan + "\n" + "DOB:" + dob + "\n" +"NAME: " + name
          # Create button for next text.
          # b1 = Button(root, text = "Next", )
            
          # Create an Exit button.
          b2 = Button(root, text = "Exit",
                      command = root.destroy) 
            
          l.pack()
          T.pack()
          # b1.pack()
          b2.pack()
            
          # Insert The Fact.
          T.insert(tk.END, Fact)
            
          tk.mainloop()


if __name__=="__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)