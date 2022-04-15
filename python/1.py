
import json
from datetime import datetime


with open('./1.json') as f:
    oids_list = json.load(f)['oids']

with open('./data.txt') as f:
    lines = (line.strip() for line in f)
    for line in lines:
        field1 = line.split()[0]
        field2 = line.split()[1]
        field3 = line.split()[2]
        # print(field1, field2, field3)

        item = {}
        oid = field1
        data_type = "integer"
        data_dicitionary_key1 = "{}正常".format(field2)
        data_dicitionary_key2 = "{}异常".format(field2)
        data_dicitionary = [{"data_dicitionary_key": data_dicitionary_key1, "data_dicitionary_val": 0}, {"data_dicitionary_key": data_dicitionary_key2, "data_dicitionary_val": 100}]
        snmp_type = "get"
        metric_code = field3
        metric_cn = field2

        item.update(oid = field1)
        item.update(data_type = "integer")
        item.update(data_dicitionary = [{"data_dicitionary_key": data_dicitionary_key1, "data_dicitionary_val": 0}, {"data_dicitionary_key": data_dicitionary_key2, "data_dicitionary_val": 100}])
        item.update(snmp_type = "get")
        item.update(metric_code = field3)
        item.update(metric_cn = field2)

        # print(item)
        # print(str(item))
        j = json.dumps(item, ensure_ascii=False)
        print("{}, ".format(j))
