"""
Test script để demo API với PostgreSQL
Mô phỏng training session của 100 users
"""

import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_BASE = "http://localhost:5001"

# ==================== Helper Functions ====================

def register_user(user_id, username):
    """Đăng ký 1 user"""
    url = f"{API_BASE}/api/users/register"
    payload = {
        "user_id": user_id,
        "username": username,
        "email": f"{user_id}@example.com"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code in [201, 409]:  # 201 = created, 409 = already exists
            return True
        return False
    except:
        return False


def start_session(user_id, unit, level, item_count):
    """Bắt đầu training session"""
    url = f"{API_BASE}/api/train/session"
    payload = {
        "user_id": user_id,
        "unit": unit,
        "level": level,
        "item_count": item_count
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 201:
            return response.json()['data']['session_id']
        return None
    except:
        return None


def record_item(user_id, session_id, item, expected, received, similarity):
    """Ghi lại kết quả của 1 item"""
    url = f"{API_BASE}/api/train/session/{session_id}/record"
    payload = {
        "user_id": user_id,
        "item": item,
        "expected": expected,
        "received": received,
        "similarity": similarity
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except:
        return False


def finish_session(user_id, session_id, duration):
    """Kết thúc training session"""
    url = f"{API_BASE}/api/train/session/{session_id}/finish"
    payload = {
        "user_id": user_id,
        "duration_seconds": duration
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except:
        return False


def get_user_stats(user_id):
    """Lấy stats của user"""
    url = f"{API_BASE}/api/stats/{user_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()['data']
        return None
    except:
        return None


# ==================== Test Functions ====================

def simulate_user_training(user_id, user_num):
    """
    Mô phỏng 1 user làm training
    - Đăng ký
    - Làm 1 session word (10 items)
    - Lấy stats
    """
    username = f"User{user_num}"
    
    # Step 1: Đăng ký
    if not register_user(user_id, username):
        return {'user_id': user_id, 'success': False, 'error': 'Registration failed'}
    
    # Step 2: Bắt đầu session
    session_id = start_session(user_id, unit=1, level='word', item_count=10)
    if not session_id:
        return {'user_id': user_id, 'success': False, 'error': 'Session creation failed'}
    
    # Step 3: Ghi lại 10 items
    test_items = [
        ("hello", "hello", "helo", 92.5),
        ("world", "world", "wrld", 88.5),
        ("military", "military", "militery", 85.0),
        ("bridge", "bridge", "brige", 90.0),
        ("engineering", "engineering", "enginering", 82.0),
        ("road", "road", "rode", 91.0),
        ("river", "river", "riber", 87.5),
        ("crossing", "crossing", "crssing", 80.0),
        ("vehicle", "vehicle", "vehicul", 86.5),
        ("fortification", "fortification", "fortifycation", 79.0)
    ]
    
    for item, expected, received, similarity in test_items:
        if not record_item(user_id, session_id, item, expected, received, similarity):
            return {'user_id': user_id, 'success': False, 'error': f'Failed to record {item}'}
    
    # Step 4: Kết thúc session
    if not finish_session(user_id, session_id, duration=240):
        return {'user_id': user_id, 'success': False, 'error': 'Failed to finish session'}
    
    # Step 5: Lấy stats
    stats = get_user_stats(user_id)
    
    return {
        'user_id': user_id,
        'success': True,
        'username': username,
        'session_id': session_id,
        'stats': stats
    }


# ==================== Main Test ====================

def test_single_user():
    """Test 1 user"""
    print("=" * 60)
    print("TEST 1: Single User Training")
    print("=" * 60)
    
    result = simulate_user_training('test_user_001', 1)
    
    if result['success']:
        print(f"✅ User {result['user_id']} training completed")
        print(f"   Session ID: {result['session_id']}")
        stats = result['stats']
        if stats:
            print(f"   Word Stats: {stats['word']}")
            print(f"   Total Sessions: {stats['total_sessions']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print()


def test_100_users_concurrent():
    """
    Test 100 users training simultaneously (concurrent)
    Đây là mô phỏng cho 100 users sử dụng app cùng lúc
    """
    print("=" * 60)
    print("TEST 2: 100 Users Concurrent Training")
    print("=" * 60)
    
    num_users = 100
    results = []
    
    print(f"Starting {num_users} concurrent training sessions...")
    start_time = time.time()
    
    # Sử dụng ThreadPoolExecutor để chạy concurrent
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {}
        for i in range(1, num_users + 1):
            user_id = f'user_{i:03d}'
            future = executor.submit(simulate_user_training, user_id, i)
            futures[future] = user_id
        
        # Collect results
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"✅ {result['user_id']} done")
            else:
                print(f"❌ {result['user_id']}: {result['error']}")
    
    elapsed = time.time() - start_time
    
    # Statistics
    successful = len([r for r in results if r['success']])
    failed = len(results) - successful
    
    print()
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Users: {num_users}")
    print(f"Successful: {successful} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {successful/num_users*100:.1f}%")
    print(f"Total Time: {elapsed:.2f} seconds")
    print(f"Average Time per User: {elapsed/num_users:.2f} seconds")
    print()
    
    # Sample stats from first successful user
    for result in results:
        if result['success'] and result.get('stats'):
            print("Sample User Stats (from first user):")
            print(json.dumps(result['stats'], indent=2))
            break


def test_health():
    """Test API health"""
    print("Testing API health...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"✅ Database: {data['database']}")
        else:
            print(f"❌ API returned {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print(f"   Make sure API is running: python api.py")


if __name__ == '__main__':
    print()
    print("🚀 PRONUNCIATION TRAINER API TEST")
    print()
    
    # Check health first
    test_health()
    print()
    
    # Run tests
    test_single_user()
    test_100_users_concurrent()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
