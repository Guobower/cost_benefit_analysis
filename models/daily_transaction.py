# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class DailyExpense( models.Model ):

    _name = 'cba.daily_expenses'

    book_date = fields.Date( string = 'Book Date',
                                default = fields.Date.today() )

    daily_expenses_line_ids = fields.One2many(   comodel_name='daily_expenses_line',
                                                    inverse_name='daily_expense_id',
                                                    string='Daily Expenses Lists' )


    total_expenses_amount = fields.Float(  compute="_compute_total_expenses_amount" )

    @api.depends('daily_expenses_line_ids' )
    def _compute_total_expenses_amount( self ):
        ''' For compute total expenses
        '''
        for recordObj in self:
            totalExpensesAmount = 0
            for dailyExpensesLineDict in self.pool.get( 'daily_expenses_line' ).read( recordObj.daily_expenses_line_ids, ['total_expenses'] ):
                totalExpensesAmount += dailyExpensesLineDict['total_expenses']
            recordObj.total_expenses_amount = totalExpensesAmount


class DailyExpenseLine( models.Model ):

    _name = 'cba.daily_expenses_line'

    daily_expenses_id = fields.Many2one( comodel_name = 'daily_expenses' )

    product_id = fields.Many2one( comodel_name = 'product' )

    vendor_id = fields.Many2one( comodel_name = 'res.partner',
                                    domain = [ ('supplier','=', True )],
                                    string = 'Vendor')

    price = fields.Float( string = 'Price', default = 0.0 )

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    total_expenses = fields.Float( compute="_compute_total_expenses" )

    @api.depends('price','quantity' )
    def _compute_total_expenses( self ):
        ''' For compute total expenses
        '''
        for recordObj in self:
            recordObj.total_expenses = recordObj.price * recordObj.quantity

class DailyIncome( models.Model ):

    _name = 'cba.daily_income'

    book_date = fields.Date( string = 'Book Date',
                                default = fields.Date.today() )

    daily_income_line_ids = fields.One2many(   comodel_name='daily_income_line',
                                                    inverse_name='daily_income_id',
                                                    string='Daily Income Lists' )


    total_income_amount = fields.Float(  compute="_compute_total_income_amount" )

    @api.depends('daily_income_line_ids' )
    def _compute_total_income_amount( self ):
        ''' For compute total income
        '''
        for recordObj in self:
            totalIncomeAmount = 0
            for dailyIncomeLineDict in self.pool.get( 'daily_income_line' ).read( recordObj.daily_income_line_ids, ['total_income'] ):
                totalIncomeAmount += dailyIncomeLineDict['total_income']
            recordObj.total_income_amount = totalIncomeAmount


class DailyIncomeLine( models.Model ):

    _name = 'cba.daily_income_line'

    daily_expenses_id = fields.Many2one( comodel_name = 'daily_expenses' )

    product_id = fields.Many2one( comodel_name = 'product' )

    price = fields.Float( string = 'Price', default = 0.0 )

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    total_amount = fields.Float( compute="_compute_total_price" )


class Cashflow( models.Model ):
    _name = 'cba.cashflow'

    name = fields.Char()

class Product( models.Model ):
    _name = 'cba.product'

    name = fields.Char()

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    uom_id = fields.Many2one( comodel_name = 'product.uom' )
