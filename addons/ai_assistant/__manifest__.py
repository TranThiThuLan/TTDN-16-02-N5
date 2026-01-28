# -*- coding: utf-8 -*-
{
    'name': 'AI Assistant',
    'version': '15.0.1.0.0',
    'category': 'Tools',
    'summary': 'Trợ lý AI thông minh tích hợp OpenRouter',
    'description': '''
        Module AI Assistant - Tích hợp AI vào hệ thống Odoo
        ====================================================
        
        Tính năng:
        - Phân tích cơ hội bán hàng và đề xuất chiến lược
        - Hỗ trợ quản lý công việc, ước tính thời gian
        - Đánh giá nhân viên và gợi ý đào tạo
        - Chat với AI để hỏi đáp
        
        Sử dụng OpenRouter API với model Xiaomi MiMo
    ''',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base', 'quan_ly_nhan_su', 'quan_ly_cong_viec', 'quan_ly_khach_hang'],
    'data': [
        'security/ir.model.access.csv',
        'data/config_data.xml',
        'views/ai_config_view.xml',
        'views/ai_chat_view.xml',
        'views/co_hoi_inherit_view.xml',
        'views/cong_viec_inherit_view.xml',
        'views/nhan_vien_inherit_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
