import logging
import uuid

from config import COLLECTION, get_config
from constants import REGION, SNAPSHOTS, TIMESTAMP
from firebase_admin import credentials, firestore, initialize_app
from models.snapshot import MythicPlusSnapshot

cred = credentials.Certificate("firebase-admin-key.json")
initialize_app(cred)

logger = logging.getLogger('firestore.repository')


class FirestoreRepository():

    def __init__(self):
        self.db = firestore.client()

    def add_snapshot_document(self, data: MythicPlusSnapshot):
        id = f"{data.date}-{data.region}-{str(uuid.uuid1())}"
        logger.info(f"Posting collection with id: {id}")
        self.db.collection(get_config().get(COLLECTION)).document(id).set(data.to_json())

    def get_latest_snapshot_document(self, region: str):
        return self.db.collection(SNAPSHOTS).where(filter=firestore.FieldFilter(REGION, "==", region)).order_by(TIMESTAMP).limit_to_last(1).get()[0].to_dict()
