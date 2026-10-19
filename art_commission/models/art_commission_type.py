from odoo import api, models, fields

class ArtCommissionType(models.Model):
    _name = 'art.commission.type'
    _description = 'Art Commission Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    base_price = fields.Float(string='Base Price')
    active = fields.Boolean(string='Active', default=True)

