#!/usr/bin/env python3
"""把分章文件拼成连续的 全书.md,顶部生成可跳转总目录。"""
import os,re,glob
ROOT=os.path.dirname(os.path.abspath(__file__))
PARTS=[
 ("第一部 · 地基:读懂符号","第1部-地基"),
 ("第二部 · 排盘:把命摆出来","第2部-排盘"),
 ("第三部 · 强弱:第一道判断","第3部-强弱"),
 ("第四部 · 格局:子平真诠的主场","第4部-格局"),
 ("第五部 · 用神:五种取法的统一","第5部-用神"),
 ("第六部 · 行运","第6部-行运"),
 ("第七部 · 六亲与应用","第7部-六亲"),
 ("第八部 · 辨伪","第8部-辨伪"),
]
PUNCT = r"[，。、．,\.\(\)（）《》「」〈〉“”\"\'：:；;!?？!·×→←↑…—–]"
def anc(h):
    """模拟 GitHub 的锚点生成:小写 → 删标点(保留空格) → 每个空格换一个连字符"""
    a = h.strip().lower()
    a = re.sub(PUNCT, "", a)
    return a.replace(" ", "-")

toc=[]; body=[]
for pname,pdir in PARTS:
    d=os.path.join(ROOT,pdir)
    if not os.path.isdir(d): continue
    files=sorted(glob.glob(os.path.join(d,"*.md")))
    if not files: continue
    toc.append(f"\n### {pname}\n")
    body.append(f"\n\n# {pname}\n\n")
    for f in files:
        raw=open(f,encoding="utf8").read()
        m=re.search(r'^# (.+)$',raw,re.M)
        title=m.group(1).strip() if m else os.path.basename(f)[:-3]
        toc.append(f"- [{title}](#{anc(title)})")
        # 去掉原文件的导航行和一级标题,降级所有标题一层
        lines=[]
        for ln in raw.split("\n"):
            if re.match(r'^> \[.*\]\(.*\)\s*[·|　]?',ln) and ("上一章" in ln or "下一章" in ln or "目录" in ln):
                continue
            if re.match(r'^> \*\*第.部完',ln): continue
            if ln.startswith("# "):
                lines.append("## "+ln[2:]); continue
            if ln.startswith("#"):
                lines.append("#"+ln); continue
            lines.append(ln)
        t="\n".join(lines)
        t=re.sub(r'\n{4,}','\n\n\n',t)
        body.append(t+"\n\n---\n")

head = """# 组合之书 · 子平命理通编(全书连续版)

> 这是把分章文件拼成的**连续阅读版**。想按章跳读,见 [分章目录](./README.md)。
> 附录:[五书冲突对照表](./附录/五书冲突对照.md)

把五本核心古籍打散重排成一本按学习顺序推进的书。每节格式:**原文(标出处)→ 白话 → 五书对照 → 要点**。

---

## 总目录
"""
out=head+"\n".join(toc)+"\n\n---\n"+"".join(body)
open(os.path.join(ROOT,"全书.md"),"w",encoding="utf8").write(out)
print(f"全书.md 生成完毕:{len(out):,} 字符")
