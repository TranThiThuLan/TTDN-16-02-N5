# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Phòng Ban'
    _rec_name = 'ten_phong_ban'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'thu_tu, ten_phong_ban'

    ten_phong_ban = fields.Char(string='Tên Phòng Ban', required=True)
    ma_phong_ban = fields.Char(string='Mã Phòng Ban')
    mo_ta = fields.Text(string='Mô Tả')
    
    parent_id = fields.Many2one('phong_ban', string='Phòng Ban Cha', ondelete='restrict', index=True)
    child_ids = fields.One2many('phong_ban', 'parent_id', string='Phòng Ban Con')
    parent_path = fields.Char(index=True, unaccent=False)
    
    truong_phong_id = fields.Many2one('nhan_vien', string='Trưởng Phòng', ondelete='set null')
    nhan_vien_ids = fields.One2many('nhan_vien', 'phong_ban_id', string='Nhân Viên')
    
    so_nhan_vien = fields.Integer(string='Số Nhân Viên', compute='_compute_so_nhan_vien', store=True)
    thu_tu = fields.Integer(string='Thứ Tự', default=10)
    
    active = fields.Boolean(string='Hoạt Động', default=True)
    
    email = fields.Char(string='Email Phòng Ban')
    dien_thoai = fields.Char(string='Điện Thoại')
    
    _sql_constraints = [
        ('unique_ma_phong_ban', 'UNIQUE(ma_phong_ban)', 'Mã phòng ban đã tồn tại!')
    ]
    
    @api.depends('nhan_vien_ids')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = len(record.nhan_vien_ids)
    
    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise models.ValidationError('Không thể tạo phòng ban có cấu trúc vòng lặp!')
    
    def name_get(self):
        result = []
        for record in self:
            name = record.ten_phong_ban
            if record.parent_id:
                name = f"{record.parent_id.ten_phong_ban} / {name}"
            result.append((record.id, name))
        return result
    
    def toggle_active(self):
        """Toggle active status"""
        for record in self:
            record.active = not record.active
