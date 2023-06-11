import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

list_appear = Blueprint("list_appear", __name__, url_prefix="/")

# main category 표출
# 사용자가 캔버스를 작성할때, 카테고리를 등록할 수 있게 목록 반환
@list_appear.route('/get_main_categories', methods=['POST', 'GET'])
def get_main_categories():
    main_category_body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'categoryLevel': 0
                        },
                    }
                ]
            }
        },
        'size': 10000
    }

    res = {'main category list': []}

    main_search_result = es.search(index='categories', body=main_category_body)

    for i in main_search_result['hits']['hits']:
        res['main category list'].append(i['_source']['categoryName'])

    return jsonify(res)

# middle category 표출
# get_main_categories에서 선택된 main category에 해당하는 middle categories 반환
@list_appear.route('/get_middle_categories', methods=['POST', 'GET'])
def get_middle_categories():
    main_category = request.args.get('main', False)

    middle_category_body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'categoryLevel': 1
                        },
                        'match': {
                            'parentCategory.categoryName': main_category
                        }
                    },
                ]
            }
        },
        'size': 10000
    }

    res = {'middle category list': []}
    if main_category:
        tag_search_result = es.search(index='categories', body=middle_category_body)

        for i in tag_search_result['hits']['hits']:
            res['middle category list'].append(i['_source']['categoryName'])

    return jsonify(res)

# tag 셋팅
# 사용자가 category를 설정하여 이에 맞는 tag목록을 표출
@list_appear.route('/get_tags', methods=['POST', 'GET'])
def get_tags():
    main_category = request.args.get('main', False)

    tag_search = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'elderCategoryInfo.categoryName': {
                                'query': main_category,
                            }
                        },
                    }
                ]
            }
        },
        'size': 10000
    }

    res = {'tags': []}

    if main_category:
        tag_search_result = es.search(index='hashtags', body=tag_search)

        for i in tag_search_result['hits']['hits']:
            res['tags'].append(i['_source']['tagName'])

    return jsonify(res)