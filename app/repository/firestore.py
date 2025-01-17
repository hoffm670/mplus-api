import uuid

from constants import REGION, SNAPSHOTS, TIMESTAMP
from firebase_admin import credentials, firestore, initialize_app
from config import get_config, IS_PROD

cred = credentials.Certificate("firebase-admin-key.json")
initialize_app(cred)


class FirestoreRepository():

    def __init__(self):
        self.db = firestore.client()

    def add_snapshot_document(self, data):
        id = f"{data['region']}-{data['date']}-{str(uuid.uuid1())}"
        data[IS_PROD] = get_config().get(IS_PROD)
        self.db.collection(SNAPSHOTS).document(id).set(data)

    def get_latest_snapshot_document(self, region: str):
        return self.db.collection(SNAPSHOTS).where(filter=firestore.FieldFilter(REGION, "==", region)).order_by(TIMESTAMP).limit_to_last(1).get()[0].to_dict()
