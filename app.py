# app.py
from flask import Flask, render_template, request, jsonify

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  return render_template('index.html',user="반원",data={'level':60,'point':360,'exp':45000})

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    # TODO: 여기에 추천 알고리즘 연결
    response = {
        "route": ["경복궁", "광장시장", "DDP"],
        "total_distance_km": 3.8
    }
    return jsonify(response)

if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)

##