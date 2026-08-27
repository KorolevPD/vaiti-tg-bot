from typing import List

from app.clients import APIClient

from .protocol import ResumeServiceProtocol
from .schemas import (
    ResumeCreate,
    ResumeData,
    ResumeDetail,
    ResumeSummary,
    ResumeUpdate,
    ResumeUploadResponse,
)


class ResumeService(APIClient, ResumeServiceProtocol):
    async def list_resumes(self) -> List[ResumeSummary]:
        r = await self._client.get("/resumes")
        r.raise_for_status()
        return [ResumeSummary.model_validate(item) for item in r.json()]

    async def get_resume(self, resume_id: str) -> ResumeDetail:
        r = await self._client.get(f"/resumes/{resume_id}")
        r.raise_for_status()
        return ResumeDetail.model_validate(r.json())

    async def create_resume_json(
        self, data: ResumeCreate
    ) -> ResumeUploadResponse:
        r = await self._client.post(
            "/resumes/json",
            json=data.model_dump(),
        )
        r.raise_for_status()
        return ResumeUploadResponse.model_validate(r.json())

    async def upload_resume_file(
        self, file: bytes, filename: str
    ) -> ResumeUploadResponse:
        r = await self._client.post(
            "/resumes/upload",
            files={"file": (filename, file)},
        )
        r.raise_for_status()
        return ResumeUploadResponse.model_validate(r.json())

    async def update_resume(
        self, resume_id: str, data: ResumeUpdate
    ) -> ResumeDetail:
        r = await self._client.put(
            f"/resumes/{resume_id}",
            json=data.model_dump(),
        )
        r.raise_for_status()
        return ResumeDetail.model_validate(r.json())

    async def delete_resume(self, resume_id: str) -> None:
        r = await self._client.delete(f"/resumes/{resume_id}")
        r.raise_for_status()

    async def set_primary_resume(self, resume_id: str) -> None:
        r = await self._client.post(f"/resumes/{resume_id}/primary")
        r.raise_for_status()

    async def export_resume_pdf(self, resume_id: str) -> bytes:
        r = await self._client.get(f"/resumes/{resume_id}/export/pdf")
        r.raise_for_status()
        return r.content

    async def get_resume_draft(self) -> ResumeData:
        r = await self._client.get("/resumes/draft")
        r.raise_for_status()
        return ResumeData.model_validate(r.json())
