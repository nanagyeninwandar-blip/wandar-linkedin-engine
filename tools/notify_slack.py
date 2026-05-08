"""
notify_slack.py — Sends a Slack message via Incoming Webhook.
Usage: python tools/notify_slack.py "Your message here"
Config: tools/config.json must contain {"slack_webhook_url": "https://hooks.slack.com/..."}
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        print("Error: tools/config.json not found.")
        print("Create it with: {\"slack_webhook_url\": \"https://hooks.slack.com/services/YOUR/WEBHOOK/URL\"}")
        return None
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def send_slack_message(webhook_url, message):
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print("Slack notification sent.")
            else:
                print(f"Slack returned status {resp.status}")
    except urllib.error.URLError as e:
        print(f"Failed to send Slack notification: {e}")


def notify_pipeline_complete(week_num, pillar_mix, output_path):
    message = (
        f"*Wandar LinkedIn Engine — Week {week_num} Complete*\n"
        f"4 posts ready for review.\n"
        f"Pillars this week: {pillar_mix}\n"
        f"Output: `{output_path}`\n"
        f"Open and review before Monday."
    )
    return message


def notify_hot_take(topic, source, pillar, virality_type, score):
    message = (
        f":zap: *HOT TAKE DETECTED*\n"
        f"Topic: {topic}\n"
        f"Source: {source}\n"
        f"Pillar: {pillar}\n"
        f"Virality type: {virality_type}\n"
        f"Relevance: {score}/10\n\n"
        f'Run `"hot take on this"` in Claude Code to generate posts.'
    )
    return message


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/notify_slack.py \"Your message here\"")
        sys.exit(1)

    config = load_config()
    if not config:
        sys.exit(1)

    webhook_url = config.get("slack_webhook_url")
    if not webhook_url or webhook_url == "YOUR_WEBHOOK_URL_HERE":
        print("Error: slack_webhook_url not configured in tools/config.json")
        print("Get your webhook URL from: https://api.slack.com/messaging/webhooks")
        sys.exit(1)

    message = sys.argv[1]
    send_slack_message(webhook_url, message)


if __name__ == "__main__":
    main()
