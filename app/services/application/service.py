from datetime import datetime as dt, timezone as tz
from typing import Any, Dict, cast

from app.clients import APIClient

from .protocol import ApplicationServiceProtocol


class ApplicationService(APIClient, ApplicationServiceProtocol):
    async def get_stats(self, s_date: float, e_date: float) -> Dict[Any, Any]:
        start_dt = dt.fromtimestamp(s_date, tz=tz.utc)
        end_dt = dt.fromtimestamp(e_date, tz=tz.utc)

        params = {
            "startDate": start_dt.isoformat().replace("+00:00", "Z"),
            "endDate": end_dt.isoformat().replace("+00:00", "Z"),
        }
        r = await self._client.get("/api/v1/application/stats", params=params)
        r.raise_for_status()
        return cast(Dict[Any, Any], r.json())
