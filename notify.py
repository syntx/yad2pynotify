import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logging.getLogger().setLevel(logging.INFO)


def send_notification(config, task_name, items):
    logging.info("Processing notification for task: %s" % task_name)
    try:
        api_key = config['api_key']
        send_to = config['send_to']
        send_from = config['send_from']
    except KeyError:
        logging.error("Notification sending config is invalid.")
        return False

    body = "<strong>%d new items found:</strong><ul>" % len(items)
    for item in items:
        body += "<li><a href='%s'>%s</a></li>" % (item, item)
    body += "</ul>"

    message = Mail(
        from_email=send_from,
        to_emails=send_to,
        subject="Yad2 Notifications for: %s" % task_name,
        html_content=body)

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        if response.status_code == 202:
            logging.info("*** EMAIL NOTIFICATION SENT ***")
        else:
            logging.warning("Error sending notification. check logs. response status code: %d" % response.status_code)
    except Exception as e:
        logging.error("Error sending notification: %r" % e.message)

