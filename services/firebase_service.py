import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore


db = None


def initialise_firebase():
    global db

    if db is not None:
        return db

    project_root = Path(__file__).resolve().parent.parent
    firebase_folder = project_root / "firebase"

    service_account_files = list(
        firebase_folder.glob("*.json")
    )

    if not service_account_files:
        raise FileNotFoundError(
            "No Firebase service-account JSON file was found "
            "inside the firebase folder."
        )

    service_account_path = service_account_files[0]

    if not firebase_admin._apps:
        credential = credentials.Certificate(
            str(service_account_path)
        )

        firebase_admin.initialize_app(credential)

    db = firestore.client()

    return db


def test_firebase_connection():
    database = initialise_firebase()

    test_reference = database.collection(
        "system"
    ).document("connection_test")

    test_reference.set({
        "status": "connected",
        "application": "Dublin Bus Rainfall Dashboard"
    })

    saved_document = test_reference.get()

    return saved_document.to_dict()