from playwright.sync_api import sync_playwright
import time
import csv

# Simplified configuration: read from fixed file `url.txt`, default headful browser, max scrolls
URL_FILE = "url.txt"
MAX_SCROLLS = 50
HEADLESS = False

def auto_scroll(page, max_scrolls=50, delay=2):
    """Automatically scroll the page until comments are loaded.

    The function scrolls the page up to `max_scrolls` times. It keeps track of how
    many comments are loaded; if the number of loaded comments does not increase
    for three consecutive iterations, scrolling stops early.
    """
    previous_count = 0
    no_new_comment_counter = 0  # stop scrolling after consecutive iterations with no new comments

    for _ in range(max_scrolls):
        # Scroll to the bottom of the page (comments area)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

        # Count currently loaded comments
        current_count = len(page.query_selector_all("span[data-e2e='comment-level-1']"))
        time.sleep(10)

        # If count hasn't increased, increment the stagnant counter and break after 3 tries
        if current_count == previous_count:
            no_new_comment_counter += 1
            if no_new_comment_counter >= 3:
                break
        else:
            no_new_comment_counter = 0

        previous_count = current_count

def scrape_tiktok_comments(video_url, max_scrolls=50, headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        

        try:
            print("Opening page:", video_url)
            page.goto(video_url, timeout=120000)
            time.sleep(5)

            # If the page prompts for human verification (captcha/login), complete it
            # manually in the visible browser. Allow a generous wait time so you can
            # finish the verification and the comments can load.
            wait_ms = 2 * 60 * 1000  # 2 minutes
            print(f"If the page prompts for human verification, please complete it in the opened browser. The script will wait until comments appear or up to {int(wait_ms/1000)} seconds...")
            # Wait for the first comment element to appear
            page.wait_for_selector("span[data-e2e='comment-level-1']", timeout=wait_ms)

            # Automatically scroll to load all comments
            auto_scroll(page, max_scrolls=max_scrolls, delay=2)

            # After scrolling, collect comment elements and try to locate the user profile for each comment
            comment_elements = page.query_selector_all("span[data-e2e='comment-level-1']")
            comments = []
            for comment in comment_elements:
                try:
                    text = comment.inner_text().strip()
                except Exception:
                    text = ""
                if not text:
                    continue

                # Search up a few ancestor levels from the comment node to find an
                # ancestor that contains an <a href="/@username"> link for the user
                try:
                    user_href = comment.evaluate('''(el) => {
                        let node = el;
                        for (let i = 0; i < 8; i++) {
                            if (!node) break;
                            let a = node.querySelector('a[href*="/@"]');
                            if (a) return a.getAttribute('href');
                            node = node.parentElement;
                        }
                        return '';
                    }''')
                except Exception:
                    user_href = ""

                # Normalize user_id (if href exists, take the part after "/@")
                user_id = ""
                if user_href:
                    try:
                        # href 可能形如 https://www.tiktok.com/@username 或 /@username
                        if "/@" in user_href:
                            user_id = user_href.split('/@')[-1].split('?')[0].strip('/')
                        else:
                            user_id = user_href.strip('/').split('/')[-1]
                    except Exception:
                        user_id = user_href

                comments.append({"user_id": user_id, "user_profile": user_href, "text": text})
        
        except Exception as e:
            print("Error occurred:", e)
            comments = []
        
        finally:
            context.close()  # 关闭 Playwright 会话
            browser.close()

        return comments

# Read URL from fixed file (url.txt)
if __name__ == "__main__":
    # 从固定文件读取 URL
    try:
        with open(URL_FILE, "r", encoding="utf-8") as f:
            video_url = f.read().strip()
    except FileNotFoundError:
        print(f"URL file not found: {URL_FILE}. Please write the TikTok video link in this file and retry.")
        raise SystemExit(1)
    except Exception as e:
        print("Failed to read URL file:", e)
        raise SystemExit(1)

    if not video_url:
        print(f"No valid URL found in {URL_FILE}. Please add a TikTok video link (one per file).")
        raise SystemExit(1)

    comments = scrape_tiktok_comments(video_url, max_scrolls=MAX_SCROLLS, headless=HEADLESS)

    print(f"\nFound {len(comments)} comments:\n")
    for idx, comment in enumerate(comments, start=1):
        uid = comment.get("user_id", "")
        print(f"{idx}. [{uid}] {comment.get('text', '')}")

    # Only generate CSV if comments were retrieved; filename is timestamp yyyymmddss.csv
    if comments:
        timestamp_str = time.strftime("%Y%m%d%S", time.localtime())  # YYYYMMDDSS
        csv_filename = f"{timestamp_str}.csv"
        try:
            # Use utf-8-sig so Excel can open non-ASCII text without corruption
            with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["index", "user_id", "user_profile", "comment"])  # header
                for i, c in enumerate(comments, start=1):
                    writer.writerow([i, c.get("user_id", ""), c.get("user_profile", ""), c.get("text", "")])
            print(f"\nSaved comments to CSV: {csv_filename}")
        except Exception as e:
            print("Error saving CSV:", e)
    else:
        print("\nNo comments retrieved; CSV not created.")
