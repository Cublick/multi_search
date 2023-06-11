import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

testtotalsearch = Blueprint("test_total_search", __name__, url_prefix="/")

# 통합검색 (name, desc, tag, region) 4개의 field에 대한 검색
@testtotalsearch.route('/test_total_search', methods=['POST', 'GET'])
def test_total_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경필요
    keyword = request.args.get("keyword", False)
    price_range = request.args.get('price', False)

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
                        'multi_match': {
                            'query': keyword,
                            'fields': ['name.ngram', 'desc.ngram', 'taggedTags.tagName',
                                       'categoryInfo.main.categoryName', 'categoryInfo.middle.categoryName']
                            # # .jaso / .ngram
                            # 'analyzer': 'suggest_search_analyzer'
                            # 'analyzer': 'my_ngram_analyzer'
                        }
                    }
                ],
                # 'filter': [
                #     {
                #         'range': {
                #             'price': range
                #         }
                #     }
                # ]
            }
        },
        '_source': ['_id'],
        'sort': [
            {
                'updatedDate': 'asc'
            }
        ],
        'size': 1000
    }

    res = {'_id': []}

    if keyword:
        # search_result = es.msearch(body=body)
        search_result = es.search(index='presentations', body=body)

        for i in search_result['hits']['hits']:
            if i['_id'] not in res['_id']:
                res['_id'].append(i['_id'])

    return jsonify(res)