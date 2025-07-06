from infrahub_sdk.generator import InfrahubGenerator  # InfrahubGeneratorベースクラスをインポート
import os  # 環境変数の取得に使用
import sys  # システム操作（標準エラー出力、終了）に使用
import requests  # HTTPリクエスト送信用

class Generator(InfrahubGenerator):
    """
    ------------------------------------------------------------------------------------------------
    目的:
      Infrahub の Generator "backup-config_all-device" 実行時に、Ansible に対して Webhook を送信する
      Webhook は、ペイロードに"all-backup"を入れて、Ansible rulebookに対してすべての機器のコンフィグ取得を指示する
    ------------------------------------------------------------------------------------------------
    """

    async def generate(self, data: dict) -> None:
        # Webhookに送信するペイロードを設定
        payload = {
            "message": "all-backup"  # 実行対象を示すメッセージ
        }

        # 環境変数WEBHOOK_URLからWebhook先URLを取得
        url = os.getenv("WEBHOOK_URL", "http://ansible-rulebook:5000/endpoint")

        try:
            # POSTリクエストを送信
            resp = requests.post(
                url,
                json=payload,  # JSONデータとしてペイロードを送信
                headers={"Content-Type": "application/json"},  # Content-Typeヘッダーを設定
                timeout=10  # タイムアウトを10秒に設定
            )
            # HTTPエラーが発生した場合は例外をスロー
            resp.raise_for_status()
        except requests.RequestException as e:
            # エラー発生時は標準エラー出力に詳細を表示し、プロセスを終了
            print(f"ERROR: failed to POST to {url}: {e}", file=sys.stderr)
            sys.exit(1)

        # 成功時のステータスコードを標準出力に表示
        print(f"Triggered playbook via webhook: status_code={resp.status_code}")
