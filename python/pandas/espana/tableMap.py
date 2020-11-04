


_tableMap = [
    {
    "id" : 242,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"]
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_total", "hospital_7d", "icu_total", "icu_7d"],
        "template": "242-hospital.json"
        },
    "beds": {
        "page": 3,
        "colNames": [ "region_name", "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "checkin", "checkout"],
        "template": "242-beds.json",
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    },
    {
    "id" : 241,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"]
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_total", "hospital_7d", "icu_total", "icu_7d"],
        "template": "239-hospital.json"
        },
    "beds": {
        "page": 3,
        "colNames": [ "region_name", "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "checkin", "checkout"],
        "template": "241-beds.json"
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    },
    {
    "id" : 239,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"]
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_total", "hospital_7d", "icu_total", "icu_7d"],
        "template": "239-hospital.json"
        },
    "beds": {
        "page": 3,
        "colNames": [ "region_name", "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "checkin", "checkout"],
        "template": "239-beds.json"
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    },
    {
    "id" : 235,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"]
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_g1", "icu_g1", "CCAA2",  "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "hospital_checkin", "hospital_checkout"]
        },
    "beds": {
        "page": 3,
        "colNames": [ "region_name", "h1", "h2", "ccaa", "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "checkin", "checkout"]
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    },
    {
    "id" : 168,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"],
        "template": "167-cases.json"
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_total", "hospital_7d", "icu_total", "icu_7d", "death_total","death_7d"],
        "template": "167-hospital.json"
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    },

    {
    "id" : 167,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1day","cases_g14","cases_g7","symptoms_g14","symptoms_g7"],
        "template": "167-cases.json"
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_g1", "icu_g1","death_total","death_7d"],
        "template": "167-hospital.json"
        },
    "death": {
        "page": 5,
        "colNumber": 3,
        "colNames": [ "region_name", "death_total", "death_7d"]
        }
    }

]

_tableCols = {
    "cases": {
        "colInt" : [ "cases_total", "cases_1day", "cases_14d", "cases_7d", "symptoms_14d", "symptoms_7d" ],
        "colFloat" : [ "cases_14d_ai", "cases_7d_ai", "symptoms_14d_ai", "symptoms_7d_ai" ]
        },
    "hospital": {
        "colInt": [ "hospital_total", "hospital_7d", "icu_total", "icu_7d", "death_total", "death_7d" ],
        "colFloat": []
        },
    "beds": {
        "colInt":    [ "hospital_cur", "icu_cur" ],
        "colFloat" : [ "hospital_ratio", "icu_ratio" ]
        }
    }


def getTableCols(tableName):
    return _tableCols[tableName]['colInt'], _tableCols[tableName]['colFloat'] 



def getTableMap(id,tableName):

    mapLen  = len(_tableMap)

    index = None

    for i in range(0,mapLen):
        if (id >= _tableMap[i]["id"]):
            index = i
            break


    if (index is None):
        raise RuntimeError("Table format not detected!")

    print(f"TableMap id:{_tableMap[i]['id']}")
    return _tableMap[index][tableName]





