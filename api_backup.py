"""
Flask API Backend cho hệ thống phân tích lỗi phát âm tiếng Anh
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from pronunciation_analyzer import PronunciationAnalyzer

app = Flask(__name__)
CORS(app)

# Database để lưu lịch sử (có thể thay bằng database thực tế)
analysis_history = []
analyzer = PronunciationAnalyzer()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Pronunciation Analyzer API'
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_pronunciation():
    """
    Phân tích lỗi phát âm
    
    Request body:
    {
        "expected": "hello",
        "received": "helo",
        "user_id": "user123" (optional)
    }
    
    Response:
    {
        "success": true,
        "data": {
            "expected": "hello",
            "received": "helo",
            "similarity": 80.5,
            "edit_distance": 1,
            "quality": "Good",
            "feedback": "...",
            "errors": [...],
            "error_breakdown": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data or 'expected' not in data or 'received' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: expected, received'
            }), 400
        
        expected = data.get('expected', '').strip()
        received = data.get('received', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not expected or not received:
            return jsonify({
                'success': False,
                'error': 'Expected and received text cannot be empty'
            }), 400
        
        # Phân tích
        analysis = analyzer.detailed_error_analysis(expected, received)
        
        # Lưu vào lịch sử
        record = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'analysis': analysis
        }
        analysis_history.append(record)
        
        return jsonify({
            'success': True,
            'data': analysis,
            'timestamp': record['timestamp']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Phân tích nhiều từ seqently
    
    Request body:
    {
        "items": [
            {"expected": "hello", "received": "helo"},
            {"expected": "world", "received": "word"}
        ],
        "user_id": "user123" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: items'
            }), 400
        
        items = data.get('items', [])
        user_id = data.get('user_id', 'anonymous')
        
        if not isinstance(items, list):
            return jsonify({
                'success': False,
                'error': 'Items must be a list'
            }), 400
        
        results = []
        statistics = {
            'total': len(items),
            'excellent': 0,
            'good': 0,
            'fair': 0,
            'poor': 0
        }
        
        for item in items:
            if 'expected' not in item or 'received' not in item:
                continue
            
            analysis = analyzer.detailed_error_analysis(
                item['expected'],
                item['received']
            )
            
            results.append(analysis)
            
            # Cập nhật thống kê
            quality = analysis['quality']
            if quality == 'Excellent':
                statistics['excellent'] += 1
            elif quality == 'Good':
                statistics['good'] += 1
            elif quality == 'Fair':
                statistics['fair'] += 1
            else:
                statistics['poor'] += 1
        
        # Lưu vào lịch sử
        record = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'batch_size': len(results),
            'results': results,
            'statistics': statistics
        }
        analysis_history.append(record)
        
        return jsonify({
            'success': True,
            'data': {
                'results': results,
                'statistics': statistics
            },
            'timestamp': record['timestamp']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Lấy thống kê tổng hợp"""
    try:
        user_id = request.args.get('user_id', None)
        
        # Lọc by user_id nếu cần
        if user_id:
            records = [r for r in analysis_history if r.get('user_id') == user_id]
        else:
            records = analysis_history
        
        total_analyses = len(records)
        
        # Tính thống kê
        stats = {
            'total_analyses': total_analyses,
            'excellent': 0,
            'good': 0,
            'fair': 0,
            'poor': 0,
            'average_similarity': 0
        }
        
        total_similarity = 0
        count_for_avg = 0
        
        for record in records:
            if 'analysis' in record:
                quality = record['analysis'].get('quality')
                similarity = record['analysis'].get('similarity', 0)
                
                if quality == 'Excellent':
                    stats['excellent'] += 1
                elif quality == 'Good':
                    stats['good'] += 1
                elif quality == 'Fair':
                    stats['fair'] += 1
                else:
                    stats['poor'] += 1
                
                total_similarity += similarity
                count_for_avg += 1
        
        if count_for_avg > 0:
            stats['average_similarity'] = round(total_similarity / count_for_avg, 2)
        
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Lấy lịch sử phân tích"""
    try:
        user_id = request.args.get('user_id', None)
        limit = int(request.args.get('limit', 50))
        
        # Lọc by user_id nếu cần
        if user_id:
            records = [r for r in analysis_history if r.get('user_id') == user_id]
        else:
            records = analysis_history
        
        # Lấy 'limit' bản ghi gần nhất
        records = records[-limit:] if limit > 0 else records
        
        return jsonify({
            'success': True,
            'data': records,
            'count': len(records),
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export', methods=['GET'])
def export_history():
    """Export lịch sử dưới dạng JSON"""
    try:
        user_id = request.args.get('user_id', None)
        
        if user_id:
            records = [r for r in analysis_history if r.get('user_id') == user_id]
        else:
            records = analysis_history
        
        return jsonify({
            'success': True,
            'data': records,
            'count': len(records),
            'exported_at': datetime.now().isoformat()
        }), 200, {
            'Content-Disposition': f'attachment;filename=pronunciation_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        }
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Xóa toàn bộ lịch sử (chỉ cho phép trong development)"""
    global analysis_history
    try:
        # Cảnh báo: chỉ nên sử dụng trong development, không phải production
        auth_token = request.headers.get('Authorization', '')
        if auth_token != 'Bearer dev-token':
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 401
        
        count = len(analysis_history)
        analysis_history = []
        
        return jsonify({
            'success': True,
            'message': f'Cleared {count} records',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("Starting Pronunciation Analyzer API...")
    print("API documentation:")
    print("  POST /api/analyze - Analyze pronunciation")
    print("  POST /api/batch-analyze - Analyze multiple words")
    print("  GET /api/stats - Get statistics")
    print("  GET /api/history - Get analysis history")
    print("  GET /api/export - Export history as JSON")
    print("  GET /api/health - Health check")
    
    # Chạy với debug=True cho phát triển, debug=False cho production
    app.run(debug=True, host='0.0.0.0', port=5000)
