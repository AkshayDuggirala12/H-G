import json
import logging
from urllib import error, request

from app.config import settings
from app.models import ClientAccessRequest, User

logger = logging.getLogger(__name__)


def send_access_request_notification(user: User, access_request: ClientAccessRequest) -> bool:
    recipient = settings.notification_email or settings.admin_email
    if (
        not recipient
        or not settings.emailjs_service_id
        or not settings.emailjs_template_id
        or not settings.emailjs_public_key
    ):
        return False

    payload = {
        "service_id": settings.emailjs_service_id,
        "template_id": settings.emailjs_template_id,
        "user_id": settings.emailjs_public_key,
        "template_params": {
            "to_email": recipient,
            "admin_email": recipient,
            "client_id": str(user.id),
            "client_name": user.name,
            "client_email": user.email,
            "age": str(access_request.age),
            "weight_kg": access_request.weight_kg,
            "height_cm": access_request.height_cm,
            "workout_frequency": access_request.workout_frequency,
            "goals": access_request.goals,
            "status": access_request.status,
            "created_at": access_request.created_at.isoformat(),
            "subject": f"New HARA-GYM access request from {user.name}",
        },
    }
    if settings.emailjs_private_key:
        payload["accessToken"] = settings.emailjs_private_key

    http_request = request.Request(
        url="https://api.emailjs.com/api/v1.0/email/send",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://localhost",
            "Referer": "http://localhost/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
        },
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=10) as response:
            success = 200 <= response.status < 300
            if success:
                logger.info(
                    "EmailJS notification sent for client_id=%s email=%s",
                    user.id,
                    user.email,
                )
            else:
                logger.warning(
                    "EmailJS notification returned unexpected status=%s for client_id=%s",
                    response.status,
                    user.id,
                )
            return success
    except error.HTTPError as exc:
        try:
            error_body = exc.read().decode("utf-8", errors="ignore")
        except Exception:
            error_body = ""
        logger.exception(
            "EmailJS HTTP error for client_id=%s status=%s body=%s",
            user.id,
            exc.code,
            error_body,
        )
        return False
    except error.URLError:
        logger.exception(
            "EmailJS connection error for client_id=%s email=%s",
            user.id,
            user.email,
        )
        return False
