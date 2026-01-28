# -*- coding: utf-8 -*-
import json
import requests
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class AIService(models.AbstractModel):
    _name = 'ai.service'
    _description = 'AI Service - Gọi API OpenRouter'

    @api.model
    def _get_headers(self, api_key):
        """Tạo headers cho API request"""
        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://odoo.local',
            'X-Title': 'Odoo AI Assistant'
        }

    @api.model
    def call_ai(self, prompt, system_prompt=None):
        """
        Gọi AI API và trả về kết quả
        
        Args:
            prompt: Câu hỏi/yêu cầu của người dùng
            system_prompt: Hướng dẫn cho AI (optional)
            
        Returns:
            str: Phản hồi từ AI hoặc thông báo lỗi
        """
        config = self.env['ai.config'].get_config()
        if not config:
            return "⚠️ Chưa cấu hình AI. Vui lòng vào Cài đặt > AI Assistant để cấu hình API Key."
        
        try:
            messages = []
            
            # Tự động lấy context dữ liệu nếu chưa có system_prompt chuyên biệt được truyền vào
            # hoặc bổ sung vào system_prompt mặc định
            data_context = ""
            if not system_prompt or "THÔNG TIN" not in system_prompt:
                data_context = self._get_data_context(prompt)

            if not system_prompt:
                system_prompt = """Bạn là trợ lý AI thông minh trong hệ thống quản lý doanh nghiệp Odoo. 
                Bạn giúp phân tích dữ liệu, đưa ra đề xuất và hỗ trợ người dùng.
                Trả lời bằng tiếng Việt, ngắn gọn và hữu ích."""
            
            if data_context:
                system_prompt += f"\n\n{data_context}"

            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
            # User prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            payload = {
                "model": config.model_name,
                "messages": messages,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            }

            response = requests.post(
                config.api_url,
                headers=self._get_headers(config.api_key),
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                return "❌ Không nhận được phản hồi từ AI."
            else:
                _logger.error(f"AI API Error: {response.status_code} - {response.text}")
                return f"❌ Lỗi API ({response.status_code}): {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Yêu cầu hết thời gian chờ. Vui lòng thử lại."
        except requests.exceptions.RequestException as e:
            _logger.error(f"AI Request Error: {str(e)}")
            return f"❌ Lỗi kết nối: {str(e)}"
        except Exception as e:
            _logger.error(f"AI Error: {str(e)}")
            return f"❌ Lỗi: {str(e)}"

    def _get_data_context(self, prompt):
        """Phân tích câu hỏi và lấy dữ liệu thống kê từ hệ thống"""
        context = []
        prompt_lower = prompt.lower()
        
        try:
            # 1. Nhân sự / Nhân viên
            if any(w in prompt_lower for w in ['nhân viên', 'nhân sự', 'người', 'staff', 'employee']):
                emp_count = self.env['nhan_vien'].search_count([])
                context.append(f"- Tổng số nhân viên hiện tại: {emp_count}")
                # Thống kê theo phòng ban
                departments = self.env['phong_ban'].search([])
                if departments:
                    dept_stats = []
                    for dept in departments:
                        count = self.env['nhan_vien'].search_count([('phong_ban_id', '=', dept.id)])
                        dept_stats.append(f"{dept.ten_phong_ban}: {count}")
                    context.append(f"- Phân bổ nhân sự: {', '.join(dept_stats)}")

            # 2. Phòng ban
            if 'phòng ban' in prompt_lower or 'department' in prompt_lower:
                dept_list = self.env['phong_ban'].search([])
                names = [d.ten_phong_ban for d in dept_list]
                context.append(f"- Danh sách phòng ban ({len(names)}): {', '.join(names)}")

            # 3. Công việc / Dự án
            if any(w in prompt_lower for w in ['công việc', 'task', 'nhiệm vụ', 'job']):
                task_total = self.env['cong_viec'].search_count([])
                task_done = self.env['cong_viec'].search_count([('trang_thai', '=', 'hoan_thanh')])
                task_todo = self.env['cong_viec'].search_count([('trang_thai', '=', 'moi')])
                context.append(f"- Tổng công việc: {task_total} (Mới: {task_todo}, Hoàn thành: {task_done})")
            
            if any(w in prompt_lower for w in ['dự án', 'project']):
                project_count = self.env['du_an'].search_count([])
                context.append(f"- Tổng số dự án: {project_count}")

            # 4. Khách hàng
            if any(w in prompt_lower for w in ['khách hàng', 'customer', 'client']):
                cust_count = self.env['khach_hang'].search_count([])
                context.append(f"- Tổng số khách hàng: {cust_count}")

            # 5. Cơ hội bán hàng
            if any(w in prompt_lower for w in ['cơ hội', 'opportunity', 'sale']):
                opp_count = self.env['co_hoi_ban_hang'].search_count([])
                context.append(f"- Tổng số cơ hội bán hàng: {opp_count}")

        except Exception as e:
            _logger.warning(f"Error getting context data: {e}")
            
        if context:
            return "\n\n[DỮ LIỆU THỰC TẾ TỪ HỆ THỐNG ODOO]:\n" + "\n".join(context) + "\n(Hãy sử dụng dữ liệu này để trả lời câu hỏi của người dùng một cách chính xác nhất)"
        return ""

    @api.model
    def analyze_opportunity(self, co_hoi):
        """Phân tích cơ hội bán hàng"""
        prompt = f"""
Phân tích cơ hội bán hàng sau và đưa ra đề xuất chiến lược:

📋 THÔNG TIN CƠ HỘI:
- Tên: {co_hoi.ten_co_hoi}
- Khách hàng: {co_hoi.khach_hang_id.ten_khach_hang}
- Loại khách hàng: {dict(co_hoi.khach_hang_id._fields['loai_khach_hang'].selection).get(co_hoi.khach_hang_id.loai_khach_hang, 'N/A')}
- Giá trị dự kiến: {co_hoi.gia_tri_du_kien:,.0f} VND
- Xác suất thành công: {co_hoi.xac_suat}%
- Giai đoạn: {dict(co_hoi._fields['giai_doan'].selection).get(co_hoi.giai_doan, 'N/A')}
- Mô tả: {co_hoi.mo_ta or 'Không có'}

Hãy phân tích và đề xuất:
1. Đánh giá tiềm năng cơ hội (cao/trung bình/thấp)
2. 3 bước tiếp theo nên thực hiện
3. Rủi ro cần lưu ý
4. Chiến lược chốt deal
"""
        system_prompt = "Bạn là chuyên gia tư vấn bán hàng B2B với 15 năm kinh nghiệm. Đưa ra phân tích chuyên sâu và thực tế."
        return self.call_ai(prompt, system_prompt)

    @api.model
    def estimate_task_time(self, cong_viec):
        """Ước tính thời gian hoàn thành công việc"""
        prompt = f"""
Ước tính thời gian và đề xuất cho công việc sau:

📋 THÔNG TIN CÔNG VIỆC:
- Tên: {cong_viec.ten_cong_viec}
- Loại: {dict(cong_viec._fields['loai_cong_viec'].selection).get(cong_viec.loai_cong_viec, 'N/A')}
- Mức độ ưu tiên: {cong_viec.muc_do_uu_tien}
- Mô tả: {cong_viec.mo_ta or 'Không có'}
- Thời gian ước tính hiện tại: {cong_viec.thoi_gian_uoc_tinh} giờ
- Dự án: {cong_viec.du_an_id.ten_du_an if cong_viec.du_an_id else 'Không có'}

Hãy phân tích:
1. Thời gian ước tính hợp lý (giờ)
2. Các bước thực hiện chính
3. Kỹ năng cần thiết
4. Rủi ro có thể gây chậm tiến độ
"""
        system_prompt = "Bạn là quản lý dự án IT với kinh nghiệm ước tính effort chính xác."
        return self.call_ai(prompt, system_prompt)

    @api.model  
    def evaluate_employee(self, nhan_vien):
        """Đánh giá nhân viên và đề xuất phát triển"""
        prompt = f"""
Gợi ý đánh giá và phát triển cho nhân viên:

👤 THÔNG TIN NHÂN VIÊN:
- Họ tên: {nhan_vien.ho_ten_dem} {nhan_vien.ten}
- Chức vụ: {nhan_vien.chuc_vu_id.ten_chuc_vu if nhan_vien.chuc_vu_id else 'N/A'}
- Phòng ban: {nhan_vien.phong_ban_id.ten_phong_ban if nhan_vien.phong_ban_id else 'N/A'}
- Ngày vào công ty: {nhan_vien.ngay_vao_cong_ty}
- Trình độ học vấn: {dict(nhan_vien._fields['trinh_do_hoc_van'].selection).get(nhan_vien.trinh_do_hoc_van, 'N/A') if nhan_vien.trinh_do_hoc_van else 'N/A'}
- Chuyên ngành: {nhan_vien.chuyen_nganh or 'N/A'}

Hãy đề xuất:
1. Điểm mạnh tiềm năng dựa trên vị trí
2. Kỹ năng nên phát triển 
3. Khóa đào tạo phù hợp
4. Lộ trình thăng tiến có thể
"""
        system_prompt = "Bạn là chuyên gia nhân sự với 10 năm kinh nghiệm phát triển nhân tài."
        return self.call_ai(prompt, system_prompt)
