

from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from werkzeug.local import LocalProxy


#: An *itsdangerous*-based serializer that can be used to pass small
#: amounts of data through untrusted channels such as a verification
#: email.
#: :type: :class:`~itsdangerous.URLSafeTimedSerializer`
secure_serializer = LocalProxy(lambda: URLSafeTimedSerializer(current_app.config['SECRET_KEY'], b'fossir'))
