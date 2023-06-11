import random
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from elasticsearch import Elasticsearch
from pprint import pprint

es = Elasticsearch(
    'http://34.64.63.141:9200', maxsize=25, timeout=30, max_retries=10, retry_on_timeout=True) # http://34.64.63.141:9200

categorysearch = Blueprint("category_search", __name__, url_prefix="/")

# 다면 검색을 위한 함수
@categorysearch.route('/category_search', methods=['POST', 'GET'])
def category_search():
    # http://daplus.net/python-%ED%94%8C%EB%9D%BC%EC%8A%A4%ED%81%AC-%EC%9A%94%EC%B2%AD%EC%97%90%EC%84%9C-%EC%88%98%EC%8B%A0-%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8-%EC%98%A4%EA%B8%B0/
    # 요청 타입에 맞춰 변경 필요
    parameters = dict(request.get_json())
    res = {'Info': [], '_id': []}
    pages = {'current': 0, 'prev': 0, 'hasPrev': False, 'next': 0, 'hasNext': 'true', 'total': 0}
    items = {'begin': 0, 'end': 0, 'total': 0}

    result = {'data': '', 'pages': '', 'items': ''}

    try:
        # pagination
        try:
            page_number = int(parameters['page'])
        except:
            page_number = 1

        if page_number == 1:
            from_range = 0
        elif page_number >= 2:
            from_range = (page_number-1)*parameters['perPage']

        # setting price range
        if not parameters['price']:
            price_range = {
                'gte': 0
            }
        else:
            if len(parameters['price']) == 1: # 이하 처리
                price_range = {
                    'gte': 0,  # gte: 이상 / gte: 초과
                    'lte': int(parameters['price'][0])  # lte: 이하 / lt: 미만
                }
            elif len(parameters['price']) == 2:
                price_range = {
                    'gte': int(parameters['price'][0]),
                    'lte': int(parameters['price'][1])
                }

        # setting likes range
        if not parameters['likes']:
            likes_range = {
                'gte': 0
            }
        else:
            if len(parameters['likes']) == 1:  # 이하 처리
                likes_range = {
                    'gte': 0,  # gte: 이상 / gte: 초과
                    'lte': int(parameters['likes'][0])  # lte: 이하 / lt: 미만
                }
            elif len(parameters['price']) == 2:
                likes_range = {
                    'gte': int(parameters['likes'][0]),
                    'lte': int(parameters['likes'][1])
                }

        # setting sort
        Tosort = {
            'updatedDate': {
                'order': 'desc'}
        }
        try:
            if parameters['sort'] == 'updatedDate':
                Tosort = {
                    'updatedDate': {
                        'order': 'desc'}
                }
            elif parameters['sort'] == 'downloadCount':
                Tosort = {
                    'downloadCount': {
                        'order': 'desc'}
                }
            elif parameters['sort'] == 'low_price':
                Tosort = {
                    'price': {
                        'order': 'asc'}
                }
            elif parameters['sort'] == 'high_price':
                Tosort = {
                    'price': {
                        'order': 'desc'}
                }
        except:
            Tosort = {
                'updatedDate': {
                    'order': 'desc'}
            }

        # When you didn't choose anything
        if not parameters['price'] and (not parameters['main']) and (not parameters['moods']) and (not parameters['likes']) and (not parameters['styles']):
            body = {
                'query': {
                    'bool': {
                        'must': {
                            'match_all': {},
                        },
                        'filter': [
                            {
                                "match": {
                                    "isSystem": parameters['isSystem']
                                }
                            },
                        ]
                    }
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }

            category_search_result = es.search(index='presentations', body=body)

            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page']-1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (parameters['perPage']*parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # only select price
        if parameters['price'] and (not parameters['main']) and (not parameters['moods']) and (not parameters['likes']) and (not parameters['styles']):
            body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'range': {
                                    'price': price_range
                                }
                            }
                        ],
                        'filter': [
                            {
                                "match": {
                                    "isSystem": parameters['isSystem']
                                }
                            },
                        ]
                    }
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }
            category_search_result = es.search(index='presentations', body=body)
            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page'] - 1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (
                            parameters['perPage'] * parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # only select moods
        if parameters['moods'] and (not parameters['main']) and (not parameters['price']) and (not parameters['likes']) and (not parameters['styles']):
            body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                        'moods.moodName': parameters['moods'],
                                }
                            }
                        ],
                        'filter': [
                            {
                                "match": {
                                    "isSystem": parameters['isSystem']
                                }
                            },
                        ]
                    }
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }
            category_search_result = es.search(index='presentations', body=body)
            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page'] - 1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (
                            parameters['perPage'] * parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # only select likes
        if parameters['likes'] and (not parameters['main']) and (not parameters['price']) and (not parameters['moods']) and (not parameters['styles']):
            body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'range': {
                                    'price': likes_range
                                }
                            }
                        ],
                        'filter': [
                            {
                                "match": {
                                    "isSystem": parameters['isSystem']
                                }
                            },
                        ]
                    }
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }

            category_search_result = es.search(index='presentations', body=body)
            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page'] - 1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (
                            parameters['perPage'] * parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # setting only sort
        if parameters['sort'] and (not parameters['main']) and (not parameters['price']) and (not parameters['moods']) and (not parameters['likes']) and (not parameters['styles']):
            body = {
                'bool': {
                    'must': [
                        {
                            'query': {
                                'match_all': {}
                            },
                        }
                    ],
                    'filter': [
                        {
                            "match": {
                                "isSystem": parameters['isSystem']
                            }
                        },
                    ]
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }
            category_search_result = es.search(index='presentations', body=body)
            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page'] - 1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (
                            parameters['perPage'] * parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # only select styles
        if parameters['styles'] and (not parameters['main']) and (not parameters['price']) and (not parameters['likes']) and (not parameters['moods']):
            body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                    'styles.styleName': parameters['styles'],
                                }
                            }
                        ],
                        'filter': [
                            {
                                "match": {
                                    "isSystem": parameters['isSystem']
                                }
                            },
                        ]
                    }
                },
                'from': from_range,
                'size': parameters['perPage'],
                'sort': [
                    Tosort
                ]
            }
            category_search_result = es.search(index='presentations', body=body)
            for i in category_search_result['hits']['hits']:
                if i['_id'] not in res['_id']:  # 중복제거
                    # Presentation Information
                    i['_source']['_id'] = i['_id']
                    res['_id'].append(i['_id'])
                    res['Info'].append(i['_source'])

                    # Calculate Presentation Page
                    pages['current'] = parameters['page']
                    if parameters['perPage'] == 1:
                        pages['prev'] = 0
                        parameters['hasPrev'] = False
                    else:
                        pages['prev'] = parameters['page'] - 1
                        parameters['hasPrev'] = True

                    if category_search_result['hits']['total']['value'] / (
                            parameters['perPage'] * parameters['page']) != 0:
                        pages['next'] = pages['current'] + 1
                        pages['hasNext'] = True
                    else:
                        pages['next'] = pages['current']
                        pages['hasNext'] = False

                    if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                        pages['total'] = 1
                    else:
                        pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

                    # Calculate Presentation number
                    items['begin'] = 1
                    items['end'] = category_search_result['hits']['total']['value']
                    items['total'] = category_search_result['hits']['total']['value']

            result['data'] = res['Info']
            result['pages'] = pages
            result['items'] = items

            return jsonify(result)

        # only select category
        if parameters['main']:
            if parameters['middle']:
                category_body = {
                    'match': {
                        'categoryInfo.middle.categoryName': {
                            'query': parameters['middle']
                        }
                    }
                }
            else:
                category_body = {
                    'match': {
                        'categoryInfo.main.categoryName': {
                            'query': parameters['main']
                        }
                    }
                }
        else:
            category_body = {
                'match_all': {}
            }

        # moods
        if parameters['moods']:
            moods_body = {
                'match': {
                    'moods.moodName': {
                        'query': parameters['moods']
                    }
                }
            }
        else:
            moods_body = {
                'match_all': {}
            }

        # styles
        if parameters['styles']:
            styles_body = {
                'match': {
                    'styles.styleName': {
                        'query': parameters['styles']
                    }
                }
            }
        else:
            styles_body = {
                'match_all': {}
            }

        # category main query body
        m_category_search = {
            'query': {
                'bool': {
                    'must': [
                        category_body,
                        moods_body,
                        styles_body
                    ],
                    'filter': [
                        {
                            'range': {
                                'price': price_range
                            },
                        },
                        # {
                        #     'range': {
                        #         'likes': likes_range
                        #     }
                        # },
                        {
                            "match": {
                                "isSystem": parameters['isSystem']
                            }
                        },
                    ]
                }
            },
            'from': from_range,
            'size': parameters['perPage'],
            'sort': [
                Tosort
            ]
        }
    except:
        m_category_search = {
            'query': {
                'bool': {
                    'must': {
                        'match_all': {},
                    },
                    'filter': [
                        {
                            "match": {
                                "isSystem": parameters['isSystem']
                            }
                        },
                    ]
                }
            },
            'from': from_range,
            'size': parameters['perPage'],
            'sort': [
                Tosort
            ]
        }

    category_search_result = es.search(index='presentations', body=m_category_search)

    for i in category_search_result['hits']['hits']:
        print(i)
        if i['_id'] not in res['_id']:  #
            # Presentation Information
            i['_source']['_id'] = i['_id']
            res['_id'].append(i['_id'])
            res['Info'].append(i['_source'])

            # Calculate Presentation Page
            pages['current'] = parameters['page']
            if parameters['perPage'] == 1:
                pages['prev'] = 0
                parameters['hasPrev'] = False
            else:
                pages['prev'] = parameters['page'] - 1
                parameters['hasPrev'] = True

            if category_search_result['hits']['total']['value'] / (parameters['perPage'] * parameters['page']) != 0:
                pages['next'] = pages['current'] + 1
                pages['hasNext'] = True
            else:
                pages['next'] = pages['current']
                pages['hasNext'] = False

            if round(category_search_result['hits']['total']['value'] // parameters['perPage']) == 0:
                pages['total'] = 1
            else:
                pages['total'] = round(category_search_result['hits']['total']['value'] // parameters['perPage']) + 1

            # Calculate Presentation number
            items['begin'] = 1
            items['end'] = category_search_result['hits']['total']['value']
            items['total'] = category_search_result['hits']['total']['value']

    result['data'] = res['Info']
    result['pages'] = pages
    result['items'] = items

    return jsonify(result)

#
