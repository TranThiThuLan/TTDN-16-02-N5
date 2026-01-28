# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CoHoiBanHang(models.Model):
    _name = 'co_hoi_ban_hang'
    _description = 'Cơ Hội Bán Hàng'
    _rec_name = 'ten_co_hoi'
    _order = 'xac_suat desc, gia_tri_du_kien desc'

    ma_co_hoi = fields.Char(string='Mã Cơ Hội', required=True, copy=False, readonly=True, default='New')
    ten_co_hoi = fields.Char(string='Tên Cơ Hội', required=True)
    
    # === KHÁCH HÀNG ===
    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng', required=True, ondelete='cascade')
    lien_he_id = fields.Many2one('lien_he_khach_hang', string='Người Liên Hệ', 
                                  domain="[('khach_hang_id', '=', khach_hang_id)]")
    
    # === NHÂN VIÊN ===
    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string='Nhân Viên Phụ Trách', ondelete='set null')
    doi_ban_hang_ids = fields.Many2many('nhan_vien', 'co_hoi_nhan_vien_rel', 'co_hoi_id', 'nhan_vien_id', 
                                         string='Đội Bán Hàng')
    
    # === GIÁ TRỊ ===
    gia_tri_du_kien = fields.Float(string='Giá Trị Dự Kiến', digits=(16, 0))
    xac_suat = fields.Integer(string='Xác Suất (%)', default=10)
    gia_tri_ky_vong = fields.Float(string='Giá Trị Kỳ Vọng', compute='_compute_gia_tri_ky_vong', store=True)
    
    # === THỜI GIAN ===
    ngay_tao = fields.Datetime(string='Ngày Tạo', default=fields.Datetime.now, readonly=True)
    ngay_du_kien_dong = fields.Date(string='Dự Kiến Đóng')
    ngay_dong = fields.Date(string='Ngày Đóng Thực Tế')
    
    # === TRẠNG THÁI ===
    giai_doan = fields.Selection([
        ('moi', 'Mới'),
        ('lien_he', 'Đã Liên Hệ'),
        ('trinh_bay', 'Trình Bày Giải Pháp'),
        ('bao_gia', 'Gửi Báo Giá'),
        ('dam_phan', 'Đàm Phán'),
        ('thang', 'Thắng'),
        ('thua', 'Thua'),
    ], string='Giai Đoạn', default='moi', tracking=True)
    
    ly_do_that_bai = fields.Selection([
        ('gia_cao', 'Giá cao'),
        ('doi_thu', 'Đối thủ cạnh tranh'),
        ('khong_nhu_cau', 'Không có nhu cầu'),
        ('ngan_sach', 'Không đủ ngân sách'),
        ('thoi_gian', 'Thời gian không phù hợp'),
        ('khac', 'Khác'),
    ], string='Lý Do Thất Bại')
    chi_tiet_ly_do = fields.Text(string='Chi Tiết Lý Do')
    
    # === NGUỒN ===
    nguon_co_hoi = fields.Selection([
        ('website', 'Website'),
        ('quang_cao', 'Quảng Cáo'),
        ('gioi_thieu', 'Giới Thiệu'),
        ('su_kien', 'Sự Kiện'),
        ('cold_call', 'Cold Call'),
        ('khac', 'Khác'),
    ], string='Nguồn')
    
    doi_thu = fields.Char(string='Đối Thủ Cạnh Tranh')
    
    # === MÔ TẢ ===
    mo_ta = fields.Text(string='Mô Tả')
    nhu_cau = fields.Text(string='Nhu Cầu Khách Hàng')
    giai_phap_de_xuat = fields.Text(string='Giải Pháp Đề Xuất')
    
    # === QUAN HỆ ===
    bao_gia_ids = fields.One2many('bao_gia', 'co_hoi_id', string='Báo Giá')
    tuong_tac_ids = fields.One2many('tuong_tac_khach_hang', 'co_hoi_id', string='Tương Tác')
    cong_viec_ids = fields.One2many('cong_viec', 'co_hoi_id', string='Công Việc Liên Quan')
    
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    _sql_constraints = [
        ('unique_ma_co_hoi', 'UNIQUE(ma_co_hoi)', 'Mã cơ hội đã tồn tại!'),
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('ma_co_hoi', 'New') == 'New':
            vals['ma_co_hoi'] = self.env['ir.sequence'].next_by_code('co_hoi_ban_hang') or 'CH-NEW'
        return super(CoHoiBanHang, self).create(vals)
    
    @api.depends('gia_tri_du_kien', 'xac_suat')
    def _compute_gia_tri_ky_vong(self):
        for record in self:
            record.gia_tri_ky_vong = record.gia_tri_du_kien * record.xac_suat / 100
    
    @api.constrains('xac_suat')
    def _check_xac_suat(self):
        for record in self:
            if record.xac_suat < 0 or record.xac_suat > 100:
                raise ValidationError('Xác suất phải nằm trong khoảng 0-100%!')
    
    @api.onchange('giai_doan')
    def _onchange_giai_doan(self):
        """Tự động cập nhật xác suất theo giai đoạn"""
        xac_suat_map = {
            'moi': 10,
            'lien_he': 20,
            'trinh_bay': 40,
            'bao_gia': 60,
            'dam_phan': 80,
            'thang': 100,
            'thua': 0,
        }
        if self.giai_doan:
            self.xac_suat = xac_suat_map.get(self.giai_doan, 10)
    
    def action_thang(self):
        """Đánh dấu cơ hội thắng"""
        for record in self:
            record.write({
                'giai_doan': 'thang',
                'xac_suat': 100,
                'ngay_dong': fields.Date.today(),
            })
            # Cập nhật nhóm khách hàng
            record.khach_hang_id.nhom_khach_hang = 'than_thiet'
    
    def action_thua(self):
        """Đánh dấu cơ hội thua"""
        for record in self:
            record.write({
                'giai_doan': 'thua',
                'xac_suat': 0,
                'ngay_dong': fields.Date.today(),
            })
    
    def action_tao_bao_gia(self):
        """Tạo báo giá từ cơ hội"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo Báo Giá',
            'res_model': 'bao_gia',
            'view_mode': 'form',
            'context': {
                'default_khach_hang_id': self.khach_hang_id.id,
                'default_co_hoi_id': self.id,
                'default_lien_he_id': self.lien_he_id.id,
                'default_nhan_vien_id': self.nhan_vien_phu_trach_id.id,
            },
        }
