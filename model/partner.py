# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
from ..unit import base_parser

_logger = logging.getLogger(__name__)

#class pricelist_partnerinfo(models.Model):
    #_inherit = 'pricelist.partnerinfo'    
    
    #product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Product', related='suppinfo_id.product_tmpl_id')
    #vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', related='suppinfo_id.name', store=True)
    #product_code = fields.Char(string='Product code', related='suppinfo_id.product_code')
    #product_name = fields.Char(string='Product name', related='suppinfo_id.product_name')
    
class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    
    @api.multi
    def get_lms_i502(self):
        #self.ensure_one()
        for item in self:
            try:
                if item.partner_license_key:
                    item.i502 = 'http://502data.com/license/' + unicode(item.partner_license_key)
                    #item.i502 = 'https://502data.com/license/' + unicode(item.partner_license_key)
            except AttributeError :
                pass
            if item.i502:
                parser = base_parser.i502_sales_lm_total(item.i502)
                item.last_month_sales = parser.get_result()[0]
        
    #supplier_info_ids = fields.One2many(comodel_name='product.supplierinfo', inverse_name='name', string='Vendor`s product offerings')
    #pricelist_partnerinfo_ids = fields.One2many(comodel_name='pricelist.partnerinfo', inverse_name='vendor_id', string='Vendor`s product offerings')
    partner_product_info_ids = fields.One2many(comodel_name='partner.product.info', 
                                              inverse_name='partner_id', 
                                              string='Partner`s production info')
    near_stores = fields.Many2many(comodel_name='res.partner', relation='near_partners_rel', 
                                  column1='leftp', 
                                  column2='rightp', 
                                  string='These are near')
    near_stores_rev = fields.Many2many(comodel_name='res.partner', relation='near_partners_rel', 
                                  column1='rightp', 
                                  column2='leftp', 
                                  string='Is near to these')
    
    last_month_sales = fields.Char(string='Last Month`s Sales')
    
        
