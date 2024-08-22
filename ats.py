from flask import Flask,render_template,request
import spacy
import PyPDF2
from rapidfuzz import fuzz
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient("mongodb+srv://datta:datta@cluster0.9ek0btm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.ATS_check
collection1 = db.resume_data
collection2 = db.matching_data

nlp_ner = spacy.load("C:\\Users\\Codegnan\\Desktop\\CRUD\\ATS\\output1\\model-best")


@app.route('/',methods=["POST","GET"])
def basic():
    if request.method == "POST":
        job_des = request.form['jobdes']
        files = request.files['filename']
        #data = files.read()
        data = ''  
        reader = PyPDF2.PdfReader(files)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            data += text

        dat1 = {'resume':data}
        #print('---------------',dat1)
        collection1.insert_one(dat1)
        score = fuzz.ratio(data, job_des)
        all_score = round(score)
        doc = nlp_ner(data)
        result= doc.ents
        # for ent in doc.ents:
        #     print(ent.text, ent.label)
        dat = ''
        for res in result:
            dat +=  str(res.text)
        dat2 = {'matching':dat}
        #print('**************************',dat2)
        collection2.insert_one(dat2)
        return render_template('home.html', result=result, score=all_score )
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)