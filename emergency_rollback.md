# 🚨 紧急回滚方案

## 如果优化后出现问题，立即执行以下步骤：

### 方案1：代码回滚（2分钟）
```bash
# 1. 恢复原始代码
git checkout HEAD~1 adaptation_simulation/backend/main.py

# 2. 推送回滚
git add .
git commit -m "Emergency rollback: restore max_workers=2"
git push origin main
```

### 方案2：直接修改（1分钟）
在 `adaptation_simulation/backend/main.py` 第209行：
```python
# 改回原始值
max_workers = min(2, multiprocessing.cpu_count(), req.num_simulations)
```

### 方案3：Railway重新部署（3分钟）
1. 登录Railway控制台
2. 选择您的项目
3. 点击 "Redeploy" 按钮
4. 选择之前的稳定版本

## 监控指标
如果出现以下情况，立即回滚：
- ❌ 响应时间超过10秒
- ❌ 内存使用率超过90%
- ❌ 出现500错误
- ❌ 用户无法正常访问

## 联系方式
如需技术支持，请保存此文档并联系开发团队。
