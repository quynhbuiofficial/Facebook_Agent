# Facebook AI Agent Assistant

Tự động tạo và đăng bài Facebook sử dụng AI Agent framework (autogen), tích hợp tìm kiếm tin tức mới nhất từ internet (DuckDuckGo), tối ưu cho Digital Marketing và xây dựng thương hiệu.

## 🚀 Tính năng nổi bật

- **Tự động viết & đăng bài Facebook**: AI Agent tự động lấy tin tức mới nhất về AI, marketing, công nghệ, sáng tạo... từ internet, tổng hợp và đăng bài lên fanpage.
- **Tích hợp Agent framework autogen**: Sử dụng autogen-agentchat để xây dựng Assistant Agent, tự động hóa quy trình lấy tin, viết bài, đăng bài.
- **Tìm kiếm tin tức bằng DuckDuckGo**: Sử dụng thư viện `ddgs` để lấy tin tức mới nhất, lọc domain, trích xuất nội dung và ảnh minh họa.
- **Tùy biến nội dung**: Bài viết được định dạng nổi bật, nhấn mạnh các từ khóa, tự động chèn thông tin liên hệ, tagline thương hiệu.
- **Chạy tự động theo lịch (GitHub Actions)**: Có thể cấu hình chạy định kỳ (2 lần/ngày) hoặc chạy thủ công.

## 🛠️ Cài đặt

1. **Clone repo & cài đặt thư viện**
   ```bash
   git clone <repo-url>
   cd push_github
   pip install -r requirements.txt
   ```

2. **Tạo file `.env` với các biến sau:**
   ```
   FB_ACCESS_TOKEN=...
   PAGE_ID=...
   GITHUB_TOKEN=...
   MODEL=...
   BLOCKED_DOMAINS=...
   ```
   - `FB_ACCESS_TOKEN`, `PAGE_ID`: Lấy từ Facebook Developer (Graph API).
   - `GITHUB_TOKEN`: Token cho Azure AI model (nếu dùng Azure).
   - `MODEL`: Tên model AI (ví dụ: gpt-4, gpt-3.5-turbo...).
   - `BLOCKED_DOMAINS`: (Tùy chọn) Danh sách domain không muốn lấy tin.

## ⚡️ Cách chạy thủ công

```bash
python fb_post.py
```
- Agent sẽ tự động lấy tin, tổng hợp, viết bài và đăng lên Facebook Page.

## 🧠 Cách hoạt động

1. **Agent Assistant** (dùng autogen-agentchat) sẽ:
   - Gọi tool `get_news_internet` để lấy tin tức mới nhất từ DuckDuckGo.
   - Tổng hợp, viết lại nội dung hấp dẫn, nhấn mạnh thương hiệu, chèn thông tin liên hệ.
   - Gọi tool `post_facebook` để đăng bài lên fanpage.
   - Kết thúc bằng thông điệp "THANKS_NE" (theo quy trình autogen).

2. **Tìm kiếm & trích xuất tin tức**:
   - Dùng DuckDuckGo (`ddgs`) để lấy các bài báo mới nhất.
   - Lọc domain không mong muốn.
   - Trích xuất tiêu đề, đoạn văn, ảnh lớn nhất từ bài báo.

3. **Định dạng & đăng bài**:
   - Tự động làm đậm các từ khóa (**bold**).
   - Chèn tagline, thông tin liên hệ, nguồn tin.
   - Đăng bài kèm ảnh lên Facebook qua Graph API.

## 🖥️ Chạy tự động với GitHub Actions

- Đã cấu hình sẵn workflow trong `fb_agent.yml` để chạy định kỳ hoặc thủ công trên GitHub Actions.
- Cần cấu hình các secrets tương ứng trong repo GitHub:
  - `FB_ACCESS_TOKEN`, `PAGE_ID`, `GITHUB_TOKEN`, `MODEL`, `BLOCKED_DOMAINS`, `VERIFY_TOKEN`

## 📦 Thư viện sử dụng

- `autogen-agentchat`, `autogen-ext[azure]`: Xây dựng AI Agent, tích hợp Azure AI.
- `ddgs`: Tìm kiếm tin tức DuckDuckGo.
- `requests`, `beautifulsoup4`: Gửi request, trích xuất nội dung web.
- `python-dotenv`: Quản lý biến môi trường.
- `Pillow`: Xử lý ảnh.
- `aiohttp`: Hỗ trợ async.

## 📄 Cấu trúc file chính

- `fb_post.py`: Code chính, định nghĩa Agent, tool, logic lấy tin, đăng bài.
- `fb_agent.yml`: Workflow GitHub Actions.
- `requirements.txt`: Danh sách thư viện.

## 📬 Liên hệ

- 📧 Email: quynhsydaole@gmail.com
- 📺 YouTube: https://www.youtube.com/@QuynhBuiOffical 
