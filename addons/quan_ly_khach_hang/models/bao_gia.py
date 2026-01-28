# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaoGia(models.Model):
    _name = 'bao_gia'
    _description = 'Báo Giá'
    _rec_name = 'ma_bao_gia'
    _order = 'ngay_tao desc'

    ma_bao_gia = fields.Char(string='Mã Báo Giá', required=True, copy=False, readonly=True, default='New')
    ten_bao_gia = fields.Char(string='Tiêu Đề Báo Giá')
    
    # === KHÁCH HÀNG ===
    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng', required=True, ondelete='cascade')
    lien_he_id = fields.Many2one('lien_he_khach_hang', string='Người Liên Hệ',
                                  domain="[('khach_hang_id', '=', khach_hang_id)]")
    co_hoi_id = fields.Many2one('co_hoi_ban_hang', string='Cơ Hội', ondelete='set null')
    
    # === NHÂN VIÊN ===
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên Bán Hàng', ondelete='set null')
    
    # === THỜI GIAN ===
    ngay_tao = fields.Datetime(string='Ngày Tạo', default=fields.Datetime.now, readonly=True)
    ngay_bao_gia = fields.Date(string='Ngày Báo Giá', default=fields.Date.today)
    ngay_hieu_luc = fields.Date(string='Hiệu Lực Đến')
    
    # === GIÁ TRỊ ===
    chi_tiet_ids = fields.One2many('bao_gia_chi_tiet', 'bao_gia_id', string='Chi Tiết Báo Giá')
    tong_tien = fields.Float(string='Tổng Tiền', compute='_compute_tong_tien', store=True, digits=(16, 0))
    chiet_khau_phan_tram = fields.Float(string='Chiết Khấu (%)', default=0)
    chiet_khau_tien = fields.Float(string='Chiết Khấu (VNĐ)', compute='_compute_chiet_khau', store=True, digits=(16, 0))
    thue_phan_tram = fields.Float(string='Thuế VAT (%)', default=10)
    thue_tien = fields.Float(string='Thuế (VNĐ)', compute='_compute_thue', store=True, digits=(16, 0))
    tong_thanh_toan = fields.Float(string='Tổng Thanh Toán', compute='_compute_tong_thanh_toan', store=True, digits=(16, 0))
    
    don_vi_tien = fields.Selection([
        ('VND', 'VNĐ'),
        ('USD', 'USD'),
    ], string='Đơn Vị Tiền', default='VND')
    
    # === TRẠNG THÁI ===
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('gui', 'Đã Gửi'),
        ('dam_phan', 'Đang Đàm Phán'),
        ('chap_nhan', 'Chấp Nhận'),
        ('tu_choi', 'Từ Chối'),
        ('het_han', 'Hết Hạn'),
    ], string='Trạng Thái', default='nhap', tracking=True)
    
    ly_do_tu_choi = fields.Text(string='Lý Do Từ Chối')
    
    # === ĐIỀU KHOẢN ===
    dieu_khoan_thanh_toan = fields.Text(string='Điều Khoản Thanh Toán')
    dieu_khoan_giao_hang = fields.Text(string='Điều Khoản Giao Hàng')
    bao_hanh = fields.Text(string='Bảo Hành')
    ghi_chu = fields.Text(string='Ghi Chú')
    
    # === FILE ===
    file_bao_gia = fields.Binary(string='File Báo Giá')
    file_bao_gia_name = fields.Char(string='Tên File')
    
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    _sql_constraints = [
        ('unique_ma_bao_gia', 'UNIQUE(ma_bao_gia)', 'Mã báo giá đã tồn tại!'),
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('ma_bao_gia', 'New') == 'New':
            vals['ma_bao_gia'] = self.env['ir.sequence'].next_by_code('bao_gia') or 'BG-NEW'
        return super(BaoGia, self).create(vals)
    
    @api.depends('chi_tiet_ids.thanh_tien')
    def _compute_tong_tien(self):
        for record in self:
            record.tong_tien = sum(record.chi_tiet_ids.mapped('thanh_tien'))
    
    @api.depends('tong_tien', 'chiet_khau_phan_tram')
    def _compute_chiet_khau(self):
        for record in self:
            record.chiet_khau_tien = record.tong_tien * record.chiet_khau_phan_tram / 100
    
    @api.depends('tong_tien', 'chiet_khau_tien', 'thue_phan_tram')
    def _compute_thue(self):
        for record in self:
            record.thue_tien = (record.tong_tien - record.chiet_khau_tien) * record.thue_phan_tram / 100
    
    @api.depends('tong_tien', 'chiet_khau_tien', 'thue_tien')
    def _compute_tong_thanh_toan(self):
        for record in self:
            record.tong_thanh_toan = record.tong_tien - record.chiet_khau_tien + record.thue_tien
    
    def action_gui(self):
        """Gửi báo giá cho khách hàng"""
        for record in self:
            record.trang_thai = 'gui'
            # Tạo tương tác
            self.env['tuong_tac_khach_hang'].create({
                'khach_hang_id': record.khach_hang_id.id,
                'co_hoi_id': record.co_hoi_id.id if record.co_hoi_id else False,
                'loai_tuong_tac': 'gui_bao_gia',
                'nhan_vien_id': record.nhan_vien_id.id if record.nhan_vien_id else False,
                'mo_ta': f'Gửi báo giá {record.ma_bao_gia} - Giá trị: {record.tong_thanh_toan:,.0f} {record.don_vi_tien}',
                'tao_cong_viec': True,
            })
    
    def action_chap_nhan(self):
        """Khách hàng chấp nhận báo giá"""
        for record in self:
            record.trang_thai = 'chap_nhan'
            if record.co_hoi_id:
                record.co_hoi_id.action_thang()
    
    def action_tu_choi(self):
        """Khách hàng từ chối báo giá"""
        for record in self:
            record.trang_thai = 'tu_choi'


class BaoGiaChiTiet(models.Model):
    _name = 'bao_gia_chi_tiet'
    _description = 'Chi Tiết Báo Giá'
    _order = 'sequence, id'

    bao_gia_id = fields.Many2one('bao_gia', string='Báo Giá', required=True, ondelete='cascade')
    sequence = fields.Integer(string='STT', default=10)
    
    ten_san_pham = fields.Char(string='Tên Sản Phẩm/Dịch Vụ', required=True)
    mo_ta = fields.Text(string='Mô Tả')
    
    don_vi = fields.Char(string='Đơn Vị', default='Cái')
    so_luong = fields.Float(string='Số Lượng', default=1)
    don_gia = fields.Float(string='Đơn Giá', digits=(16, 0))
    chiet_khau = fields.Float(string='Chiết Khấu (%)', default=0)
    
    thanh_tien = fields.Float(string='Thành Tiền', compute='_compute_thanh_tien', store=True, digits=(16, 0))
    
    @api.depends('so_luong', 'don_gia', 'chiet_khau')
    def _compute_thanh_tien(self):
        for record in self:
            subtotal = record.so_luong * record.don_gia
            record.thanh_tien = subtotal - (subtotal * record.chiet_khau / 100)
