import firebase_admin
from firebase_admin import firestore, credentials
import uuid

SCANS = 'scans'
SNAPSHOTS = 'snapshot'


class FirestoreRepository():

    def __init__(self):
        cred = credentials.Certificate("firebase-admin-key.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_scan_document(self, data):
        id = str(uuid.uuid1())
        self.db.collection(SCANS).document(id).set(data)

    def add_snapshot_document(self, data):
        id = str(uuid.uuid1())
        self.db.collection(SNAPSHOTS).document(id).set(data)

    def get_latest_snapshot_document(self, region: str):
        return self.db.collection(SNAPSHOTS).where(filter=firestore.FieldFilter("region", "==", region)).order_by("timestamp").limit_to_last(1).get()[0].to_dict()
