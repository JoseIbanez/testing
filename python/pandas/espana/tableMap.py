


_tableMap = [
    {
    "id" : 239,
    "cases": {
        "page": 1,
        "colNames": ["region_name","cases_total","cases_1d","cases_g14","cases_g7","symptoms_g14","symptoms_g7"]
        },
    "hospital": {
        "page": 3,
        "colNames": [ "region_name", "hospital_total", "hospital_7d", "icu_total", "icu_7d"],
        "template": "239-hospital.json"
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
        "colNumber": 10, 
        "colNames": []
        },
    "hospital": {
        "page": 3,
        "colNumber": 10,
        "colNames": [ "region_name", "hospital_g1", "icu_g1", "CCAA2",  "hospital_cur", "hospital_ratio", "icu_cur", "icu_ratio", "hospital_checkin", "hospital_checkout"]
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





