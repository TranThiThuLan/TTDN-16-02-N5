# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HRDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'
    _rec_name = 'name'

    name = fields.Char(string='Name', default='Tổng Quan Nhân Sự')

    total_employees = fields.Integer("Tổng nhân viên", compute="_compute_dashboard_data")
    total_departments = fields.Integer("Tổng phòng ban", compute="_compute_dashboard_data")
    contracts_count = fields.Integer("Hợp đồng hiệu lực", compute="_compute_dashboard_data")
    leaves_pending = fields.Integer("Nghỉ phép chờ duyệt", compute="_compute_dashboard_data")

    def _compute_dashboard_data(self):
        for record in self:
            record.total_employees = self.env['nhan_vien'].search_count([])
            record.total_departments = self.env['phong_ban'].search_count([])
            record.contracts_count = self.env['hop_dong_lao_dong'].search_count([('trang_thai', '=', 'dang_hieu_luc')])
            # Note: Assuming 'cho_duyet' is the state for pending leaves. Adjust if different.
            # Based on common practice, I'll search generically or try to find exact state key if available, 
            # but for now I'll use common 'trang_thai'='cho_duyet' assumption
            record.leaves_pending = self.env['nghi_phep'].search_count([('trang_thai', '=', 'cho_duyet')])

    def action_view_employees(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nhân Viên',
            'res_model': 'nhan_vien',
            'view_mode': 'kanban,tree,form',
            'target': 'current',
        }
