"""Offline regression checks for the public adapters; no credentials or real sites."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


crawl = load('crawl', 'check-crawlability/scripts/crawl_check.py')
page = load('page', 'page-seo-inspector/scripts/page_seo_inspector.py')
from bs4 import BeautifulSoup
import requests


def response(url, text='', status=200, content_type='text/plain'):
    result = requests.Response()
    result.url = url
    result.status_code = status
    result._content = text.encode()
    result.encoding = 'utf-8'
    result.headers['Content-Type'] = content_type
    return result


class CrawlTests(unittest.TestCase):
    def test_only_root_robots_governs(self):
        with patch.object(crawl.requests, 'get', return_value=response('https://example.com/robots.txt', status=404)) as get:
            result = crawl.check_robots('https://example.com', ['/products/', '/'])
        self.assertEqual(get.call_args.args[0], 'https://example.com/robots.txt')
        self.assertEqual(get.call_count, 1)
        self.assertEqual(result['rules_state'], 'not_found')

    def test_training_rule_does_not_block_search(self):
        result = crawl.check_ai_crawlers('User-agent: GPTBot\nDisallow: /', '/products/a')
        self.assertEqual(result['bots']['GPTBot']['status'], 'blocked')
        self.assertEqual(result['bots']['OAI-SearchBot']['status'], 'not_declared')
        self.assertEqual(result['critical_blocked'], [])

    def test_specific_group_merged_allow_longest_and_comments(self):
        text = '''User-agent: *
Disallow: /
User-agent: Googlebot
Disallow: /products/ # private
User-agent: Googlebot
Allow: /products/public/
Disallow: /*.pdf$
'''
        groups = crawl._parse_robots_sections(text)
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/products/private/'), 'blocked')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/products/public/a'), 'allowed')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/a.pdf'), 'blocked')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/a.pdf?download=1'), 'allowed')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Bingbot', '/'), 'blocked_by_wildcard')

    def test_allow_tie_and_percent_encoded_path(self):
        groups = crawl._parse_robots_sections('User-agent: *\nDisallow: /a\nAllow: /a\nDisallow: /caf%C3%A9')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/a'), 'allowed')
        self.assertEqual(crawl._bot_crawl_status(groups, 'Googlebot', '/café'), 'blocked_by_wildcard')

    def test_failed_robots_is_unknown(self):
        for status in (403, 429, 503):
            with self.subTest(status=status), patch.object(crawl.requests, 'get', return_value=response('https://example.com/robots.txt', status=status)):
                robots = crawl.check_robots('https://example.com')
                result = crawl.check_ai_crawlers(robots['content_full'])
                self.assertEqual(result['bots']['Googlebot']['status'], 'unknown')
        with patch.object(crawl.requests, 'get', side_effect=requests.Timeout('test timeout')):
            self.assertEqual(crawl.check_robots('https://example.com')['rules_state'], 'unknown')

    def test_html_fallback_is_not_rules_or_sitemap(self):
        with patch.object(crawl.requests, 'get', return_value=response('https://example.com/fallback', '<html><body>Not found</body></html>', content_type='text/html')):
            self.assertEqual(crawl.check_robots('https://example.com')['rules_state'], 'unknown')
            self.assertFalse(crawl.check_sitemap('https://example.com')['found'])

    def test_namespaced_sitemap_index_counts_maps(self):
        xml = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://example.com/a.xml</loc></sitemap></sitemapindex>'
        with patch.object(crawl.requests, 'get', return_value=response('https://example.com/sitemap.xml', xml, content_type='application/xml')):
            result = crawl.check_sitemap('https://example.com')
        self.assertTrue(result['found'])
        self.assertEqual(result['url_count'], 1)
        self.assertEqual(result['count_kind'], 'child_sitemaps')

    def test_main_checks_input_page_not_only_origin(self):
        url = 'https://example.com/products/a?size=large'
        with patch.object(sys, 'argv', ['crawl_check.py', url]), \
             patch.object(crawl, 'check_https_redirect', return_value={}), \
             patch.object(crawl, 'check_robots', return_value={'content_full': ''}), \
             patch.object(crawl, 'check_sitemap', return_value={}), \
             patch.object(crawl, 'check_llms_txt', return_value={}), \
             patch.object(crawl, 'check_llms_markdown_pairs', return_value={}), \
             patch.object(crawl, 'check_page_headers', return_value={}) as headers, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            crawl.main()
        headers.assert_called_once_with(url)
        self.assertEqual(json.loads(output.getvalue())['ai_crawlers']['bots']['Googlebot']['tested_path'], '/products/a?size=large')


class PageTests(unittest.TestCase):
    def test_graph_arrays_and_scalars_do_not_crash(self):
        for data in ({'@graph': [{'@type': ['Product', 'Thing'], 'name': 'Cabinet'}, {'@type': 'Organization'}]}, [None, 'text', {'@type': 'Article'}], 42):
            with self.subTest(data=data):
                soup = BeautifulSoup('<script type="application/ld+json">' + json.dumps(data) + '</script>', 'html.parser')
                result, checks = page.check_schema(soup)
                self.assertIsInstance(result['schema_types'], list)
        self.assertEqual(page.check_schema(BeautifulSoup('<script type="application/ld+json">{"@graph":[{"@type":["Product","Thing"]}]}</script>', 'html.parser'))[0]['schema_types'], ['Product', 'Thing'])

    def test_relative_canonical_and_none_directive(self):
        soup = BeautifulSoup('<link rel="canonical" href="/products/a"><meta name="robots" content="none">', 'html.parser')
        result, checks = page.check_indexability({'headers': {}, 'final_url': 'https://example.com/products/a'}, soup)
        self.assertTrue(any(c.name == 'Canonical tag' and c.status == 'pass' for c in checks))
        self.assertTrue(any(c.name == 'Meta robots tag' and c.status == 'critical' for c in checks))

    def test_editorial_length_and_xdefault_are_not_failures(self):
        soup = BeautifulSoup('<html lang="en"><title>Pump</title><meta name="description" content="Pump specifications."><link hreflang="en" href="https://example.com/en"></html>', 'html.parser')
        _, checks = page.check_meta(soup)
        self.assertFalse(any(c.status in ('critical', 'warning') for c in checks))

    def test_non_web_links_do_not_count_as_internal(self):
        soup = BeautifulSoup('<body><a href="mailto:a@example.com">Mail</a><a href="tel:1">Call</a><a href="#a">Jump</a><a href="javascript:void(0)">Menu</a><a href="/products">Products</a><a href="https://other.example/x">Other</a></body>', 'html.parser')
        result, checks = page.check_content({'final_url': 'https://example.com/'}, soup)
        self.assertEqual(result['internal_links'], 1)
        self.assertEqual(result['external_links'], 1)
        self.assertEqual(next(c.status for c in checks if c.name == 'Word count'), 'info')

    def test_fetch_failure_no_score(self):
        with patch.object(page.requests, 'get', side_effect=requests.Timeout('fixture')), \
             patch.object(sys, 'argv', ['page_seo_inspector.py', 'https://example.com', '--json']), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit):
                page.main()
        self.assertNotIn('score', json.loads(output.getvalue()))

    def test_full_json_cli_flow(self):
        url = 'https://example.com/product'
        html = '<html lang="en"><head><title>Industrial Cabinet</title><link rel="canonical" href="/product"><script type="application/ld+json">{"@graph":[{"@type":"Product","name":"Cabinet"}]}</script></head><body><h1>Cabinet</h1><p>IP rating needs confirmation.</p></body></html>'
        with patch.object(page.requests, 'get', return_value=response(url, html, content_type='text/html')), \
             patch.object(sys, 'argv', ['page_seo_inspector.py', url, '--json']), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            page.main()
        result = json.loads(output.getvalue())
        self.assertEqual(result['structured_data']['schema_types'], ['Product'])
        self.assertEqual(result['score_kind'], 'custom_checklist_not_google_score')
        self.assertEqual(result['indexability']['canonical'], '/product')


if __name__ == '__main__':
    unittest.main()
