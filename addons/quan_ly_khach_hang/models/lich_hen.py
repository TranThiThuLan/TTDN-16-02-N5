# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta

class LichHen(models.Model):
    _name = 'lich_hen'
    _description = 'Lịch Hẹn Khách Hàng'
    _rec_name = 'tieu_de'
    _order = 'ngay_hen desc'

    tieu_de = fields.Char(string='Tiêu Đề', required=True)
    
    # === KHÁCH HÀNG ===
    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng', required=True, ondelete='cascade')
    lien_he_id = fields.Many2one('lien_he_khach_hang', string='Người Liên Hệ',
                                  domain="[('khach_hang_id', '=', khach_hang_id)]")
    co_hoi_id = fields.Many2one('co_hoi_ban_hang', string='Cơ Hội Liên Quan',
                                 domain="[('khach_hang_id', '=', khach_hang_id)]")
    
    # === NHÂN VIÊN ===
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên Phụ Trách', ondelete='set null')
    nguoi_tham_gia_ids = fields.Many2many('nhan_vien', 'lich_hen_nhan_vien_rel', 'lich_hen_id', 'nhan_vien_id',
                                           string='Người Tham Gia')
    
    # === THỜI GIAN ===
    ngay_hen = fields.Datetime(string='Thời Gian Hẹn', required=True)
    thoi_luong = fields.Float(string='Thời Lượng (giờ)', default=1)
    ngay_ket_thuc = fields.Datetime(string='Thời Gian Kết Thúc', compute='_compute_ngay_ket_thuc', store=True)
    
    # === ĐỊA ĐIỂM ===
    loai_cuoc_hen = fields.Selection([
        ('truc_tiep', 'Gặp Trực Tiếp'),
        ('online', 'Họp Online'),
        ('dien_thoai', 'Gọi Điện'),
    ], string='Loại Cuộc Hẹn', default='truc_tiep')
    
    dia_diem = fields.Char(string='Địa Điểm')
    link_meeting = fields.Char(string='Link Meeting', help='Link Zoom/Google Meet/Teams')
    
    # === TRẠNG THÁI ===
    trang_thai = fields.Selection([
        ('du_kien', 'Dự Kiến'),
        ('xac_nhan', 'Đã Xác Nhận'),
        ('hoan_thanh', 'Hoàn Thành'),
        ('huy', 'Đã Hủy'),
        ('doi_lich', 'Đã Đổi Lịch'),
    ], string='Trạng Thái', default='du_kien', tracking=True)
    
    # === MỤC ĐÍCH ===
    muc_dich = fields.Selection([
        ('gioi_thieu', 'Giới Thiệu Sản Phẩm'),
        ('demo', 'Demo Sản Phẩm'),
        ('dam_phan', 'Đàm Phán Hợp Đồng'),
        ('ho_tro', 'Hỗ Trợ Kỹ Thuật'),
        ('bao_tri', 'Bảo Trì'),
        ('khac', 'Khác'),
    ], string='Mục Đích')
    
    # === MÔ TẢ ===
    mo_ta = fields.Text(string='Mô Tả')
    noi_dung_cuoc_hop = fields.Text(string='Nội Dung Cuộc Họp')
    ket_luan = fields.Text(string='Kết Luận')
    buoc_tiep_theo = fields.Text(string='Bước Tiếp Theo')
    
    # === GHI CHÚ ===
    ghi_chu = fields.Text(string='Ghi Chú')
    
    # === NHẮC NHỞ ===
    nhac_truoc = fields.Integer(string='Nhắc Trước (phút)', default=30)
    da_nhac = fields.Boolean(string='Đã Nhắc', default=False)
    
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    @api.depends('ngay_hen', 'thoi_luong')
    def _compute_ngay_ket_thuc(self):
        for record in self:
            if record.ngay_hen and record.thoi_luong:
                record.ngay_ket_thuc = record.ngay_hen + timedelta(hours=record.thoi_luong)
            else:
                record.ngay_ket_thuc = record.ngay_hen
    
    def action_xac_nhan(self):
        """Xác nhận lịch hẹn"""
        for record in self:
            record.trang_thai = 'xac_nhan'
            # Tạo tương tác
            self.env['tuong_tac_khach_hang'].create({
                'khach_hang_id': record.khach_hang_id.id,
                'co_hoi_id': record.co_hoi_id.id if record.co_hoi_id else False,
                'loai_tuong_tac': 'lich_hen',
                'nhan_vien_id': record.nhan_vien_id.id if record.nhan_vien_id else False,
                'mo_ta': f'Lịch hẹn: {record.tieu_de} - {record.ngay_hen.strftime("%d/%m/%Y %H:%M")}',
                'tao_cong_viec': True,
            })
    
    def action_hoan_thanh(self):
        """Đánh dấu hoàn thành"""
        for record in self:
            record.trang_thai = 'hoan_thanh'
    
    def action_huy(self):
        """Hủy lịch hẹn"""
        for record in self:
            record.trang_thai = 'huy'
