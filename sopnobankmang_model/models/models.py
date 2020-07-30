# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class Customer(models.Model):
    _name = 'customer'

    name = fields.Char(string="Combine Name", compute='_com_name')
    acc_id = fields.Char(string="Account ID", required=True)
    acc_fname = fields.Char(string="First Name", required=True)
    acc_lname = fields.Char(string="Last Name", required=True)
    f_s_name = fields.Char(string="F/Spouse Name")
    c_gender = fields.Selection((('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')), string="Gender")
    c_age = fields.Char(string="Age", required=True)
    c_nid = fields.Char(string="Nationnal ID No", required=True)
    c_r_date = fields.Date(string="Registration Date", required=True)
    c_mobile = fields.Char(string="Mobile Number", required=True)
    c_religion = fields.Selection((('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Boudhoo', 'Boudhoo'),
                                   ('Khristan', 'khristan')), string='Religion')
    c_address = fields.Text(string="Address")
    c_r_image = fields.Binary(string="Customer Image")
    c_r_fee = fields.Integer(string="Reg Fees")

    state = fields.Selection([
        ('draft', 'Pending'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list

    c_r_year = fields.Selection('_get_years', string="Select Year", required=True)

    def _com_name(self):

        for j in self:
            f_n = j.acc_id
            s_c = j.acc_fname
            c_n = ''

            if f_n:
                c_n += f_n + ''
            if s_c:
                c_n += s_c

            j.name = c_n


    c_fname_lname = fields.Char(string="Add First and Last name", compute='_get_fnamelname')
    @api.depends('acc_fname', 'acc_lname')
    def _get_fnamelname(self):
        for rect in self:
            f_name = rect.acc_fname
            l_name = rect.acc_lname
            j_name = f_name +" "+ l_name
            rect.update({
                'c_fname_lname': j_name
            })
    #sequence number create
    reg_sec = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('reg_sec', _('New')) == _('New'):
            vals['reg_sec'] = self.env['ir.sequence'].next_by_code('send.sms.sequence') or _('New')
        result = super(Customer, self).create(vals)
        return result

    def done_registration(self):
        return self.write({'state': 'done'})

    def cancel_registration(self):
        return self.write({'state': 'cancel'})

    def open_customer_loan_form(self):

        return {
            'name': _('Customer Loan'),
            'type': 'ir.actions.act_window',
            'res_model': 'customer_loan',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name':self.id,
            }
        }

    _sql_constraints = [
        ('customer_acc_id', 'unique(acc_id)', 'Customer Account ID Must Be Unique !'),
    ]


class customer_loan(models.Model):
    _name = 'customer_loan'

    name = fields.Many2one('customer', string="Select Cusotmer", required=True)
    cus_loan_acid = fields.Char(string="Cutomer Acc ID", required=True)
    cus_loan_name = fields.Char(string="Cutomer Nmae", required=True)
    cus_loan_date = fields.Date(string="Loan Date", required=True)
    cus_loan_amount = fields.Integer(string="Loan Amount", required=True)
    cus_loan_interest = fields.Integer(string="Loan Interest", compute='_get_sum_loan')
    cus_loan_total = fields.Integer(string="Total Payable Amount", compute='_get_sum_tloan')
    cus_loan_duration = fields.Selection((('2 Month', '2 Month'), ('4 Month', '4 Month'),
                                          ('6 Month', '6 Month')), string="Loan Duration")
    cus_status = fields.Selection((('Active', 'Active'), ('Deactivate', 'Deactivate')), string="Status", required=True)
    # l_amount = fields.Integer(string="sdsdds")

    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list
    cus_loan_year = fields.Selection('_get_years', string="Loan Year", required=True)

    @api.onchange('name')
    def onchange_name(self):
        loan_id = self.name.acc_id
        loan_name = self.name.c_fname_lname

        self.cus_loan_acid = loan_id
        self.cus_loan_name = loan_name


    @api.depends('cus_loan_amount')
    def _get_sum_loan(self):

        for rec in self:
            rec.update({
                'cus_loan_interest': int(((rec.cus_loan_amount * 25) // 100)),
            })

    @api.depends('cus_loan_amount', 'cus_loan_interest')
    def _get_sum_tloan(self):
        for rect in self:
            rect.update({
                'cus_loan_total':rect.cus_loan_amount + rect.cus_loan_interest
            })


class daily_payment(models.Model):
    _name = 'daily_payment'
    _order = 'c_payment_date desc'

    id = fields.Char(string="ID")
    name = fields.Many2one('customer_loan', string="Search Customer", required=True, domain=[('cus_status','=','Active')])
    c_payment_id = fields.Char(string="Customer ID", required=True)
    c_account_no = fields.Char(string="Customer Acc No", required=True)
    c_payment_name = fields.Char(string="Customer Name", required=True)
    c_payment_date = fields.Date(string="Payment Date", default=datetime.today())
    c_payment_notes = fields.Text(string="Payment Notes")
    c_main_loan = fields.Integer(string="Main Loan")
    c_loan_amount = fields.Integer(string="With Interest loan")
    c_payment_daily = fields.Integer(string="Daily Payment", required=True)
    c_payment_mainamnt = fields.Integer(string="Main Amount", required=True)
    c_payment_interest = fields.Integer(string="Interest Amount", required=True)
    c_payment_due = fields.Integer(string="Due With Interest")
    c_total_pay = fields.Integer(string="Total Main Amount Pay")
    ########
    payment_sec = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    @api.model
    def create(self, vals):
        n_id = vals.get('name')
        if n_id:
            c_loan_amount = vals.get('c_loan_amount')
            c_payment_daily = vals.get('c_payment_daily')
            # c_main_loan = vals.get('c_main_loan')
            c_payment_mainamnt = vals.get('c_payment_mainamnt')

            if c_loan_amount:
                lit = []
                lit2 =[]
                see = 0
                see2 = 0
                see3 = 0
                see4 = 0
                final_due = 0
                b = self.env['daily_payment'].search([('name', '=' , n_id)])
                if b:
                    for item in b:
                        lit.append(item.c_payment_daily)
                        lit2.append(item.c_payment_mainamnt)
                    if len(lit) > 0 and len(lit2) > 0:
                        see = sum(lit) + c_payment_daily
                        see3 = sum(lit2) + c_payment_mainamnt
                        final_due = int(c_loan_amount - see)
                    v = super(daily_payment, self).create(vals)
                    v.c_payment_due = final_due
                    v.c_total_pay = see3
                    return v
                else:
                    see2 = c_payment_daily
                    see4 = c_payment_mainamnt
                    final_due = int(c_loan_amount - see2)
                    v = super(daily_payment, self).create(vals)
                    v.c_payment_due = final_due
                    v.c_total_pay = see4
                    return v

    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list

    c_payment_year = fields.Selection('_get_years', string="Select Year", required=True)

    @api.onchange('name', 'c_loan_amount', 'c_payment_daily', 'c_payment_mainamnt', 'c_payment_interest', 'c_payment_due')
    def onchange_name(self):
        pay_id = self.name.id
        pay_name = self.name.cus_loan_name
        pay_acc_id = self.name.cus_loan_acid
        pay_loan = self.name.cus_loan_total
        main_loan_a = self.name.cus_loan_amount
        self.c_payment_id = pay_id
        self.c_payment_name = pay_name
        self.c_account_no = pay_acc_id
        self.c_loan_amount = pay_loan
        self.c_main_loan = main_loan_a

        savings = self.env['daily_payment'].search([('name', '=', pay_id)])
        if savings:
            lit = []
            lit2 = []
            see = 0
            see2 = 0
            see3 = 0
            see4 = 0
            final_due = 0
            for item in savings:
                lit.append(item.c_payment_daily)
                lit2.append(item.c_payment_mainamnt)
            if len(lit) > 0 and len(lit2) > 0:
                see = sum(lit) + self.c_payment_daily
                see3 = sum(lit2) + self.c_payment_mainamnt
                final_due = (self.c_loan_amount - see)
                self.c_total_pay = see3
                self.c_payment_due = final_due
        else:
            see2 = self.c_payment_daily
            see4 = self.c_payment_mainamnt
            final_due = (self.c_loan_amount - see2)
            self.c_total_pay = see4
            self.c_payment_due = final_due

    @api.model
    def _create(self, vals):
        if vals.get('payment_sec', _('New')) == _('New'):
            vals['payment_sec'] = self.env['ir.sequence'].next_by_code('customer.payment.sequence') or _('New')
        result = super(daily_payment, self)._create(vals)
        return result

######### SHOW AMMOUNT ###########
    main_ammn_show = fields.Integer('', compute='show_status')
    interest_ammn_show = fields.Integer('', compute='show_status')
    total_ammn_show = fields.Integer('', compute='show_status')

    @api.depends('c_payment_mainamnt', 'c_payment_interest', 'c_payment_date')
    def show_status(self):
        date_show = self.c_payment_date

        search = self.env['daily_payment'].search([('c_payment_date', '=', date_show)])
        if search:
            a = []
            b = []
            for i in search:
                a.append(i.c_payment_mainamnt)
                b.append(i.c_payment_interest)
            if len(a) > 0 and len(b) > 0:
                a = sum(a) + self.c_payment_mainamnt
                b = sum(b) + self.c_payment_interest
                sum_show = a + b
                self.main_ammn_show = a
                self.interest_ammn_show = b
                self.total_ammn_show = sum_show

        else:
            a2 = self.c_payment_mainamnt
            b2 = self.c_payment_interest
            sum_show2 = a2 + b2
            self.main_ammn_show = a2
            self.interest_ammn_show = b2
            self.total_ammn_show = sum_show2

    def open_customer_savings_form(self):

        return {
            'name': _('Customer Savings'),
            'type': 'ir.actions.act_window',
            'res_model': 'customer_savings',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name':self.name.id,
            }
        }

#########################


class PaidLoan(models.Model):
    _name = 'paid_loan'

    name = fields.Many2one('customer_loan', string="Search Customer", required=True, domain=[('cus_status','=','Active')])
    cus_loan_take = fields.Integer(string="Loan Amount")
    paid_amount = fields.Integer(string="Paid Amount")
    paid_date = fields.Date(string="Paid Date", required=True)
    available_loan = fields.Integer(string="Outdoor loan")
    paid_status = fields.Char(string="Paid Status", required=True)
    paid_ID = fields.Char(string="Loan id", required=True)


    @api.model
    def create(self, vals):
        paid_name = vals.get('name')
        if paid_name:
            t = 0
            cus_loan_take = vals.get('cus_loan_take')
            paid_amount = vals.get('paid_amount')
            paid_id = vals.get('paid_ID')

            if cus_loan_take == paid_amount:
                v = self.env['customer_loan'].search([])
                for i in v:
                    t += i.cus_loan_amount

                paid = vals.get('paid_amount')
                final = t - paid
                vals['available_loan'] = final

                self._cr.execute("UPDATE customer_loan SET cus_status='Deactivate' WHERE cus_loan_acid=%s",
                                 (str(paid_id),))
                self._cr.execute("UPDATE customer_loan SET cus_loan_amount=0 WHERE cus_loan_acid=%s",
                                 (str(paid_id),))

                return super(PaidLoan, self).create(vals)

            else:
                raise UserError('You have to pay the rest')


    @api.onchange('name', 'cus_loan_take', 'paid_amount')
    def onchange_name(self):
        paiable_loan_ = self.name.cus_loan_acid
        loan_gate = self.name.cus_loan_amount
        paid_status = self.paid_status

        self.paid_ID = paiable_loan_
        self.cus_loan_take = loan_gate

        id = self.name.id
        d_p_s = self.env['daily_payment'].search([('c_payment_id','=', id)])
        if d_p_s:
            x = []
            for i in d_p_s:
                x.append(i.c_payment_mainamnt)

            if len(x) > 0:
                y = sum(x)
                self.paid_amount = y
                # raise UserError(_(y))
        if (self.cus_loan_take == self.paid_amount):
            self.paid_status = "PAID AMOUNT"
        else:
            self.paid_status = "NOT PAID"

class CustomerStatus(models.Model):
    _name = 'customer_status'

    name = fields.Many2one('customer_loan', string="Search Customer", required=True)
    search_date = fields.Datetime(string="Date")
    cus_search_loan = fields.Integer(string="Main Amount")
    cus_search_interest = fields.Integer(string="Interest Amount")
    cus_paid_tilltoday = fields.Integer(string="Paid Till")
    cus_paid_interest = fields.Integer(string="Interest Paid Till")
    cus_due_pay = fields.Integer(string="Due Pay", required=True)
    cus_due_interest = fields.Integer(string="Due Interest", required=True)


    @api.onchange('name')
    def onchange_name(self):
        paiable_loan_ = self.name.cus_loan_amount
        loan_interest = self.name.cus_loan_interest

        self.cus_search_loan = paiable_loan_
        self.cus_search_interest = loan_interest

        id = self.name.id
        d_p_s = self.env['daily_payment'].search([('c_payment_id', '=', id)])
        if d_p_s:
            a = []
            b = []
            c = []
            for i in d_p_s:
                a.append(i.c_payment_mainamnt)
                b.append(i.c_payment_interest)

            if len(a) > 0 and len(b) > 0:
                x = sum(a)
                y = sum(b)
                final_a = paiable_loan_ - x
                final_b = loan_interest - y

                self.cus_paid_tilltoday = x
                self.cus_paid_interest = y
                self.cus_due_pay = final_a
                self.cus_due_interest = final_b

class CustomerSavings(models.Model):
    _name = 'customer_savings'

    name = fields.Many2one('customer', string="Search Customer", required=True)
    cus_id = fields.Char(string="Customer ID")
    savings_id = fields.Char(string="Savings ID", required=True)
    savings_name = fields.Char(string="Customer Name", required=True)
    savings_date = fields.Date(string="Savings Date", required=True)
    savings_amount = fields.Integer(string="Savings Amount")
    worth_amount = fields.Integer(string="Worth Amouunt")
    totalsavings = fields.Integer(string="Total Savings")

    @api.model
    def create(self, vals):
        n_id = vals.get('name')

        if n_id:
            savings_amount = vals.get('savings_amount')
            worth_amount = vals.get('worth_amount')
            # totalsavings = vals.get('totalsavings')

            if savings_amount or worth_amount:
                lit = []
                lit2 = []
                see = 0
                see2 = 0
                see3 = 0
                see4 = 0
                final_savings = 0
                b = self.env['customer_savings'].search([('name', '=', n_id)])
                if b:
                    for item in b:
                        lit.append(item.savings_amount)
                        lit2.append(item.worth_amount)
                    if len(lit) > 0 and len(lit2) > 0:
                        see = sum(lit) + savings_amount
                        see3 = sum(lit2) + worth_amount
                        final_savings = int(see - see3)
                    v = super(CustomerSavings, self).create(vals)
                    v.totalsavings = final_savings
                    return v
                else:
                    see2 = savings_amount
                    see4 = worth_amount
                    final_savings = int(see2 - see4)
                    v = super(CustomerSavings, self).create(vals)
                    v.totalsavings = final_savings
                    return v

    @api.onchange('name', 'savings_amount', 'worth_amount', 'totalsavings')
    def onchange_name(self):
        cus_acc_id = self.name.id
        cus_savings_id = self.name.acc_id
        cus_savings_name = self.name.c_fname_lname

        self.cus_id = cus_acc_id
        self.savings_id = cus_savings_id
        self.savings_name = cus_savings_name

        savings = self.env['customer_savings'].search([('name', '=', cus_acc_id)])
        if savings:
            lit = []
            lit2 = []
            see = 0
            see2 = 0
            see3 = 0
            see4 = 0
            final_due = 0
            for item in savings:
                lit.append(item.savings_amount)
                lit2.append(item.worth_amount)
            if len(lit) > 0 and len(lit2) > 0:
                see = sum(lit) + self.savings_amount
                see3 = sum(lit2) + self.worth_amount
                final_savings = (see - see3)
                self.totalsavings = final_savings
        else:
            see2 = self.savings_amount
            see4 = self.worth_amount
            final_savings = (see2 - see4)
            self.totalsavings = final_savings

class CustomerSavingsStatus(models.Model):
    _name = 'customer_savings_stutas'

    name = fields.Many2one('customer', string="Search Customer", required=True)
    savings_name = fields.Char(string="Customer Name", required=True)
    total_savings = fields.Integer(string="Total Savings")
    worth_savings = fields.Integer(string="Worth Amount")
    available_savings = fields.Integer(string="Available Amount")

    @api.onchange('name')
    def onchange_name(self):
        savingsname = self.name.c_fname_lname
        self.savings_name = savingsname

        id = self.name.id
        savings = self.env['customer_savings'].search([('cus_id', '=', id)])
        if savings:
            x = []
            y = []
            for i in savings:
                x.append(i.savings_amount)
                y.append(i.worth_amount)

            if len(x) > 0:
                a = sum(x)
                b = sum(y)
                total_amount = a - b

                self.total_savings = int(a)
                self.worth_savings = int(b)
                self.available_savings = int(total_amount)
                # raise UserError(_(y))

class PaidSavings(models.Model):
    _name = 'paid_savings'

    name = fields.Many2one('customer', string="Search Customer", required=True)
    customer_id = fields.Char(string="Customer ID", required=True)
    customer_savings_name = fields.Char(string="Customer Name", required=True)
    date_paid_savings = fields.Date(string="Paid Date", required=True)
    customer_status = fields.Char(string="Customer Status", required=True)
    total_savings = fields.Integer(string="Total Savings", required=True)
    # savings_interest = fields.Integer(string="Savings Interest", required=True, compute='_get_total_savings')
    # total_savings_interest = fields.Integer(string="Total Paid", required=True, compute='_get_total_savings2')
    savings_interest = fields.Integer(string="Savings Interest", required=True)
    total_savings_interest = fields.Integer(string="Total Paid", required=True)

    @api.onchange('name', 'total_savings')
    def onchange_name(self):
        savings_id = self.name.acc_id
        savings_name = self.name.c_fname_lname
        savings_intr = self.total_savings

        self.customer_id = savings_id
        self.customer_savings_name = savings_name
        self.customer_status = 'PAID'
        self.savings_interest = (savings_intr*25)//100
        self.total_savings_interest = savings_intr + self.savings_interest



class DailySavings(models.Model):
    _name = 'daily_savings'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name", required=True)
    select_date = fields.Date(string="Select Date", required=True)
    all_save_amount = fields.Integer(string="Save Amount")
    worth_save_amount = fields.Integer(string="Worth Amount")
    per_day_total = fields.Integer(string="Per Day Total Savings")

    @api.onchange('select_date')
    def onchange_name(self):
        date = self.select_date

        savings = self.env['customer_savings'].search([('savings_date', '=', date)])
        if savings:
            x = []
            y = []
            for i in savings:
                x.append(i.savings_amount)
                y.append(i.worth_amount)

            if len(x) > 0:
                a = sum(x)
                b = sum(y)
                total_amount = a - b

                self.all_save_amount = a
                self.worth_save_amount = b
                self.per_day_total = total_amount
                # raise UserError(_(y))

class DailyEarnLoan(models.Model):
    _name = 'daily_earn_loan'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name",
                                  required=True)
    select_earn_date = fields.Date(string="Select Date", required=True)
    all_main_amount = fields.Integer(string="Total Main Amount")
    all_interest_amount = fields.Integer(string="Total Interest Amount")

    @api.onchange('select_earn_date')
    def onchange_name(self):
        date = self.select_earn_date

        earn_amouunt = self.env['daily_payment'].search([('c_payment_date', '=', date)])
        if earn_amouunt:
            x = []
            y = []
            for i in earn_amouunt:
                x.append(i.c_payment_mainamnt)
                y.append(i.c_payment_interest)

            if len(x) > 0 and len(y) > 0:
                a = sum(x)
                b = sum(y)

                self.all_main_amount = a
                self.all_interest_amount = b
                # raise UserError(_(y))


class DailyCashDrawer(models.Model):
    _name = 'daily_cash_drawer'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name",
                                  required=True)
    cash_date = fields.Date(string="Select Date", required=True)
    earn_cash = fields.Integer(string="Daily Earn Cash")
    expense_loan = fields.Integer(string="Expense Loan")
    expense_savings = fields.Integer(string="Expense Savings")
    daily_cash_drawer = fields.Integer(string="Daily Cash Drawer")
    final_cash = fields.Integer(string="Final Cash Drawer")
    admin_pockets_pay = fields.Integer(string="Admins Pay Cash")
    admins_comment = fields.Selection((('Admin Can Cut The Amount in Next Day Earn Amount '
                                        , 'Admin Can Cut The Amount in Next Day Earn Amount')
                                       , ('Admin Can Take The Due Amount', 'Admin Can Take The Due Amount'))
                                      , string="Admins Due Comment")

    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list
    cash_year = fields.Selection('_get_years', string="Cash Year", required=True)

    @api.onchange('earn_cash','expense_loan','expense_savings','daily_cash_drawer','cash_date')
    def onchange_name(self):
        total_earn_cash = self.earn_cash

        self.daily_cash_drawer = total_earn_cash - (self.expense_loan+self.expense_savings)

        date = self.cash_date
        if date:
            daily_cash_drawer = self.daily_cash_drawer

            lit = []
            see = 0
            see2 = 0
            final_amount = 0

            b = self.env['daily_cash_drawer'].search([])
            if b:
                for item in b:
                    lit.append(item.daily_cash_drawer)

                if len(lit) > 0:
                    see = sum(lit) + daily_cash_drawer
                    final_amount = see
                    self.final_cash = final_amount
                # raise UserError(_(final_amount))
                # return v
            else:
                see2 = daily_cash_drawer
                final_amount = see2
                self.final_cash = final_amount
                # # raise UserError(_(final_amount))
                # return v

            earn_amouunt = self.env['customer_loan'].search([('cus_loan_date', '=', date)])
            savings = self.env['paid_savings'].search([('date_paid_savings', '=', date)])
            if earn_amouunt or savings:
                x = []
                # y = []
                for i in earn_amouunt:
                    x.append(i.cus_loan_amount)

                if len(x) > 0 :
                    a = sum(x)

                    self.expense_loan = a

                x = []
                # y = []
                for i in savings:
                    x.append(i.total_savings_interest)
                    # y.append(i.worth_amount)

                if len(x) > 0:
                    a = sum(x)
                    # b = sum(y)
                    # total_amount = a - b
                    self.expense_savings = a
            dailt_earn = self.env['daily_earn_drawer'].search([('earn_cash_date', '=', date)])
            if dailt_earn:
                x = []
                # y = []
                for i in dailt_earn:
                    x.append(i.perday_total_cash)
                if x:
                    a = sum(x)
                    self.earn_cash = a
                else:
                    see4 = 000
                    self.earn_cash = see4


class DailyEarnCash(models.Model):
    _name = 'daily_earn_drawer'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name",
                                  required=True)
    earn_cash_date = fields.Date(string="Select Date", required=True)
    earn_main_cash = fields.Integer(string="Earn Main Amount", required=True)
    earn_day_savings = fields.Integer(string="Earn Savings")
    worth_day_savings = fields.Integer(string="Worth Savings")
    perday_interest = fields.Integer(string="Earn Interest")
    company_expense = fields.Integer(string="Company Expense")
    perday_total_interest = fields.Integer(string="Total Interest ")
    perday_total_cash = fields.Integer(string="Total Cash Per Day", required=True)
    notes = fields.Text(string="Notes")

    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list
    earn_cash_year = fields.Selection('_get_years', string="Cash Year", required=True)

    @api.onchange('earn_cash_date', 'earn_main_cash', 'earn_day_savings', 'perday_interest', 'company_expense')
    def onchange_name(self):
        date = self.earn_cash_date

        earn_amouunt = self.env['daily_payment'].search([('c_payment_date', '=', date)])
        savings = self.env['customer_savings'].search([('savings_date', '=', date)])
        if earn_amouunt or savings:
            x = []
            y = []
            for i in earn_amouunt:
                x.append(i.c_payment_mainamnt)
                y.append(i.c_payment_interest)

            if len(x) > 0 and len(y) > 0:
                a = sum(x)
                b = sum(y)

                self.earn_main_cash = a
                self.perday_interest = b

            x = []
            y = []
            for i in savings:
                x.append(i.savings_amount)
                y.append(i.worth_amount)

            if len(x) > 0:
                a = sum(x)
                b = sum(y)
                # total_amount = a - b

                self.earn_day_savings = a
                self.worth_day_savings = b
                # self.earn_day_savings = total_amount

        total_main_cash = self.earn_main_cash

        self.perday_total_interest = self.perday_interest - self.company_expense
        self.perday_total_cash = ((total_main_cash + self.earn_day_savings + self.perday_interest)
                                    - (self.worth_day_savings + self.company_expense))


    # @api.onchange('earn_main_cash', 'earn_day_savings', 'perday_interest', 'company_expense')
    # def onchange_name(self):
    #     total_main_cash = self.earn_main_cash
    #
    #     self.perday_total_interest = self.perday_interest - self.company_expense
    #     self.perday_total_cash = (total_main_cash + self.earn_day_savings + self.perday_total_interest)

class AnnualIncome(models.Model):
    _name = 'annual_income'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name",
                                  required=True)
    annual_estimate_date = fields.Date(string="Annual Estimate Date", required=True)
    annual_income = fields.Integer(stirng="Annual Income")
    annual_expense = fields.Integer(stirng="Annual Expense")
    total_annual_income = fields.Integer(string="Total Income")
    annual_notes = fields.Text(stirng="Annual Notes")


    def _get_years(self):
        year_list = []
        for i in range(2019, 2100):
            year_list.append((str(i), str(i)))
        return year_list
    estimate_cash_year = fields.Selection('_get_years', string="Annual Cash Year", required=True)

    @api.onchange('estimate_cash_year', 'annual_income')
    def onchange_name(self):
        year = self.estimate_cash_year

        annula_cash_amouunt = self.env['daily_earn_drawer'].search([('earn_cash_year', '=', year)])
        if annula_cash_amouunt:
            x = []
            y = []
            for i in annula_cash_amouunt:
                x.append(i.perday_interest)
                y.append(i.company_expense)

            if len(x) > 0 or len(y) > 0 :
                a = sum(x)
                b = sum(y)

                total = a - b

                self.annual_income = a
                self.annual_expense = b
                self.total_annual_income = total
            else:
                c = sum(x)
                d = sum(y)
                total2 = c -d
                self.annual_income = c
                self.annual_expense = d
                self.total_annual_income = total2
                # raise UserError('No Income')

class dashBoard(models.Model):
    _name = 'dash_board'

    admin_name = fields.Selection((('Bidhan Roy', 'Bidhan Roy'), ('Ful Babu', 'Ful Babu')), string="Admin Name")
    annual_estimate_date = fields.Date(string="Annual Estimate Date")
    title_text = fields.Char(stirng="Title")
    number = fields.Integer(stirng="Number", compute='change')
    final_number = fields.Integer(string="SST")

    # _defaults :(
    #     {
    #         'number': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'lib.resource'),
    #     })
























