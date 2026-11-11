"""公开分发边界和索引功能验证。"""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"mistery-knowledge/references/index.jsonl"

class PublicIndexTests(unittest.TestCase):
    """验证公开索引与原文的区分。"""
    def test_public_record_schema(self):
        """用途：禁止全文及会话字段进入公开数据；参数：无；返回：无。"""
        with INDEX.open(encoding="utf-8") as stream:
            records=[json.loads(line) for line in stream if line.strip()]
        allowed={"id","author","date","time_iso","url","topics","text","content_kind","text_origin"}
        self.assertGreater(len(records),0)
        self.assertEqual(len(records),len({p["id"] for p in records}))
        for post in records:
            self.assertEqual(set(post),allowed)
            self.assertEqual(post["author"],"wr0789")
            self.assertIn(post["content_kind"],["source_index","editorial_summary"])
            self.assertIn("非推文原文",post["text_origin"])
            self.assertTrue(post["text"].startswith(("整理概括：","主题索引：")))
            self.assertLess(len(post["text"]),160)
    def test_subject_search(self):
        """用途：验证公开摘要能定位恒科定投来源；参数：无；返回：无。"""
        path=ROOT/"mistery-knowledge/scripts/jiansuo.py"
        spec=importlib.util.spec_from_file_location("public_search",path)
        api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
        result=api.search_posts(api.load_posts(),"恒科 定投")
        self.assertIn("2113124439365730315",{p["id"] for p in result})
        self.assertTrue(all(p["content_kind"]!="original" for p in result))

if __name__=="__main__":
    unittest.main()
