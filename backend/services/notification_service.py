import json
import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials, messaging


_firebase_initialized = False


def initialize_firebase() -> None:
    """
    Initialize Firebase Admin SDK using credentials from environment.

    FIREBASE_CREDENTIALS can contain either:
    1. Path to a Firebase service-account JSON file
    2. JSON string containing the service-account credentials
    """

    global _firebase_initialized

    if _firebase_initialized:
        return

    credentials_value = os.getenv("FIREBASE_CREDENTIALS")

    if not credentials_value or not credentials_value.strip():
        raise ValueError(
            "FIREBASE_CREDENTIALS environment variable is missing"
        )

    credentials_value = credentials_value.strip()

    if os.path.isfile(credentials_value):
        cred = credentials.Certificate(credentials_value)

    else:
        try:
            service_account_info = json.loads(credentials_value)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "FIREBASE_CREDENTIALS must be a valid file path "
                "or Firebase service-account JSON"
            ) from exc

        cred = credentials.Certificate(service_account_info)

    firebase_admin.initialize_app(cred)

    _firebase_initialized = True


def send_fcm_notification(
    fcm_token: str,
    title: str,
    body: str
) -> str:
    """
    Send a push notification to a single FCM device token.

    Returns Firebase message ID.
    """

    if not fcm_token or not fcm_token.strip():
        raise ValueError("FCM token must not be empty")

    initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=fcm_token.strip()
    )

    return messaging.send(message)