# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TuongTacKhachHang(models.Model):
    _name = 'tuong_tac_khach_hang'
    _description = 'Lịch Sử Tương Tác Khách Hàng'
    _rec_name = 'loai_tuong_tac'
    _order = 'ngay_tuong_tac desc'

    # === KHÁCH HÀNG ===
    khach_hang_id = fields.Many2one('khach_hang', string='Khách Hàng', required=True, ondelete='cascade')
    lien_he_id = fields.Many2one('lien_he_khach_hang', string='Người Liên Hệ',
                                  domain="[('khach_hang_id', '=', khach_hang_id)]")
    co_hoi_id = fields.Many2one('co_hoi_ban_hang', string='Cơ Hội Liên Quan',
                                 domain="[('khach_hang_id', '=', khach_hang_id)]")
    
    # === NHÂN VIÊN ===
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân Viên Thực Hiện', ondelete='set null')
    
    # === LOẠI TƯƠNG TÁC ===
    loai_tuong_tac = fields.Selection([
        ('goi_dien', 'Gọi Điện'),
        ('email', 'Gửi Email'),
        ('gap_mat', 'Gặp Mặt'),
        ('lich_hen', 'Lịch Hẹn'),
        ('gui_bao_gia', 'Gửi Báo Giá'),
        ('demo', 'Demo Sản Phẩm'),
        ('ho_tro', 'Hỗ Trợ'),
        ('khieu_nai', 'Khiếu Nại'),
        ('khac', 'Khác'),
    ], string='Loại Tương Tác', required=True)
    
    # === THỜI GIAN ===
    ngay_tuong_tac = fields.Datetime(string='Thời Gian', default=fields.Datetime.now, required=True)
    thoi_luong = fields.Integer(string='Thời Lượng (phút)', default=15)
    
    # === KẾT QUẢ ===
    ket_qua = fields.Selection([
        ('thanh_cong', 'Thành Công'),
        ('can_theo_doi', 'Cần Theo Dõi'),
        ('khong_lien_lac_duoc', 'Không Liên Lạc Được'),
        ('tu_choi', 'Từ Chối'),
        ('chua_xac_dinh', 'Chưa Xác Định'),
    ], string='Kết Quả', default='chua_xac_dinh')
    
    # === MÔ TẢ ===
    mo_ta = fields.Text(string='Mô Tả')
    noi_dung_trao_doi = fields.Text(string='Nội Dung Trao Đổi')
    buoc_tiep_theo = fields.Text(string='Bước Tiếp Theo')
    
    # === TẠO CÔNG VIỆC ===
    tao_cong_viec = fields.Boolean(string='Tạo Công Việc', default=False)
    cong_viec_id = fields.Many2one('cong_viec', string='Công Việc Được Tạo', readonly=True)
    
    # === GHI CHÚ ===
    ghi_chu = fields.Text(string='Ghi Chú')
    
    @api.model
    def create(self, vals):
        record = super(TuongTacKhachHang, self).create(vals)
        
        # Tự động tạo công việc nếu được yêu cầu
        if vals.get('tao_cong_viec'):
            record._tao_cong_viec_tu_tuong_tac()
        
        return record
    
    def _tao_cong_viec_tu_tuong_tac(self):
        """Tạo công việc từ tương tác khách hàng"""
        for record in self:
            # Xác định tên công việc dựa trên loại tương tác
            ten_cong_viec_map = {
                'goi_dien': f'Gọi điện KH: {record.khach_hang_id.ten_khach_hang}',
                'email': f'Phản hồi email KH: {record.khach_hang_id.ten_khach_hang}',
                'gap_mat': f'Gặp mặt KH: {record.khach_hang_id.ten_khach_hang}',
                'lich_hen': f'Lịch hẹn KH: {record.khach_hang_id.ten_khach_hang}',
                'gui_bao_gia': f'Theo dõi báo giá KH: {record.khach_hang_id.ten_khach_hang}',
                'demo': f'Demo sản phẩm cho KH: {record.khach_hang_id.ten_khach_hang}',
                'ho_tro': f'Hỗ trợ KH: {record.khach_hang_id.ten_khach_hang}',
                'khieu_nai': f'Xử lý khiếu nại KH: {record.khach_hang_id.ten_khach_hang}',
                'khac': f'Công việc với KH: {record.khach_hang_id.ten_khach_hang}',
            }
            
            ten_cong_viec = ten_cong_viec_map.get(record.loai_tuong_tac, f'Công việc KH: {record.khach_hang_id.ten_khach_hang}')
            
            # Tìm dự án mặc định hoặc tạo mới
            du_an = self.env['du_an'].search([('ten_du_an', 'ilike', 'Bán hàng')], limit=1)
            if not du_an:
                du_an = self.env['du_an'].search([], limit=1)
            
            if du_an:
                # Tạo công việc
                cong_viec = self.env['cong_viec'].create({
                    'ten_cong_viec': ten_cong_viec,
                    'mo_ta': f"{record.mo_ta or ''}\n\nBước tiếp theo: {record.buoc_tiep_theo or 'Chưa xác định'}",
                    'du_an_id': du_an.id,
                    'nhan_vien_ids': [(6, 0, [record.nhan_vien_id.id])] if record.nhan_vien_id else [],
                    'khach_hang_id': record.khach_hang_id.id,
                    'co_hoi_id': record.co_hoi_id.id if record.co_hoi_id else False,
                    'loai_cong_viec': 'ban_hang',
                })
                
                record.cong_viec_id = cong_viec.id
    
    def action_tao_cong_viec(self):
        """Button để tạo công việc thủ công"""
        for record in self:
            if not record.cong_viec_id:
                record.tao_cong_viec = True
                record._tao_cong_viec_tu_tuong_tac()
