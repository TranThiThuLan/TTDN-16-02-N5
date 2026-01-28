# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AIChat(models.Model):
    _name = 'ai.chat'
    _description = 'Lịch sử chat với AI'
    _order = 'create_date desc'
    _rec_name = 'tieu_de'

    tieu_de = fields.Char(string='Tiêu đề', compute='_compute_tieu_de', store=True)
    user_id = fields.Many2one('res.users', string='Người dùng', default=lambda self: self.env.user)
    message_ids = fields.One2many('ai.chat.message', 'chat_id', string='Tin nhắn')
    
    # Quick input
    quick_message = fields.Text(string='Nhập câu hỏi')
    
    @api.depends('message_ids', 'create_date')
    def _compute_tieu_de(self):
        for record in self:
            if record.message_ids:
                first_msg = record.message_ids.sorted('create_date')[0] if record.message_ids else None
                if first_msg:
                    record.tieu_de = first_msg.content[:50] + '...' if len(first_msg.content) > 50 else first_msg.content
                else:
                    record.tieu_de = f"Chat {record.id}"
            else:
                record.tieu_de = f"Cuộc hội thoại mới"

    def action_send_message(self):
        """Gửi tin nhắn và nhận phản hồi AI"""
        self.ensure_one()
        if not self.quick_message:
            return
        
        # Tạo tin nhắn user
        self.env['ai.chat.message'].create({
            'chat_id': self.id,
            'role': 'user',
            'content': self.quick_message
        })
        
        # Gọi AI
        ai_response = self.env['ai.service'].call_ai(self.quick_message)
        
        # Tạo tin nhắn AI
        self.env['ai.chat.message'].create({
            'chat_id': self.id,
            'role': 'assistant', 
            'content': ai_response
        })
        
        # Xóa input
        self.quick_message = False
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.chat',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_new_chat(self):
        """Tạo cuộc hội thoại mới"""
        new_chat = self.create({})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.chat',
            'res_id': new_chat.id,
            'view_mode': 'form',
            'target': 'current',
        }


class AIChatMessage(models.Model):
    _name = 'ai.chat.message'
    _description = 'Tin nhắn chat AI'
    _order = 'create_date asc'

    chat_id = fields.Many2one('ai.chat', string='Cuộc hội thoại', ondelete='cascade')
    role = fields.Selection([
        ('user', 'Người dùng'),
        ('assistant', 'AI Assistant'),
        ('system', 'Hệ thống')
    ], string='Vai trò', required=True)
    content = fields.Text(string='Nội dung', required=True)
    create_date = fields.Datetime(string='Thời gian', readonly=True)
