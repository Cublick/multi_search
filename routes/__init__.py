# __init__.py 폴더에서 가장 먼저 실행

# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위폴더 접근

from . import multi_search, presentations_total_search, category_tag_list_appear, price_search, mood_search, tag_search, rating_search
from flask import jsonify,  Flask, request, redirect
from flasgger import Swagger

app = Flask(__name__)

app.register_blueprint(multi_search.categorysearch) # blueprint : flask에서 제공하는 라이브러리, (파일명.menutest파일에서의 me_ca 사용할 명)
# app.register_blueprint(total_search.totalsearch)
app.register_blueprint(category_tag_list_appear.list_appear)
app.register_blueprint(price_search.pricesearch)
app.register_blueprint(mood_search.moodsearch)
app.register_blueprint(tag_search.tagsearch)
app.register_blueprint(rating_search.ratingsearch)

@app.route("/")
def hello():
    return "Cublick Digital"