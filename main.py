from playwright.sync_api import sync_playwright
import time

def auto_scroll(page, max_scrolls=50, delay=2):
    """
    Fungsi untuk scroll otomatis hingga semua komentar termuat.
    """
    previous_count = 0
    no_new_comment_counter = 0  # Jika berturut-turut tidak ada komentar baru, hentikan scroll

    for _ in range(max_scrolls):
        # Scroll ke elemen terakhir komentar
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

        # Hitung jumlah komentar saat ini
        current_count = len(page.query_selector_all("span[data-e2e='comment-level-1']"))
        time.sleep(10)

        # Jika jumlah komentar tidak bertambah setelah beberapa kali scroll, hentikan loop
        if current_count == previous_count:
            no_new_comment_counter += 1
            if no_new_comment_counter >= 3:  # Jika 3 kali berturut-turut tidak ada komentar baru, hentikan scrolling
                break
        else:
            no_new_comment_counter = 0  # Reset counter jika ada komentar baru

        previous_count = current_count

def scrape_tiktok_comments(video_url, max_scrolls=50):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(video_url, timeout=60000)
            time.sleep(5)

            # Tunggu elemen komentar pertama muncul
            page.wait_for_selector("span[data-e2e='comment-level-1']", timeout=15000)

            # Scroll otomatis untuk memuat semua komentar
            auto_scroll(page, max_scrolls=max_scrolls, delay=2)

            # Ambil semua komentar setelah scrolling selesai
            comment_elements = page.query_selector_all("span[data-e2e='comment-level-1']")
            comments = [comment.inner_text().strip() for comment in comment_elements if comment.inner_text().strip()]
        
        except Exception as e:
            print("Terjadi kesalahan:", e)
            comments = []
        
        finally:
            context.close()  # Tutup sesi Playwright
            browser.close()

        return comments

# Contoh penggunaan
if __name__ == "__main__":
    video_url = "https://www.tiktok.com/@iben_ma/video/7469490771532467462?lang=id-ID"
    comments = scrape_tiktok_comments(video_url, max_scrolls=50)

    print(f"\nDitemukan {len(comments)} komentar:\n")
    for idx, comment in enumerate(comments, start=1):
        print(f"{idx}. {comment}")
