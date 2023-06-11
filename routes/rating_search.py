import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

ratingsearch = Blueprint("rating_search", __name__, url_prefix="/")

# 다면 검색을 위한 함수
@ratingsearch.route('/rating_search', methods=['POST', 'GET'])
def rating_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경 필요
    rating = request.args.get('rating', False)

    # paginations
    try:
        page_number = int(request.args.get('page', 1))
    except:
        page_number = 1

    if page_number == 1:
        from_range = 0
    elif page_number >= 2:
        from_range = (page_number - 1) * 20

    # rating
    if not rating:
        rating_range = {
            'gte': 0
        }
    else:
        rating_range = {
            'gte': rating
        }

    body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'range': {
                            'downloadCount': rating_range
                        }
                    }
                ]
            }
        },
        'sort': {
            'downloadCount': 'asc'
        },
        'from': from_range,
        'size': 20
    }

    res = {'_id': [], 'name': []}

    search_result = es.search(index='presentations', body=body)

    for i in search_result['hits']['hits']:
        if i['_id'] not in res['_id']:
            res['name'].append(i['_source']['name'])
            res['_id'].append(i['_id'])

    return jsonify(res)

#
