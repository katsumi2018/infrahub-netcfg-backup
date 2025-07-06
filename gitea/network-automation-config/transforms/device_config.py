import logging
from pathlib import Path
from infrahub_sdk.transforms import InfrahubTransform

LOG = logging.getLogger(__name__)

class DeviceConfig(InfrahubTransform):
    """
    ------------------------------------------------------------------------------------------------
    目的:
      queries/device_name.gql から渡されるデバイス名を使い、
      リポジトリ内の config/<device>.txt を読み込んで
      その内容を Infrahubu内で text/plain の Artifact として返す。
    ------------------------------------------------------------------------------------------------
    """

    # .infrahub.yml の queries セクションで定義したクエリ名
    query = "device_name_query"

    async def transform(self, data):  # noqa: D401
        # 1) デバイス名を取得
        device_name = data["InfraDevice"]["edges"][0]["node"]["name"]["value"]

        # 2) リポジトリのルート配下から config/<device>.txt を探す
        cfg_path = Path(self.root_directory) / "config" / f"{device_name}.txt"

        if not cfg_path.is_file():
            # Prefect のログでも分かりやすいよう、詳細にエラーを出す
            raise FileNotFoundError(
                f"Config file '{cfg_path}' not found. "
                "Ensure that config/<device>.txt exists in the repository "
                f"and is committed to branch '{self.branch_name}'."
            )

        # 3) そのまま text/plain として返す
        return cfg_path.read_text(encoding="utf-8")