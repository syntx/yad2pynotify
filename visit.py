import logging
from splinter import Browser
from notify import send_notification
from time import sleep

WAIT_BETWEEN_TASKS = 10


def visit_all_tasks(config, db):
    browser = None
    for task in config.get('tasks', []):
        if browser:
            logging.info('Waiting for %d seconds...' % WAIT_BETWEEN_TASKS)
            sleep(WAIT_BETWEEN_TASKS)
        try:
            browser = Browser('chrome', headless=True)
            task_name = task["name"]
            logging.info("Running task: %s..." % task_name)
            if task_name not in db:
                db[task_name] = {}
            logging.info("Waiting for page to load...")
            browser.visit(task["url"])
            logging.info("Done loading page.")
            items = browser.find_by_css('div[class="feeditem table"]')
            logging.info("Got %d items..." % len(items))
            new_items = []
            for item in items:
                try:
                    # logging.info("Parsing next item...")
                    div = item.find_by_tag("div").first
                    item_id = div['item-id']
                    item_url = "https://www.yad2.co.il/s/c/" + item_id
                    if item_id not in db[task_name]:
                        logging.info("*** New item detected: %s", item_url)
                        # save item in db
                        db[task_name][item_id] = item_url
                        # store for sending notification:
                        new_items.append(item_url)
                    else:
                        logging.info("Existing item detected: %s", item_url)
                except Exception as ex:
                    logging.error("Error parsing item from page: %r", ex)
            # send notifications for task:
            if new_items:
                send_notification(config['sendgrid'], task_name, new_items)
            logging.info("Finished task: %s" % task_name)
        finally:
            browser.quit()

