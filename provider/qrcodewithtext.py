from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class QrcodewithtextProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            print("Validating credentials...")

            print("Credentials are valid!")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
