import firebase_admin
from firebase_admin import credentials, db, firestore, storage
import json
import os


# Prepare firebase database
# Firebase console → “Project settings” → “Service accounts” → “Generate new private key” and save the JSON
# next to this main.py file and name it adminsdk.json
cred = credentials.Certificate("adminsdk.json")

# Fill the links
# Example databaseURL: https://example.europe-west1.firebasedatabase.app/
# Example storageBucket: example.firebasestorage.app
firebase_admin.initialize_app(cred, {
    "databaseURL": "REALTIME_DATABASE_LINK",
    "storageBucket": "FIREBASE_STORAGE_BUCKET_LINK"
})
fs = firestore.client()


# Realtime database json
def realtime_json():
    data = db.reference('/').get()

    backup_path = "backup/realtime.json"
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2)
    print("realtime.json Done ✅")


# Firestore json
def firestore_json():
    def fetch_collection(col_ref):
        data = {}
        for doc in col_ref.stream():
            doc_dict = doc.to_dict() or {}
            # fetch subcollections
            subs = {sub.id: fetch_collection(sub)
                    for sub in doc.reference.collections()}
            if subs:
                doc_dict.update({k: v for k, v in subs.items()})
            data[doc.id] = doc_dict
        return data

    all_data = {}
    for root_col in fs.collections():
        all_data[root_col.id] = fetch_collection(root_col)

    backup_path = "backup/firestore.json"
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print("firestore.json Done ✅")


# Firebase storage structure json
def storage_json():
    def build_tree(blobs):
        tree = {}
        for blob in blobs:
            parts = blob.name.split("/")
            node = tree
            for p in parts[:-1]:
                node = node.setdefault(p, {})
            node[parts[-1]] = None
        return tree

    structure = build_tree(storage.bucket().list_blobs())
    backup_path = "backup/storage_structure.json"
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w") as f:
        json.dump(structure, f, indent=2)
    print("storage_structure.json Done ✅")


realtime_json()
firestore_json()
storage_json()
