# 🎤 Hệ thống Luyện Tập Phát Âm Tiếng Anh Quân Sự

**Chương trình luyện tập phát âm tiếng Anh chuyên ngành quân sự với phân tích lỗi chi tiết sử dụng AI.**

Dành cho những người học tiếng Anh còn gặp khó khăn trong phát âm, hệ thống này sẽ:
1. **Phát âm mẫu** - Nghe từ/cụm từ/câu mẫu
2. **Ghi âm đầu vào** - Nhanh chóng nhận dạng phát âm của bạn
3. **Phân tích chi tiết** - Tìm ra 3 loại lỗi (Sai âm, Thiếu âm, Thêm âm)
4. **Đưa ra feedback** - Hướng dẫn cải thiện cụ thể
5. **Cho phép thử lại** - Nếu không nhận diện được hoặc chất lượng kém

---

## 📦 Cấu trúc Project

```
phat_am_tieng_anh/
├── main.py                          # Chương trình chính (Interactive CLI)
├── api.py                           # Flask API Backend (Analytics)
├── pronunciation_analyzer.py        # Module phân tích lỗi phát âm (Levenshtein)
│
├── 📚 UNIT 1: Military Bridge-Road Building (Xây dựng Cầu Đường Quân Sự)
│   ├── unit1_word.py                # 40+ từ vựng
│   ├── unit1_phrase.py              # 50+ cụm từ
│   └── unit1_sentence.py            # 40+ câu
│
├── 📚 UNIT 2: River Crossing (Vượt Sông)
│   ├── unit2_word.py                # 45+ từ vựng
│   ├── unit2_phrase.py              # 50+ cụm từ
│   └── unit2_sentence.py            # 45+ câu
│
├── 📚 GENERAL: NATO & Miscellaneous (Chung & Từ Khác)
│   ├── word.py                      # Từ điển từ đơn & NATO
│   ├── phrase.py                    # Từ điển cụm từ
│   └── sentence.py                  # Từ điển câu
│
├── requirements.txt                 # Python dependencies
└── README.md                        # (This file)
```

---

## 🚀 Cài Đặt & Sử Dụng

### 1️⃣ **Cài Đặt Dependencies**

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt
```

### 2️⃣ **Chạy Chương trình Chính** (CLI Mode)

```bash
python main.py
```

**Menu Chính - Chọn Unit:**
```
============================================================
CHƯƠNG TRÌNH HỌC PHÁT ÂM TIẾNG ANH - ENGLISH PRONUNCIATION
============================================================
Vui lòng chọn Unit muốn luyện tập (Choose Unit):
============================================================
  1 - Unit 1: Military Bridge-Road Building (Cầu Đường Quân Sự)
  2 - Unit 2: River Crossing (Vượt Sông)
  3 - Unit 3: (Chưa có)
  G - General: NATO & Military Terms (Từ vựng chung)
  0 - Exit (Thoát)
============================================================
```

---

## 📖 Cấu Trúc Bài Học

Mỗi **Unit** được thiết kế theo **3 mức độ học tập**:

```
Unit → Words (Từ đơn) → Phrases (Cụm từ) → Sentences (Câu)
       ↓ 5 giây         ↓ 8 giây          ↓ 10 giây
    (Đủ thời gian      (Cần thêm        (Câu dài,
     phát âm)         thời gian)       cần nhiều thời gian)
```

Khi bạn chọn một Unit (ví dụ: `1`), chương trình sẽ:
1. ✅ Tự động luyện tập **toàn bộ Từ vựng** trong Unit 1
2. ✅ Sau đó, luyện tập **toàn bộ Cụm từ** trong Unit 1
3. ✅ Cuối cùng, luyện tập **toàn bộ Câu** trong Unit 1
4. ✅ Tạo báo cáo tổng kết với thống kê độ chính xác

---

### **Quy Trình Luyện Tập Mỗi Mục:**

```
1️⃣ Chương trình phát âm mẫu
   ↓
2️⃣ Bạn nghe và chuẩn bị
   ↓
3️⃣ Bạn nói vào microphone (Thời gian ghi âm: 5-10 giây tuỳ loại)
   ↓
4️⃣ Chương trình phân tích chi tiết:
   - Tính tương đồng (0-100%)
   - Chất lượng phát âm (Excellent/Good/Fair/Poor)
   - Tìm lỗi cụ thể (Sai âm, Thiếu, Thêm)
   - Đưa feedback
   ↓
5️⃣ Nếu qua kiểm tra (≥70%):
   ✅ Ghi nhận kết quả, chuyển mục tiếp theo
   ↓
6️⃣ Nếu không đạt (<70%) hoặc không nhận diện:
   🔄 Tự động cho phép thử lại 1 lần
   ❓ Nếu lần 2 vẫn kém: Hỏi "Bạn có muốn đọc lại không? (y/n)"
```

---

### **Ví Dụ Output Luyện Tập:**

```
============================================================
📊 PHÂN TÍCH PHÁT ÂM
============================================================
Expected: Military bridge
Received: Military brige
Similarity: 85.5%
Quality: Good
Feedback: Phát âm tốt, nhưng còn một vài lỗi nhỏ.

🔍 Chi tiết lỗi (1 lỗi):
  1. DELETION: Thiếu 'd' tại vị trí 13

📈 Tóm tắt: Sai âm (0), Thiếu (1), Thêm (0)
============================================================

✅ Đạt yêu cầu (85.5% ≥ 70%). Tiếp tục mục tiếp theo...
```

---

### **Thống Kê Sau Phiên Luyện Tập:**

```
============================================================
📊 BÁO CÁO TỔNG KẾT PHIÊN LUYỆN TẬP
============================================================
Unit: Unit 1 - Military Bridge-Road Building
Tổng số từ: 15 (Từ vựng: 5, Cụm từ: 5, Câu: 5)

Excellent: 5  ⭐⭐⭐⭐⭐
Good:      7  ⭐⭐⭐⭐
Fair:      2  ⭐⭐⭐
Poor:      1  ⭐

Độ chính xác tổng: 84.5%
============================================================
```

---

## 🎯 Các Unit Có Sẵn

### **Unit 1: Military Bridge-Road Building (Xây dựng Cầu Đường Quân Sự)**

**Chủ đề:** Công trình cây cầu, đường quân sự, thiết bị PMP, TMM-6

**Nội dung:**
- 📝 **40+ Từ vựng**: Pontoon, Bridge, Abutment, Mooring, Sapper, Combat engineer, TMM-6, v.v.
- 📚 **50+ Cụm từ**: Pontoon bridge, Floating bridge, Bridge installation, Carrying capacity, v.v.
- 📖 **40+ Câu**: Mô tả cấu trúc cầu, quy trình lắp ráp, khả năng chở tải, v.v.

**Ứng dụng:** Dành cho những người học kỹ thuật xây dựng công trình quân sự (Cầu, Đường)

---

### **Unit 2: River Crossing (Vượt Sông)**

**Chủ đề:** Phương tiện qua sông, phà quân sự, vượt chướng ngại nước

**Nội dung:**
- 📝 **45+ Từ vựng**: Ferry, Crossing, Cable ferry, Reaction ferry, Amphibious, TMM-6, v.v.
- 📚 **50+ Cụm từ**: River crossing, Water obstacle, Pontoon ferry, Cable ferry operation, v.v.
- 📖 **45+ Câu**: Định nghĩa các phương tiện, tác vụ vượt sông, thông số kỹ thuật TMM-6, v.v.

**Ứng dụng:** Dành cho những người học về các tác vụ vượt chướng ngại nước

---

### **General Mode: NATO & Miscellaneous**

**Chứa:** Từ điển NATO chuẩn, từ vựng quân sự tiêu chuẩn, cụm từ chung

**Sử dụng khi:** Muốn luyện tập từ vựng chung, không theo Unit cụ thể

---

## ⏱️ Thời Gian Ghi Âm (Dynamic Timeout)

Chương trình tự động điều chỉnh thời gian ghi âm dựa trên độ dài nội dung:

| Loại | Thời gian ghi âm | Mục đích |
|------|-----------------|---------|
| **From (Từ đơn)** | 5 giây | Đủ thời gian phát âm từ đơn ngắn |
| **Cụm từ** | 8 giây | Cho phép phát âm cụm từ dài hơn |
| **Câu** | 10 giây | Cho phép phát âm câu phức tạp với dừa đầu |

**Lợi ích:**
- ✅ Không bị cắt âm (âm thanh không bị đứt giữa chừng)
- ✅ Có đủ thời gian để phát âm tự nhiên
- ✅ Giảm căng thẳng, nâng cao chất lượng ghi âm

---

## 🔄 Cơ Chế Thử Lại (Retry Mechanism)

Khi phát âm không đạt yêu cầu:

```
Lần 1: Phát âm không được nhận diện
  ↓
🤖 Tự động cho thử lại 1 lần
  ↓
Lần 2: Đạt ≥70%? → Tiếp tục ✅
      Không đạt? → Hỏi bạn: "Bạn có muốn đọc lại không?" ❓
      Lần 3 có? → Xài kết quả tốt nhất của 2 lần ✅
      Từ chối? → Ghi nhận lần tốt nhất, tiếp tục ✅
```

This prevents frustration from one missed recording while still maintaining learning progress.

---

## 🔬 Backend API (Optional - Advanced Users)

Ngoài giao diện dòng lệnh (CLI), hệ thống còn cung cấp **Flask REST API** để tích hợp vào các ứng dụng khác.

### **Chạy Flask API:**

```bash
python api.py
```

API sẽ chạy tại: `http://localhost:5000`

---

### **Các Endpoint API:**

#### **POST /api/analyze** - Phân tích một từ
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "expected": "hello",
    "received": "helo",
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "expected": "hello",
    "received": "helo",
    "similarity": 80.5,
    "edit_distance": 1,
    "quality": "Good",
    "feedback": "Phát âm tốt, nhưng còn một vài lỗi nhỏ.",
    "errors": [
      {
        "type": "deletion",
        "position": 4,
        "expected": "l",
        "received": "",
        "description": "Thiếu âm: l"
      }
    ],
    "error_breakdown": {
      "substitutions": 0,
      "deletions": 1,
      "insertions": 0
    }
  }
}
```

---

#### **POST /api/batch-analyze** - Phân tích nhiều từ
```bash
curl -X POST http://localhost:5000/api/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"expected": "hello", "received": "helo"},
      {"expected": "world", "received": "word"},
      {"expected": "perfect", "received": "perfekt"}
    ],
    "user_id": "user123"
  }'
```

---

#### **GET /api/stats** - Thống kê
```bash
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/stats?user_id=user123
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_analyses": 10,
    "excellent": 3,
    "good": 5,
    "fair": 2,
    "poor": 0,
    "average_similarity": 87.5
  }
}
```

---

#### **GET /api/history** - Lịch sử
```bash
curl http://localhost:5000/api/history
curl http://localhost:5000/api/history?user_id=user123&limit=10
```

---

#### **GET /api/export** - Xuất JSON
```bash
curl http://localhost:5000/api/export > history.json
curl http://localhost:5000/api/export?user_id=user123 > user_history.json
```

---

#### **GET /api/health** - Kiểm tra trạng thái
```bash
curl http://localhost:5000/api/health
```

---

## 🔬 Module `pronunciation_analyzer.py`

### **Tính Năng:**

#### 1. **Tính Levenshtein Distance**
```python
from pronunciation_analyzer import PronunciationAnalyzer

analyzer = PronunciationAnalyzer()
distance = analyzer.levenshtein_distance("hello", "helo")
# Output: 1
```

#### 2. **Tính Độ Giống Nhau (%)**
```python
similarity = analyzer.similarity_score("hello", "helo")
# Output: 80.5
```

#### 3. **Phân Tích Chi Tiết Lỗi**
```python
analysis = analyzer.detailed_error_analysis("hello", "helo")
# Returns: {
#   'expected': 'hello',
#   'received': 'helo',
#   'similarity': 80.5,
#   'edit_distance': 1,
#   'errors': [{'type': 'deletion', 'position': 4, ...}],
#   'quality': 'Good',
#   'feedback': '...',
#   'error_breakdown': {'substitutions': 0, 'deletions': 1, 'insertions': 0}
# }
```

#### 4. **Tạo Feedback Chi Tiết**
```python
feedback = analyzer.get_detailed_feedback(analysis)
# Returns: String với chi tiết lỗi
```

---

## 📊 Chất Lượng Phát Âm

| Quality | Similarity | Mô tả |
|---------|-----------|-------|
| Excellent | ≥ 95% | Phát âm rất tốt! |
| Good | 85-94% | Phát âm tốt, nhưng còn lỗi nhỏ |
| Fair | 70-84% | Phát âm chưa chính xác, cần cải thiện |
| Poor | < 70% | Phát âm cần nhiều cải thiện |

---

## 🎯 Các Loại Lỗi Phát Âm

### 1. **Substitution (Sai Âm)**
- Phát âm sai âm khác
- Ví dụ: "th" → "s" (think → sink)

### 2. **Deletion (Thiếu Âm)**
- Bỏ qua một âm
- Ví dụ: "hello" → "helo" (thiếu "l")

### 3. **Insertion (Thêm Âm)**
- Phát âm thêm một âm không cần
- Ví dụ: "word" → "worde" (thêm "e")

---

## 💡 Ví Dụ Sử Dụng

### **Test Module Locally**

```bash
python pronunciation_analyzer.py
```

Output:
```
============================================================
Expected: hello
Received: helo
============================================================
📊 Điểm tương đồng: 80.5%
🎯 Chất lượng phát âm: Good
💬 Nhận xét: Phát âm tốt, nhưng còn một vài lỗi nhỏ.

🔍 Chi tiết lỗi:
  1. DELETION: Thiếu: 'l'

📈 Tóm tắt: Sai âm (0), Thiếu (1), Thêm (0)
```

---

## 📈 Thống Kê & báo cáo

Sau mỗi phiên luyện tập, chương trình tạo báo cáo:

```
============================================================
📊 BÁO CÁO TỔNG KẾT PHIÊN LUYỆN TẬP
============================================================
Tổng số từ: 5
Excellent: 2
Good: 2
Fair: 1
Poor: 0
Độ chính xác tổng: 80.0%
============================================================
```

---

## 🔧 Mở Rộng & Customization

### **Thêm Từ Vào Từ Điển:**

Sửa `word.py`, `phrase.py`, hoặc `sentence.py`:

```python
# word.py
custom_dict = {
    "example": "ví dụ",
    "computer": "máy tính",
    # Thêm từ tại đây...
}
```

### **Tích Hợp Model AI Tốt Hơn:**

Hiện tại dùng Google Speech Recognition. Có thể nâng cấp:
- **Wav2Vec 2.0** - Accuracy cao hơn
- **Whisper** (OpenAI) - Xử lý nhiều ngôn ngữ
- **DeepSpeech** - Fast & local processing

---

## 📝 Lưu Ý Quan Trọng

1. **Microphone**: Cần kết nối microphone để sử dụng chế độ CLI
2. **Internet**: Google Speech Recognition cần kết nối mạng
3. **Tiếng Anh**: Hiện tại chỉ hỗ trợ tiếng Anh (có thể mở rộng)
4. **Audio Quality**: Chất lượng âm thanh ảnh hưởng đến độ chính xác nhận diện

---

## 🆘 Troubleshooting

### **Lỗi: "No module named 'pronunciation_analyzer'"**
```bash
# Đảm bảo bạn ở đúng thư mục
cd /path/to/phat_am_tieng_anh
python main.py
```

### **Lỗi: Microphone không hoạt động**
```bash
# macOS
brew install portaudio
pip install --upgrade pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
```

### **Lỗi: "Port 5000 already in use"**
```bash
# Thay đổi port trong api.py
app.run(port=5001)  # Hoặc port khác

# Hoặc kill process đang dùng port 5000
lsof -i :5000
kill -9 <PID>
```

---

## 📚 Tài Liệu Tham Khảo

- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [gTTS Documentation](https://gtts.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [IPA Phonetic Guide](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)

---

## 📄 License

MIT License - Tự do sử dụng cho mục đích học tập & nghiên cứu

---

## 🎓 Đề Tài Nghiên Cứu

**"Xây dựng hệ thống phát hiện lỗi phát âm tiếng Anh sử dụng trí tuệ nhân tạo phục vụ đào tạo trong môi trường quân sự"**

### Các Chương:
- ✅ Chương 1: Giới thiệu & Lý do chọn đề tài
- ✅ Chương 2: Cơ sở lý thuyết (Speech Recognition, Deep Learning)
- ✅ Chương 3: Phương pháp đề xuất (Architecture & Pipeline)
- ✅ Chương 4: Xây dựng hệ thống (CLI + Flask API)
- ⏳ Chương 5: Thực nghiệm & Kết quả (Sắp hoàn thành)

---

**👨‍💻 Liên hệ & Hỗ trợ:** Vui lòng tạo issue nếu có câu hỏi!

**🚀 Mục tiêu tiếp theo:** Xây dựng giao diện web & thêm model AI tiên tiến hơn
