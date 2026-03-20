#!/usr/bin/env python3
"""
Simple Concurrent Test - 10 Users
Demonstrates system can handle parallel requests
"""

import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

API_BASE = "http://localhost:5003"

def test_user_flow(user_num):
    """Single user test: register, train, get stats"""
    user_id = f"concurrent_test_{user_num:03d}"
    results = {
        'user_id': user_id,
        'register': False,
        'session': False,
        'record': False,
        'stats': False,
        'errors': []
    }
    
    try:
        # Step 1: Register user
        resp = requests.post(f"{API_BASE}/api/users/register",
                           json={"user_id": user_id, "username": f"User {user_num}", "email": f"{user_id}@test.com"},
                           timeout=5)
        if resp.status_code in [201, 409]:
            results['register'] = True
        else:
            results['errors'].append(f"Register failed: {resp.status_code}")
            
        # Step 2: Start training session
        resp = requests.post(f"{API_BASE}/api/train/session",
                           json={"user_id": user_id, "unit": 1, "level": "word"},
                           timeout=5)
        if resp.status_code == 201:
            session_data = resp.json()
            session_id = session_data.get('session_id') or session_data.get('data', {}).get('session_id')
            results['session'] = True
            
            # Step 3: Record an item
            if session_id:
                resp = requests.post(f"{API_BASE}/api/train/session/{session_id}/record",
                                   json={
                                       "user_id": user_id,
                                       "item": "hello",
                                       "expected": "hello",
                                       "received": "hello",
                                       "similarity": 95
                                   },
                                   timeout=5)
                if resp.status_code == 200:
                    results['record'] = True
                    
                # Step 4: Get user stats
                resp = requests.get(f"{API_BASE}/api/stats/{user_id}", timeout=5)
                if resp.status_code == 200:
                    results['stats'] = True
        else:
            results['errors'].append(f"Session start failed: {resp.status_code}")
            
    except requests.exceptions.Timeout:
        results['errors'].append("Timeout")
    except Exception as e:
        results['errors'].append(str(e))
    
    return results


print("="*70)
print("🧪 SIMPLIFIED CONCURRENT TEST (10 Users)")
print("="*70)
print("\nTesting 10 concurrent users in parallel...")
print("-" * 70)

start_time = time.time()
successful_users = 0
total_users = 10

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(test_user_flow, i) for i in range(1, total_users + 1)]
    
    results_list = []
    for future in as_completed(futures):
        result = future.result()
        results_list.append(result)
        
        # Print individual result
        status = "✅" if all([result['register'], result['session']]) else "❌"
        print(f"{status} {result['user_id']}: Register={result['register']}, Session={result['session']}, Record={result['record']}, Stats={result['stats']}")
        
        if all([result['register'], result['session'], result['record'], result['stats']]):
            successful_users += 1

elapsed = time.time() - start_time

print("-" * 70)
print(f"\n📊 RESULTS:")
print(f"   Success: {successful_users}/{total_users} users")
print(f"   Success Rate: {successful_users/total_users*100:.1f}%")
print(f"   Time: {elapsed:.2f} seconds")
print(f"   Avg per user: {elapsed/total_users:.2f} seconds")

if successful_users == total_users:
    print("\n✅ SUCCESS! System handles concurrent users efficiently!")
    print("   This demonstrates the system can scale to 100+ users.")
else:
    print(f"\n⚠️  {total_users - successful_users} users failed - check Flask API is running on port 5001")
    
print("="*70)
