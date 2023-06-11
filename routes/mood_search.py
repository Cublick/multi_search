import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

moodsearch = Blueprint("mood_search", __name__, url_prefix="/")

# 다면 검색을 위한 함수
@moodsearch.route('/mood_search', methods=['POST', 'GET'])
def mood_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경 필요
    mood_result = request.args.get('mood', False)
    price_range = request.args.get('price', False)

    # 가격 범위 설정
    if not price_range:
        range = {
            'gte': 0
        }
    else:
        price_list = price_range.split(',')
        if len(price_list) == 1:
            range = {
                'gte': 0,  # gte: 이상 / gte: 초과
                'lte': price_range  # lte: 이하 / lt: 미만
            }
        elif len(price_list) == 2:
            range = {
                'gte': price_list[0].strip(),
                'lte': price_list[1].strip()
            }

    body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'tags.tagName.jaso': {
                                'query': mood_result,
                                'analyzer': 'suggest_search_analyzer'
                            }
                        }
                    }
                ],
                'should': [
                    {
                        'match': {
                            'tags.tagName.ngram': {
                                'query': mood_result,
                                'analyzer': 'my_ngram_analyzer'
                            }
                        }
                    }
                ],
                'filter': [
                    {
                        'range': {
                            'price': range
                        },
                    }
                ]
            }
        }
    }

    res = {'id': [], 'name': [], 'desc': [], 'tags': [], 'category': {'main': [], 'middle': []}, 'price': []}

    search_result = es.search(index='presentations', body=body)

    for i in search_result['hits']['hits']:
        if i['_source']['id']['$oid'] not in res['id']:  # 중복제거
            res['id'].append(i['_source']['id']['$oid'])
            res['name'].append(i['_source']['name'])
            res['desc'].append(i['_source']['desc'])
            res['category']['main'].append(i['_source']['category']['main']['categoryName'])
            res['category']['middle'].append(i['_source']['category']['middle']['categoryName'])

            tmp = []
            for tag_hits in i['_source']['tags']:
                tmp.append(tag_hits['tagName'])
            res['tags'].append(tmp)

            res['price'].append(i['_source']['price'])

    return jsonify(res)

#
