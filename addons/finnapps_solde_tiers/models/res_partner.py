# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class ResPartner(models.Model):
    _inherit = 'res.partner'

    move_line_ids = fields.One2many(
        string='Ecritures comptable',
        comodel_name='account.move.line',
        inverse_name='partner_id',
    )


    solde = fields.Float(
        string="Solde",
        compute='get_the_solde',
        store=True,

    )

    def get_solde(self):
        sudo = self.sudo()
        sql_receivable = "SELECT id FROM account_account WHERE account_type in ('asset_receivable','asset_payable')"
        sql_posted = "SELECT id FROM account_move WHERE state = 'posted'"
        for record in self:
            ids = tuple(record.env['account.move.line'].search([('partner_id','=',record.id),('move_id.state','=', 'posted')]).ids)
            if ids :
                if len(ids) == 1:
                    sql = "select SUM(debit - credit) as solde FROM account_move_line WHERE account_move_line.id IN ({}) and account_id IN ({}) ".format(ids[0], sql_receivable)
                else:
                    sql = "select SUM(debit - credit) as solde FROM account_move_line WHERE account_move_line.id IN {} and account_id IN({}) ".format(ids, sql_receivable)


                self.env.cr.execute(sql)
                aml = self.env.cr.dictfetchall()

                return aml[0]['solde']
        
        return 0


    @api.depends('move_line_ids')
    def get_the_solde(self):
        self.solde = self.get_solde()
