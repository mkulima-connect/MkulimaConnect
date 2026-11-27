## Deploy live (GitHub-connected host)

Repo is deploy-ready. No platform CLI is installed locally; deploy via a host dashboard connected to GitHub.

### Render (recommended quick path)
1. Push is already on `main`: https://github.com/mkulima-connect/MkulimaConnect
2. In Render: New + > Blueprint or Web Service, connect the GitHub repo.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn MkulimaSystem.wsgi:application`
5. Set env vars:
   - `SECRET_KEY` = strong random value
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `<your-service>.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://<your-service>.onrender.com`
   - `PAYMENT_GATEWAY_ENABLED` = `False`
   - `REDIS_URL` = Redis URL (if using Channels/WebSocket in production)
6. Deploy. App should be live at the Render URL.

### Railway/other
Use same build/start commands and env vars. For Channels, provision Redis and set `REDIS_URL`.
