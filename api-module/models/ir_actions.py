from collections import defaultdict
import requests

from odoo import models, fields
from odoo.exceptions import UserError


class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[(
        'api_call', 'Call External API')], ondelete={'api_call': 'cascade'})

    description = fields.Text(string='Description')
    url = fields.Char(string='URL')
    method = fields.Selection(
        selection=[('get', 'GET'), ('post', 'POST')],
        string='Method',
        required=True,
        default='get'
    )
    content_type = fields.Selection(
        selection=[('text/xml', 'XML'), ('application/json', 'JSON')],
        string='Content Type',
        required=True,
    )
    headers = fields.One2many(string='Headers', inverse_name='api_id' ,comodel_name='api.header')
    payload = fields.Text() 

    def create(self, vals_list):
        res = super(IrActionsServer, self).create(vals_list)
        for val in vals_list:
            if val.get('state') == 'api_call':    
                if not val.get('url'):
                    raise UserError('API must have a url')
                xml = val.get('payload')
                headers = {'Content-Type': val.get('content_type')}
                api_result = requests.post(
                    val.get('url'),  data=xml, headers=headers)
                print(api_result.json())
        return res

    def _run_action_api_call(self, eval_context=None):
        headers = {'Content-Type': self.content_type}
        xml = self.payload
        if self.method == 'get':
            api_result = requests.get(self.url,  self.body)
        else:
            api_result = requests.post(self.url,  data=xml, headers=headers)
            raise UserError(api_result.json())

    def xml2dict(self,t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.xml2dict, children):
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

    def json2xml(self,json_obj, line_padding="", origin_obj=None):
        result_list = list()

        json_obj_type = type(json_obj)

        if json_obj_type is list:
            for sub_elem in json_obj:
                result_list.append("%s<%s>" % (line_padding, origin_obj))
                result_list.append(self.json2xml(sub_elem, "\t" + line_padding))
                result_list.append("%s</%s>" % (line_padding, origin_obj))

            return "\n".join(result_list)

        if json_obj_type is dict:
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                if type(sub_obj) is list:
                    result_list.append(
                        self.json2xml(sub_obj, line_padding, tag_name))
                else:
                    result_list.append("%s<%s>" % (line_padding, tag_name))
                    result_list.append(self.json2xml(sub_obj, "\t" + line_padding))
                    result_list.append("%s</%s>" % (line_padding, tag_name))

            return "\n".join(result_list)

        return "%s%s" % (line_padding, json_obj)
