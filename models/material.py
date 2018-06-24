# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class Material( models.Model ):

	_name = 'cba.material'
	
	display_name = fields.Char(
    	string='Name', compute='_compute_display_name',
	)

	name = fields.Char()
    
	quantity_per_unit = fields.Float( string = 'Quantity', default = 0.0 )
	
	uom_id = fields.Many2one( comodel_name = 'product.uom', string = 'Unit of Measurement' )
	
	expenses_history_ids = fields.One2many(   comodel_name='cba.daily_expenses_line',
                                                    inverse_name='material_id',
                                                    string='Expenses History' )
    
	avg_price_per_unit = fields.Float( compute="_compute_avg_price_per_unit" )
	

	@api.one
	@api.depends('name', 'uom_id.name', 'quantity_per_unit')
	def _compute_display_name(self):

		self.display_name = '{} : ({} {})'.format( self.name, self.quantity_per_unit, self.uom_id.name )
    
	def _compute_avg_price_per_unit( self ):
		''' For compute avg price
		'''
		dailyExpensesLineModel = self.pool.get( 'cba.daily_expenses_line' )
		
		for recordObj in self:
			
			dailyExpensesLineObjList = recordObj.expenses_history_ids
			
			dailyExpensesLineCount = len( dailyExpensesLineObjList )
			
			totalExpensesAmount = sum( [ dailyExpensesLineObj.price_per_unit for dailyExpensesLineObj in dailyExpensesLineObjList ] )
		 	
			try:
				recordObj.avg_price_per_unit = ( totalExpensesAmount / dailyExpensesLineCount ) / recordObj.quantity_per_unit
			except ZeroDivisionError:
				recordObj.avg_price_per_unit = 0.0    
