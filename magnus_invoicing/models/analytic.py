# -*- coding: utf-8 -*-
# Copyright 2018 Magnus ((www.magnus.nl).)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime, timedelta

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Confirmed'),
        ('delayed', 'Delayed'),
        ('invoiceable', 'To be Invoiced'),
        ('progress', 'In Progress'),
        ('invoiced', 'Invoiced'),
        ('write_off', 'Write-Off'),
        ('change-chargecode', 'Change-Chargecode'),
    ],
        string='Status',
        readonly=True,
        copy=False,
        index=True,
        track_visibility='onchange',
        default='draft'
    )

    @api.multi
    def write(self, vals):
        ctx = self.env.context.copy()
        if 'state' in vals:
            ctx.update({'state': True})
        return super(AccountAnalyticLine, self.with_context(ctx)).write(vals)

    def _check_state(self):
        """
        to check if any lines computes method calls allow to modify
        :return: True or super
        """
        context = self.env.context.copy()
        if not 'active_model' in context \
                or 'active_invoice_id' in context \
                or 'cc' in context and context['cc']\
                or 'state' in context and context['state']:
            return True
        return super(AccountAnalyticLine, self)._check_state()

