from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Công Việc Dự Án'
    _rec_name = 'ten_cong_viec'
    _order = 'muc_do_uu_tien desc, han_chot'

    ten_cong_viec = fields.Char(string='Tên Công Việc', required=True)
    mo_ta = fields.Text(string='Mô Tả')
    du_an_id = fields.Many2one('du_an', string='Dự Án', required=True, ondelete='cascade')

    nhan_vien_ids = fields.Many2many('nhan_vien', 'cong_viec_nhan_vien_rel', 'cong_viec_id', 'nhan_vien_id', string='Nhân Viên Tham Gia')

    han_chot = fields.Datetime(string='Hạn Chót')
    ngay_bat_dau = fields.Datetime(string='Ngày Bắt Đầu', default=fields.Datetime.now)
    
    giai_doan_id = fields.Many2one('giai_doan_cong_viec', string='Giai Đoạn')

    nhat_ky_cong_viec_ids = fields.One2many('nhat_ky_cong_viec', 'cong_viec_id', string='Nhật Ký Công Việc')

    thoi_gian_con_lai = fields.Char(string="Thời Gian Còn Lại", compute="_compute_thoi_gian_con_lai", store=True)
    
    danh_gia_nhan_vien_ids = fields.One2many('danh_gia_nhan_vien', 'cong_viec_id', string='Đánh Giá Nhân Viên')
    
    nhan_vien_display = fields.Char(string="Nhân Viên Tham Gia (Tên + Mã Định Danh)", compute="_compute_nhan_vien_display")

    phan_tram_cong_viec = fields.Float(
        string="Phần Trăm Hoàn Thành", 
        compute="_compute_phan_tram_cong_viec", 
        store=True
    )
    
    # === TRƯỜNG MỚI: LOẠI CÔNG VIỆC ===
    loai_cong_viec = fields.Selection([
        ('phat_trien', 'Phát Triển'),
        ('kiem_thu', 'Kiểm Thử'),
        ('thiet_ke', 'Thiết Kế'),
        ('nghien_cuu', 'Nghiên Cứu'),
        ('ho_tro', 'Hỗ Trợ'),
        ('ban_hang', 'Bán Hàng'),
        ('marketing', 'Marketing'),
        ('hanh_chinh', 'Hành Chính'),
        ('khac', 'Khác'),
    ], string='Loại Công Việc', default='phat_trien')
    
    # === MỨC ĐỘ ƯU TIÊN ===
    muc_do_uu_tien = fields.Selection([
        ('1', 'Thấp'),
        ('2', 'Trung Bình'),
        ('3', 'Cao'),
        ('4', 'Khẩn Cấp'),
    ], string='Mức Độ Ưu Tiên', default='2')
    
    # === TRẠNG THÁI ===
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang Thực Hiện'),
        ('cho_duyet', 'Chờ Duyệt'),
        ('hoan_thanh', 'Hoàn Thành'),
        ('huy', 'Đã Hủy'),
    ], string='Trạng Thái', default='moi', tracking=True)
    
    # === THỜI GIAN ===
    thoi_gian_uoc_tinh = fields.Float(string='Thời Gian Ước Tính (giờ)', default=0)
    thoi_gian_thuc_te = fields.Float(string='Thời Gian Thực Tế (giờ)', compute='_compute_thoi_gian_thuc_te', store=True)
    
    # === GHI CHÚ ===
    ghi_chu = fields.Text(string='Ghi Chú')
    active = fields.Boolean(string='Hoạt Động', default=True)

    @api.depends('nhat_ky_cong_viec_ids.muc_do')
    def _compute_phan_tram_cong_viec(self):
        for record in self:
            if record.nhat_ky_cong_viec_ids:
                total_progress = sum(record.nhat_ky_cong_viec_ids.mapped('muc_do'))
                record.phan_tram_cong_viec = total_progress / len(record.nhat_ky_cong_viec_ids)
            else:
                record.phan_tram_cong_viec = 0.0

    @api.depends('nhan_vien_ids')
    def _compute_nhan_vien_display(self):
        for record in self:
            record.nhan_vien_display = ', '.join(record.nhan_vien_ids.mapped('display_name'))

    @api.depends('han_chot')
    def _compute_thoi_gian_con_lai(self):
        for record in self:
            if record.han_chot:
                now = datetime.now()
                delta = record.han_chot - now
                if delta.total_seconds() > 0:
                    days = delta.days
                    hours = delta.seconds // 3600
                    record.thoi_gian_con_lai = f"{days} ngày, {hours} giờ"
                else:
                    record.thoi_gian_con_lai = "Hết hạn"
            else:
                record.thoi_gian_con_lai = "Chưa có hạn chót"
    
    @api.depends('nhat_ky_cong_viec_ids')
    def _compute_thoi_gian_thuc_te(self):
        """Tính tổng thời gian thực tế từ nhật ký công việc"""
        for record in self:
            # Giả sử mỗi nhật ký là 1 đơn vị công việc
            record.thoi_gian_thuc_te = len(record.nhat_ky_cong_viec_ids) * 2  # Ước tính 2 giờ mỗi nhật ký

    @api.onchange('du_an_id')
    def _onchange_du_an_id(self):
        if self.du_an_id:
            self.nhan_vien_ids = [(6, 0, self.du_an_id.nhan_vien_ids.ids)]

    @api.constrains('du_an_id')
    def _check_du_an_tien_do(self):
        for record in self:
            if record.du_an_id and record.du_an_id.tien_do_du_an == 'hoan_thanh':
                raise ValidationError("Không thể thêm công việc vào dự án đã hoàn thành.")

    @api.constrains('nhan_vien_ids')
    def _check_nhan_vien_trong_du_an(self):
        for record in self:
            if record.du_an_id:
                nhan_vien_du_an_ids = record.du_an_id.nhan_vien_ids.ids
                for nhan_vien in record.nhan_vien_ids:
                    if nhan_vien.id not in nhan_vien_du_an_ids:
                        raise ValidationError(f"Nhân viên {nhan_vien.display_name} không thuộc dự án này.")
    
    def action_bat_dau(self):
        """Bắt đầu thực hiện công việc"""
        for record in self:
            record.write({
                'trang_thai': 'dang_thuc_hien',
                'ngay_bat_dau': datetime.now(),
            })
    
    def action_hoan_thanh(self):
        """Đánh dấu hoàn thành"""
        for record in self:
            record.trang_thai = 'hoan_thanh'
    
    def action_huy(self):
        """Hủy công việc"""
        for record in self:
            record.trang_thai = 'huy'
    
    def action_tao_nhat_ky(self):
        """Tạo nhật ký công việc"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Thêm Nhật Ký',
            'res_model': 'nhat_ky_cong_viec',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cong_viec_id': self.id,
                'default_nhan_vien_ids': [(6, 0, self.nhan_vien_ids.ids)],
            },
        }
