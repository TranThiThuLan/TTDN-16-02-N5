# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách Hàng'
    _rec_name = 'ten_khach_hang'
    _order = 'ten_khach_hang'

    # === THÔNG TIN CƠ BẢN ===
    ma_khach_hang = fields.Char(string='Mã Khách Hàng', required=True, copy=False, readonly=True, default='New')
    ten_khach_hang = fields.Char(string='Tên Khách Hàng', required=True)
    
    loai_khach_hang = fields.Selection([
        ('ca_nhan', 'Cá Nhân'),
        ('doanh_nghiep', 'Doanh Nghiệp'),
    ], string='Loại Khách Hàng', default='doanh_nghiep', required=True)
    
    anh_dai_dien = fields.Binary(string='Ảnh/Logo', attachment=True)
    
    # === THÔNG TIN DOANH NGHIỆP ===
    ma_so_thue = fields.Char(string='Mã Số Thuế')
    website = fields.Char(string='Website')
    linh_vuc_kinh_doanh = fields.Char(string='Lĩnh Vực Kinh Doanh')
    quy_mo = fields.Selection([
        ('nho', 'Nhỏ (< 50 nhân viên)'),
        ('vua', 'Vừa (50-200 nhân viên)'),
        ('lon', 'Lớn (> 200 nhân viên)'),
    ], string='Quy Mô')
    
    # === THÔNG TIN LIÊN HỆ ===
    email = fields.Char(string='Email')
    dien_thoai = fields.Char(string='Điện Thoại')
    fax = fields.Char(string='Fax')
    dia_chi = fields.Text(string='Địa Chỉ')
    thanh_pho = fields.Char(string='Thành Phố')
    quoc_gia_id = fields.Many2one('res.country', string='Quốc Gia')
    
    # === THÔNG TIN NGÂN HÀNG ===
    so_tai_khoan = fields.Char(string='Số Tài Khoản')
    ten_ngan_hang = fields.Char(string='Tên Ngân Hàng')
    chi_nhanh = fields.Char(string='Chi Nhánh')
    
    # === PHÂN LOẠI ===
    nhom_khach_hang = fields.Selection([
        ('tiem_nang', 'Tiềm Năng'),
        ('moi', 'Mới'),
        ('than_thiet', 'Thân Thiết'),
        ('vip', 'VIP'),
        ('khong_hoat_dong', 'Không Hoạt Động'),
    ], string='Nhóm Khách Hàng', default='tiem_nang')
    
    nguon_khach_hang = fields.Selection([
        ('website', 'Website'),
        ('quang_cao', 'Quảng Cáo'),
        ('gioi_thieu', 'Giới Thiệu'),
        ('su_kien', 'Sự Kiện'),
        ('cold_call', 'Cold Call'),
        ('khac', 'Khác'),
    ], string='Nguồn Khách Hàng')
    
    # === NHÂN VIÊN PHỤ TRÁCH ===
    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string='Nhân Viên Phụ Trách', ondelete='set null')
    
    # === QUAN HỆ ===
    lien_he_ids = fields.One2many('lien_he_khach_hang', 'khach_hang_id', string='Người Liên Hệ')
    co_hoi_ids = fields.One2many('co_hoi_ban_hang', 'khach_hang_id', string='Cơ Hội Bán Hàng')
    bao_gia_ids = fields.One2many('bao_gia', 'khach_hang_id', string='Báo Giá')
    lich_hen_ids = fields.One2many('lich_hen', 'khach_hang_id', string='Lịch Hẹn')
    tuong_tac_ids = fields.One2many('tuong_tac_khach_hang', 'khach_hang_id', string='Lịch Sử Tương Tác')
    
    # === THỐNG KÊ ===
    so_co_hoi = fields.Integer(string='Số Cơ Hội', compute='_compute_thong_ke', store=True)
    tong_gia_tri_co_hoi = fields.Float(string='Tổng Giá Trị Cơ Hội', compute='_compute_thong_ke', store=True)
    so_bao_gia = fields.Integer(string='Số Báo Giá', compute='_compute_thong_ke', store=True)
    
    # === GHI CHÚ ===
    ghi_chu = fields.Text(string='Ghi Chú')
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    ngay_tao = fields.Datetime(string='Ngày Tạo', default=fields.Datetime.now, readonly=True)
    ngay_cap_nhat = fields.Datetime(string='Cập Nhật Lần Cuối', readonly=True)
    
    _sql_constraints = [
        ('unique_ma_khach_hang', 'UNIQUE(ma_khach_hang)', 'Mã khách hàng đã tồn tại!'),
        ('unique_ma_so_thue', 'UNIQUE(ma_so_thue)', 'Mã số thuế đã tồn tại!'),
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('ma_khach_hang', 'New') == 'New':
            vals['ma_khach_hang'] = self.env['ir.sequence'].next_by_code('khach_hang') or 'KH-NEW'
        return super(KhachHang, self).create(vals)
    
    def write(self, vals):
        vals['ngay_cap_nhat'] = fields.Datetime.now()
        return super(KhachHang, self).write(vals)
    
    @api.depends('co_hoi_ids', 'bao_gia_ids')
    def _compute_thong_ke(self):
        for record in self:
            record.so_co_hoi = len(record.co_hoi_ids)
            record.tong_gia_tri_co_hoi = sum(record.co_hoi_ids.mapped('gia_tri_du_kien'))
            record.so_bao_gia = len(record.bao_gia_ids)
    
    def action_xem_co_hoi(self):
        """Mở danh sách cơ hội của khách hàng"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cơ Hội Bán Hàng',
            'res_model': 'co_hoi_ban_hang',
            'view_mode': 'tree,form',
            'domain': [('khach_hang_id', '=', self.id)],
            'context': {'default_khach_hang_id': self.id},
        }
    
    def action_tao_tuong_tac(self):
        """Tạo tương tác mới"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ghi Nhận Tương Tác',
            'res_model': 'tuong_tac_khach_hang',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_khach_hang_id': self.id},
        }
