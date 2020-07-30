# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class CustomePaymentReportWizard(models.TransientModel):

    _name = 'customer.payment.report.wizard'

    customer_account_no = fields.Char(string="Account Number", required=True)
    customer_all_data = fields.Boolean(string="All Entry", default=False)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'customer_account_no': self.customer_account_no,
                'customer_all_data' : self.customer_all_data,
            }
        }

        return self.env.ref('sopnobankmang_model.payment_report').report_action(self, data=data)

class CustomerPaymetnReport(models.AbstractModel):

    _name = 'report.sopnobankmang_model.customer_payment_report_view'

    @api.model
    def get_report_values(self, docids, data=None):

        customer_account_no = data['form']['customer_account_no']
        customer_all_data = data['form']['customer_all_data']

        docs = []
        total_amount = 0
        lit = []
        # customers = self.env['daily_payment'].search([('c_account_no', '=', customer_account_no),])
        if customer_all_data == True:
            customers = self.env['daily_payment'].search([('c_account_no', '=', customer_account_no),])
            for rec in customers:

                docs.append({
                    'customer': rec.c_payment_name,
                    'amount': rec.c_payment_daily,
                })

        else:
            customers = self.env['customer'].search([('acc_id', '=', customer_account_no)])
            for rec in customers:
                loan_customer = self.env['daily_payment'].search([
                    ('c_account_no', '=', rec.acc_id),
                ])
                for loan in loan_customer:
                    lit.append(loan.c_payment_daily)
                    if len(lit) > 0:
                        total_amount = sum(lit)

                docs.append({
                    'customer': rec.name,
                    'amount': total_amount,
                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'customer_account_no': customer_account_no,
            'docs': docs,
        }
