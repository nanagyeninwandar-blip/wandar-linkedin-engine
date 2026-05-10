"""
Quick Slack webhook test.
Run: python tools/test_slack.py <your-webhook-url>
"""
import sys
import requests

def test(webhook_url):
    print(f"Sending test message to: {webhook_url[:50]}...")
    resp = requests.post(
        webhook_url,
        json={"text": "✅ Wandar pipeline Slack test — webhook is working."},
        timeout=10,
    )
    print(f"HTTP status: {resp.status_code}")
    print(f"Response:    {resp.text}")
    if resp.status_code == 200 and resp.text == "ok":
        print("\nSUCCESS — Slack webhook is working correctly.")
    else:
        print("\nFAILED — see response above for the error.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/test_slack.py <webhook-url>")
        sys.exit(1)
    test(sys.argv[1])
