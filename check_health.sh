#!/bin/bash
# 系统健康检查脚本

echo "======================================="
echo "  歌颜随动 系统健康检查"
echo "======================================="
echo ""

# 检查后端
echo "1. 检查后端服务..."
BACKEND_STATUS=$(curl -s http://localhost:8000/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ 后端运行正常"
    echo "   响应: $BACKEND_STATUS"
else
    echo "   ❌ 后端未运行或无响应"
fi
echo ""

# 检查前端
echo "2. 检查前端服务..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501 2>/dev/null)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "   ✅ 前端运行正常 (HTTP $FRONTEND_STATUS)"
else
    echo "   ❌ 前端未运行 (HTTP $FRONTEND_STATUS)"
fi
echo ""

# 检查进程
echo "3. 检查运行进程..."
BACKEND_PROC=$(ps aux | grep "python -m backend.api.main" | grep -v grep)
FRONTEND_PROC=$(ps aux | grep "streamlit run app.py" | grep -v grep)

if [ ! -z "$BACKEND_PROC" ]; then
    echo "   ✅ 后端进程正在运行"
    echo "      $(echo "$BACKEND_PROC" | awk '{print $2, $11, $12, $13, $14}')"
else
    echo "   ❌ 后端进程未运行"
fi

if [ ! -z "$FRONTEND_PROC" ]; then
    echo "   ✅ 前端进程正在运行"
    echo "      $(echo "$FRONTEND_PROC" | awk '{print $2, $11, $12, $13, $14}')"
else
    echo "   ❌ 前端进程未运行"
fi
echo ""

# 检查日志
echo "4. 检查最新日志..."
if [ -f logs/backend.log ]; then
    echo "   后端日志 (最后5行):"
    tail -5 logs/backend.log | strings | sed 's/^/      /'
else
    echo "   ⚠️  后端日志文件不存在"
fi
echo ""

# 检查上传文件
echo "5. 检查上传文件..."
UPLOAD_COUNT=$(ls -1 data/uploads/*.mp3 2>/dev/null | wc -l)
echo "   已上传文件数: $UPLOAD_COUNT"
if [ $UPLOAD_COUNT -gt 0 ]; then
    echo "   最新文件:"
    ls -lht data/uploads/*.mp3 2>/dev/null | head -3 | awk '{print "      " $9, "(" $5 ")"}'
fi
echo ""

# 测试API
echo "6. 测试API端点..."
# 测试健康检查
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ /health - 正常"
else
    echo "   ❌ /health - 异常"
fi

# 测试API文档
DOCS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null)
if [ "$DOCS" = "200" ]; then
    echo "   ✅ /docs - 正常 (HTTP $DOCS)"
else
    echo "   ❌ /docs - 异常 (HTTP $DOCS)"
fi
echo ""

# 总结
echo "======================================="
echo "  访问地址"
echo "======================================="
echo "  前端界面: http://localhost:8501"
echo "  后端API:  http://localhost:8000"
echo "  API文档:  http://localhost:8000/docs"
echo "======================================="
echo ""

# 返回状态
if [ ! -z "$BACKEND_PROC" ] && [ ! -z "$FRONTEND_PROC" ]; then
    echo "✅ 系统运行正常！"
    exit 0
else
    echo "⚠️  部分服务未运行，请检查！"
    echo "   使用 ./start_all.sh 启动所有服务"
    exit 1
fi
