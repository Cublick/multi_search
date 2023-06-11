import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True)

totalsearch = Blueprint("total_search", __name__, url_prefix="/")

# 통합검색 (name, desc, tag, region) 4개의 field에 대한 검색
@totalsearch.route('/total_search', methods=['POST', 'GET'])
def total_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경 필요
    keyword = request.args.get("keyword", False)

    # keyword 저장
    def search_terms():
        body = {
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "search_term": keyword
                        }
                    }
                }
            }
        }

        search_es = es.search(index='search_term', body=body)

        # 만약 값이 없다면 keyword 를 search_term index에 저장
        if search_es['hits']['total']['value'] == 0:
            doc = {
                "search_term": keyword,
                "count": 1
            }
            es.index(index="search_term", doc_type="_doc", body=doc)

        # search_term index에 이미 keyword가 있다면 count+1
        else:

            id = search_es['hits']['hits'][0]['_id']
            count = search_es['hits']['hits'][0]['_source']['count']
            source_to_update = {
                "doc": {
                    "search_term": keyword,
                    "count": count + 1
                }
            }

            es.update(index="search_term", doc_type="_doc",
                      id=id, body=source_to_update)

# -------------------------------------------------------------------------------------------------

    # pagination
    try:
        page_number = int(request.args.get('page', 1))
    except:
        page_number = 1

    if page_number == 1:
        from_range = 0
    elif page_number >= 2:
        from_range = (page_number-1)*20

    if not keyword:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        }
                    ],
                    "filter": [
                        {
                            "match": {
                                "isSystem": False
                            }
                        }
                    ]
                }
            },
            'from': from_range,
            'size': 20
        }
    else:
        body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "term": {
                                "name.ngram": {
                                    "value": keyword,
                                    "boost": 6,
                                }
                            },
                        },
                        {
                            "term": {
                                "categoryInfo.main.categoryName.ngram": {
                                    "value": keyword,
                                    "boost": 700
                                }
                            }
                        },
                        {
                            "term": {
                                "categoryInfo.middle.categoryName.ngram": {
                                    "value": keyword,
                                    "boost": 700
                                }
                            }
                        },
                        {
                            "term": {
                                "taggedTags.tagName": {
                                    "value": keyword,
                                    "boost": 5
                                }
                            }
                        },
                        {
                            "term": {
                                "desc.ngram": {
                                    "value": keyword,
                                    "boost": 1
                                }
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                    "filter": [
                        {
                            "match": {
                                "isSystem": False
                            }
                        }
                    ]
                },
            },
            'sort': [
                {
                    "_score": {
                        "order": "desc"
                    },
                },
            ],
            'from': from_range,
            'size': 20
        }

    res = {'_id': [], 'name': []}

    search_result = es.search(index='presentations', body=body) # , scroll='1s'

    # pprint(search_result)

    for i in search_result['hits']['hits']:
        if i['_id'] not in res['_id']:
            res['name'].append(i['_source']['name'])
            res['_id'].append(i['_id'])

    ## scroll -- 10,000개 이상 표출할때 // 속도 조금 걸림
    # while len(search_result['hits']['hits']):
    #     search_result = es.scroll(
    #         scroll_id=search_result['_scroll_id'],
    #         scroll='1s'
    #     )
    #
    #     for i in search_result['hits']['hits']:
    #         if i['_id'] not in res['_id']:
    #             res['_id'].append(i['_id'])
    #             res['name'].append(i['_source']['name'])

    # search_terms()

    return jsonify(res)