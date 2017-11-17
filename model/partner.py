# -*- coding: utf-8 -*-
from openerp import models, fields, api, http
import logging, os, sys, base64
from ..unit import base_parser, bin_fetcher

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
    def get_image(self):
        for i in self:
            if i.image_url:
                
                fetcher = bin_fetcher.b_fetcher(self.image_url)
                image_name = fetcher.get_file_name_from_url()
                if os.name == 'nt':
                    addons_path = './'
                else:
                    addons_path = '/opt/odoo/'
#                addons_path = i.env.http.addons_manifest['web']['addons_path']
                _logger.info('Addons path is: %s' % unicode(addons_path))
                full_name = os.path.join(addons_path, image_name)
#                full_name = os.path.join(addons_path,'modulename','static','src','img', image_name)
                fetcher.fetch_to(full_name)
                f = open(full_name,'rb')
                img  = f.read()
#                img_encoded = img
                img_encoded = base64.b64encode(img)
                i.image = img_encoded
           #     i.image = i.env['ir.attachment'].create({'name':image_name, 'type':'binary', 'res_id':i.id,
           #                                    'res_model':'res.partner', 'datas':base64.encodestring(f.read())})
                                               #'res_model':'res.partner', 'url':addons_path, 'datas':base64.encode(f.read())})
                f.close()
#                i.env['ir.attachment'].create({'name':image_name, 'type':'url', 'res_id':i.id, 'res_model':'res.partner', 'url':i.image_url})
                
            
    @api.multi
    def fetch_i502(self):
        for i in self:
            try:
                if i.partner_license_key:
                    i.i502 = 'http://502data.com/license/' + unicode(i.partner_license_key)
            except AttributeError :
                pass
            if i.i502:            
                driver = base_parser.phantomjs_parser()
                html_page = driver.get_page(i.i502)

    
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
                res = parser.get_result()
                if res:
                    _logger.info('get_lms_i502 res is : %s'  % unicode(res))
                    if len(res) == 3:
                        item.last_month_sales, item.total_sales, item.image_url = res
                
        
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
    total_sales = fields.Char(string='Total Sales')
    plk = fields.Char(string='PLK')
    
    image_url = fields.Char(string='Image url')
    
    @api.multi
    def get502data(self):
        self.get_lms_i502()
        if self.image_url:
            self.get_image()
        
