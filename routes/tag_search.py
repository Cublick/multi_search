import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

tagsearch = Blueprint("tag_search", __name__, url_prefix="/")

# 다면 검색을 위한 함수
@tagsearch.route('/tag_search', methods=['POST', 'GET'])
def tag_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경 필요
    tag_result = request.args.get("tag", False)
    main_result = request.args.get('main', False) # 대분류

    body = {
        'query': {
            'bool': {
                'should': [
                    {
                        "term": {
                            "categoryInfo.main.categoryName": main_result
                        }
                    }
                ],
                'filter': [
                    {
                        'match': {
                            'taggedTags.tagName': {
                                'query': tag_result
                            }
                        }
                    }
                ]
            }
        },
        'size': 10000
    }

    res = {'_id': [], 'name': []}

    tag_search_result = es.search(index='presentations', body=body)

    for i in tag_search_result['hits']['hits']:
        if i['_id'] not in res['_id']:
            res['_id'].append(i['_id'])
            res['name'].append(i['_source']['name'])

    return jsonify(res)

#
