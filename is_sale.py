# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_sale_order_address(osv.osv):
    _inherit = 'sale.order'
    
    _columns = {
        'partner_group_id': fields.many2one('res.partner', 'Adresse groupe', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Adresse groupe de la commande courante"),
    }
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(is_sale_order_address, self).onchange_partner_id(cr, uid, ids, part, context=context)
        print 'res ******', res
        if part:
            partner = self.pool.get('res.partner').browse(cr, uid, part, context=context)
            if partner.is_adr_livraison:
                res['value'].update({'partner_shipping_id': partner.is_adr_livraison.id })
            if partner.is_adr_facturation:
                res['value'].update({'partner_invoice_id': partner.is_adr_facturation.id })
            if partner.is_adr_groupe:
                res['value'].update({'partner_group_id': partner.is_adr_groupe.id })
            else:
                res['value'].update({'partner_group_id': res['value']['partner_invoice_id'] })

        return res

is_sale_order_address()