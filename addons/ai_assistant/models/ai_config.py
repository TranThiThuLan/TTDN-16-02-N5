# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AIConfig(models.Model):
    _name = 'ai.config'
    _description = 'Cấu hình AI Assistant'
    _rec_name = 'name'

    name = fields.Char(string='Tên cấu hình', default='OpenRouter Config')
    api_key = fields.Char(string='API Key', required=True, help='API Key từ OpenRouter')
    model_name = fields.Char(string='Model', default='xiaomi/mimo-v2-flash:free', 
                             help='Tên model AI sử dụng')
    api_url = fields.Char(string='API URL', default='https://openrouter.ai/api/v1/chat/completions')
    max_tokens = fields.Integer(string='Max Tokens', default=2000)
    temperature = fields.Float(string='Temperature', default=0.7)
    active = fields.Boolean(string='Hoạt động', default=True)
    
    @api.model
    def get_config(self):
        """Lấy cấu hình AI đang hoạt động"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            return False
        return config
