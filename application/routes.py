from application import app
from flask import render_template, url_for, request, redirect, session
from application import utils
import secrets
import os
from application.forms import MyForm

from googletrans import Translator 
from gtts import gTTS 

import cv2
import pytesseract
import numpy as np

@app.route("/")
def index():
    return render_template("index.html", title = "Home Page")


@app.route("/upload", methods={"POST", "GET"})
def upload():
    if request.method == "POST":

        sentence = ""
        
        f = request.files.get("file")
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(20) + f".{extension}"

        file_location = os.path.join(app.config["UPLOADED_PATH"], generated_filename)
        f.save(file_location)

        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

        img = cv2.imread(file_location)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # boxes = pytesseract.image_to_data(img)
        # for i, box in enumerate(boxes.splitlines()):
        #     if i == 0:
        #         continue

        #     box = box.split()

        #     if len(box) == 12:
        #         sentence += box[11] + " "

        sentence = pytesseract.image_to_string(img)
            
        # print(sentence)
        session["sentence"] = sentence

        os.remove(file_location)

        return redirect("/decoded/")

    return render_template("upload.html", title = "Upload Page")

@app.route("/decoded", methods={"POST", "GET"})
def decoded():

    sentence = session.get("sentence")

    form = MyForm()

    if request.method == "POST":

        text_data = form.text_field.data
        translate_to = form.language_field.data

        print("Tanslate to: ", translate_to)

        def translate_text(text, destlang):
            # print(text, destlang)
            translated_text = translator.translate(text, dest=destlang)
            return translated_text.text

        translator = Translator()
        translated_text = translate_text(text_data, translate_to)

        print(translated_text)

        form.text_field.data = translated_text

        speak = gTTS(text=translated_text, lang=translate_to, slow=False)

        generated_audio_filename = secrets.token_hex(10) + ".mp3"
        file_location = os.path.join(app.config["AUDIO_FILE_UPLOAD"], generated_audio_filename)
        speak.save(file_location)

        # Using OS module to run the translated voice.
        # playsound('captured_voice.mp3')
        # os.remove('captured_voice.mp3')
        # print(text)

        return render_template(
            "decoded.html", 
            title = "Translation Page", 
            form = form,
            audio = True, 
            file = generated_audio_filename
            )
    
    else :
        form.text_field.data = sentence
        session["sentence"] = ""

    return render_template("decoded.html", title = "Translation Page", form = form,  audio = False)
