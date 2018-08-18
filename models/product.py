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

	process_time = fields.Float( string = 'Process Time (Min)' )
	
	profit_loss = fields.Float( compute="_compute_profit_loss", string = 'Profit/Loss')
	
	bom_line_ids = fields.One2many( comodel_name = 'cba.bill_of_material',
									inverse_name='product_id' )
													
	def _compute_product_total_cost( self ):
		'''	
		'''
		#	assign value
		for recordObj in self:
			cost_per_outcome = 0.0
			for bomLineObj in recordObj.bom_line_ids:
				cost_per_outcome += bomLineObj.actual_cost_per_ref_unit
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

	actual_cost_per_ref_unit = fields.Float( compute="_compute_actual_cost" )

	def _compute_actual_cost( self ):
		'''	convert uom to reference unit and convert price 
		'''

		#	loop over record obj
		for recordObj in self:

			materials_used_per_ref_unit = recordObj.uom_id.factor * recordObj.materials_used 
			
			recordObj.actual_cost_per_ref_unit = materials_used_per_ref_unit * recordObj.material_id.actual_price_per_ref_unit
	
    
