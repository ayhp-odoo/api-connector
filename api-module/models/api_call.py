from odoo import models, fields, api
from odoo.exceptions import UserError
import requests


class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[(
        'api_call', 'Call External API')], ondelete={'api_call': 'cascade'})

    api_name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    url = fields.Char(string='URL')
    method = fields.Selection(
        selection=[('get', 'GET'), ('post', 'POST')],
        string='Method',
        required=True,
        default='get'
    )
    headers = fields.Text(string='Headers')
    body = fields.Text(string='Body')
    response_type = fields.Selection(
        selection=[('json', 'JSON'), ('text', 'Text')],
        string='Response Type',
        required=True,
        default='json'
    )

    query = fields.Char(string='Query')
    access_key = fields.Char(string='Acces Token')
    payload = fields.Text('payload')  # , render_engine='qweb',
    # translate=True, sanitize=False)

    def create(self, vals_list):
        res = super(IrActionsServer, self).create(vals_list)
        for val in vals_list:
            if not val.get('api_name'):
                raise UserError('API must have a name')
            if not val.get('url'):
                raise UserError('API must have a url')
            xml = val.get('payload')
            headers = {'Content-Type': 'text/xml'}
            api_result = requests.post(
                val.get('url'),  data=xml, headers=headers)
            print(api_result.json())
        return res

    def _run_action_api_call(self, eval_context=None):
        # headers = {
        #      #'access_key': '062d2886e5ba140c2fb8cbd740c751de',
        #      #'query': 'Mexico City'
        #      #'access_key': self.access_key,
        #      #'query': self.query,
        #      'Content-type': 'text/xml',
        #      #'body': self.payload
        # }
        headers = {'Content-Type': 'text/xml'}
        xml = self.payload
        if self.method == 'get':
            api_result = requests.get(self.url,  self.body)
        else:
            api_result = requests.post(self.url,  data=xml, headers=headers)
            raise UserError(api_result.json().get(
                'recived data').get('note').get('to')[0])
