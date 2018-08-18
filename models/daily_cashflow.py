# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class DailyExpense( models.Model ):

	_name = 'cba.daily_expenses'
	
	display_name = fields.Char(
    	string='Name', compute='_compute_display_name',
	)

	date = fields.Date( string = 'Date',
    			default = fields.Date.today() )

	daily_expenses_line_ids = fields.One2many(   comodel_name='cba.daily_expenses_line',
                                                    inverse_name='daily_expense_id',
                                                    string='Daily Expenses Lists' )


	total_expenses_amount = fields.Float(  compute="_compute_total_expenses_amount" )

#	@api.depends('daily_expenses_line_ids' )
	def _compute_total_expenses_amount( self ):
		''' For compute total expenses
		'''
		for recordObj in self:
			totalExpensesAmount = 0
			for dailyExpensesLineObj in recordObj.daily_expenses_line_ids:
				totalExpensesAmount += dailyExpensesLineObj.total_price
			recordObj.total_expenses_amount = totalExpensesAmount
			
	@api.one
	@api.depends('date', 'total_expenses_amount')
	def _compute_display_name(self):

		self.display_name = '{} : {}'.format( self.date, self.total_expenses_amount )


class DailyExpenseLine( models.Model ):

	_name = 'cba.daily_expenses_line'

	daily_expense_id = fields.Many2one( comodel_name = 'cba.daily_expenses' )

	date = fields.Date( related = 'daily_expense_id.date' )

	material_id = fields.Many2one( comodel_name = 'cba.material' )

	supplier_id = fields.Many2one( comodel_name = 'res.partner',
                                	domain = [ ('supplier','=', True )],
                                	string = 'Supplier')
				    
	quantity = fields.Float( string = 'Quantity', default = 0.0 )

	price_per_unit = fields.Float( string = 'Price per unit', default = 0.0 )

	total_price = fields.Float( compute="_compute_total_expenses" )

	@api.depends('price_per_unit','quantity' )
	def _compute_total_expenses( self ):
		''' For compute total expenses
		'''
		for recordObj in self:
			recordObj.total_price = recordObj.price_per_unit * recordObj.quantity


class DailyIncome( models.Model ):

    _name = 'cba.daily_income'

    date = fields.Date( string = 'Date', default = fields.Date.today() )

    daily_income = fields.Float()
	
#
#    daily_income_line_ids = fields.One2many(   comodel_name='cba.daily_income_line',
#                                                    inverse_name='daily_income_id',
#                                                    string='Daily Income Lists' )
#
#
#    total_income_amount = fields.Float(  compute="_compute_total_income_amount" )
#
#    @api.depends('daily_income_line_ids' )
#    def _compute_total_income_amount( self ):
#        ''' For compute total income
#        '''
#        for recordObj in self:
#            totalIncomeAmount = 0
#            for dailyIncomeLineObj in recordObj.daily_income_line_ids:
#                totalIncomeAmount += dailyIncomeLineObj.total_income
#            recordObj.total_income_amount = totalIncomeAmount
#
#
#class DailyIncomeLine( models.Model ):
#
#    _name = 'cba.daily_income_line'
#
#    daily_income_id = fields.Many2one( comodel_name = 'cba.daily_income' )
#
#    product_id = fields.Many2one( comodel_name = 'cba.product' )
#
#    price = fields.Float( string = 'Price', default = 0.0 )
#
#    quantity = fields.Float( string = 'Quantity', default = 0.0 )
#
#    total_amount = fields.Float( compute="_compute_total_price" )
#
#
#class Cashflow( models.Model ):
#    _name = 'cba.cashflow'
#
#    name = fields.Char()
