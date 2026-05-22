import math

from mysql.connector import Error

from services.article_service import get_article_count, get_articles_paginated
from services.scheduler_service import scheduler_controller
from services.source_service import (
    add_source,
    delete_source,
    list_categories,
    list_sources,
    source_exists,
    update_source,
)


def print_line():
    print("-" * 90)


def read_int(prompt: str, allow_empty: bool = False):
    while True:
        value = input(prompt).strip()
        if allow_empty and not value:
            return None
        if value.isdigit():
            return int(value)
        print("Gia tri khong hop le. Vui long nhap so nguyen.")


def show_categories():
    categories = list_categories()
    print("Danh sach chuyen muc:")
    for cat in categories:
        print(f"  {cat['id']}. {cat['category_name']}")


def list_sources_menu():
    sources = list_sources()
    print_line()
    print("DANH SACH NGUON TIN")
    print_line()
    if not sources:
        print("Chua co nguon tin nao.")
        return

    for src in sources:
        state = "Dang hoat dong" if src["is_active"] == 1 else "Da tat"
        print(
            f"[{src['id']}] {src['source_name']} | {src['category_name']} | {src['parser_type']} | {state}\n"
            f"URL: {src['url']}"
        )
        print_line()


def add_source_menu():
    print_line()
    print("THEM NGUON TIN")
    print_line()
    name = input("Ten nguon tin: ").strip()
    url = input("URL nguon tin: ").strip()

    show_categories()
    category_id = read_int("Chon ma chuyen muc (category_id): ")
    parser_type = input("Loai bo phan tach (vnexpress/tuoitre/generic): ").strip().lower() or "generic"

    if parser_type not in {"vnexpress", "tuoitre", "generic"}:
        print("Loai bo phan tach khong hop le.")
        return

    if not name or not url:
        print("Ten nguon tin va URL khong duoc de trong.")
        return

    try:
        add_source(name, url, category_id, parser_type)
        print("Them nguon tin thanh cong.")
    except (ValueError, Error) as exc:
        print(f"Loi khi them nguon tin: {exc}")


def update_source_menu():
    print_line()
    print("CAP NHAT NGUON TIN")
    print_line()

    source_id = read_int("Nhap ma nguon tin can sua: ")
    if not source_exists(source_id):
        print("Khong tim thay nguon tin.")
        return

    name = input("Ten nguon tin moi: ").strip()
    url = input("URL moi: ").strip()

    show_categories()
    category_id = read_int("Chon ma chuyen muc moi (category_id): ")
    parser_type = input("Loai bo phan tach moi (vnexpress/tuoitre/generic): ").strip().lower() or "generic"
    is_active = read_int("Trang thai (1=dang hoat dong, 0=da tat): ")

    if parser_type not in {"vnexpress", "tuoitre", "generic"}:
        print("Loai bo phan tach khong hop le.")
        return

    if is_active not in {0, 1}:
        print("Trang thai khong hop le.")
        return

    try:
        update_source(source_id, name, url, category_id, parser_type, is_active)
        print("Cap nhat nguon tin thanh cong.")
    except (ValueError, Error) as exc:
        print(f"Loi khi cap nhat nguon tin: {exc}")


def delete_source_menu():
    print_line()
    print("XOA NGUON TIN")
    print_line()
    source_id = read_int("Nhap ma nguon tin can xoa: ")

    confirm = input("Ban chac chan muon xoa? (y/n): ").strip().lower()
    if confirm != "y":
        print("Da huy thao tac.")
        return

    try:
        delete_source(source_id)
        print("Xoa nguon tin thanh cong.")
    except (ValueError, Error) as exc:
        print(f"Loi khi xoa nguon tin: {exc}")


def source_management_menu():
    while True:
        print_line()
        print("QUAN LY NGUON TIN")
        print_line()
        print("1. Xem danh sach nguon tin")
        print("2. Them nguon tin")
        print("3. Sua nguon tin")
        print("4. Xoa nguon tin")
        print("0. Quay lai")

        choice = input("Chon: ").strip()
        if choice == "1":
            list_sources_menu()
        elif choice == "2":
            add_source_menu()
        elif choice == "3":
            update_source_menu()
        elif choice == "4":
            delete_source_menu()
        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le.")


def view_articles_menu():
    page_size = 10
    current_page = 1

    while True:
        total = get_article_count()
        total_pages = max(1, math.ceil(total / page_size))
        if current_page > total_pages:
            current_page = total_pages

        articles = get_articles_paginated(current_page, page_size)

        print_line()
        print(f"DANH SACH TIN TUC - Trang {current_page}/{total_pages} - Tong {total} bai")
        print_line()

        if not articles:
            print("Chua co tin tuc nao trong he thong.")
        else:
            for idx, article in enumerate(articles, start=1):
                status = "Da lay noi dung" if article["status"] == 1 else "Moi lay link"
                print(
                    f"{idx}. [{article['id']}] {article['title']}\n"
                    f"   Nguon tin: {article['source_name']} | Chuyen muc: {article['category_name']}\n"
                    f"   Trang thai: {status}\n"
                    f"   URL: {article['url']}"
                )
                print_line()

        nav = input("Nhan N (Trang tiep), P (Trang truoc), Q (Thoat): ").strip().lower()
        if nav == "n":
            if current_page < total_pages:
                current_page += 1
            else:
                print("Dang o trang cuoi.")
        elif nav == "p":
            if current_page > 1:
                current_page -= 1
            else:
                print("Dang o trang dau.")
        elif nav == "q":
            break
        else:
            print("Lenh khong hop le.")


def cronjob_menu():
    while True:
        print_line()
        print("DIEU KHIEN BO LAP LICH")
        print_line()
        print(f"Trang thai bo lap lich: {'DANG CHAY' if scheduler_controller.is_running else 'DANG DUNG'}")
        print("1. Bat bo lap lich")
        print("2. Tat bo lap lich")
        print("3. Chay thu cong tac vu lay danh sach link")
        print("4. Chay thu cong tac vu lay noi dung chi tiet")
        print("0. Quay lai")

        choice = input("Chon: ").strip()
        if choice == "1":
            scheduler_controller.start()
            print("Bo lap lich da duoc bat.")
        elif choice == "2":
            scheduler_controller.stop()
            print("Bo lap lich da duoc tat.")
        elif choice == "3":
            scheduler_controller.run_link_job()
        elif choice == "4":
            scheduler_controller.run_detail_job()
        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le.")


def main_menu():
    while True:
        print_line()
        print("HE THONG TONG HOP TIN TUC")
        print_line()
        print("1. Quan ly nguon tin")
        print("2. Xem tin tuc")
        print("3. Dieu khien bo lap lich")
        print("0. Thoat")

        choice = input("Nhap lua chon: ").strip()
        if choice == "1":
            source_management_menu()
        elif choice == "2":
            view_articles_menu()
        elif choice == "3":
            cronjob_menu()
        elif choice == "0":
            scheduler_controller.stop()
            print("Tam biet!")
            break
        else:
            print("Lua chon khong hop le.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        scheduler_controller.stop()
        print("\nDa dung chuong trinh.")
    except Error as exc:
        print(f"Loi ket noi/co so du lieu: {exc}")
