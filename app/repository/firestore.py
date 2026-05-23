import logging
import uuid

from config import get_collection_for_tier
from constants import REGION, TIMESTAMP
from firebase_admin import credentials, firestore, initialize_app
from models.snapshot import MythicPlusSnapshot

cred = credentials.Certificate("firebase-admin-key.json")
initialize_app(cred)

logger = logging.getLogger('firestore.repository')


class FirestoreRepository():

    def __init__(self):
        self.db = firestore.client()

    def add_snapshot_document(self, data: MythicPlusSnapshot):
        collection = get_collection_for_tier(data.tier)
        id = f"{data.date}-{data.region}-{str(uuid.uuid1())}"
        logger.info(f"Posting to {collection} with id: {id}")
        self.db.collection(collection).document(id).set(data.to_json())

    def get_latest_snapshot_document(self, region: str, tier: str):
        collection = get_collection_for_tier(tier)
        return self.db.collection(collection).where(
            filter=firestore.FieldFilter(REGION, "==", region)
        ).order_by(TIMESTAMP).limit_to_last(1).get()[0].to_dict()
