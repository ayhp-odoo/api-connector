from odoo import models, fields, api
from odoo.exceptions import UserError
import requests


class ApiCall(models.Model):
    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[(
        'api_call', 'Call External API')], ondelete={'api_call': 'cascade'})

    api_name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    url = fields.Char(string='URL', required=True)
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
    access_key = fields.Char(string='access_key')
    payload = fields.Text('payload')  # , render_engine='qweb',
    # translate=True, sanitize=False)

    def _run_action_api_call(self, eval_context=None):
        # headers = {
        #      #'access_key': '062d2886e5ba140c2fb8cbd740c751de',
        #      #'query': 'Mexico City'
        #      #'access_key': self.access_key,
        #      #'query': self.query,
        #      'Content-type': 'text/xml',
        #      #'body': self.payload
        # }

        xml = self.payload
        # set the type of payload the API accepts
        headers = {'Content-Type': 'text/xml'}
        api_result = requests.post(self.url,  data=xml, headers=headers)
        raise UserError(api_result.json().get(
            'recived data').get('note').get('to')[0])
