import json
import os
import urllib.request
import urllib.error

# Colab で立てた FastAPI の公開 URL。
# 実行時に LLM_API 環境変数があればそちらを優先します。
API_ROOT = os.getenv("LLM_API", "https://f26c-34-125-15-195.ngrok-free.app")
API_URL = API_ROOT.rstrip("/") + "/generate"


def handler(event, context):
    """
    event["body"] には ChatGPT 形式の JSON が送られてくる想定。
    {
        "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "こんにちは"},
            ...
        ]
    }
    ここでは最後の user メッセージだけを prompt に使う。
    """
    try:
        body = json.loads(event.get("body", "{}"))
        messages = body.get("messages", [])
        if not messages:
            return _resp(400, {"error": "messages is empty"})

        prompt = messages[-1]["content"]

        # FastAPI へ POST
        req_data = json.dumps({"prompt": prompt}).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as res:
            res_json = json.load(res)

        reply_text = res_json.get("generated_text", "")
        return _resp(200, {"reply": reply_text})

    except urllib.error.HTTPError as e:
        return _resp(e.code, {"error": e.read().decode()})
    except Exception as e:
        return _resp(500, {"error": str(e)})


def _resp(status, body_dict):
    """ヘルパー：JSON レスポンスを統一フォーマットで返す"""
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_dict, ensure_ascii=False),
    }