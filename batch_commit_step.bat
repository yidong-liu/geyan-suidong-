@echo off
chcp 65001 > nul
echo ============================================================
echo Git 分批提交工具 - 逐目录提交避免超时
echo ============================================================
echo.

REM 配置Git缓冲区大小
echo 配置 Git 缓冲区...
git config http.postBuffer 524288000
git config http.maxRequestBuffer 524288000
git config core.compression 0

echo.
echo 开始分批提交...
echo.

REM 第一批：提交核心Python文件
echo [批次 1/6] 提交核心Python文件...
git add *.py
git commit --no-verify -m "feat(live2d): Add core Python files"
echo.

REM 第二批：提交Markdown文档
echo [批次 2/6] 提交文档文件...
git add *.md
git commit --no-verify -m "feat(live2d): Add documentation files"
echo.

REM 第三批：提交shell脚本和配置
echo [批次 3/6] 提交脚本和配置...
git add *.sh *.txt *.bat
git add .gitignore .env.example
git commit --no-verify -m "feat(live2d): Add scripts and configuration"
echo.

REM 第四批：提交backend目录
echo [批次 4/6] 提交backend目录...
git add backend/
git commit --no-verify -m "feat(live2d): Add backend module"
echo.

REM 第五批：提交frontend目录
echo [批次 5/6] 提交frontend目录...
git add frontend/
git commit --no-verify -m "feat(live2d): Add frontend module"
echo.

REM 第六批：提交其他目录
echo [批次 6/6] 提交其他目录...
git add config/ data/ models/ tests/ docs/ logs/ plug/
git add test_audio.wav
git commit --no-verify -m "feat(live2d): Add remaining directories and resources"
echo.

echo ============================================================
echo 所有批次提交完成！
echo ============================================================
echo.
echo 查看提交历史（最近6次）:
git log --oneline -6
echo.
echo 现在可以推送到远程仓库:
echo   git push origin main
echo 或
echo   git push origin master
echo.
echo 如果推送失败，可以尝试:
echo   git push origin main --no-verify
echo   或使用强制推送（谨慎）:
echo   git push origin main --force
echo.
pause
