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

es = Elasticsearch('localhost:9200', timeout=1000, max_retries=10, retry_on_timeout=True)

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
                            "min_gram": 1,
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
                            "min_gram": "1",
                            "max_gram": "10"
                        }
                    }
                }
            }
        },

        "mappings": {
            "properties": {
                "id": {
                    "properties": {
                        "$oid": {
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

                'categoryLevel': {
                    'type': 'integer',
                },

                'childCategories': {
                    'properties': {
                        'categoryId': {
                            'properties': {
                                '$oid': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                }
                            }
                        },
                        'categoryName': {
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

                'categoryName': {
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
                },

                'v': {
                    'type': 'integer'
                },

                'parentCategory': {
                    'properties': {
                        'categoryId': {
                            'properties': {
                                '$oid': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                }
                            }
                        },
                        'categoryName': {
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

            }
        }
    }

var = [{
  "id": {
    "$oid": "63577aa32d98059c54cb5837"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "한식",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "63578d4aa6fe4ea5846de9c7"
    },
    "categoryName": "음식"
  }
},{
  "id": {
    "$oid": "63577ab02d98059c54cb5838"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "양식",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "63578d4aa6fe4ea5846de9c7"
    },
    "categoryName": "음식"
  }
},{
  "id": {
    "$oid": "63577ab92d98059c54cb5839"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "중식",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "63578d4aa6fe4ea5846de9c7"
    },
    "categoryName": "음식"
  }
},{
  "id": {
    "$oid": "63578d4aa6fe4ea5846de9c7"
  },
  "categoryLevel": 0,
  "childCategories": [
    {
      "categoryId": {
        "$oid": "63577aa32d98059c54cb5837"
      },
      "categoryName": "한식"
    },
    {
      "categoryId": {
        "$oid": "63577ab02d98059c54cb5838"
      },
      "categoryName": "양식"
    },
    {
      "categoryId": {
        "$oid": "63577ab92d98059c54cb5839"
      },
      "categoryName": "중식"
    },
    {
      "categoryId": {
        "$oid": "6357935de4938f75d027290b"
      },
      "categoryName": "일식"
    },
    {
      "categoryId": {
        "$oid": "63579364e4938f75d027290c"
      },
      "categoryName": "동남아식"
    }
  ],
  "categoryName": "음식",
  "v": 0
},{
  "id": {
    "$oid": "6357935de4938f75d027290b"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "일식",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "63578d4aa6fe4ea5846de9c7"
    },
    "categoryName": "음식"
  }
},{
  "id": {
    "$oid": "63579364e4938f75d027290c"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "동남아식",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "63578d4aa6fe4ea5846de9c7"
    },
    "categoryName": "음식"
  }
},{
  "id": {
    "$oid": "6357937ce4938f75d027290d"
  },
  "categoryLevel": 0,
  "childCategories": [
    {
      "categoryId": {
        "$oid": "63579380e4938f75d027290e"
      },
      "categoryName": "상의"
    },
    {
      "categoryId": {
        "$oid": "63579384e4938f75d027290f"
      },
      "categoryName": "하의"
    },
    {
      "categoryId": {
        "$oid": "63579388e4938f75d0272910"
      },
      "categoryName": "모자"
    },
    {
      "categoryId": {
        "$oid": "6357938ce4938f75d0272911"
      },
      "categoryName": "데님"
    },
    {
      "categoryId": {
        "$oid": "63579391e4938f75d0272912"
      },
      "categoryName": "아우터"
    }
  ],
  "categoryName": "의류",
  "v": 0
},{
  "id": {
    "$oid": "63579380e4938f75d027290e"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "상의",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "6357937ce4938f75d027290d"
    },
    "categoryName": "의류"
  }
},{
  "id": {
    "$oid": "63579384e4938f75d027290f"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "하의",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "6357937ce4938f75d027290d"
    },
    "categoryName": "의류"
  }
},{
  "id": {
    "$oid": "63579388e4938f75d0272910"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "모자",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "6357937ce4938f75d027290d"
    },
    "categoryName": "의류"
  }
},{
  "id": {
    "$oid": "6357938ce4938f75d0272911"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "데님",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "6357937ce4938f75d027290d"
    },
    "categoryName": "의류"
  }
},{
  "id": {
    "$oid": "63579391e4938f75d0272912"
  },
  "categoryLevel": 1,
  "childCategories": [],
  "categoryName": "아우터",
  "v": 0,
  "parentCategory": {
    "categoryId": {
      "$oid": "6357937ce4938f75d027290d"
    },
    "categoryName": "의류"
  }
}]



if es.indices.exists(index="category_test"):
    pass
else:
    es.indices.create(index="category_test", body=document)

# es.index(index="category_test") #, body=var) # , body=var)
helpers.bulk(es, var, index="category_test")

