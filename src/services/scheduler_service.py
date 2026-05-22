import threading
import time

import schedule
from requests import RequestException

from config import settings
from crawler import extract_article_detail, extract_article_links
from services.article_service import create_article, get_articles_by_status, update_article_detail
from services.source_service import get_active_sources


class SchedulerController:
    def __init__(self):
        self._thread = None
        self._running = False
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self):
        with self._lock:
            if self._running:
                return
            schedule.clear()
            schedule.every().day.at(settings.link_job_time).do(self.run_link_job)
            schedule.every(settings.detail_job_interval_minutes).minutes.do(self.run_detail_job)
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        with self._lock:
            if not self._running:
                return
            self._running = False
            schedule.clear()

    def _loop(self):
        while self._running:
            schedule.run_pending()
            time.sleep(1)

    def run_link_job(self):
        sources = get_active_sources()
        total_new = 0

        for source in sources:
            try:
                links = extract_article_links(source["url"], source["parser_type"])
                for title, url in links:
                    inserted = create_article(
                        source_id=source["id"],
                        category_id=source["category_id"],
                        title=title,
                        url=url,
                    )
                    if inserted:
                        total_new += 1
            except RequestException as exc:
                print(f"[TAC VU LAY LINK] Loi request voi nguon tin {source['source_name']}: {exc}")
            except Exception as exc:
                print(f"[TAC VU LAY LINK] Loi khong xac dinh voi nguon tin {source['source_name']}: {exc}")

        print(f"[TAC VU LAY LINK] Hoan tat. So bai moi them: {total_new}")

    def run_detail_job(self):
        pending_articles = get_articles_by_status(status=0, limit=100)
        updated = 0

        for article in pending_articles:
            try:
                source = self._find_source_of_article(article["source_id"])
                parser_type = source["parser_type"] if source else "generic"
                detail = extract_article_detail(article["url"], parser_type)

                summary = detail["summary"][:1000] if detail["summary"] else ""
                content = detail["content"]
                if not content:
                    continue

                update_article_detail(article["id"], summary, content)
                updated += 1
            except RequestException as exc:
                print(f"[TAC VU LAY CHI TIET] Loi request voi bai viet {article['id']}: {exc}")
            except Exception as exc:
                print(f"[TAC VU LAY CHI TIET] Loi khong xac dinh voi bai viet {article['id']}: {exc}")

        print(f"[TAC VU LAY CHI TIET] Hoan tat. So bai cap nhat: {updated}")

    @staticmethod
    def _find_source_of_article(source_id: int):
        sources = get_active_sources()
        for src in sources:
            if src["id"] == source_id:
                return src
        return None


scheduler_controller = SchedulerController()
