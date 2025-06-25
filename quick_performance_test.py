#!/usr/bin/env python3
"""
紧急性能测试脚本 - 3小时内验证优化效果
"""
import asyncio
import aiohttp
import time
import json
from datetime import datetime

# 配置
BACKEND_URL = "https://web-production-5fb04.up.railway.app"  # 您的Railway URL
TEST_USERS = 5  # 先测试5个用户，确认稳定后再增加

async def single_user_test(session, user_id):
    """单个用户测试"""
    start_time = time.time()
    
    payload = {
        "user_name": f"test_user_{user_id}",
        "scenario_name": f"emergency_test_{user_id}",
        "mode": "Monte Carlo Simulation Mode",
        "num_simulations": 20,  # 减少仿真次数以快速测试
        "decision_vars": [{
            "year": 2026,
            "planting_trees_amount": 100.0,
            "house_migration_amount": 50.0,
            "dam_levee_construction_cost": 10.0,
            "paddy_dam_construction_cost": 5.0,
            "capacity_building_cost": 8.0,
            "transportation_invest": 12.0,
            "agricultural_RnD_cost": 15.0,
            "cp_climate_params": 4.5
        }],
        "current_year_index_seq": {
            "temp": 15.0,
            "precip": 1700.0,
            "municipal_demand": 100.0,
            "available_water": 1000.0,
            "crop_yield": 100.0,
            "hot_days": 30.0,
            "extreme_precip_freq": 0.1,
            "ecosystem_level": 100.0,
            "levee_level": 0.5,
            "high_temp_tolerance_level": 0.0,
            "forest_area": 0.0,
            "urban_level": 100.0,
            "resident_capacity": 0.0,
            "transportation_level": 0.0,
            "levee_investment_total": 0.0,
            "RnD_investment_total": 0.0,
            "risky_house_total": 10000.0,
            "non_risky_house_total": 0.0,
            "resident_burden": 5.379e8,
            "biodiversity_level": 100.0
        }
    }
    
    try:
        async with session.post(f"{BACKEND_URL}/simulate", json=payload, timeout=300) as response:
            if response.status == 200:
                result = await response.json()
                end_time = time.time()
                duration = end_time - start_time
                return {
                    "user_id": user_id,
                    "success": True,
                    "duration": duration,
                    "status": response.status,
                    "data_points": len(result.get("data", []))
                }
            else:
                return {
                    "user_id": user_id,
                    "success": False,
                    "duration": time.time() - start_time,
                    "status": response.status,
                    "error": await response.text()
                }
    except Exception as e:
        return {
            "user_id": user_id,
            "success": False,
            "duration": time.time() - start_time,
            "status": 0,
            "error": str(e)
        }

async def concurrent_test(num_users=TEST_USERS):
    """并发测试"""
    print(f"🚀 开始 {num_users} 用户并发测试...")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    connector = aiohttp.TCPConnector(limit=20, limit_per_host=20)
    timeout = aiohttp.ClientTimeout(total=600)  # 10分钟超时
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # 并发执行所有用户测试
        tasks = [single_user_test(session, i) for i in range(num_users)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 分析结果
        successful_tests = [r for r in results if isinstance(r, dict) and r.get("success")]
        failed_tests = [r for r in results if isinstance(r, dict) and not r.get("success")]
        exceptions = [r for r in results if not isinstance(r, dict)]
        
        print(f"\n📊 测试结果:")
        print(f"✅ 成功: {len(successful_tests)}/{num_users}")
        print(f"❌ 失败: {len(failed_tests)}")
        print(f"💥 异常: {len(exceptions)}")
        
        if successful_tests:
            durations = [r["duration"] for r in successful_tests]
            print(f"\n⏱️ 性能指标:")
            print(f"平均响应时间: {sum(durations)/len(durations):.2f} 秒")
            print(f"最快响应时间: {min(durations):.2f} 秒")
            print(f"最慢响应时间: {max(durations):.2f} 秒")
            
            # 计算每年仿真时间
            avg_duration = sum(durations)/len(durations)
            time_per_year = avg_duration / 75  # 75年仿真
            print(f"每年仿真时间: {time_per_year:.3f} 秒")
            
            if time_per_year < 1.5:
                print("🎉 性能优化成功！每年仿真时间 < 1.5秒")
            elif time_per_year < 2.5:
                print("✅ 性能有改善，每年仿真时间 < 2.5秒")
            else:
                print("⚠️ 性能仍需优化，每年仿真时间 > 2.5秒")
        
        if failed_tests:
            print(f"\n❌ 失败详情:")
            for test in failed_tests:
                print(f"用户 {test['user_id']}: {test.get('error', 'Unknown error')}")
        
        if exceptions:
            print(f"\n💥 异常详情:")
            for i, exc in enumerate(exceptions):
                print(f"任务 {i}: {exc}")
        
        return len(successful_tests) == num_users

async def health_check():
    """健康检查"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/ping", timeout=10) as response:
                if response.status == 200:
                    print("✅ 后端服务正常")
                    return True
                else:
                    print(f"❌ 后端服务异常: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ 无法连接后端: {e}")
        return False

async def main():
    """主测试流程"""
    print("🔍 紧急性能测试开始")
    print("=" * 50)
    
    # 健康检查
    if not await health_check():
        print("❌ 后端服务不可用，测试终止")
        return
    
    # 逐步增加用户数测试
    test_scenarios = [3, 5, 8, 10, 15]
    
    for num_users in test_scenarios:
        print(f"\n🧪 测试 {num_users} 个并发用户...")
        success = await concurrent_test(num_users)
        
        if success:
            print(f"✅ {num_users} 用户测试通过")
            if num_users >= 15:
                print("🎉 目标达成！支持15个并发用户")
                break
        else:
            print(f"❌ {num_users} 用户测试失败")
            if num_users > 3:
                print(f"⚠️ 建议最大并发用户数: {test_scenarios[test_scenarios.index(num_users)-1]}")
            break
        
        # 等待5秒再进行下一轮测试
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
