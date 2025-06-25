#!/usr/bin/env python3
"""
实时性能监控脚本 - 部署后持续监控
"""
import asyncio
import aiohttp
import time
import json
from datetime import datetime

BACKEND_URL = "https://web-production-5fb04.up.railway.app"

async def check_health():
    """健康检查"""
    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.get(f"{BACKEND_URL}/ping", timeout=5) as response:
                duration = time.time() - start_time
                return {
                    "status": response.status,
                    "response_time": duration,
                    "healthy": response.status == 200 and duration < 2.0
                }
    except Exception as e:
        return {
            "status": 0,
            "response_time": 999,
            "healthy": False,
            "error": str(e)
        }

async def quick_simulation_test():
    """快速仿真测试"""
    payload = {
        "user_name": "monitor_test",
        "scenario_name": "health_check",
        "mode": "Monte Carlo Simulation Mode",
        "num_simulations": 5,  # 最小仿真次数
        "decision_vars": [{
            "year": 2026,
            "planting_trees_amount": 10.0,
            "house_migration_amount": 5.0,
            "dam_levee_construction_cost": 1.0,
            "paddy_dam_construction_cost": 1.0,
            "capacity_building_cost": 1.0,
            "transportation_invest": 1.0,
            "agricultural_RnD_cost": 1.0,
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
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.post(f"{BACKEND_URL}/simulate", json=payload, timeout=60) as response:
                duration = time.time() - start_time
                if response.status == 200:
                    result = await response.json()
                    time_per_year = duration / 75  # 75年仿真
                    return {
                        "success": True,
                        "duration": duration,
                        "time_per_year": time_per_year,
                        "data_points": len(result.get("data", [])),
                        "performance_good": time_per_year < 2.0
                    }
                else:
                    return {
                        "success": False,
                        "duration": duration,
                        "status": response.status,
                        "error": await response.text()
                    }
    except Exception as e:
        return {
            "success": False,
            "duration": 999,
            "error": str(e)
        }

async def monitor_loop():
    """监控循环"""
    print("🔍 开始实时监控...")
    print("按 Ctrl+C 停止监控")
    print("=" * 60)
    
    consecutive_failures = 0
    
    while True:
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # 健康检查
            health = await check_health()
            
            # 性能测试
            perf = await quick_simulation_test()
            
            # 显示结果
            if health["healthy"] and perf.get("success"):
                status = "🟢 正常"
                consecutive_failures = 0
                time_per_year = perf.get("time_per_year", 999)
                if time_per_year < 1.0:
                    perf_status = "🚀 优秀"
                elif time_per_year < 2.0:
                    perf_status = "✅ 良好"
                else:
                    perf_status = "⚠️ 一般"
                
                print(f"[{timestamp}] {status} | 响应: {health['response_time']:.2f}s | "
                      f"仿真: {time_per_year:.3f}s/年 {perf_status}")
            else:
                consecutive_failures += 1
                status = "🔴 异常"
                error_msg = health.get("error", "") or perf.get("error", "")
                print(f"[{timestamp}] {status} | 错误: {error_msg[:50]}")
                
                # 连续失败警告
                if consecutive_failures >= 3:
                    print(f"🚨 警告: 连续 {consecutive_failures} 次失败，建议检查系统状态")
                    if consecutive_failures >= 5:
                        print("🚨 严重: 建议立即回滚到之前版本")
            
            # 等待30秒再次检查
            await asyncio.sleep(30)
            
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
            break
        except Exception as e:
            print(f"[{timestamp}] 💥 监控异常: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(monitor_loop())
