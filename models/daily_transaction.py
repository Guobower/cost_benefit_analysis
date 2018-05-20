# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, timedelta

class DailyExpense( models.Model ):

    _name = 'daily_expenses'

    book_date = fields.Date( string = 'Book Date',
                                default = fields.Date.today() )

    daily_expenses_line_ids = fields.One2many(   comodel_name='daily_expenses_line',
                                                    inverse_name='daily_expense_id',
                                                    string='Daily Expenses Lists' )


    total_expenses_amount = fields.Float(  compute="_compute_net_amount" )


class DailyExpenseLine( models.Model ):

    _name = 'daily_expenses_line'

    daily_expenses_id = fields.Many2one( comodel_name = 'daily_expenses' )

    product_id = fields.Many2one( comodel_name = 'product' )

    vendor_id = fields.Many2one( comodel_name = 'res.partner',
                                    domain = [ ('supplier','=', True )],
                                    string = 'Vendor')

    price = fields.Float( string = 'Price', default = 0.0 )

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    total_expenses = fields.Float( compute="_compute_total_expenses" )

    @api.depends('price','_compute_total_expenses' )
    def _compute_total_price( self ):
        ''' For compute total price
        '''
        for recordObj in self:
            if recordObj.price  == 0 or recordObj.quantity == 0 :
                recordObj._compute_total_expenses = 0

            recordObj.total_expenses = recordObj.price * recordObj.quantity

class DailyIncome( models.Model ):

    _name = 'daily_income'

    book_date = fields.Date( string = 'Book Date',
                                default = fields.Date.today() )

    daily_income_line_ids = fields.One2many(   comodel_name='daily_income_line',
                                                    inverse_name='daily_income_id',
                                                    string='Daily Income Lists' )


    total_imcome_amount = fields.Float(  compute="_compute_net_amount" )


class DailyIncomeLine( models.Model ):

    _name = 'daily_income_line'

    daily_expenses_id = fields.Many2one( comodel_name = 'daily_expenses' )

    product_id = fields.Many2one( comodel_name = 'product' )

    price = fields.Float( string = 'Price', default = 0.0 )

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    total_amount = fields.Float( compute="_compute_total_price" )


class Cashflow( models.Model ):
    _name = 'cashflow'

    name = fields.Char()

class Product( models.Model ):
    _name = 'product'

    name = fields.Char()

    quantity = fields.Float( string = 'Quantity', default = 0.0 )

    uom_id = fields.Many2one( comodel_name = 'product.uom' )
