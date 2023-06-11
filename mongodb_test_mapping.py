import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import json
import datetime
from elasticsearch import helpers, Elasticsearch
import csv
import time

from elasticsearch import Elasticsearch

csv.field_size_limit(100000000)

# 'http://ec2-54-180-112-236.ap-northeast-2.compute.amazonaws.com:9220'
es = Elasticsearch('http://34.64.63.141:9200', timeout=1000, max_retries=10, retry_on_timeout=True)

document = \
    {
        "settings": {
            "index": {
                "number_of_replicas": "0",
                "max_ngram_diff": 50,
                "analysis": {
                    "filter": {
                        "suggest_filter": {
                            "type": "ngram",
                            "min_gram": 2,
                            "max_gram": 50
                        },
                        "my_synonyms": {
                            "type": "synonym",
                            "synonyms_path": "synonym.txt",
                            "updateable": True
                        }
                    },
                    "analyzer": {
                        "nori": {
                            "tokenizer": "nori_tokenizer"
                        },
                        "my_ngram_analyzer": {
                            "tokenizer": "my_ngram_tokenizer"
                        },
                        "suggest_search_analyzer": {
                            "type": "custom",
                            "tokenizer": "jaso_search_tokenizer"
                        },
                        "suggest_index_analyzer": {
                            "type": "custom",
                            "tokenizer": "jaso_index_tokenizer",
                            "filter": [
                                "suggest_filter"
                            ]
                        },
                        "synonym_analyzer": {
                            "tokenizer": "whitespace",
                            "filter": ["my_synonyms"]
                        },
                        "my_analyzer": {
                            "tokenizer": "whitespace",
                            "filter": ["lowercase", ]
                        }
                    },
                    "tokenizer": {
                        "jaso_search_tokenizer": {
                            "type": "jaso_tokenizer",
                            "mistype": True,
                            "chosung": False
                        },
                        "jaso_index_tokenizer": {
                            "type": "jaso_tokenizer",
                            "mistype": True,
                            "chosung": True
                        },
                        "my_ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": "2",
                            "max_gram": "10"
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },

                "bgAudio": {
                    "properties": {
                        "isRepeat": {
                            "type": "boolean"
                        },
                        "audios": {
                            "type": "nested"
                        }
                    }
                },

                "bg": {
                    "properties": {
                        "type": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "fileType": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "md5": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "mimeType": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },

                "code": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },

                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": "my_ngram_analyzer"
                        },
                        "jaso": {
                            "type": "text",
                            "analyzer": "suggest_index_analyzer"
                        }
                    }
                },

                "desc": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": "my_ngram_analyzer"
                        },
                        "jaso": {
                            "type": "text",
                            "analyzer": "suggest_index_analyzer"
                        }
                    }
                },

                "lock": {
                    "type": "boolean",
                },

                "accessRight": {
                    "type": "long",
                },

                "orientation": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                    }
                },

                "ratio": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                    }
                },

                "width": {
                    "type": "long"
                },

                "height": {
                    "type": "long"
                },

                "bgAudioEnable": {
                    "type": "boolean"
                },

                "bgEnable": {
                    "type": "boolean"
                },

                "tags": {
                    'type': "nested",
                },

                "regions": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": "my_ngram_analyzer"
                        },
                        "jaso": {
                            "type": "text",
                            "analyzer": "suggest_index_analyzer"
                        }
                    }
                },

                "status": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                    }
                },

                "downloadCount": {
                    "type": "long"
                },

                "viewCount": {
                    "type": "long"
                },

                "isPrivate": {
                    "type": "boolean"
                },

                "isSystem": {
                    "type": "boolean"
                },

                "payLevelAccess": {
                    "type": "text",
                    'fields': {
                        'keyword': {
                            'type': 'keyword',
                            'ignore_above': 256
                        },
                    }
                },

                "isGridTpl": {
                    "type": "boolean"
                },

                "mobility": {
                    "type": "boolean"
                },

                "rules": {
                    "type": "nested"
                },

                "asset": {
                    "properties": {
                        "name": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "md5": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "fileType": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },

                "groups": {
                    "type": "nested"
                },

                "sharedList": {
                    "type": "nested"
                },

                "createdDate": {
                    "properties": {
                        "$date": {
                            "properties": {
                                "$numberLong": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                }
                            }
                        }
                    }
                },

                "updatedDate": {
                    "properties": {
                        "$date": {
                            "properties": {
                                "$numberLong": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                }
                            }
                        }
                    }
                },

                "owner": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },

                "v": {
                    "type": "long",
                },

                "categoryInfo": {
                    "properties": {
                        "main": {
                            "properties": {
                                "categoryId": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "categoryLevel": {
                                    "type": "long"
                                },
                                "categoryName": {
                                    "type": "text",
                                    "fields": {
                                        "jaso": {
                                            "type": "text",
                                            "analyzer": "suggest_index_analyzer"
                                        },
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        },
                                        "ngram": {
                                            "type": "text",
                                            "analyzer": "my_ngram_analyzer"
                                        }
                                    }
                                }
                            }
                        },
                        "middle": {
                            "properties": {
                                "categoryId": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "categoryLevel": {
                                    "type": "long"
                                },
                                "categoryName": {
                                    "type": "text",
                                    "fields": {
                                        "jaso": {
                                            "type": "text",
                                            "analyzer": "suggest_index_analyzer"
                                        },
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        },
                                        "ngram": {
                                            "type": "text",
                                            "analyzer": "my_ngram_analyzer"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },

                "price": {
                    "type": "long",
                },

                "taggedTags": {
                    "properties": {
                        "tagId": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        'tagName': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256
                                },
                                'ngram': {
                                    'type': 'text',
                                    'analyzer': 'my_ngram_analyzer'
                                },
                                'jaso': {
                                    'type': 'text',
                                    'analyzer': 'suggest_index_analyzer'
                                }
                            }
                        }
                    }
                },

                "moods": {
                    "properties": {
                        "moodId": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "moodName": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                }
            }
        }
    }

if es.indices.exists(index="mapping_test"):
    pass
else:
    es.indices.create(index="mapping_test", body=document)

# with open(r'C:\Users\com\Desktop\김천 데이터\구글 크롤링 데이터\숙박\gimcheon_accommodation_processing.csv', 'r', encoding='utf-8') as f:
#     reader = csv.DictReader(f)
var = {
   "id": "63589f6ecba1dc001a866523",

   "bgAudio":{
      "isRepeat":False,
      "audios":[

      ]
   },
   "bg":{
      "id":"#ffffff",
      "type":"COLOR",
      "fileType":"",
      "md5":"",
      "mimeType":""
   },
   "code":"undefined",
   "name":"LED test 128by256",
   "desc":"Test for LED (128*256)",
   "lock":False,
   "accessRight":63,
   "orientation":"PORTRAIT",
   "ratio":"NONE",
   "width":128,
   "height":256,
   "bgAudioEnable":True,
   "bgEnable":True,
   "tags":[

   ],
   "regions":"[{\"id\":\"1664518287749\",\"type\":\"FRAME\",\"lock\":false,\"events\":[],\"zOrder\":0,\"slideEffect\":{\"code\":\"\",\"speed\":5,\"repeat\":false,\"delay\":10},\"x\":-110.65,\"y\":-133.09,\"width\":512,\"height\":512,\"rotate\":0,\"bg\":{\"type\":\"COLOR\",\"id\":\"#ffffff00\"},\"bgEnable\":\"false\",\"properties\":{\"caption\":\"\",\"alpha\":255,\"name\":\"rectangle_2.svg\",\"shapeType\":\"FREE\",\"fillColor\":\"#000000ff\",\"fillPattern\":\"\",\"lineColor\":\"#000000ff\",\"linePattern\":\"SOLID\",\"lineDepth\":1,\"data\":\"<g id=\\\"1664518287749\\\" style=\\\"stroke: rgb(0,0,0); stroke-width: 1; stroke-dasharray: 0 0; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\\\" transform=\\\"translate(0 0)\\\" >\\n\\t<path id=\\\"svg_1\\\" d=\\\"M 476 403.5 h -440 c -11 0 -20 -9 -20 -20 v -255 c 0 -11 9 -20 20 -20 h 440 c 11 0 20 9 20 20 v 255 c 0 11 -9 20 -20 20 z\\\" style=\\\"stroke: rgb(0,0,0); stroke-width: 10; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\\\" transform=\\\" matrix(1 0 0 1 0 0) \\\" stroke-linecap=\\\"round\\\" />\\n</g>\\n\",\"oriWidth\":512,\"oriHeight\":512},\"wrapContent\":false},{\"id\":\"1664518216230\",\"type\":\"TEXT\",\"lock\":false,\"events\":[],\"zOrder\":1,\"slideEffect\":{\"code\":\"\",\"speed\":5,\"repeat\":false,\"delay\":10},\"x\":42.04,\"y\":1.38,\"width\":244.03,\"height\":50.85,\"rotate\":89.97,\"bg\":{\"type\":\"COLOR\",\"id\":\"#ffffff00\"},\"bgEnable\":\"false\",\"properties\":{\"caption\":\"\",\"alpha\":255,\"align\":\"center\",\"textEffect\":{\"code\":\"none\",\"speed\":10,\"repeat\":false},\"text\":\"HELLO CUBLICK\",\"name\":\"HELLO CUBLICK\",\"fontName\":\"Anton\",\"fontStyle\":{\"bold\":false,\"italic\":false,\"underline\":false,\"strikethrough\":false},\"fontSize\":\"45\",\"fontColor\":\"#ffffffff\",\"strokeWidth\":0,\"strokeColor\":\"#ffffff00\",\"shadowDX\":1,\"shadowDY\":1,\"shadowRadius\":1,\"shadowColor\":\"#00000000\",\"textLineSpacing\":1.16,\"styles\":{},\"singleLine\":false},\"wrapContent\":false},{\"id\":\"1664518251627\",\"type\":\"FRAME\",\"lock\":false,\"events\":[],\"zOrder\":2,\"slideEffect\":{\"code\":\"\",\"speed\":5,\"repeat\":false,\"delay\":10},\"x\":48.72,\"y\":13.58,\"width\":61.44,\"height\":87.04,\"rotate\":0,\"bg\":{\"type\":\"COLOR\",\"id\":\"#ffffff00\"},\"bgEnable\":\"false\",\"properties\":{\"caption\":\"\",\"alpha\":255,\"name\":\"shape_heart_2.svg\",\"shapeType\":\"FREE\",\"fillColor\":\"#ff0000ff\",\"fillPattern\":\"\",\"lineColor\":\"#ff0000ff\",\"linePattern\":\"SOLID\",\"lineDepth\":1,\"data\":\"<g id=\\\"1664518251627\\\" style=\\\"stroke: rgb(255,0,0); stroke-width: 1; stroke-dasharray: 0 0; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,0,0); fill-rule: nonzero; opacity: 1;\\\" transform=\\\"translate(0 0)\\\" >\\n\\t<path id=\\\"svg_1\\\" d=\\\"M 16 170.1 c 0 82.9 74.9 142 131.3 186.6 c 58.6 46.3 90 71.3 108.7 90 c 18.8 -18.8 49.4 -44.7 108.7 -90 c 57.2 -43.7 131.3 -104.6 131.3 -187.5 c 0 -121.7 -165 -142.5 -240 -30 c -75 -112.5 -240 -91.7 -240 30.9 z\\\" style=\\\"stroke: rgb(255,0,0); stroke-width: 10; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,0,0); fill-rule: nonzero; opacity: 1;\\\" transform=\\\" matrix(1 0 0 1 0 0) \\\" stroke-linecap=\\\"round\\\" />\\n</g>\\n\",\"oriWidth\":512,\"oriHeight\":512},\"wrapContent\":false}]",
   "status":"ACTIVATED",
   "downloadCount":19,
   "viewCount":2,
   "isPrivate":True,
   "isSystem":False,
   "payLevelAccess":"FREE",
   "isGridTpl":False,
   "mobility":False,
   "rules":[

   ],
   "assets":[

   ],
   "groups":[

   ],
   "sharedList":[

   ],
   "createdDate":{
      "$date":{
         "$numberLong":"1666752366981"
      }
   },
   "updatedDate":{
      "$date":{
         "$numberLong":"1666752367884"
      }
   },
   "owner": "592d1d91b138731350b1d2ff",

   "v":0,
   "categoryInfo":{
      "main":{
         "categoryId": "63578d4aa6fe4ea5846de9c7",
         "categoryName": "음식",
         "categoryLevel": 0
      },
      "middle":{
         "categoryId": "63577aa32d98059c54cb5837",
         "categoryName":"한식",
         "categoryLevel":1
      }
   },
   "price": 6000,
   "taggedTags":[
      {
         "tagId": "6360cb9a58d1b57be0a637d2",
         "tagName":"비빔밥"
      }
   ],
    "moods": {
        "moodId": "6360cb9a58d1c68be0a637d2",
        "moodName": "따뜻한"
    }
}

es.index(index="mapping_test", body=var)
# helpers.bulk(es, var, index="mapping_test_2")
