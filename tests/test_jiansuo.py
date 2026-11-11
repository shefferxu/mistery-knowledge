"""检索行为测试。"""
import importlib.util
from pathlib import Path
import unittest
path = Path(__file__).resolve().parents[1] / "mistery-knowledge" / "scripts" / "jiansuo.py"
spec = importlib.util.spec_from_file_location("jiansuo", path)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)

class SearchTests(unittest.TestCase):
    """验证中文、日期、作者和顺序。"""
    def setUp(self):
        """用途：构造语料；参数：无；返回：无。"""
        self.posts = [
            {"id":"1","author":"wr0789","text":"恒科定投，使用闲置资金","date":"2026-10-22","topics":["港股与恒科"],"time_iso":"2026-10-22T01:00:00+08:00"},
            {"id":"2","author":"guest","text":"恒科定投保证赚钱","date":"2026-10-22","topics":["港股与恒科"],"time_iso":"2026-10-22T02:00:00+08:00"},
            {"id":"3","author":"wr0789","text":"只做三浪主升","date":"2026-11-07","topics":["技术分析与交易策略"],"time_iso":"2026-11-07T01:00:00+08:00"}]
    def test_author_and_chinese_and_query(self):
        """用途：检验作者与多词；参数：无；返回：无。"""
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"恒科 闲置")],["1"])
        self.assertEqual(api.search_posts(self.posts,"保证赚钱"),[])
    def test_context_is_explicit(self):
        """用途：检验背景作者；参数：无；返回：无。"""
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"保证赚钱",include_context=True)],["2"])
    def test_date_boundaries_and_topic(self):
        """用途：检验日期含首尾；参数：无；返回：无。"""
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"",since="2026-10-22",until="2026-10-22",topic="港股与恒科")],["1"])
    def test_any_and_empty_results(self):
        """用途：检验或匹配与未命中；参数：无；返回：无。"""
        self.assertEqual(len(api.search_posts(self.posts,"恒科 三浪",any_term=True)),2)
        self.assertEqual(api.search_posts(self.posts,"不存在"),[])
    def test_exact_context_id(self):
        """用途：按明确 ID 定位背景帖子；参数：无；返回：无。"""
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"",post_id="2")],["2"])
    def test_id_and_order(self):
        """用途：检验单帖与排序；参数：无；返回：无。"""
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"",post_id="3")],["3"])
        self.assertEqual([p["id"] for p in api.search_posts(self.posts,"",order="oldest")],["1","3"])

if __name__=="__main__":
    unittest.main()
