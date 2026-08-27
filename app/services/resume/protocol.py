from typing import List, Protocol

from .schemas import (
    ResumeCreate,
    ResumeData,
    ResumeDetail,
    ResumeSummary,
    ResumeUpdate,
    ResumeUploadResponse,
)


class ResumeServiceProtocol(Protocol):
    async def list_resumes(self) -> List[ResumeSummary]: ...
    async def get_resume(self, resume_id: str) -> ResumeDetail: ...

    async def create_resume_json(
        self, data: ResumeCreate
    ) -> ResumeUploadResponse: ...

    async def upload_resume_file(
        self, file: bytes, filename: str
    ) -> ResumeUploadResponse: ...

    async def update_resume(
        self, resume_id: str, data: ResumeUpdate
    ) -> ResumeDetail: ...

    async def delete_resume(self, resume_id: str) -> None: ...
    async def set_primary_resume(self, resume_id: str) -> None: ...
    async def export_resume_pdf(self, resume_id: str) -> bytes: ...
    async def get_resume_draft(self) -> ResumeData: ...
