import uuid

import firebase_admin
from constants import REGION, SNAPSHOTS, TIMESTAMP
from firebase_admin import credentials, firestore


class FirestoreRepository():

    def __init__(self):
        cred = credentials.Certificate("firebase-admin-key.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_snapshot_document(self, data):
        id = str(uuid.uuid1())
        self.db.collection(SNAPSHOTS).document(id).set(data)

    def get_latest_snapshot_document(self, region: str):
        return self.db.collection(SNAPSHOTS).where(filter=firestore.FieldFilter(REGION, "==", region)).order_by(TIMESTAMP).limit_to_last(1).get()[0].to_dict()
