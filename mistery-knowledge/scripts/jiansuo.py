"""检索 Mistery 归档。仅使用 Python 标准库，默认限定作者本人。"""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def search_posts(posts, query, include_context=False, since=None, until=None,
                 topic=None, any_term=False, post_id=None, order="relevance"):
    """用途：筛选并排序推文；参数：语料、关键词及筛选项；返回：匹配记录列表。"""
    terms = [term.casefold() for term in re.split(r"\s+", query.strip()) if term]
    results = []
    for post in posts:
        if not post_id and not include_context and post.get("author") != "wr0789":
            continue
        if post_id and post.get("id") != post_id.rstrip("/").split("/")[-1]:
            continue
        if since and post["date"] < since:
            continue
        if until and post["date"] > until:
            continue
        if topic and topic not in post.get("topics", []):
            continue
        haystack = (post.get("text", "") + " " + " ".join(post.get("topics", [])) + " " + post.get("id", "")).casefold()
        matches = [term in haystack for term in terms]
        if terms and not (any(matches) if any_term else all(matches)):
            continue
        results.append(post)
    if order in ("oldest", "newest"):
        results.sort(key=lambda p: (p["time_iso"], p["id"]), reverse=order=="newest")
    else:
        results.sort(key=lambda p: (sum(min(p.get("text","").casefold().count(t),5) for t in terms),
                                   len(p.get("text",""))>=300,p["time_iso"]), reverse=True)
    return results

def load_posts(path=None):
    """用途：读取归档；参数：可选 JSONL 路径；返回：记录列表。"""
    path = Path(path) if path else ROOT / "references" / "index.jsonl"
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]

def main():
    """用途：运行命令行检索；参数：命令行；返回：退出码。"""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query",nargs="?",default="")
    parser.add_argument("--id",dest="post_id")
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--topic")
    parser.add_argument("--any",dest="any_term",action="store_true")
    parser.add_argument("--include-context",action="store_true",help="搜索其他作者的背景材料")
    parser.add_argument("--order",choices=["relevance","oldest","newest"],default="relevance")
    parser.add_argument("--limit",type=int,default=8,help="0 表示全部匹配")
    parser.add_argument("--stats",action="store_true")
    parser.add_argument("--data",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    for value in (args.since,args.until):
        if value:
            from datetime import date
            try:
                date.fromisoformat(value)
            except ValueError:
                parser.error("日期必须为 YYYY-MM-DD")
    if args.since and args.until and args.since>args.until:
        parser.error("起始日期不得晚于结束日期")
    if args.limit<0:
        parser.error("limit 不能小于 0")
    coverage_path=ROOT/"references"/"coverage.json"
    coverage=json.loads(coverage_path.read_text(encoding="utf-8")) if coverage_path.exists() else {}
    posts=load_posts(args.data) if args.data or not args.stats else []
    if args.data:
        coverage={"distribution":"user_supplied","completeness":"unknown","total_records":len(posts),"note":"用户提供的本地资料；覆盖范围未验证。"}
    if args.stats:
        output=coverage
    else:
        matched=search_posts(posts,args.query,args.include_context,args.since,args.until,
                             args.topic,args.any_term,args.post_id,args.order)
        chosen=matched[:args.limit] if args.limit else matched
        by_id={p["id"]:p for p in posts}
        chosen_ids={p["id"] for p in chosen}
        related_ids={p[k] for p in chosen for k in ("in_reply_to","quoted_id") if p.get(k)}
        output={"query":args.query,"total_matches":len(matched),"returned":len(chosen),
                "coverage":coverage,"posts":chosen,
                "related_context":[by_id[i] for i in sorted(related_ids) if i in by_id and i not in chosen_ids],
                "missing_context_ids":sorted(related_ids-by_id.keys())}
    text=json.dumps(output,ensure_ascii=False,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+"\n",encoding="utf-8")
        print(str(args.output.resolve()))
    else:
        print(text)
    return 0

if __name__=="__main__":
    sys.exit(main())
