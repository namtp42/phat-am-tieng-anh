"""
Module phân tích lỗi phát âm tiếng Anh
Cung cấp các hàm để phát hiện và đánh giá lỗi phát âm
"""

import difflib
from difflib import SequenceMatcher


class PronunciationError:
    """Lớp biểu diễn một lỗi phát âm"""
    def __init__(self, error_type, position, expected, received, description=""):
        self.error_type = error_type  # 'substitution', 'deletion', 'insertion'
        self.position = position
        self.expected = expected
        self.received = received
        self.description = description
    
    def __repr__(self):
        return f"{self.error_type.upper()}: '{self.expected}' → '{self.received}' at pos {self.position}"
    
    def to_dict(self):
        return {
            'type': self.error_type,
            'position': self.position,
            'expected': self.expected,
            'received': self.received,
            'description': self.description
        }


class PronunciationAnalyzer:
    """Phân tích lỗi phát âm"""
    
    @staticmethod
    def levenshtein_distance(s1, s2):
        """Tính Levenshtein distance giữa hai chuỗi"""
        if len(s1) < len(s2):
            return PronunciationAnalyzer.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def similarity_score(expected, received):
        """Tính độ giống nhau giữa thực tế và dự kiến (0-100%)"""
        matcher = SequenceMatcher(None, expected.lower(), received.lower())
        ratio = matcher.ratio()
        return round(ratio * 100, 2)
    
    @staticmethod
    def detailed_error_analysis(expected, received):
        """Phân tích chi tiết các lỗi phát âm
        
        Args:
            expected: Chuỗi phát âm đúng
            received: Chuỗi phát âm của người học
            
        Returns:
            dict: Chứa thông tin lỗi và đánh giá
        """
        expected = expected.lower().strip()
        received = received.lower().strip()
        
        errors = []
        
        # Sử dụng SequenceMatcher để tìm alignment
        matcher = SequenceMatcher(None, expected, received)
        matching_blocks = matcher.get_matching_blocks()
        
        # Phân tích từng khác biệt
        expected_pos = 0
        received_pos = 0
        
        for block in matching_blocks:
            # Kiểm tra các phần không khớp trước block này
            if expected_pos < block.a or received_pos < block.b:
                exp_segment = expected[expected_pos:block.a]
                rec_segment = received[received_pos:block.b]
                
                # Phân loại lỗi
                if exp_segment and not rec_segment:
                    # Deletion (thiếu âm)
                    for i, char in enumerate(exp_segment):
                        errors.append(PronunciationError(
                            'deletion',
                            expected_pos + i,
                            char,
                            '',
                            f'Thiếu âm: {char}'
                        ))
                elif rec_segment and not exp_segment:
                    # Insertion (thêm âm)
                    for i, char in enumerate(rec_segment):
                        errors.append(PronunciationError(
                            'insertion',
                            expected_pos,
                            '',
                            char,
                            f'Thêm âm: {char}'
                        ))
                elif exp_segment and rec_segment:
                    # Substitution (sai âm)
                    for i, (e_char, r_char) in enumerate(zip(exp_segment, rec_segment)):
                        if e_char != r_char:
                            errors.append(PronunciationError(
                                'substitution',
                                expected_pos + i,
                                e_char,
                                r_char,
                                f'Sai âm: {e_char} → {r_char}'
                            ))
            
            # Cập nhật vị trí
            expected_pos = block.a + block.size
            received_pos = block.b + block.size
        
        # Tính các chỉ số đánh giá
        similarity = PronunciationAnalyzer.similarity_score(expected, received)
        edit_distance = PronunciationAnalyzer.levenshtein_distance(expected, received)
        
        # Đánh giá chất lượng
        if similarity >= 95:
            quality = "Excellent"
            feedback = "Phát âm rất tốt!"
        elif similarity >= 85:
            quality = "Good"
            feedback = "Phát âm tốt, nhưng còn một vài lỗi nhỏ."
        elif similarity >= 70:
            quality = "Fair"
            feedback = "Phát âm chưa chính xác, cần cải thiện."
        else:
            quality = "Poor"
            feedback = "Phát âm cần nhiều cải thiện."
        
        return {
            'expected': expected,
            'received': received,
            'similarity': similarity,
            'edit_distance': edit_distance,
            'errors': [e.to_dict() for e in errors],
            'error_count': len(errors),
            'quality': quality,
            'feedback': feedback,
            'error_breakdown': {
                'substitutions': len([e for e in errors if e.error_type == 'substitution']),
                'deletions': len([e for e in errors if e.error_type == 'deletion']),
                'insertions': len([e for e in errors if e.error_type == 'insertion']),
            }
        }
    
    @staticmethod
    def get_detailed_feedback(analysis_result):
        """Tạo feedback chi tiết dựa trên kết quả phân tích"""
        result = analysis_result
        feedback_lines = [
            f"📊 Điểm tương đồng: {result['similarity']}%",
            f"🎯 Chất lượng phát âm: {result['quality']}",
            f"💬 Nhận xét: {result['feedback']}",
        ]
        
        if result['errors']:
            feedback_lines.append("\n🔍 Chi tiết lỗi:")
            for i, error in enumerate(result['errors'], 1):
                error_info = error
                if isinstance(error, dict):
                    msg = f"  {i}. {error_info['type'].upper()}: "
                    if error_info['type'] == 'substitution':
                        msg += f"'{error_info['expected']}' → '{error_info['received']}'"
                    elif error_info['type'] == 'deletion':
                        msg += f"Thiếu: '{error_info['expected']}'"
                    elif error_info['type'] == 'insertion':
                        msg += f"Thêm: '{error_info['received']}'"
                    feedback_lines.append(msg)
        
        # Tóm tắt lỗi
        breakdown = result['error_breakdown']
        if breakdown['substitutions'] + breakdown['deletions'] + breakdown['insertions'] > 0:
            feedback_lines.append(f"\n📈 Tóm tắt: Sai âm ({breakdown['substitutions']}), "
                                f"Thiếu ({breakdown['deletions']}), "
                                f"Thêm ({breakdown['insertions']})")
        
        return "\n".join(feedback_lines)


if __name__ == "__main__":
    # Test
    analyzer = PronunciationAnalyzer()
    
    test_cases = [
        ("hello", "helo"),
        ("perfect", "perfekt"),
        ("world", "word"),
    ]
    
    for expected, received in test_cases:
        print(f"\n{'='*60}")
        print(f"Expected: {expected}")
        print(f"Received: {received}")
        print('='*60)
        result = analyzer.detailed_error_analysis(expected, received)
        feedback = analyzer.get_detailed_feedback(result)
        print(feedback)
