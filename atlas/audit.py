
import logging
from pathlib import Path
from contextvars import ContextVar

request_id_context = ContextVar("request_id", default="no-request")

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("atlas.audit")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "atlas_audit.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)



def log_agent_event(
    tool_name: str,
    outcome: str
) -> None:
    request_id = request_id_context.get()

    logger.info(
        "request_id=%s | Agent tool=%s outcome=%s",
        request_id,
        tool_name,
        outcome
    )

