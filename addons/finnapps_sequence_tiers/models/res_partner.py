# -*- coding: utf-8 -*-
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    compte_tiers = fields.Char(
        string="Compte tiers",
    )

    _sql_constraints = [
        ('compte_tiers', 'UNIQUE (compte_tiers)', 'Compte tiers existe déjà'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        for partner in res:
            seq = ""
            if not partner.compte_tiers:
                if partner.customer and partner.supplier:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.customer') or ""
                elif partner.customer:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.customer') or ""
                elif partner.supplier:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.supplier') or ""
                
                if seq:
                    partner.update({'compte_tiers': seq})

        return res

    def write(self, vals):
        res =  super(ResPartner, self).write(vals)
        for partner in self:
            seq = ""
            if not partner.compte_tiers:
                if partner.customer and partner.supplier:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.customer') or ""
                elif partner.customer:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.customer') or ""
                elif partner.supplier:
                    seq = self.env['ir.sequence'].next_by_code('res.partner.supplier') or ""
                if seq:
                    partner.update({'compte_tiers': seq})
        return res



    @api.depends('is_company', 'name', 'compte_tiers', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        for partner in self:
            if partner.compte_tiers:
                display_value = '[' + str(partner.compte_tiers) + '] ' + str(partner.name)
            else:
                display_value = partner.name
            
            partner.display_name = display_value


   
   