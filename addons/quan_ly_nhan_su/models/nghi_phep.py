# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class NghiPhep(models.Model):
    _name = 'nghi_phep'
    _description = 'Đơn Xin Nghỉ Phép'
    _rec_name = 'ma_don'
    _order = 'ngay_tao desc'

    ma_don = fields.Char(string='Mã Đơn', required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên', required=True, ondelete='cascade')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng Ban', related='nhan_vien_id.phong_ban_id', store=True)
    
    loai_nghi = fields.Selection([
        ('nghi_phep_nam', 'Nghỉ phép năm'),
        ('nghi_om', 'Nghỉ ốm'),
        ('nghi_thai_san', 'Nghỉ thai sản'),
        ('nghi_cuoi', 'Nghỉ cưới'),
        ('nghi_tang', 'Nghỉ tang'),
        ('nghi_khong_luong', 'Nghỉ không lương'),
        ('nghi_khac', 'Nghỉ khác'),
    ], string='Loại Nghỉ', required=True, default='nghi_phep_nam')
    
    ngay_bat_dau = fields.Date(string='Ngày Bắt Đầu', required=True)
    ngay_ket_thuc = fields.Date(string='Ngày Kết Thúc', required=True)
    so_ngay = fields.Float(string='Số Ngày Nghỉ', compute='_compute_so_ngay', store=True)
    
    ly_do = fields.Text(string='Lý Do Nghỉ', required=True)
    
    nguoi_duyet_id = fields.Many2one('nhan_vien', string='Người Duyệt')
    ngay_duyet = fields.Date(string='Ngày Duyệt')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ Duyệt'),
        ('duyet', 'Đã Duyệt'),
        ('tu_choi', 'Từ Chối'),
        ('huy', 'Đã Hủy'),
    ], string='Trạng Thái', default='nhap', tracking=True)
    
    ghi_chu = fields.Text(string='Ghi Chú')
    ly_do_tu_choi = fields.Text(string='Lý Do Từ Chối')
    
    ngay_tao = fields.Datetime(string='Ngày Tạo', default=fields.Datetime.now, readonly=True)
    
    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_so_ngay(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc:
                delta = record.ngay_ket_thuc - record.ngay_bat_dau
                record.so_ngay = delta.days + 1  # Bao gồm cả ngày cuối
            else:
                record.so_ngay = 0
    
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc < record.ngay_bat_dau:
                raise ValidationError('Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu!')
    
    @api.model
    def create(self, vals):
        if vals.get('ma_don', 'New') == 'New':
            vals['ma_don'] = self.env['ir.sequence'].next_by_code('nghi_phep') or 'NP-NEW'
        return super(NghiPhep, self).create(vals)
    
    def action_gui_duyet(self):
        """Gửi đơn xin duyệt"""
        for record in self:
            record.trang_thai = 'cho_duyet'
    
    def action_duyet(self):
        """Duyệt đơn nghỉ phép"""
        for record in self:
            record.write({
                'trang_thai': 'duyet',
                'nguoi_duyet_id': self.env.user.employee_id.id if hasattr(self.env.user, 'employee_id') else False,
                'ngay_duyet': date.today(),
            })
    
    def action_tu_choi(self):
        """Từ chối đơn nghỉ phép"""
        for record in self:
            record.trang_thai = 'tu_choi'
    
    def action_huy(self):
        """Hủy đơn nghỉ phép"""
        for record in self:
            record.trang_thai = 'huy'
    
    def action_ve_nhap(self):
        """Đưa về trạng thái nháp"""
        for record in self:
            record.trang_thai = 'nhap'


class PhepNam(models.Model):
    _name = 'phep_nam'
    _description = 'Phép Năm Nhân Viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên', required=True, ondelete='cascade')
    nam = fields.Integer(string='Năm', required=True, default=lambda self: date.today().year)
    
    so_ngay_duoc_phep = fields.Float(string='Số Ngày Được Phép', default=12)
    so_ngay_da_nghi = fields.Float(string='Số Ngày Đã Nghỉ', compute='_compute_so_ngay_da_nghi', store=True)
    so_ngay_con_lai = fields.Float(string='Số Ngày Còn Lại', compute='_compute_so_ngay_con_lai', store=True)
    
    so_ngay_chuyen_tu_nam_truoc = fields.Float(string='Chuyển Từ Năm Trước', default=0)
    
    _sql_constraints = [
        ('unique_nhan_vien_nam', 'UNIQUE(nhan_vien_id, nam)', 'Mỗi nhân viên chỉ có 1 bản ghi phép năm cho mỗi năm!')
    ]
    
    @api.depends('nhan_vien_id', 'nam')
    def _compute_so_ngay_da_nghi(self):
        for record in self:
            nghi_phep = self.env['nghi_phep'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('loai_nghi', '=', 'nghi_phep_nam'),
                ('trang_thai', '=', 'duyet'),
                ('ngay_bat_dau', '>=', f'{record.nam}-01-01'),
                ('ngay_ket_thuc', '<=', f'{record.nam}-12-31'),
            ])
            record.so_ngay_da_nghi = sum(nghi_phep.mapped('so_ngay'))
    
    @api.depends('so_ngay_duoc_phep', 'so_ngay_da_nghi', 'so_ngay_chuyen_tu_nam_truoc')
    def _compute_so_ngay_con_lai(self):
        for record in self:
            record.so_ngay_con_lai = record.so_ngay_duoc_phep + record.so_ngay_chuyen_tu_nam_truoc - record.so_ngay_da_nghi
