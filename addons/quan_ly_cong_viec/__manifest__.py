# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Công Việc",

    'summary': """
        Module quản lý công việc và dự án""",

    'description': """
        Module Quản Lý Công Việc bao gồm:
        - Quản lý dự án
        - Quản lý công việc với mức độ ưu tiên và trạng thái
        - Nhật ký công việc
        - Đánh giá nhân viên
        - Liên kết với khách hàng (từ module quan_ly_khach_hang)
        - Dashboard tổng quan
    """,

    'author': "TTDN-15-03-N6",
    'website': "http://www.yourcompany.com",
    'category': 'Project',
    'version': '1.0',

    'depends': ['base', 'quan_ly_nhan_su'],

    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_data.xml',
        'views/dashboard_view.xml',
        'views/du_an_view.xml',
        'views/giai_doan_cong_viec_view.xml',
        'views/cong_viec_view.xml',
        'views/nhat_ky_cong_viec_view.xml',
        'views/tai_nguyen.xml',
        'views/danh_gia_nhan_vien_view.xml',
        'views/menu.xml',
        'demo/demo_data.xml',
    ],


    
    'installable': True,
    'application': True,
    'auto_install': False,
    
    'assets': {
        'web.assets_backend': [
            '/quan_ly_cong_viec/static/css/dashboard.css',
        ],
    },
}
