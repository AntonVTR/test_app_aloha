def open_and_check(context, url, expected, log):
    page = context.new_page()
    page.goto(url)
    title = page.title()
    log.info(f"Opened {url}: {title}")
    assert expected in title, f"Expected '{expected}' in title but got '{title}'"
    return page

def test_tabs_open_close_focus(browser_context, request):
    log = request.node._logger
    ctx = browser_context

    page1 = open_and_check(ctx, "https://example.com", "Example", log)
    page2 = open_and_check(ctx, "https://duckduckgo.com", "DuckDuckGo", log)

    page2.close()
    log.info("Closed tab 2")

    assert not page1.is_closed(), "Tab 1 is unexpectedly closed"
    log.info(f"Active tab now: {page1.title()}")