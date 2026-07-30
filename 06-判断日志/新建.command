#!/bin/bash
# 双击运行:新建一条判断日志
cd "$(dirname "$0")"
read -p "代号(如 老王 / 滴天髓-甲木-01):" NAME
[ -z "$NAME" ] && NAME="未命名"
F="$(date +%Y-%m-%d)-${NAME}.md"
if [ -e "$F" ]; then echo "已存在:$F"; else cp 模板.md "$F"; sed -i '' "s/# 判断日志 · \[代号\]/# 判断日志 · ${NAME}/" "$F"
sed -i '' "s/> 日期:YYYY-MM-DD/> 日期:$(date +%Y-%m-%d)/" "$F"; fi
echo "已创建:$F"
open -a TextEdit "$F" 2>/dev/null || open "$F"
