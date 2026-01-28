# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Khách Hàng",

    'summary': """
        Module quản lý khách hàng và hoạt động bán hàng""",

    'description': """
        Module Quản Lý Khách Hàng (CRM) bao gồm:
        - Quản lý thông tin khách hàng (cá nhân/doanh nghiệp)
        - Quản lý người liên hệ
        - Quản lý cơ hội bán hàng
        - Quản lý báo giá
        - Quản lý lịch hẹn
        - Lịch sử tương tác với khách hàng
        - Tự động tạo công việc từ hoạt động bán hàng
    """,

    'author': "TTDN-15-03-N6",
    'website': "http://www.yourcompany.com",
    'category': 'Sales/CRM',
    'version': '1.0',

    'depends': ['base', 'quan_ly_nhan_su', 'quan_ly_cong_viec'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/dashboard_data.xml',
        'views/khach_hang_view.xml',
        'views/lien_he_view.xml',
        'views/co_hoi_view.xml',
        'views/bao_gia_view.xml',
        'views/lich_hen_view.xml',
        'views/tuong_tac_view.xml',
        'views/cong_viec_inherit_view.xml',
        'views/dashboard_view.xml',
        'views/menu.xml',
        'demo/demo_data.xml',
    ],


    
    'installable': True,
    'application': True,
    'auto_install': False,
    
    'assets': {
        'web.assets_backend': [
            '/quan_ly_khach_hang/static/css/style.css',
        ],
    },
}
