"""
Flask API Backend cho hệ thống phân tích lỗi phát âm tiếng Anh - Integrated with PostgreSQL
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from pronunciation_analyzer import PronunciationAnalyzer
from database import SessionLocal, User, TrainingSession, UserStats, init_db
import json
import time

app = Flask(__name__)

# CORS configuration - allow all origins for now
CORS(app, resources={r"/api/*": {"origins": "*"}})

analyzer = PronunciationAnalyzer()

# Initialize database trên startup
@app.before_request
def startup():
    try:
        init_db()
    except:
        pass


# ==================== USER ENDPOINTS ====================

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """
    Đăng ký user mới
    
    Request: {"user_id": "user123", "username": "John", "email": "john@example.com"}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id is required'}), 400
        
        db = SessionLocal()
        
        # Check if user exists
        existing = db.query(User).filter(User.user_id == user_id).first()
        if existing:
            db.close()
            return jsonify({'success': False, 'error': 'User already exists'}), 409
        
        # Create user
        user = User(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email')
        )
        
        # Create stats
        stats = UserStats(user_id=user_id)
        
        db.add(user)
        db.add(stats)
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'data': {'user_id': user_id, 'created_at': user.created_at.isoformat()}
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Lấy thông tin user"""
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            db.close()
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        result = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'total_sessions': len(user.sessions)
        }
        
        db.close()
        return jsonify({'success': True, 'data': result}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== TRAINING ENDPOINTS ====================

@app.route('/api/analyze', methods=['POST'])
def analyze_pronunciation():
    """
    Phân tích lỗi phát âm đơn lẻ + save vào database
    
    Request: {"expected": "hello", "received": "helo", "user_id": "user123"}
    """
    try:
        data = request.get_json()
        expected = data.get('expected', '').strip()
        received = data.get('received', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not expected or not received:
            return jsonify({'success': False, 'error': 'expected and received are required'}), 400
        
        # Phân tích
        analysis = analyzer.detailed_error_analysis(expected, received)
        
        # Save to database nếu user_id tồn tại
        if user_id != 'anonymous':
            db = SessionLocal()
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                # Sẽ được gọi từ /api/train endpoint
                pass
            db.close()
        
        return jsonify({
            'success': True,
            'data': analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/train/session', methods=['POST'])
def start_training_session():
    """
    Bắt đầu session training
    
    Request: {
        "user_id": "user123",
        "unit": 1,
        "level": "word",
        "item_count": 10
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        unit = data.get('unit', 0)
        level = data.get('level', 'word').lower()
        item_count = data.get('item_count', 10)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id is required'}), 400
        
        if level not in ['word', 'phrase', 'sentence']:
            return jsonify({'success': False, 'error': 'level must be word, phrase, or sentence'}), 400
        
        db = SessionLocal()
        
        # Check user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            db.close()
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Create training session
        session = TrainingSession(
            user_id=user_id,
            unit=unit,
            level=level,
            item_count=item_count,
            total_items=item_count,
            details={}
        )
        
        db.add(session)
        db.commit()
        session_id = session.id
        db.close()
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session_id,
                'user_id': user_id,
                'unit': unit,
                'level': level,
                'item_count': item_count
            }
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/train/session/<int:session_id>/record', methods=['POST'])
def record_item_result(session_id):
    """
    Ghi lại kết quả của 1 item trong session
    
    Request: {
        "user_id": "user123",
        "item": "hello",
        "expected": "hello",
        "received": "helo",
        "similarity": 92.5
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        item = data.get('item', '')
        expected = data.get('expected', '').strip()
        received = data.get('received', '').strip()
        similarity = data.get('similarity', 0)
        
        db = SessionLocal()
        session = db.query(TrainingSession).filter(
            TrainingSession.id == session_id,
            TrainingSession.user_id == user_id
        ).first()
        
        if not session:
            db.close()
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Phân tích
        analysis = analyzer.detailed_error_analysis(expected, received)
        quality = analysis['quality']
        
        # Update session
        if session.details is None:
            session.details = {}
        
        session.details[item] = {
            'expected': expected,
            'received': received,
            'similarity': similarity,
            'quality': quality
        }
        
        # Update counts
        if quality == 'Excellent':
            session.excellent += 1
        elif quality == 'Good':
            session.good += 1
        elif quality == 'Fair':
            session.fair += 1
        else:
            session.poor += 1
        
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session_id,
                'item': item,
                'quality': quality,
                'similarity': similarity
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/train/session/<int:session_id>/finish', methods=['POST'])
def finish_training_session(session_id):
    """
    Kết thúc session & tính toán stats
    
    Request: {"user_id": "user123", "duration_seconds": 300}
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        duration_seconds = data.get('duration_seconds', 0)
        
        db = SessionLocal()
        session = db.query(TrainingSession).filter(
            TrainingSession.id == session_id,
            TrainingSession.user_id == user_id
        ).first()
        
        if not session:
            db.close()
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Calculate average
        total = session.excellent + session.good + session.fair + session.poor
        if total > 0:
            session.average_score = (
                session.excellent * 100 +
                session.good * 87.5 +
                session.fair * 77.5 +
                session.poor * 50
            ) / (total * 100)
        
        session.duration_seconds = duration_seconds
        
        # Update user stats
        stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        if stats:
            stats.total_sessions += 1
            stats.total_training_seconds += duration_seconds
            
            # Update per-level stats
            if session.level == 'word':
                stats.word_excellent += session.excellent
                stats.word_good += session.good
                stats.word_fair += session.fair
                stats.word_poor += session.poor
                word_total = session.excellent + session.good + session.fair + session.poor
                if word_total > 0:
                    stats.word_avg_score = (stats.word_excellent * 100 + stats.word_good * 87.5 + 
                                           stats.word_fair * 77.5 + stats.word_poor * 50) / (word_total * 100)
            
            elif session.level == 'phrase':
                stats.phrase_excellent += session.excellent
                stats.phrase_good += session.good
                stats.phrase_fair += session.fair
                stats.phrase_poor += session.poor
                phrase_total = session.excellent + session.good + session.fair + session.poor
                if phrase_total > 0:
                    stats.phrase_avg_score = (stats.phrase_excellent * 100 + stats.phrase_good * 87.5 + 
                                             stats.phrase_fair * 77.5 + stats.phrase_poor * 50) / (phrase_total * 100)
            
            elif session.level == 'sentence':
                stats.sentence_excellent += session.excellent
                stats.sentence_good += session.good
                stats.sentence_fair += session.fair
                stats.sentence_poor += session.poor
                sentence_total = session.excellent + session.good + session.fair + session.poor
                if sentence_total > 0:
                    stats.sentence_avg_score = (stats.sentence_excellent * 100 + stats.sentence_good * 87.5 + 
                                               stats.sentence_fair * 77.5 + stats.sentence_poor * 50) / (sentence_total * 100)
        
        db.commit()
        
        result = {
            'session_id': session_id,
            'user_id': user_id,
            'unit': session.unit,
            'level': session.level,
            'excellent': session.excellent,
            'good': session.good,
            'fair': session.fair,
            'poor': session.poor,
            'average_score': round(session.average_score, 2),
            'duration_seconds': duration_seconds
        }
        
        db.close()
        return jsonify({'success': True, 'data': result}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== STATISTICS ENDPOINTS ====================

@app.route('/api/stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    """Lấy tất cả stats của user"""
    try:
        db = SessionLocal()
        stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        
        if not stats:
            db.close()
            return jsonify({'success': False, 'error': 'Stats not found'}), 404
        
        result = {
            'user_id': user_id,
            'total_sessions': stats.total_sessions,
            'total_training_seconds': stats.total_training_seconds,
            'word': {
                'excellent': stats.word_excellent,
                'good': stats.word_good,
                'fair': stats.word_fair,
                'poor': stats.word_poor,
                'avg_score': round(stats.word_avg_score, 2)
            },
            'phrase': {
                'excellent': stats.phrase_excellent,
                'good': stats.phrase_good,
                'fair': stats.phrase_fair,
                'poor': stats.phrase_poor,
                'avg_score': round(stats.phrase_avg_score, 2)
            },
            'sentence': {
                'excellent': stats.sentence_excellent,
                'good': stats.sentence_good,
                'fair': stats.sentence_fair,
                'poor': stats.sentence_poor,
                'avg_score': round(stats.sentence_avg_score, 2)
            }
        }
        
        db.close()
        return jsonify({'success': True, 'data': result}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats/<user_id>/sessions', methods=['GET'])
def get_user_sessions(user_id):
    """Lấy tất cả training sessions của user"""
    try:
        limit = int(request.args.get('limit', 50))
        
        db = SessionLocal()
        sessions = db.query(TrainingSession).filter(
            TrainingSession.user_id == user_id
        ).order_by(TrainingSession.created_at.desc()).limit(limit).all()
        
        result = []
        for session in sessions:
            result.append({
                'session_id': session.id,
                'unit': session.unit,
                'level': session.level,
                'item_count': session.item_count,
                'excellent': session.excellent,
                'good': session.good,
                'fair': session.fair,
                'poor': session.poor,
                'average_score': round(session.average_score, 2),
                'duration_seconds': session.duration_seconds,
                'created_at': session.created_at.isoformat()
            })
        
        db.close()
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== HEALTH & INFO ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái API"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Pronunciation Analyzer API (PostgreSQL)'
        }), 200
    except:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/info', methods=['GET'])
def api_info():
    """Thông tin về API"""
    return jsonify({
        'service': 'Military English Pronunciation Trainer API',
        'version': '2.0',
        'database': 'PostgreSQL',
        'endpoints': {
            'users': [
                'POST /api/users/register',
                'GET /api/users/<user_id>'
            ],
            'training': [
                'POST /api/train/session',
                'POST /api/train/session/<session_id>/record',
                'POST /api/train/session/<session_id>/finish'
            ],
            'stats': [
                'GET /api/stats/<user_id>',
                'GET /api/stats/<user_id>/sessions'
            ]
        }
    }), 200


if __name__ == '__main__':
    # Production configuration
    port = int(os.getenv('PORT', 5003))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    app.run(debug=debug, host=host, port=port, threaded=True)
