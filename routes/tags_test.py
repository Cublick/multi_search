# import random
# from flasgger import swag_from
# from flask import jsonify, request, Blueprint
# from elasticsearch import Elasticsearch
# es = Elasticsearch(
#     'http://34.64.63.141:9200', maxsize=25)
#
# tags = Blueprint("tags_test", __name__, url_prefix="/")
#
# @tags.route('/test', methods=['POST', 'GET'])
# def test():
#     # tag 서치할때 모든 데이터를 가져와 전체 태그목록, 해당하는 category의 목록을 반환
#     tag_search = {
#         'query': {
#             'match_all': {}
#         },
#         'size': 2
#     }
#
#     dd = es.search(index='cublick_production', body=tag_search)
#     print(dd)
#
#     return 'test'


# global main_category
#
# # @mongodb.route('/main_category_setting', methods=['POST', 'GET'])
# def main_category_setting():
#     global main_category
#     main_category = 'pp'
#
#     # main_category = request.args.get()
#
# main_category_setting()
# print(main_category)