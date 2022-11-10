from collections import defaultdict
from xml.etree import cElementTree as ET
import requests
import json


def xml2dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(xml2dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

xml_data = ET.XML("""
    <student>
      <id>DEL</id>
      <name> Jack </name>
      <email>jack@example.com</email>
      <email>jack2@example.com</email>
      <smeseter>
      <name>Jack</name>
      </smeseter>
      <class>CSE</class>
      <cgpa> 7.5</cgpa>
    </student>
""")

d = json.dumps(xml2dict(xml_data))

print(d)





try:
    headers = {
    #'access_key': '062d2886e5ba140c2fb8cbd740c751de',
        'Content-Type': 'application/json',
    #'query': 'kdjvbkdjz'
    #     'access_key': self.access_key,
    #     'query': self.query
    }
    my_dict = {
        "a": {
            "b": "c"
        }
    }
    
    my_dict = json.dumps(my_dict)
    
    # body = {
    #    'data': xml2dict(xml_data)
    # }
    api_result = requests.post('http://192.168.10.52:7000/api/v1/api/json', headers=headers, data=d)
    #api_response = api_result.json()
    #print(api_response)
    print(api_result.json())
    # if not api_response['success']: 
    #     print("quiiiiii")
    #     raise Exception(api_response['error']['info'])
        
    
    # print(u'Current temperature in %s is %d℃' %
    #         (api_response['location']['name'], api_response['current']['temperature']))


except Exception as e:
    print("Aquii",e)





