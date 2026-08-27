from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.types.input_file import BufferedInputFile

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.bot.utils import safe_response

from .callbacks import ResumeAction, ResumeCallback
from .fsm import ResumeState
from .views import get_resume_file, upload_resume_file

router = Router()


@router.callback_query(ResumeCallback.filter(F.action == ResumeAction.UPLOAD))
async def resume_upload(cb: CallbackQuery, state: FSMContext) -> None:
    await safe_response(
        cb,
        "Отправь PDF-файл с твоим резюме.",
        InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
    )
    await state.set_state(ResumeState.waiting_for_pdf)


@router.callback_query(
    ResumeCallback.filter(F.action == ResumeAction.DOWNLOAD)
)
async def resume_download(cb: CallbackQuery, auth_header: str) -> None:
    data = await get_resume_file(auth_header)

    if not data:
        await cb.answer("❌ Резюме не найдено.")
        return

    if cb.message:
        await cb.message.answer_document(BufferedInputFile(data, "Резюме.pdf"))
        await cb.answer()


@router.message(ResumeState.waiting_for_pdf, F.document)
async def handle_resume_pdf(
    msg: Message, state: FSMContext, auth_header: str
) -> None:
    document = msg.document
    if document is None:
        return

    file_name = document.file_name
    if file_name is None or not file_name.lower().endswith(".pdf"):
        await safe_response(msg, "Файл должен быть в формате PDF.")
        return

    if msg.bot:
        file = await msg.bot.get_file(document.file_id)
        if file and file.file_path:
            file_bytes = await msg.bot.download_file(file.file_path)
            if file_bytes:
                file_data = file_bytes.read()

    if file_data:
        r = await upload_resume_file(file_data, file_name, auth_header)
        if r.status == "success":
            await state.clear()
            await safe_response(
                msg,
                "✅ Резюме успешно загружено!",
                InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
            )
            return

    await safe_response(msg, "❌ Не удалось загрузить резюме.")


@router.message(ResumeState.waiting_for_pdf)
async def handle_not_document(message: Message) -> None:
    await message.answer("❌ Отправьте PDF-файл.")
