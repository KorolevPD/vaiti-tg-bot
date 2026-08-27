from typing import Optional

from app.core.config import settings
from app.services.resume.schemas import ResumeUploadResponse
from app.services.resume.service import ResumeService


def get_service(auth_header: str) -> ResumeService:
    return ResumeService(settings.SERVICES_URL, auth_header)


async def get_resume_file(auth_header: str) -> Optional[bytes]:
    service = get_service(auth_header)
    resumes = await service.list_resumes()
    resume = next((r for r in resumes if r.is_primary), None)
    if resume:
        return await service.export_resume_pdf(resume.id)
    return None


async def upload_resume_file(
    file: bytes, filename: str, auth_header: str
) -> ResumeUploadResponse:
    service = get_service(auth_header)
    return await service.upload_resume_file(file, filename)
