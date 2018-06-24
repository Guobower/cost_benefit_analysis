# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class Material( models.Model ):

    _name = 'cba.meterial'

    name = fields.Char()

    quantity_per_unit = fields.Float( string = 'Quantity', default = 0.0 )

    uom_id = fields.Many2one( comodel_name = 'product.uom' )
    
