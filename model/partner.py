# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

#class pricelist_partnerinfo(models.Model):
    #_inherit = 'pricelist.partnerinfo'    
    
    #product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Product', related='suppinfo_id.product_tmpl_id')
    #vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', related='suppinfo_id.name', store=True)
    #product_code = fields.Char(string='Product code', related='suppinfo_id.product_code')
    #product_name = fields.Char(string='Product name', related='suppinfo_id.product_name')
    
class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    #supplier_info_ids = fields.One2many(comodel_name='product.supplierinfo', inverse_name='name', string='Vendor`s product offerings')
    #pricelist_partnerinfo_ids = fields.One2many(comodel_name='pricelist.partnerinfo', inverse_name='vendor_id', string='Vendor`s product offerings')
    partner_product_info_ids = fields.One2many(comodel_name='partner.product.info', 
                                              inverse_name='partner_id', 
                                              string='Partner`s production info')
    
        
