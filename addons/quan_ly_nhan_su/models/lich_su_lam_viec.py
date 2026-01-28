# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LichSuLamViec(models.Model):
    _name = 'lich_su_lam_viec'
    _description = 'Bảng chứa thông tin Lịch sử làm việc'
    _rec_name = 'ten_lich_su'
    _order = 'ngay_bat_dau desc'

    ten_lich_su = fields.Char(string="Tên Công Việc/Vị Trí")
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân Viên", ondelete='cascade', required=True)
    
    # Thông tin công ty/tổ chức
    ten_cong_ty = fields.Char(string="Tên Công Ty/Tổ Chức")
    dia_chi_cong_ty = fields.Char(string="Địa Chỉ Công Ty")
    
    # Thời gian
    ngay_bat_dau = fields.Date(string="Ngày Bắt Đầu")
    ngay_ket_thuc = fields.Date(string="Ngày Kết Thúc")
    dang_lam = fields.Boolean(string="Đang Làm", help="Đánh dấu nếu vẫn đang làm việc tại đây")
    
    # Vị trí & Chức vụ
    chuc_vu = fields.Char(string="Chức Vụ")
    phong_ban = fields.Char(string="Phòng Ban")
    
    # Mô tả công việc
    mo_ta_cong_viec = fields.Text(string="Mô Tả Công Việc")
    thanh_tuu = fields.Text(string="Thành Tựu Đạt Được")
    
    # Lương
    muc_luong = fields.Float(string="Mức Lương", digits=(16, 0))
    
    # Lý do nghỉ
    ly_do_nghi = fields.Text(string="Lý Do Nghỉ Việc")
    
    # Người tham chiếu
    nguoi_tham_chieu = fields.Char(string="Người Tham Chiếu")
    sdt_tham_chieu = fields.Char(string="SĐT Người Tham Chiếu")
    
    loai_lich_su = fields.Selection([
        ('trong_cong_ty', 'Trong Công Ty'),
        ('ngoai_cong_ty', 'Trước Khi Vào Công Ty'),
    ], string="Loại", default='ngoai_cong_ty')
    
    @api.onchange('dang_lam')
    def _onchange_dang_lam(self):
        if self.dang_lam:
            self.ngay_ket_thuc = False
            self.ly_do_nghi = False
