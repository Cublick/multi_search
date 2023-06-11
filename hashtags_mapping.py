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
                "__v": {
                    "type": "long"
                },

                "elderCategoryInfo": {
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
                        "categoryName": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
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

                        "oplog_date": {
                            "type": "date",
                            "format": "yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis"
                        },

                        "oplog_ts": {
                            "properties": {
                                "I": {
                                    "type": "long"
                                },
                                "T": {
                                    "type": "long"
                                }
                            }
                        },

                        "tagName": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
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