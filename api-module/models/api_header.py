from odoo import models, fields


class ApiHeader(models.Model):
    _name = 'api.header'
    _description = 'API Header'

    key = fields.Char(string='Key')
    value = fields.Char(string='Value')
    server_id = fields.Many2one(
        string='API', comodel_name='ir.actions.server', readonly=True)
