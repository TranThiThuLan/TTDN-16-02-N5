# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'display_name'
    _order = 'ho_va_ten'

    # === THÔNG TIN CƠ BẢN ===
    ma_dinh_danh = fields.Char(string="Mã Định Danh", copy=False)
    ho_ten_dem = fields.Char(string="Họ Tên Đệm")
    ten = fields.Char(string="Tên", required=True)
    ho_va_ten = fields.Char(string="Họ và Tên", compute='_tinh_ho_va_ten', store=True)
    display_name = fields.Char(string='Tên Hiển Thị', compute='_compute_display_name', store=True)
    
    anh_dai_dien = fields.Binary(string="Ảnh Đại Diện", attachment=True)
    
    ngay_sinh = fields.Date(string="Ngày Sinh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ], string="Giới Tính")
    
    # === THÔNG TIN LIÊN LẠC ===
    email = fields.Char(string="Email")
    email_cong_ty = fields.Char(string="Email Công Ty")
    so_dien_thoai = fields.Char(string="Số Điện Thoại")
    so_dien_thoai_khan_cap = fields.Char(string="SĐT Khẩn Cấp")
    nguoi_lien_he_khan_cap = fields.Char(string="Người Liên Hệ Khẩn Cấp")
    
    # === ĐỊA CHỈ ===
    que_quan = fields.Char(string="Quê Quán")
    dia_chi_hien_tai = fields.Text(string="Địa Chỉ Hiện Tại")
    thanh_pho = fields.Char(string="Thành Phố")
    quoc_gia_id = fields.Many2one('res.country', string="Quốc Gia")
    
    # === GIẤY TỜ TÙY THÂN ===
    so_cmnd = fields.Char(string="Số CMND/CCCD")
    ngay_cap_cmnd = fields.Date(string="Ngày Cấp")
    noi_cap_cmnd = fields.Char(string="Nơi Cấp")
    so_ho_chieu = fields.Char(string="Số Hộ Chiếu")
    ngay_het_han_ho_chieu = fields.Date(string="Ngày Hết Hạn Hộ Chiếu")
    
    # === THÔNG TIN NGÂN HÀNG ===
    so_tai_khoan = fields.Char(string="Số Tài Khoản")
    ten_ngan_hang = fields.Char(string="Tên Ngân Hàng")
    chi_nhanh_ngan_hang = fields.Char(string="Chi Nhánh")
    
    # === THÔNG TIN CÔNG VIỆC ===
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức Vụ", ondelete="set null")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng Ban", ondelete="set null")
    nguoi_quan_ly_id = fields.Many2one("nhan_vien", string="Người Quản Lý Trực Tiếp", ondelete="set null")
    nhan_vien_cap_duoi_ids = fields.One2many("nhan_vien", "nguoi_quan_ly_id", string="Nhân Viên Cấp Dưới")
    
    ngay_vao_cong_ty = fields.Date(string="Ngày Vào Công Ty")
    ngay_nghi_viec = fields.Date(string="Ngày Nghỉ Việc")
    so_nam_lam_viec = fields.Float(string="Số Năm Làm Việc", compute='_compute_so_nam_lam_viec', store=True)
    
    trang_thai_lam_viec = fields.Selection([
        ('dang_lam', 'Đang Làm Việc'),
        ('thu_viec', 'Đang Thử Việc'),
        ('nghi_phep', 'Đang Nghỉ Phép'),
        ('nghi_thai_san', 'Nghỉ Thai Sản'),
        ('da_nghi_viec', 'Đã Nghỉ Việc'),
    ], string="Trạng Thái", default='dang_lam')
    
    hinh_thuc_lam_viec = fields.Selection([
        ('toan_thoi_gian', 'Toàn thời gian'),
        ('ban_thoi_gian', 'Bán thời gian'),
        ('tu_xa', 'Làm việc từ xa'),
        ('thoi_vu', 'Thời vụ'),
    ], string="Hình Thức Làm Việc", default='toan_thoi_gian')
    
    # === LƯƠNG & HỢP ĐỒNG ===
    luong_co_ban = fields.Float(string="Lương Cơ Bản", digits=(16, 0))
    hop_dong_ids = fields.One2many('hop_dong_lao_dong', 'nhan_vien_id', string="Hợp Đồng Lao Động")
    hop_dong_hien_tai_id = fields.Many2one('hop_dong_lao_dong', string="Hợp Đồng Hiện Tại", 
                                            compute='_compute_hop_dong_hien_tai', store=True)
    
    # === NGHỈ PHÉP ===
    nghi_phep_ids = fields.One2many('nghi_phep', 'nhan_vien_id', string="Đơn Nghỉ Phép")
    phep_nam_ids = fields.One2many('phep_nam', 'nhan_vien_id', string="Phép Năm")
    so_ngay_phep_con_lai = fields.Float(string="Số Ngày Phép Còn", compute='_compute_so_ngay_phep_con_lai')
    
    # === LIÊN KẾT DỰ ÁN & CÔNG VIỆC ===
    lich_su_lam_viec_ids = fields.One2many('lich_su_lam_viec', 'nhan_vien_id', string="Lịch Sử Làm Việc")
    nhom_du_an_ids = fields.Many2many('nhom_du_an', string='Nhóm Dự Án')
    du_an_ids = fields.Many2many('du_an', 'nhan_vien_du_an_rel', 'nhan_vien_id', 'du_an_id', string='Dự Án Đang Tham Gia')
    cong_viec_ids = fields.Many2many('cong_viec', 'nhan_vien_cong_viec_rel', 'nhan_vien_id', 'cong_viec_id', string='Công Việc Tham Gia')
    
    # === HỌC VẤN & CHỨNG CHỈ ===
    trinh_do_hoc_van = fields.Selection([
        ('thpt', 'THPT'),
        ('trung_cap', 'Trung Cấp'),
        ('cao_dang', 'Cao Đẳng'),
        ('dai_hoc', 'Đại Học'),
        ('thac_si', 'Thạc Sĩ'),
        ('tien_si', 'Tiến Sĩ'),
    ], string="Trình Độ Học Vấn")
    chuyen_nganh = fields.Char(string="Chuyên Ngành")
    truong_tot_nghiep = fields.Char(string="Trường Tốt Nghiệp")
    
    # === GHI CHÚ ===
    ghi_chu = fields.Text(string="Ghi Chú")
    active = fields.Boolean(string="Hoạt Động", default=True)
    
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email đã tồn tại, vui lòng chọn email khác!'),
        ('unique_ma_dinh_danh', 'UNIQUE(ma_dinh_danh)', 'Mã định danh đã tồn tại, vui lòng chọn mã khác!'),
        ('unique_so_cmnd', 'UNIQUE(so_cmnd)', 'Số CMND/CCCD đã tồn tại!'),
    ]

    @api.depends("ho_ten_dem", "ten")
    def _tinh_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = f"{record.ho_ten_dem} {record.ten}".strip()
            elif record.ten:
                record.ho_va_ten = record.ten
            else:
                record.ho_va_ten = ""

    @api.onchange("ten", "ho_ten_dem")
    def _onchange_tinh_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join([tu[0] for tu in record.ho_ten_dem.lower().split() if tu])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau
            else:
                record.ma_dinh_danh = False

    @api.depends('ho_va_ten', 'ma_dinh_danh')
    def _compute_display_name(self):
        for record in self:
            if record.ma_dinh_danh:
                record.display_name = f"{record.ho_va_ten} ({record.ma_dinh_danh})"
            else:
                record.display_name = record.ho_va_ten or "Chưa có tên"
    
    @api.depends('ngay_vao_cong_ty')
    def _compute_so_nam_lam_viec(self):
        today = date.today()
        for record in self:
            if record.ngay_vao_cong_ty:
                delta = today - record.ngay_vao_cong_ty
                record.so_nam_lam_viec = round(delta.days / 365.25, 1)
            else:
                record.so_nam_lam_viec = 0
    
    @api.depends('hop_dong_ids', 'hop_dong_ids.trang_thai')
    def _compute_hop_dong_hien_tai(self):
        for record in self:
            hop_dong = record.hop_dong_ids.filtered(
                lambda h: h.trang_thai in ('dang_hieu_luc', 'sap_het_han')
            ).sorted('ngay_bat_dau', reverse=True)
            record.hop_dong_hien_tai_id = hop_dong[0] if hop_dong else False
    
    def _compute_so_ngay_phep_con_lai(self):
        current_year = date.today().year
        for record in self:
            phep_nam = record.phep_nam_ids.filtered(lambda p: p.nam == current_year)
            record.so_ngay_phep_con_lai = phep_nam[0].so_ngay_con_lai if phep_nam else 0
    
    def action_xem_hop_dong(self):
        """Mở danh sách hợp đồng của nhân viên"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hợp Đồng Lao Động',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id},
        }
    
    def action_xem_nghi_phep(self):
        """Mở danh sách đơn nghỉ phép của nhân viên"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đơn Nghỉ Phép',
            'res_model': 'nghi_phep',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id},
        }