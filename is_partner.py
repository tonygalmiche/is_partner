# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
        'is_code': fields.char('Code'),
        'is_adr_code': fields.char('Code adresse'),
        'is_adr_livraison': fields.many2one('res.partner', 'Adresse de livraison'),
        'is_adr_facturation': fields.many2one('res.partner', 'Adresse de facturation'),
        'is_adr_groupe': fields.many2one('res.partner', 'Adresse groupe'),
    }
    
    _sql_constraints = [
        ('code_adr_uniq', 'unique(is_code, is_adr_code, company_id)', u'Le code et le code adresse doivent être uniques par société!'),
    ]
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name =  "%s, %s" % (record.parent_id.name, name)
            if record.is_company:
                if record.is_code and record.is_adr_code:
                    name =  "%s (%s/%s)" % (name, record.is_code, record.is_adr_code)
                if record.is_code and not record.is_adr_code:
                    name =  "%s (%s)" % (name, record.is_code)
                                    
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res
    
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}        
        partner = self.browse(cr, uid, id, context=context)   
        if partner.is_company:           
            default.update({
                'is_code': partner.is_code + ' (copie)',
                'is_adr_code': partner.is_adr_code + ' (copie)',
        })
        return super(is_partner, self).copy(cr, uid, id, default, context=context)
    

    
is_partner()