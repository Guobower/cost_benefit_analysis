# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

def getListFromFieldName( inputDictList, fieldName ):
	'''
	'''
	resultList = list()
	for inputDict in inputDictList:
		if isinstance( inputDict[fieldName], list ):
			inputDict[fieldName] = list( inputDict[fieldName] )
		resultList.extend( inputDict[fieldName] )
	
	return resultList

class Product( models.Model ):

	_name = 'cba.product'
	
	name = fields.Char(string = 'Product Name')
	
	product_outcome = fields.Integer( string = 'Product Outcome' )
	
	cost_per_outcome = fields.Float( compute="_compute_product_total_cost", string = 'Cost Per Outcome')
	
	sale_price = fields.Float()
	
	profit_loss = fields.Float( compute="_compute_profit_loss", string = 'Profit/Loss')
	
	bom_line_ids = fields.One2many( comodel_name = 'cba.bill_of_material',
									inverse_name='product_id' )
													
	def _compute_product_total_cost( self ):
		'''	
		'''
		#	assign value
		for recordObj in self:
			cost_per_outcome = 0.0
			for bomObj in recordObj.bom_line_ids:
				materialObj = bomObj.material_id
				materialUsed = bomObj.materials_used
				
				cost_per_outcome += ( materialUsed * materialObj.avg_price_per_unit )
			recordObj.cost_per_outcome = cost_per_outcome / recordObj.product_outcome
			
	def _compute_profit_loss( self ):
		'''
		'''
		
		for recordObj in self:
			
			recordObj.profit_loss = recordObj.sale_price - recordObj.cost_per_outcome

class BillOfMaterialLine( models.Model ):

	_name = 'cba.bill_of_material'
	
	product_id = fields.Many2one( comodel_name = 'cba.product' )
	
	material_id = fields.Many2one( comodel_name = 'cba.material' )
	
	materials_used = fields.Float( string = 'Materials Used In Manufacturing' )
	
	uom_id = fields.Many2one( related = 'material_id.uom_id' )
	
	
    
