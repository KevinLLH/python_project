#es的文档、索引的CRUD操作

#索引初始化操作
#指定分片和副本的数量
#shards一旦设置不能修改

PUT lcsoft
{
  "settings": {
    "index":{
      "number_of_shards":5,
      "number_of_replicas":1
    }
  }
}

#获取设置信息
GET lcsoft/_settings
#获取所有的设置
GET _all/_settings
#获取所有设置第二种方法
GET _settings
#同时获取几个索引
GET .kibana,lcsoft/_settings

#修改副本的数量
PUT lcsoft/_settings
{
  "number_of_replicas": 2
}
#获取所有的索引信息
GET _all

#获取单个索引信息
GET lcsoft

PUT lagou
{
  "settings": {
    "index":{
      "number_of_shards":5,
      "number_of_replicas":1
    }
  }
}

#保存文档/不知名id将会自动生成uuid
PUT lagou/job/1
{
  "title":"pyton分布式爬虫开发",
  "salary_min":15000,
  "city":"北京",
  "company":{
    "name":"百度",
    "company_addr":"北京市软件园"
  },
  "publish_data":"2017-4-16",
  "comments":15
}

#增加文档
POST lagou/job/
{
  "title":"python django 开发工程师",
  "salary_min":30000,
  "city":"上海",
  "company":{
    "name":"美团科技",
    "company_addr":"北京市软件园A区"
  },
  "publish_data":"2017-4-16",
  "comments":20
}

#获取
GET lagou/job/1
#第二种方式
GET lagou/job/1?_source
#获取某个字段
GET lagou/job/1?_source=title,city

#修改文章
PUT lagou/job/1
{
  "title":"pyton分布式爬虫开发",
  "salary_min":15000,
  "company":{
    "name":"百度",
    "company_addr":"北京市软件园"
  },
  "publish_data":"2017-4-16",
  "comments":15
}
#增量修改
POST lagou/job/1/_update
{
  "doc": {
      "comments":20
  }

}


#删除job
DELETE lagou/job/1

#删除type
DELETE lagou/job

#删除索引
DELETE lagou


#批量查询
GET _mget
{
  "docs":[
    {
      "_index":"testdb",
      "_type":"job1",
      "_id":1
    },
    {
      "_index":"testdb",
      "_type":"job2",
      "_id":2
    }
    ]
}

#批量查询同一个索引下的type
GET testdb/_mget
{
  "docs":[
    {
      "_type":"job1",
      "_id":1
    },
    {
      "_type":"job2",
      "_id":2
    }
    ]
}

#获取id为1 id为2的都在job下的数据

GET testdb/job1/_mget
{
  "docs":[
    {
      "_id":1
    },
    {
      "_id":2
    }
    ]
}

#同上方法二
GET testdb/job1/_mget
{
  "ids":[1,2]
}


#批量操作
POST _bulk
{"index":{"_index":"lagou","_type":"job","_id":"6"}}
{"title":"java开发","salary_min":15000,"city":"北京","company":{"name":"百度","company_addr":"北京市软件园"},"publish_data":"2017-4-16","comments":15}
{"index":{"_index":"lagou","_type":"job2","_id":"7"}}
{"title":"java爬虫开发","salary_min":15000,"city":"上海","company":{"name":"美团","company_addr":"北京市软件园"},"publish_data":"2017-4-16","comments":15}


#放入数据
PUT lagou/job/1
{
  "title":"python开发工程师",
  "salary_min":30000,
  "city":"北京",
  "company":{
    "name":"百度",
    "company_addr":"北京市软件园A区"
  },
  "publish_data":"2017-4-16",
  "comments":20
}

#建立索引 analyzer分析器为ik_max_word
PUT lagou
{
  "mappings": {
    "job":{
      "properties": {
        "title":{
          "store": true, 
          "type": "text"
          , "analyzer": "ik_max_word"
        },
        "salary_min":{
          "type": "integer"
        },
        "city":{
          "type": "keyword"
        },
        "company":{
          "properties": {
            "name":{
              "store":true,
              "type":"text"
            },
            "company_addr":{
              "type":"text"
            },
            "employee_count":{
              "type":"integer"
            }
          }
        },
        "publish_date":{
          "type": "date",
          "format": "yyyy-MM-dd"
        },
        "comments":{
          "type": "integer"
        }
      }
    }
  }
}



#获取mapping
GET lagou/_mapping

#获取index下边制定的job
GET lagou/_mapping/job

#获取集群里面的所有mapping
GET _all/_mapping


#match查询,会分词
GET lagou/_search
{
  "query": {
    "match": {
      "title": "python"
    }
  }
}

#term查询，不会分词
GET lagou/_search
{
  "query": {
    "term": {
      "title":"python"
    }
  }
}

#terms查询
GET lagou/_search
{
  "query": {
    "terms": {
      "title": [
        "工程师",
        "django",
        "系统"
      ]
    }
  }
}

#控制查询的返回数量,from从哪里开始取几个
GET lagou/_search
{
  "query": {
    "match":{
      "title":"python"
    }
  },
  "from":1,
  "size":2
}

#match_all查询,把所有数据都返回来
GET lagou/_search
{
  "query":{
    "match_all":{}
  }
}

#match_phrase查询
#短语查询slop是距离，就是分词后两个分词之间允许的误差
GET /lagou/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query":"python系统",
        "slop":6
        
      }
    }
  }
}

#multi_match查询
#可以指定多个字段
#查询title和desc这两个字段里面包含python的关键词文档,^3权重3倍
GET lagou/_search
{
  "query": {
    "multi_match": {
      "query": "query",
      "fields": ["title^3","desc"]
    }
  }
}

#指定返回字段
GET lagou/_search
{
  "stored_fields": ["title","company_name"],
  "query": {
    "match": {
      "title": "python"
    }
  }
}

#通过sort把结果排序
GET lagou/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "comments": {
        "order": "desc"
      }
    }
  ]
}

#查询范围
#range查询gte大于等于(e),lte小于等于,boost权重
GET lagou/_search
{
  "query": {
    "range": {
      "comments": {
        "gte": 10,
        "lte": 20,
        "boost": 2.0
      }
    }
  }
}

#查询时间
GET lagou/_search
{
  "query": {
    "range":{
      "gte":"2017-04-01",
      "lte":"now"
    }
  }
}

#wildcard模糊查询
GET lagou/_search
{
  "query": {
    "wildcard": {
      "title": {
        "value": "pyth*n",
        "boost": 2.0
      }
    }
  }
}



#bool查询
#老版本的filtered已经被bool替换
#用bool 包括 must should must_not 来完成
#bool:{
#  "filter":[],
#  "must":[],
#  "should":[],
#  "must_not":[],
#}

#建立测试数据
POST lagou/testjob/_bulk
{"index":{"_id":1}}
{"salary":10,"title":"python"}
{"index":{"_id":2}}
{"salary":20,"title":"Scrapy"}
{"index":{"_id":3}}
{"salary":30,"title":"Django"}
{"index":{"_id":4}}
{"salary":30,"title":"Elasticsearch"}

DELETE lagou/testjob

#简单过滤查询
#最简单的filter查询
#select * from testjob where salary=20
#薪资为20k的工作
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all":{}
      },
      "filter": {
        "term": {
          "salary": 20
        }
      }
    }
  }
}

#也可以制定多个值
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all":{}
      },
      "filter": {
        "terms": {
          "salary": [
            10,
            20
          ]
        }
      }
    }
  }
}

#select * from testjob where title="Python"
#Python在倒排存取的时候已经转换成小写保存进去了
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all":{}
      },
      "filter": {
        "term": {
          "title": "Python"
        }
      }
    }
  }
}


#查看分析器解析的结果
GET _analyze
{
  "analyzer": "ik_max_word",
  "text": "Python网络开发工程师"
}


#bool过滤查询，可以做组合过滤查询
#select * from testjob where (salary=20 OR title=Python) AND (ssalary != 30)
#查询薪资等于20k或者工作为python的工作，排除价格为30k的
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {"salary":20}},
        {"term":{"title":"python"}}
      ],
      "must_not":{
        "term":{"price":30}
      }
    }
  }
}

#嵌套查询
#select * from testjob where title="python" or (title="django" AND salary=30)

GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "should": [
        {"term":{"title":"python"}},
        {"bool":{"must":[
          {"term":{"title":"elasticsearch"}},
          {"term":{"salary":30}}
          ]}}
      ]
    }
  }
}

#过滤空和非空
#建立测试数据

POST lagou/testjob2/_bulk
{"index":{"_id":1}}
{"tags":["search"]}
{"index":{"_id":2}}
{"tags":["search","python"]}
{"index":{"_id":3}}
{"other_field":["some data"]}
{"index":{"_id":4}}
{"tags":null}
{"index":{"_id":5}}
{"tags":["search",null]}

#处理null空值的方法
#select tags from testjob2 where tags is not NULL
GET lagou/testjob2/_search
{
  "query": {
    "bool": {
      "filter": {
        "exists": {
          "field": "tags"
        }
      }
    }
  }
}

GET lagou/testjob2/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "tags"
        }
      }
    }
  }
}

#模糊搜索fuzzy
#match查询,会分词
GET lagou/_search
{
  "query": {
    "fuzzy": {
      "title": "python"
    },
    "_source":["title"]
  }
}

GET lagou/_search
{
  "query": {
    "fuzzy": {
      "title": {
        "value": "linx",
        "fuzziness": 0.5,
        "prefix_length": 0
      }
    },
    "_source":["title"]
  }
}

