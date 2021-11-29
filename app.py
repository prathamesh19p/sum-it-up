import text_summ as ts
import re
import requests                                    
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask("__name__")

paragraphs = []

@app.route('/')
@app.route('/css/')
@app.route('/img/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getvalue():
    url_str = request.form['name']
    rem = "Please Only Enter the Hindu Editorial Article!"
    if url_str=="":
        return render_template('index.html', rem=rem)
    else:
        response = requests.get(str(url_str))
        cap = re.findall('[0-9]+\.ece', url_str)
        cap1 = re.findall('[0-9]+', cap[0])
        divid = "content-body-14269002-" + cap1[0]
        soup = BeautifulSoup(response.content, "html.parser")
        layout = soup.find("div", attrs={"id": divid})
        paragraphs = layout.find_all('p')
        SentRank = ts.summa(paragraphs)
        sentGen = ts.gensima(paragraphs)
        return render_template('index.html', sentGen=sentGen, SentRank=SentRank)



if __name__ == '__main__':
    app.run(debug=True)
