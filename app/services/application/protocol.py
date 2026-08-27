from typing import Any, Dict, Protocol


class ApplicationServiceProtocol(Protocol):
    async def get_stats(self, start: int, end: int) -> Dict[Any, Any]: ...
