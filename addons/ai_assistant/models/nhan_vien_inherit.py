# -*- coding: utf-8 -*-
from odoo import models, fields, api

class NhanVienAI(models.Model):
    _inherit = 'nhan_vien'

    ai_evaluation = fields.Text(string='Đánh giá từ AI', readonly=True)
    ai_evaluation_date = fields.Datetime(string='Ngày đánh giá', readonly=True)

    def action_ai_evaluate(self):
        """Đánh giá và gợi ý phát triển từ AI"""
        self.ensure_one()
        result = self.env['ai.service'].evaluate_employee(self)
        self.write({
            'ai_evaluation': result,
            'ai_evaluation_date': fields.Datetime.now()
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '🤖 Đánh giá AI hoàn tất',
                'message': 'Kết quả đánh giá đã được cập nhật trong tab AI Evaluation',
                'type': 'success',
                'sticky': False,
            }
        }
