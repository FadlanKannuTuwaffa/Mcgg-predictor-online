SETUP (step-by-step)
====================

1) Create a new GitHub repository (empty) and upload the ZIP contents to it
   - Or initialize locally and `git push` to a new repo.

2) Backend (FastAPI)
   - The backend uses SQLite by default for easy quick start.
   - To run locally (development):
     ```
     cd backend
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     export JWT_SECRET="change_this_secret"
     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
     ```
   - API docs: http://localhost:8000/docs
   - Create an admin user (locally) using the `create_admin.py` helper or update DB manually.

3) Mobile app (Kivy) - development
   - Edit `mobile/api_client.py` BASE url if backend is local:
     ```
     export MCGG_API="http://10.0.2.2:8000"   # emulator / LAN address
     ```
   - Run:
     ```
     cd mobile
     python main.py
     ```

4) GitHub Actions / Build APK
   - In your repo settings -> Secrets -> Actions add:
     - KEYSTORE_BASE64 : base64 of your signing JKS file (if you want signed builds)
     - KEYSTORE_PASSWORD
     - KEY_ALIAS
     - KEY_PASSWORD
   - Push to main branch or run workflow manually in Actions -> Build Signed APK.

5) Keystore creation (example):
   On your local machine (not inside repo), generate keystore:
   ```
   keytool -genkeypair -v -keystore mcgg-release-key.jks -alias mcgg-xbot-key \
     -keyalg RSA -keysize 2048 -validity 10000
   ```
   Then base64-encode to upload as secret:
   ```
   base64 mcgg-release-key.jks | tr -d '\n' > keystore.b64
   # copy keystore.b64 content into KEYSTORE_BASE64 secret
   ```

6) After a successful build, download artifact from Actions.
