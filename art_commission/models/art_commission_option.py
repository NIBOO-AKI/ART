from odoo import models, fields, api

class ArtCommissionOption(models.Model):
    _name = 'art.commission.option'
    _description = 'Art Commission Option'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    extra_price = fields.Float(string='Extra Price')

