# -*- coding: utf-8 -*-
from odoo import models, fields

class CongViecInherit(models.Model):
    """Kế thừa model cong_viec để thêm liên kết với khách hàng"""
    _inherit = 'cong_viec'
    
    # Thêm liên kết với khách hàng khi module quan_ly_khach_hang được cài đặt
    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng Liên Quan', ondelete='set null')
    co_hoi_id = fields.Many2one('co_hoi_ban_hang', string='Cơ Hội Bán Hàng', ondelete='set null',
                                 domain="[('khach_hang_id', '=', khach_hang_id)]")
