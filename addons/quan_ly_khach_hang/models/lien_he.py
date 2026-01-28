# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LienHeKhachHang(models.Model):
    _name = 'lien_he_khach_hang'
    _description = 'Người Liên Hệ'
    _rec_name = 'ho_ten'
    _order = 'la_lien_he_chinh desc, ho_ten'

    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng', required=True, ondelete='cascade')
    
    # === THÔNG TIN CÁ NHÂN ===
    ho_ten = fields.Char(string='Họ Tên', required=True)
    chuc_danh = fields.Char(string='Chức Danh')
    phong_ban = fields.Char(string='Phòng Ban')
    
    anh_dai_dien = fields.Binary(string='Ảnh Đại Diện', attachment=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
    ], string='Giới Tính')
    
    # === THÔNG TIN LIÊN HỆ ===
    email = fields.Char(string='Email')
    dien_thoai = fields.Char(string='Điện Thoại')
    dien_thoai_di_dong = fields.Char(string='Di Động')
    
    # === MỨC ĐỘ ẢNH HƯỞNG ===
    la_lien_he_chinh = fields.Boolean(string='Là Liên Hệ Chính', default=False)
    muc_do_anh_huong = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung Bình'),
        ('cao', 'Cao'),
        ('quyet_dinh', 'Quyết Định'),
    ], string='Mức Độ Ảnh Hưởng', default='trung_binh')
    
    # === GHI CHÚ ===
    thong_tin_bo_sung = fields.Text(string='Thông Tin Bổ Sung')
    ghi_chu = fields.Text(string='Ghi Chú')
    
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    @api.onchange('la_lien_he_chinh')
    def _onchange_la_lien_he_chinh(self):
        """Nếu đánh dấu là liên hệ chính, tự động set mức ảnh hưởng cao"""
        if self.la_lien_he_chinh:
            self.muc_do_anh_huong = 'cao'
