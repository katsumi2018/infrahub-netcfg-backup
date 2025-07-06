from infrahub_sdk.generator import InfrahubGenerator  # Infrahub SDKのジェネレータ基底クラスをインポート
import os  # 環境変数の取得に使用
import sys  # システム操作（標準エラー出力や終了）に使用
import requests  # HTTPリクエスト送信用

class Generator(InfrahubGenerator):
    """
    ------------------------------------------------------------------------------------------------
    目的:
      Infrahub の Generator "backup-config_one-device" 実行時に、Ansible に対して Webhook を送信する
      Webhook は、ペイロードに取得したいホスト名を入れて、Ansible rulebookに対して対象ホストに対してコンフィグ取得を指示する
    ------------------------------------------------------------------------------------------------
    """
    async def generate(self, data: dict) -> None:
        # データからデバイス名を抽出
        # data: GraphQLクエリで取得したInfraDeviceノードの情報を含む辞書
        device_name = data["InfraDevice"]["edges"][0]["node"]["name"]["value"]  # 最初のノードのname.valueを取得

        # Webhookに送信するペイロードを設定
        payload = {
            "message": device_name  # デバイス名をメッセージとして指定
        }

        # 環境変数WEBHOOK_URLからWebhook先URLを取得
        url = os.getenv("WEBHOOK_URL", "http://ansible-rulebook:5000/endpoint")

        try:
            # POSTリクエストを送信
            resp = requests.post(
                url,
                json=payload,  # JSON形式でペイロードを送信
                headers={"Content-Type": "application/json"},  # Content-Typeヘッダを設定
                timeout=10  # タイムアウトを秒単位で指定
            )
            # HTTPステータスコードがエラーを示す場合、例外を発生させる
            resp.raise_for_status()
        except requests.RequestException as e:
            # エラー発生時には標準エラーに詳細を出力し、プロセスを終了
            print(f"ERROR: failed to POST to {url}: {e}", file=sys.stderr)
            sys.exit(1)

        # 成功時にはステータスコードをログ出力
        print(f"Triggered playbook via webhook: status_code={resp.status_code}")
