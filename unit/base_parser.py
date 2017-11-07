# -*- coding: utf-8 -*-

import requests
from  lxml import html, etree
import logging
from selenium import webdriver
import os

_logger = logging.getLogger(__name__)

class base_parser(object):
    def __init__(self, url):
        self.url = url        
    
    def take_from_url(self):
        if self.url:
            res = requests.get(self.url, allow_redirects=True, verify=False).text
            self.page_text = res
            return(self.page_text)
    
    def get_html_tree(self, text=None):
        if not text:
            if not self.page_text:
                text = self.take_from_url()
            else:
                text = self.page_text
                
        self.html_tree = html.fromstring(text)
        return self.html_tree
    
    def get_block_unparsed_lines(self, html_tree=None, block_pattern=None):
        '''Return block of unparsed lines from lxml tree (source_tree) using xpath pattern block_pattern'''
        
        if not block_pattern:
            return False
        
        if not html_tree:
            if not self.html_tree:
                html_tree = self.get_html_tree()
            else:
                html_tree = self.html_tree
                
        try:
            result = html_tree.xpath(block_pattern)[0]
        except IndexError:
            return False
        
        self.block_unparsed_lines = result
        return self.block_unparsed_lines
    
    def get_unparsed_lines(self, pattern=None):
        if not self.block_unparsed_lines:
            if self.get_block_unparsed_lines():
                return self.block_unparsed_lines.xpath(pattern)
        return False
    
    def get_record_uline_patt(uline, patt):
        ''' Get record from unparsed line uline using pattern patt'''
        result = uline.xpath(patt)[0] 
        return result
    
    def get_image(self, patt):
        #if not self.html_tree:
            #html_tree = self.get_html_tree()
        #else:
            #html_tree = self.html_tree        
        html_tree = self.get_html_tree()        
        #image_link = html_tree.xpath(patt)[0]
        
        if os.name == 'nt':
            driver = webdriver.PhantomJS(executable_path="c:\\Python27\\phantomjs.exe", port=7777, service_log_path=os.path.devnull)
        else:
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs", port=7777, service_log_path=os.path.devnull)
        driver.get(self.url)
        results = driver.find_elements_by_xpath('.//div[@class="col-md-8"]/div[@class="pull-left"]/a/img')
        image_link = results[0].get_attribute('src')
        driver.quit()
        
        return image_link
    
class i502_sales_lm_total(base_parser):

    def get_result(self):
        s = self
        s.take_from_url()            
        s.get_html_tree()            
        s.get_block_unparsed_lines(block_pattern='//table[@class="table table-bordered table-striped"]')            
        unparsed_lines =  s.get_unparsed_lines(pattern='.//tr')        
        if unparsed_lines:
            lm_sales, total, image = unparsed_lines[1][1].text, unparsed_lines[-1][1].text, self.get_image(
                './/div[@class="col-md-8"]/div[@class="pull-left"]/a/img/@src') 
            return lm_sales, total, image        
        return False
            

if __name__=='__main__':
    myparser = base_parser('https://502data.com/license/415645')    
    myparser.take_from_url()
    myparser.get_html_tree()
    myparser.get_block_unparsed_lines(block_pattern='//table[@class="table table-bordered table-striped"]')
    unparsed_lines =  myparser.get_unparsed_lines(pattern='.//tr')
    print('Last month sales are %s' % unicode(unparsed_lines[1][1].text))
    print('Total sales are %s' % unicode(unparsed_lines[-1][1].text))
    for node in unparsed_lines:
    #for node in myparser.take_from_url().get_html_tree().get_block_unparsed_lines(pattern='//table[@class="table table-bordered table-striped"]').get_unparsed_lines(pattern='.//tr'):
        l = node.xpath('.//td')
#        l = etree.tostring(node.xpath('.//td'))
        if len(l):
            print len(l)
            for item in l:
                print('etree.tostring(item): %s' % unicode(etree.tostring(item)))
                print(item.text)                


