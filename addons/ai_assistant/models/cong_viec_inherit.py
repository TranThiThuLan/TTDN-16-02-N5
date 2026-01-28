# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CongViecAI(models.Model):
    _inherit = 'cong_viec'

    ai_suggestion = fields.Text(string='Gợi ý từ AI', readonly=True)
    ai_suggestion_date = fields.Datetime(string='Ngày gợi ý', readonly=True)

    def action_ai_estimate(self):
        """Ước tính thời gian và gợi ý từ AI"""
        self.ensure_one()
        result = self.env['ai.service'].estimate_task_time(self)
        self.write({
            'ai_suggestion': result,
            'ai_suggestion_date': fields.Datetime.now()
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '🤖 Phân tích công việc hoàn tất',
                'message': 'Kết quả gợi ý đã được cập nhật trong tab AI Suggestion',
                'type': 'success',
                'sticky': False,
            }
        }
