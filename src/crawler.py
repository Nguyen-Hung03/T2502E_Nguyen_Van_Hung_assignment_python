from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from config import settings


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def _request_html(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=settings.request_timeout)
    response.raise_for_status()
    return response.text


def _normalize_url(base_url: str, href: str) -> str:
    return urljoin(base_url, href.strip())


def _is_valid_news_url(url: str, domain: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and domain in parsed.netloc


def extract_article_links(source_url: str, parser_type: str):
    html = _request_html(source_url)
    soup = BeautifulSoup(html, "html.parser")

    if parser_type == "vnexpress":
        items = _extract_vnexpress_links(soup, source_url)
    elif parser_type == "tuoitre":
        items = _extract_tuoitre_links(soup, source_url)
    else:
        items = _extract_generic_links(soup, source_url)

    unique = []
    seen = set()
    for title, url in items:
        if not title or not url or url in seen:
            continue
        seen.add(url)
        unique.append((title.strip(), url.strip()))
    return unique


def _extract_vnexpress_links(soup: BeautifulSoup, source_url: str):
    results = []
    selectors = ["h3.title-news a", "h2.title-news a", "article h3 a"]
    for selector in selectors:
        for a_tag in soup.select(selector):
            href = a_tag.get("href")
            title = a_tag.get_text(" ", strip=True)
            if not href:
                continue
            full_url = _normalize_url(source_url, href)
            if _is_valid_news_url(full_url, "vnexpress.net"):
                results.append((title, full_url))
    return results


def _extract_tuoitre_links(soup: BeautifulSoup, source_url: str):
    results = []
    selectors = ["h3.box-title-text a", "h3.title-news a", "article h3 a"]
    for selector in selectors:
        for a_tag in soup.select(selector):
            href = a_tag.get("href")
            title = a_tag.get_text(" ", strip=True)
            if not href:
                continue
            full_url = _normalize_url(source_url, href)
            if _is_valid_news_url(full_url, "tuoitre.vn"):
                results.append((title, full_url))
    return results


def _extract_generic_links(soup: BeautifulSoup, source_url: str):
    domain = urlparse(source_url).netloc
    results = []
    for a_tag in soup.select("a[href]"):
        href = a_tag.get("href")
        title = a_tag.get_text(" ", strip=True)
        if not href or len(title) < 25:
            continue
        full_url = _normalize_url(source_url, href)
        if _is_valid_news_url(full_url, domain):
            results.append((title, full_url))
        if len(results) >= 80:
            break
    return results


def extract_article_detail(article_url: str, parser_type: str):
    html = _request_html(article_url)
    soup = BeautifulSoup(html, "html.parser")

    title = _extract_title(soup)
    summary = _extract_summary(soup)

    if parser_type == "vnexpress":
        content = _extract_vnexpress_content(soup)
    elif parser_type == "tuoitre":
        content = _extract_tuoitre_content(soup)
    else:
        content = _extract_generic_content(soup)

    if not summary and content:
        summary = content[:250]

    return {
        "title": title,
        "summary": summary,
        "content": content,
    }


def _extract_title(soup: BeautifulSoup) -> str:
    h1 = soup.select_one("h1")
    return h1.get_text(" ", strip=True) if h1 else ""


def _extract_summary(soup: BeautifulSoup) -> str:
    og_desc = soup.find("meta", attrs={"name": "description"})
    if og_desc and og_desc.get("content"):
        return og_desc["content"].strip()
    first_p = soup.select_one("p")
    return first_p.get_text(" ", strip=True) if first_p else ""


def _extract_vnexpress_content(soup: BeautifulSoup) -> str:
    paragraphs = soup.select("article.fck_detail p.Normal, article.fck_detail p")
    texts = [p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)]
    return "\n".join(texts)


def _extract_tuoitre_content(soup: BeautifulSoup) -> str:
    paragraphs = soup.select("div.detail-content p, div#main-detail-body p")
    texts = [p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)]
    return "\n".join(texts)


def _extract_generic_content(soup: BeautifulSoup) -> str:
    paragraphs = soup.select("p")
    texts = []
    for p in paragraphs:
        text = p.get_text(" ", strip=True)
        if len(text) >= 40:
            texts.append(text)
        if len(texts) >= 30:
            break
    return "\n".join(texts)
