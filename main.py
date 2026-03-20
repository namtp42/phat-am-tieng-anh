import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import webbrowser
import wikipedia
import difflib
import random
import time
import threading
from word import word_dict
from phrase import phrase_dict
from sentence import sentence_dict
from unit1_word import word_dict as unit1_word_dict
from unit1_phrase import phrase_dict as unit1_phrase_dict
from unit1_sentence import sentence_dict as unit1_sentence_dict
from unit2_word import word_dict as unit2_word_dict
from unit2_phrase import phrase_dict as unit2_phrase_dict
from unit2_sentence import sentence_dict as unit2_sentence_dict
from unit3_word import word_dict as unit3_word_dict
from unit3_phrase import phrase_dict as unit3_phrase_dict
from unit3_sentence import sentence_dict as unit3_sentence_dict
from unit4_word import word_dict as unit4_word_dict
from unit4_phrase import phrase_dict as unit4_phrase_dict
from unit4_sentence import sentence_dict as unit4_sentence_dict
from pronunciation_analyzer import PronunciationAnalyzer

def speak(text):
    print(f"Bot: {text}")
    tts = gTTS(text=text, lang='en', slow=False)
    filename = 'voice.mp3'
    tts.save(filename)
    # Sử dụng lệnh hệ thống afplay của macOS để phát âm thanh ổn định hơn
    os.system(f"afplay {filename}")
    # Đợi một chút để đảm bảo âm thanh phát xong hoàn toàn
    time.sleep(0.5)
    # Xóa file sau khi phát xong để tránh lỗi ghi đè hoặc rác
    if os.path.exists(filename):
        os.remove(filename)

def speak_word(text):
    """Phát âm một từ/cụm từ/câu một cách rõ ràng, với tốc độ chậm hơn."""
    print(f"Bot: {text}")
    tts = gTTS(text=text, lang='en', slow=True)
    filename = 'voice.mp3'
    tts.save(filename)
    os.system(f"afplay {filename}")
    time.sleep(0.5)
    if os.path.exists(filename):
        os.remove(filename)

def listen(item_type="word"):
    """Nghe giọng nói người học với đếm ngược thời gian
    
    Args:
        item_type: Loại item - 'word' (từ), 'phrase' (cụm từ), 'sentence' (câu)
                   để điều chỉnh timeout thích hợp
    """
    # Điều chỉnh thời gian timeout dựa trên loại item
    timeout_duration = 7  # timeout tổng cộng (giây)
    phrase_time_limit = 12  # thời gian tối đa phát âm từ một item
    
    if item_type == "word":
        timeout_duration = 7
        phrase_time_limit = 12
    elif item_type == "phrase":
        timeout_duration = 9  # Cho phép lâu hơn để nói cụm từ
        phrase_time_limit = 20
    elif item_type == "sentence":
        timeout_duration = 15  # Cho phép lâu hơn để nói câu đầy đủ
        phrase_time_limit = 45
    
    result = {"text": "", "error": None}
    
    def record_audio():
        """Thread function để ghi âm"""
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                # Tự động điều chỉnh ngưỡng ồn
                r.adjust_for_ambient_noise(source, duration=0.5)
                # phrase_time_limit: Ngắt nếu nói quá dài để tránh treo
                audio = r.listen(source, timeout=timeout_duration, phrase_time_limit=phrase_time_limit)
                text = r.recognize_google(audio, language="en-US")
                result["text"] = text
        except sr.WaitTimeoutError:
            result["error"] = "TIMEOUT"
        except sr.UnknownValueError:
            result["error"] = "UNKNOWN"
        except sr.RequestError as e:
            result["error"] = "REQUEST_ERROR"
        except Exception as e:
            result["error"] = f"ERROR: {str(e)}"
    
    # Bắt đầu thread ghi âm
    thread = threading.Thread(target=record_audio, daemon=True)
    print(f"🎤 Listening... (Hãy nói gì đó bằng tiếng Anh)")
    thread.start()
    
    # Đếm ngược thời gian
    start_time = time.time()
    last_print = timeout_duration
    
    while thread.is_alive():
        elapsed = time.time() - start_time
        remaining = max(0, timeout_duration - elapsed)
        
        # Chỉ in khi remaining thay đổi (mỗi 1 giây)
        if int(remaining) < last_print and int(remaining) >= 0:
            last_print = int(remaining)
            print(f"⏱️  Time remaining: {last_print}s", end="\r", flush=True)
        
        time.sleep(0.1)
    
    thread.join()
    print("Recognizing...       \n")  # Clear line và new line
    
    # Xử lý kết quả
    if result["error"] == "TIMEOUT":
        print("... Time out (Không nghe thấy tiếng động)")
        return ""
    elif result["error"]:
        print(f"... (Không nhận dạng được hoặc có lỗi)")
        return ""
    elif result["text"]:
        print(f"You: {result['text']}")
        return result["text"]
    else:
        print("... (Không nhận dạng được)")
        return ""

def run_training_session(levels, count=None):
    """Chạy phiên luyện tập cho danh sách các cấp độ/chủ đề.
    
    Args:
        levels: Danh sách các cấp độ (level_name, level_dict)
        count: Số lượng từ/cụm từ/câu muốn luyện tập. Nếu None thì luyện tập tất cả."""
    analyzer = PronunciationAnalyzer()
    
    # Dùng dict để theo dõi thống kê từng level
    level_stats = {}
    overall_total = 0
    overall_excellent = 0
    overall_good = 0
    overall_fair = 0
    overall_poor = 0
    
    for level_name, level_data in levels:
        # Khởi tạo thống kê cho level này
        level_stats[level_name] = {
            "total": 0,
            "excellent": 0,
            "good": 0,
            "fair": 0,
            "poor": 0
        }
        
        # Hiển thị thông báo bắt đầu phần học mới
        level_messages = {
            "word": ("📝 STARTING WORD PRONUNCIATION TRAINING", "Bắt đầu luyện tập phát âm Từ vựng"),
            "phrase": ("📚 STARTING PHRASE PRONUNCIATION TRAINING", "Bắt đầu luyện tập phát âm Cụm từ"),
            "sentence": ("📖 STARTING SENTENCE PRONUNCIATION TRAINING", "Bắt đầu luyện tập phát âm Câu")
        }
        
        if level_name in level_messages:
            eng_msg, vn_msg = level_messages[level_name]
            print(f"\n{'='*60}")
            print(f"{eng_msg}")
            print(f"({vn_msg})")
            print(f"{'='*60}\n")
            speak(eng_msg)
            time.sleep(0.5)
        
        # Chuyển đổi dict thành list để có thể giới hạn số lượng
        items = list(level_data.items())
        
        # Nếu count được chỉ định, chọn ngẫu nhiên 'count' items
        if count is not None and count > 0:
            items = random.sample(items, min(count, len(items)))
        
        for target_phrase, meaning in items:
            level_stats[level_name]["total"] += 1
            overall_total += 1
            retry_count = 0
            max_retries = 1
            best_analysis = None
            
            while retry_count <= max_retries:
                # Nói hướng dẫn
                if retry_count == 0:
                    speak(f"Please repeat: {target_phrase}")
                else:
                    speak(f"Let's try again. Please repeat: {target_phrase}")
                
                # Đợi một chút rồi nói từ/cụm từ/câu rõ ràng
                time.sleep(0.3)
                speak_word(target_phrase)
                print(f"\n📖 Meaning (Nghĩa): {meaning}")
                
                user_repeat = listen(item_type=level_name)
                
                if not user_repeat:
                    # Không nhận diện được
                    if retry_count < max_retries:
                        print(f"\n⚠️  Không nhận diện được lần {retry_count + 1}")
                        speak("Sorry, I did not understand. Let me try again.")
                        retry_count += 1
                        continue
                    else:
                        # Đã hết retry
                        print(f"\n❌ Không nhận diện được sau {max_retries + 1} lần cố gắng")
                        speak("Sorry, I could not hear you clearly. Let's move on to the next word.")
                        level_stats[level_name]["poor"] += 1
                        overall_poor += 1
                        break
                else:
                    # Có nhận diện được - phân tích
                    analysis = analyzer.detailed_error_analysis(target_phrase, user_repeat)
                    
                    print(f"\n{'='*60}")
                    print(f"📊 PHÂN TÍCH PHÁT ÂM (Lần {retry_count + 1})")
                    print(f"{'='*60}")
                    print(f"Expected: {analysis['expected']}")
                    print(f"Received: {analysis['received']}")
                    print(f"Similarity: {analysis['similarity']}%")
                    print(f"Quality: {analysis['quality']}")
                    print(f"Feedback: {analysis['feedback']}")
                    
                    # Hiển thị phiên âm quốc tế (IPA) nếu có cho word và phrase
                    if level_name in ["word", "phrase"]:
                        # Import dynamic để lấy IPA
                        try:
                            if level_name == "word":
                                from word import word_ipa_dict
                                ipa = word_ipa_dict.get(target_phrase, "")
                            else:  # phrase
                                from phrase import phrase_ipa_dict
                                ipa = phrase_ipa_dict.get(target_phrase, "")
                            
                            if ipa:
                                print(f"🔤 IPA (Phiên âm quốc tế): /{ipa}/")
                        except (ImportError, KeyError):
                            pass
                    
                    # Hiển thị chi tiết lỗi nếu có
                    if analysis['errors']:
                        print(f"\n🔍 Chi tiết lỗi ({len(analysis['errors'])} lỗi):")
                        for i, error in enumerate(analysis['errors'], 1):
                            error_type = error['type'].upper()
                            if error['type'] == 'substitution':
                                print(f"  {i}. {error_type}: '{error['expected']}' → '{error['received']}'")
                            elif error['type'] == 'deletion':
                                print(f"  {i}. {error_type}: Thiếu '{error['expected']}'")
                            elif error['type'] == 'insertion':
                                print(f"  {i}. {error_type}: Thêm '{error['received']}'")
                    
                    # Tóm tắt lỗi
                    breakdown = analysis['error_breakdown']
                    print(f"\n📈 Tóm tắt: Sai âm ({breakdown['substitutions']}), "
                          f"Thiếu ({breakdown['deletions']}), "
                          f"Thêm ({breakdown['insertions']})")
                    print(f"{'='*60}\n")
                    
                    # Phát âm nhận xét
                    speak(f"I heard: {user_repeat}")
                    speak(analysis['feedback'])
                    
                    # Lưu analysis tốt nhất (lần đầu tiên có nhận diện được)
                    best_analysis = analysis
                    quality = analysis['quality']
                    
                    # Nếu chất lượng không tốt và còn retry, hỏi user có muốn đọc lại không
                    if quality == "Poor" and retry_count < max_retries:
                        print("\n🔄 Phát âm của bạn chưa tốt. Bạn có muốn đọc lại không? (y/n)")
                        retry_choice = input("Nhập lựa chọn (y/n): ").strip().lower()
                        if retry_choice == 'y':
                            speak("Okay, let's try again.")
                            retry_count += 1
                            continue
                    
                    # Cập nhật thống kê chất lượng - cả level và overall
                    if quality == "Excellent":
                        level_stats[level_name]["excellent"] += 1
                        overall_excellent += 1
                    elif quality == "Good":
                        level_stats[level_name]["good"] += 1
                        overall_good += 1
                    elif quality == "Fair":
                        level_stats[level_name]["fair"] += 1
                        overall_fair += 1
                    else:
                        level_stats[level_name]["poor"] += 1
                        overall_poor += 1
                    
                    # Thoát khỏi vòng lặp retry
                    break
    
    # Báo cáo tổng kết - chi tiết từng level
    if overall_total > 0:
        print(f"\n{'='*60}")
        print(f"📊 BÁO CÁO TỔNG KẾT PHIÊN LUYỆN TẬP")
        print(f"{'='*60}\n")
        
        # Hiển thị thống kê cho từng level
        level_names = ["word", "phrase", "sentence"]
        level_display_names = {
            "word": "📝 WORDS (Từ vựng)",
            "phrase": "📚 PHRASES (Cụm từ)",
            "sentence": "📖 SENTENCES (Câu)"
        }
        
        for level_name in level_names:
            if level_name in level_stats and level_stats[level_name]["total"] > 0:
                stats = level_stats[level_name]
                total = stats["total"]
                excellent = stats["excellent"]
                good = stats["good"]
                fair = stats["fair"]
                poor = stats["poor"]
                
                # Tính độ chính xác cho level này
                if total > 0:
                    accuracy = round((excellent + good) / total * 100, 1)
                else:
                    accuracy = 0.0
                
                print(f"{level_display_names[level_name]}")
                print(f"Tổng số: {total}")
                print(f"  Excellent: {excellent}  ⭐⭐⭐⭐⭐")
                print(f"  Good:      {good}  ⭐⭐⭐⭐")
                print(f"  Fair:      {fair}  ⭐⭐⭐")
                print(f"  Poor:      {poor}  ⭐")
                print(f"  Độ chính xác: {accuracy}%")
                print()
        
        # Tính độ chính xác tổng
        overall_accuracy = round((overall_excellent + overall_good) / overall_total * 100, 1) if overall_total > 0 else 0
        
        # Hiển thị tổng kết
        print(f"{'='*60}")
        print(f"🎓 TỔNG KẾT CHUNG")
        print(f"{'='*60}")
        print(f"Tổng cộng: {overall_total} items")
        print(f"  Excellent: {overall_excellent}  ⭐⭐⭐⭐⭐")
        print(f"  Good:      {overall_good}  ⭐⭐⭐⭐")
        print(f"  Fair:      {overall_fair}  ⭐⭐⭐")
        print(f"  Poor:      {overall_poor}  ⭐")
        print(f"\nĐộ chính xác tổng: {overall_accuracy}%")
        print(f"{'='*60}\n")
        
        speak(f"Training complete. Overall accuracy: {overall_accuracy} percent.")

def show_menu():
    """Hiển thị menu chọn Unit."""
    print("\n" + "="*60)
    print("CHƯƠNG TRÌNH HỌC PHÁT ÂM TIẾNG ANH - ENGLISH PRONUNCIATION")
    print("="*60)
    print("\nVui lòng chọn Unit muốn luyện tập (Choose Unit):")
    print("="*60)
    print("  1 - Unit 1: Military Bridge-Road Building (Cầu Đường Quân Sự)")
    print("  2 - Unit 2: River Crossing (Vượt Sông)")
    print("  3 - Unit 3: Military Engineering Vehicles (Xe Máy Công Binh)")
    print("  4 - Unit 4: Bomb - Mine, Fortifications (Bom Mìn, Công Sự)")
    print("  G - General: NATO & Military Terms (Từ vựng chung)")
    print("  0 - Exit (Thoát)")
    print("="*60)
    
    try:
        choice = input("\nNhập lựa chọn của bạn (Enter your choice): ").strip().upper()
        return choice
    except KeyboardInterrupt:
        print("\n\nProgram terminated.")
        return '0'

def get_count():
    """Hỏi người dùng số lượng từ muốn luyện tập."""
    print("\n📚 Số lượng từ muốn luyện tập (How many items do you want to practice?)")
    while True:
        try:
            count_str = input("Nhập số từ (Enter number, or 0 for all): ").strip()
            count = int(count_str)
            if count >= 0:
                return count if count > 0 else None
            else:
                print("❌ Vui lòng nhập số lớn hơn 0 (Please enter a number greater than 0)")
        except ValueError:
            print("❌ Vui lòng nhập một số hợp lệ (Please enter a valid number)")

if __name__ == "__main__":
    try:
        while True:
            choice = show_menu()
            
            if choice == '1':
                # Unit 1: Complete training (Words -> Phrases -> Sentences)
                print("\n" + "="*60)
                print("✅ UNIT 1: MILITARY BRIDGE-ROAD BUILDING (CẦU ĐƯỜNG QUÂN SỰ)")
                print("="*60)
                print("\nLuyện tập: Từ → Cụm từ → Câu")
                count = get_count()
                speak("Unit one training. We will start with words, then phrases, then sentences.")
                training_levels = [
                    ("word", unit1_word_dict),
                    ("phrase", unit1_phrase_dict),
                    ("sentence", unit1_sentence_dict)
                ]
                run_training_session(training_levels, count=count)
                speak("Unit one training complete. Excellent work!")
                print("="*60 + "\n")
                
            elif choice == '2':
                # Unit 2: Complete training (Words -> Phrases -> Sentences)
                print("\n" + "="*60)
                print("✅ UNIT 2: RIVER CROSSING (VƯỢT SÔNG)")
                print("="*60)
                print("\nLuyện tập: Từ → Cụm từ → Câu")
                count = get_count()
                speak("Unit two training. We will start with words, then phrases, then sentences.")
                training_levels = [
                    ("word", unit2_word_dict),
                    ("phrase", unit2_phrase_dict),
                    ("sentence", unit2_sentence_dict)
                ]
                run_training_session(training_levels, count=count)
                speak("Unit two training complete. Excellent work!")
                print("="*60 + "\n")
                
            elif choice == 'G':
                # General training (Words -> Phrases -> Sentences)
                print("\n" + "="*60)
                print("✅ GENERAL: NATO & MILITARY TERMS")
                print("="*60)
                print("\nLuyện tập: Từ → Cụm từ → Câu")
                count = get_count()
                speak("General training. We will start with words, then phrases, then sentences.")
                training_levels = [
                    ("word", word_dict),
                    ("phrase", phrase_dict),
                    ("sentence", sentence_dict)
                ]
                run_training_session(training_levels, count=count)
                speak("General training complete. Excellent work!")
                print("="*60 + "\n")
                
            elif choice == '3':
                # Unit 3: Complete training (Words -> Phrases -> Sentences)
                print("\n" + "="*60)
                print("✅ UNIT 3: MILITARY ENGINEERING VEHICLES (XE MÁY CÔNG BINH)")
                print("="*60)
                print("\nLuyện tập: Từ → Cụm từ → Câu")
                count = get_count()
                speak("Unit three training. We will start with words, then phrases, then sentences.")
                training_levels = [
                    ("word", unit3_word_dict),
                    ("phrase", unit3_phrase_dict),
                    ("sentence", unit3_sentence_dict)
                ]
                run_training_session(training_levels, count=count)
                speak("Unit three training complete. Excellent work!")
                print("="*60 + "\n")
                
            elif choice == '4':
                # Unit 4: Complete training (Words -> Phrases -> Sentences)
                print("\n" + "="*60)
                print("✅ UNIT 4: BOMB - MINE, FORTIFICATIONS (BOM MÌN, CÔNG SỰ)")
                print("="*60)
                print("\nLuyện tập: Từ → Cụm từ → Câu")
                count = get_count()
                speak("Unit four training. We will start with words, then phrases, then sentences.")
                training_levels = [
                    ("word", unit4_word_dict),
                    ("phrase", unit4_phrase_dict),
                    ("sentence", unit4_sentence_dict)
                ]
                run_training_session(training_levels, count=count)
                speak("Unit four training complete. Excellent work!")
                print("="*60 + "\n")
                
            elif choice == '0':
                speak("Thank you for using the English pronunciation trainer. Goodbye!")
                print("👋 Tạm biệt (Goodbye)!\n")
                break
                
            else:
                print("❌ Lựa chọn không hợp lệ (Invalid choice). Vui lòng chọn lại.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated. Goodbye!\n")