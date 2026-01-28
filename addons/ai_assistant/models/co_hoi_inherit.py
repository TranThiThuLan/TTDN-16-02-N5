# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoHoiBanHangAI(models.Model):
    _inherit = 'co_hoi_ban_hang'

    ai_analysis = fields.Text(string='Phân tích AI', readonly=True)
    ai_analysis_date = fields.Datetime(string='Ngày phân tích', readonly=True)

    def action_ai_analyze(self):
        """Phân tích cơ hội bán hàng bằng AI"""
        self.ensure_one()
        result = self.env['ai.service'].analyze_opportunity(self)
        self.write({
            'ai_analysis': result,
            'ai_analysis_date': fields.Datetime.now()
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '🤖 Phân tích AI hoàn tất',
                'message': 'Kết quả phân tích đã được cập nhật trong tab AI Analysis',
                'type': 'success',
                'sticky': False,
            }
        }
