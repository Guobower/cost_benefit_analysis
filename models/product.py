# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class Product( models.Model ):

    _name = 'cba.product'

    name = fields.Char()

    purchase_quantity = fields.Float( string = 'Quantity', default = 0.0 )

    purchase_uom_id = fields.Many2one( comodel_name = 'product.uom' )
    
    is_purchase_able = fields.Boolean( string = 'Can be Purchase?' )
    
    produce_uom_id = fields.Many2one( comodel_name = 'product.uom' )
    
    is_sale_able = fields.Boolean( string = 'Can be Sale?' )
    
