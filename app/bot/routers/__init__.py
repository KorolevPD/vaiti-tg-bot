from app.bot.flows.skill_selector import router as skill_selector_router

from .companies import router as companies_router
from .cover_letters import router as cover_letters_router
from .menu import router as menu_router
from .noop import router as noop_router
from .profile import router as profile_router
from .resume import router as resume_router
from .skills_catalog import router as skills_catalog_router
from .statistic import router as statistic_router
from .support import router as support_router
from .trainer import router as trainer_router
from .vacancies import router as vacancies_router

all_routers = (
    skill_selector_router.router,
    companies_router.router,
    cover_letters_router.router,
    menu_router.router,
    noop_router.router,
    profile_router.router,
    resume_router.router,
    skills_catalog_router.router,
    statistic_router.router,
    support_router.router,
    trainer_router.router,
    vacancies_router.router,
)

all_commands = [
    menu_router.bot_command,
    profile_router.bot_command,
    companies_router.bot_command,
    skills_catalog_router.bot_command,
    vacancies_router.bot_command,
    statistic_router.bot_command,
    trainer_router.bot_command,
    support_router.bot_command,
]
