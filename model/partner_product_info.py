# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class partner_product_info(models.Model):
#class partner_product(models.Model):
    _name = 'partner.product.info'    
#    _name = 'partner.product'    
    
    name = fields.Char(string='Partner`s product name')
    product_id = fields.Many2one(comodel_name='product.product', string='Our corresponding product')    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner Store')    
    price_one_gram = fields.Float(string="One gramm price")    

#class partner_product_info(models.Model):
    #_name = 'partner.product.info'    
    
    #partner_product_id = fields.Many2one(comodel_name='partner.product', string='Partner`s product')    
    
    #product_id = fields.Many2one(comodel_name='product.product', related='partner_product_id.product_id', string='Our corresponding product')    
    #partner_id = fields.Many2one(comodel_name='res.partner', related='partner_product_id.partner_id', store=True)    
    
    #price_one_gram = fields.Float(string="One gramm price", digits=2)    
    