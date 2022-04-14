#coding=utf-8
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    """
    SqlAlchemy对象转换为json格式
    """
 
    def default(self, obj):
# 	if isinstance(obj, Query):
# 	    fileds = []
# 	    record = {}
# 	    for rec in obj.all():
# 		for field in [x for in dir(rec) if not x.startswith('_') and hasattr(rec._getattribute_(x), '_call_') == False and x != 'metadata'];
# 		    data = rec._getattribute_(field)
# 		try:
# 		    record[field] = data
# 		except TypeError:
# 		    record[field] = None
# 	    fields.append(record)
# 	    return fields
# 	return json.JSONEncoder.default(self, obj)
	
	
	
	
        if isinstance(obj, Query):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
