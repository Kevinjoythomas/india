# from flask_cors import CORS
from flask import Flask,render_template,request,redirect
import pickle
import sklearn
import joblib
import groq
from groq import Groq
import os
import json
import requests
import re
import cv2
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow,imread
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import pyttsx3





    

app = Flask(__name__)
# cors = CORS(app,resources={r'/*':{'origin':'*'}})ṇ

cache={'chats':[]}

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = 'llama3-70b-8192'
def run_conversation(user_prompt):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
           "content": "Your primary role is to support aspiring Indian artisans by providing concise, practical guidance tailored to their craft. Respond as if you’re texting a friend—friendly, clear, and to the point. Focus exclusively on artisan-related topics: troubleshooting techniques, sourcing materials, skill-building tips, and step-by-step roadmaps for career growth. Politely decline any questions outside the scope of artisanal work. While you aim to offer reliable advice, your responses are educational and should complement—rather than replace—hands‑on mentorship or professional training."

        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tool_choice="auto",  
        max_tokens=4096
    )
    response_message = response.choices[0].message.content
    return response_message 
@app.route('/')
def test():
    return render_template('index.html')

@app.route('/login')
def log():
    return render_template('login.html')





@app.route('/test')
def tesasfasf():
   return render_template('test1.html')

@app.route('/features',methods=["POST","GET"])
def features():
   return render_template("features.html")
      

def format_response(resp):
  """
  Convert list responses into formatted markdown strings.
  If resp is a list, the first element is the intro text,
  and subsequent elements are label-description pairs.
  """
  if isinstance(resp, list):
    intro = resp[0]
    items = []
    # Process label-description pairs
    for i in range(1, len(resp), 2):
      label = resp[i]
      desc = resp[i+1] if i+1 < len(resp) else ''
      items.append(f"- **{label}**{desc}")
    return intro + "\n\n" + "\n".join(items)
  return resp
  
  
@app.route('/ChatBot', methods=['GET', 'POST'])
def ChatBot():
    if request.method == 'POST':
        q = request.form.get('prompt', '').strip()
        if not q:
            return render_template('ChatBot.html', data=cache['chats'])

        raw_answer = run_conversation(q)
        # Format list outputs for readability
        answer = format_response(raw_answer)

        cache['chats'].append((q, answer))
        return render_template('ChatBot.html', data=cache['chats'])

    # GET: clear chat on fresh load
    cache['chats'].clear()
    return render_template('ChatBot.html', data=cache['chats'])




   
         


   


if __name__ == '__main__':
  app.run(debug=True) 