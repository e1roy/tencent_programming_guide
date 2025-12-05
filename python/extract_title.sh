# 本脚本用来提取 markdown 文件标题

awk '
/^```/ { in_block = !in_block; next }
in_block { next }
{ if (/^#{1,2} /) print }
'  README.md