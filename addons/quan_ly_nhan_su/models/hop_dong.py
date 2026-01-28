# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp Đồng Lao Động'
    _rec_name = 'ma_hop_dong'
    _order = 'ngay_bat_dau desc'

    ma_hop_dong = fields.Char(string='Mã Hợp Đồng', required=True, copy=False)
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên', required=True, ondelete='cascade')
    
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Hợp đồng thử việc'),
        ('xac_dinh_thoi_han', 'Hợp đồng xác định thời hạn'),
        ('khong_thoi_han', 'Hợp đồng không xác định thời hạn'),
        ('thoi_vu', 'Hợp đồng thời vụ'),
        ('cong_tac_vien', 'Hợp đồng cộng tác viên'),
    ], string='Loại Hợp Đồng', required=True, default='thu_viec')
    
    ngay_bat_dau = fields.Date(string='Ngày Bắt Đầu', required=True)
    ngay_ket_thuc = fields.Date(string='Ngày Kết Thúc')
    thoi_han = fields.Integer(string='Thời Hạn (tháng)', compute='_compute_thoi_han', store=True)
    
    luong_co_ban = fields.Float(string='Lương Cơ Bản', digits=(16, 0))
    phu_cap = fields.Float(string='Phụ Cấp', digits=(16, 0))
    tong_luong = fields.Float(string='Tổng Lương', compute='_compute_tong_luong', store=True, digits=(16, 0))
    
    chuc_vu_id = fields.Many2one('chuc_vu', string='Chức Vụ')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng Ban')
    
    trang_thai = fields.Selection([
        ('moi', 'Mới tạo'),
        ('dang_hieu_luc', 'Đang hiệu lực'),
        ('sap_het_han', 'Sắp hết hạn'),
        ('het_han', 'Hết hạn'),
        ('cham_dut', 'Chấm dứt'),
    ], string='Trạng Thái', default='moi', compute='_compute_trang_thai', store=True, readonly=False)
    
    da_cham_dut = fields.Boolean(string='Đã Chấm Dứt', default=False)
    
    ghi_chu = fields.Text(string='Ghi Chú')
    file_hop_dong = fields.Binary(string='File Hợp Đồng')
    file_hop_dong_name = fields.Char(string='Tên File')
    
    nguoi_ky_id = fields.Many2one('nhan_vien', string='Người Ký (Đại diện công ty)')
    ngay_ky = fields.Date(string='Ngày Ký')
    
    _sql_constraints = [
        ('unique_ma_hop_dong', 'UNIQUE(ma_hop_dong)', 'Mã hợp đồng đã tồn tại!')
    ]
    
    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_thoi_han(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc:
                delta = record.ngay_ket_thuc - record.ngay_bat_dau
                record.thoi_han = delta.days // 30
            else:
                record.thoi_han = 0
    
    @api.depends('luong_co_ban', 'phu_cap')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = (record.luong_co_ban or 0) + (record.phu_cap or 0)
    
    @api.depends('ngay_bat_dau', 'ngay_ket_thuc', 'loai_hop_dong', 'da_cham_dut')
    def _compute_trang_thai(self):
        today = date.today()
        for record in self:
            # Kiểm tra nếu đã chấm dứt hợp đồng thủ công
            if record.da_cham_dut:
                record.trang_thai = 'cham_dut'
            elif not record.ngay_bat_dau:
                record.trang_thai = 'moi'
            elif record.ngay_bat_dau > today:
                record.trang_thai = 'moi'
            elif record.loai_hop_dong == 'khong_thoi_han':
                record.trang_thai = 'dang_hieu_luc'
            elif record.ngay_ket_thuc:
                if record.ngay_ket_thuc < today:
                    record.trang_thai = 'het_han'
                elif record.ngay_ket_thuc <= today + timedelta(days=30):
                    record.trang_thai = 'sap_het_han'
                else:
                    record.trang_thai = 'dang_hieu_luc'
            else:
                record.trang_thai = 'dang_hieu_luc'
    
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau:
                if record.ngay_ket_thuc < record.ngay_bat_dau:
                    raise ValidationError('Ngày kết thúc phải lớn hơn ngày bắt đầu!')
    
    @api.model
    def create(self, vals):
        if not vals.get('ma_hop_dong'):
            vals['ma_hop_dong'] = self.env['ir.sequence'].next_by_code('hop_dong_lao_dong') or 'HD-NEW'
        return super(HopDongLaoDong, self).create(vals)
    
    def action_cham_dut(self):
        """Chấm dứt hợp đồng"""
        for record in self:
            record.da_cham_dut = True
