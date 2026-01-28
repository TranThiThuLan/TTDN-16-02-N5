<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP - Giải pháp Quản trị Doanh nghiệp tổng thể, được xây dựng và phát triển trong học phần Thực tập doanh nghiệp. Hệ thống được phát triển dựa trên nền tảng Odoo, tập trung sâu vào hai nghiệp vụ chính: **Quản lý Khách hàng (CRM)** và **Quản lý Công việc (Task Management)**, nhằm tối ưu hóa quy trình kinh doanh và nâng cao hiệu suất làm việc.

### 🌟 Các Phân hệ Chính

#### 🤝 Quản lý Khách hàng (CRM)
Giải pháp toàn diện giúp doanh nghiệp quản lý mối quan hệ khách hàng và quy trình bán hàng:
- **Quản lý 360 độ**: Lưu trữ chi tiết thông tin khách hàng (cá nhân/doanh nghiệp) và đầu mối liên hệ.
- **Cơ hội kinh doanh**: Theo dõi, đánh giá và chuyển đổi tiềm năng thành đơn hàng.
- **Hoạt động bán hàng**: Quản lý báo giá, lịch hẹn và lịch sử tương tác chi tiết.
- **Tích hợp quy trình**: Tự động liên kết và khởi tạo công việc từ các hoạt động bán hàng, giúp bộ phận kinh doanh và kỹ thuật phối hợp nhịp nhàng.

#### 📋 Quản lý Công việc & Dự án
Công cụ đắc lực để tổ chức, theo dõi và đánh giá hiệu quả công việc:
- **Tổ chức Dự án**: Quản lý đa dự án với cấu trúc giai đoạn rõ ràng.
- **Điều phối Công việc**: Phân công task, thiết lập mức độ ưu tiên (KPIs) và theo dõi trạng thái thời gian thực.
- **Nhật ký & Đánh giá**: Ghi nhận nhật ký công việc (Timesheet) và hệ thống đánh giá nhân viên khách quan.
- **Dashboard trực quan**: Báo cáo tổng quan, biểu đồ thống kê giúp nhà quản lý nắm bắt tiến độ tức thì.
- **Kết nối dữ liệu**: Liên kết chặt chẽ với dữ liệu khách hàng và nhân sự. 

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Các project đã thực hiện dựa trên Platform

Một số project sinh viên đã thực hiện:
- #### [Khoá 15](./docs/projects/K15/README.md)
- #### [Khoá 16](./docs/projects/K16/README.md)
- #### [Khoá 17](./docs/projects/K17/README.md)
## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project.
```
git clone https://github.com/FIT-DNU/Business-Internship.git
```
#### 4.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
#### 4.1.3. Khởi tạo môi trường ảo.
- Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo
```
source venv/bin/activate
```
- Chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
pip3 install -r requirements.txt
```
### 4.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo docker-compose up -d
```
### 4.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```
Có thể kế thừa từ file **odoo.conf.template**
### 4.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```
Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

## 📝 5. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---

    
