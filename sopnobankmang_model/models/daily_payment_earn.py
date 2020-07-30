from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class DailyPaymentEarn(models.Model):
    _inherit = 'daily_payment'

    def customer_payment_confirm(self):

        try:
            if not self.env['daily_earn_loan'].search([('select_earn_date', '=', self.c_payment_date)]):
                self.env['daily_earn_loan'].create(
                    {'admin_name': 'Bidhan Roy', 'select_earn_date': self.c_payment_date, 'all_main_amount': self.c_payment_mainamnt,
                     'all_interest_amount': self.c_payment_interest})

            record = self.env['daily_earn_loan'].search([('select_earn_date', '=', self.c_payment_date)])
            update_main_amount = record.all_main_amount + self.c_payment_mainamnt
            update_interest_amount = record.all_interest_amount + self.c_payment_interest
            if record:
                self._cr.execute("UPDATE daily_earn_loan SET all_main_amount=%s, all_interest_amount=%s WHERE select_earn_date=%s",
                                (update_main_amount, update_interest_amount, self.c_payment_date))
        except:
            pass

        return self.write({'state': 'paid'})