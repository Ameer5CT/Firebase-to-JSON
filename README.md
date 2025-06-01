# Firebase-to-JSON
Extract Firebase data (Firestore Database, Realtime Database and Storage structure) to JSON files

## How to use:
1. Go to Firebase console → “Project settings” → “Service accounts” → “Generate new private key” and save the JSON next to the main.py file and name it adminsdk.json
2. Replace "REALTIME_DATABASE_LINK" and "FIREBASE_STORAGE_BUCKET_LINK" with your database links that you can find in the Firebase console.
3. Run main.py just like how you run any python file and you will get the three JSON files in a folder called backup next to the main.py file.

Note: You need to have "firebase_admin" library, You can install it by running "pip install firebase-admin" in the console.
