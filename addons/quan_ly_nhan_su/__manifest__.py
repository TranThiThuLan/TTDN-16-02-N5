# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Nhân Sự",

    'summary': """
        Module quản lý nhân sự toàn diện cho doanh nghiệp""",

    'description': """
        Module Quản Lý Nhân Sự bao gồm:
        - Quản lý thông tin nhân viên
        - Quản lý phòng ban, chức vụ
        - Quản lý hợp đồng lao động
        - Quản lý nghỉ phép, phép năm
        - Quản lý lịch sử làm việc
    """,

    'author': "TTDN-15-03-N6",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_data.xml',
        'views/chuc_vu.xml',
        'views/phong_ban_view.xml',
        'views/nhom_du_an_view.xml',
        'views/nhan_vien_view.xml',
        'views/hop_dong_view.xml',
        'views/nghi_phep_view.xml',
        'views/lich_su_lam_viec_view.xml',
        'views/dashboard_view.xml',
        'views/menu.xml',
        'demo/demo_data.xml',
    ],



    
    'installable': True,
    'application': True,
    'auto_install': False,
    
    'assets': {
        'web.assets_backend': [
            '/quan_ly_nhan_su/static/css/style.css',
        ],
    },
}
