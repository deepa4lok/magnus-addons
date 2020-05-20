# -*- coding: utf-8 -*-
# Copyright 2018 Magnus ((www.magnus.nl).)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = "res.users"


    @api.multi
    def _get_operating_unit_id(self):
        """ Compute Operating Unit of Employee based on the OU in the
        top Department."""
        employee_id = self._get_related_employees()
        assert len(employee_id) == 1, 'Only one employee can have this user_id'
        if employee_id.department_id:
            dep = self.env['hr.department'].search([
                ('parent_id', '=', False),
                '|',
                ('id', '=', employee_id.department_id.id),
                ('child_ids', 'in', [employee_id.department_id.id]),
                '|',
                ('id', '=', employee_id.department_id.parent_id.id),
                ('child_ids', 'in', [employee_id.department_id.parent_id.id] if employee_id.department_id.parent_id else [])
            ])
        else:
            raise ValidationError(_('The Employee in the Analytic line has '
                                    'no department defined. Please complete'))
        return dep.operating_unit_id
