# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CRMDashboard(models.Model):
    _name = 'crm.dashboard'
    _description = 'CRM Dashboard'
    _rec_name = 'name'

    name = fields.Char(string='Name', default='Tổng Quan Kinh Doanh')

    total_customers = fields.Integer("Tổng khách hàng", compute="_compute_dashboard_data")
    total_opportunities = fields.Integer("Tổng cơ hội", compute="_compute_dashboard_data")
    won_opportunities = fields.Integer("Cơ hội thành công", compute="_compute_dashboard_data")
    expected_revenue = fields.Float("Doanh thu dự kiến", compute="_compute_dashboard_data")
    
    pending_quotes = fields.Integer("Báo giá đang xử lý", compute="_compute_dashboard_data")
    
    def _compute_dashboard_data(self):
        for record in self:
            record.total_customers = self.env['khach_hang'].search_count([])
            record.total_opportunities = self.env['co_hoi_ban_hang'].search_count([])
            record.won_opportunities = self.env['co_hoi_ban_hang'].search_count([('giai_doan', '=', 'thanh_cong')])
            record.pending_quotes = self.env['bao_gia'].search_count([('trang_thai', 'in', ['moi', 'gui_khach'])])
            
            # Tính tổng doanh thu dự kiến (ví dụ: tổng giá trị cơ hội)
            opps = self.env['co_hoi_ban_hang'].search([])
            record.expected_revenue = sum(opp.gia_tri_du_kien for opp in opps)
