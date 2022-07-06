def json2xml(json_obj, line_padding="", origin_obj=None):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append("%s<%s>" % (line_padding, origin_obj))
            result_list.append(json2xml(sub_elem, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, origin_obj))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            if type(sub_obj) is list:
                result_list.append(
                    json2xml(sub_obj, line_padding, tag_name))
            else:
                result_list.append("%s<%s>" % (line_padding, tag_name))
                result_list.append(json2xml(sub_obj, "\t" + line_padding))
                result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)


dictionary = {'student': {'id': 'DEL', 'name': 'Jack', 'email': [
    'jack@example.com', 'jack2@example.com'], 'semester': {'name': 'Jack'}, 'class': 'CSE', 'cgpa': '7.5'}}

print(json2xml(dictionary))
