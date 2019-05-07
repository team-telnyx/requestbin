from datetime import timedelta
import logging
import os

logging.basicConfig(level=logging.WARNING)
_LOG = logging.getLogger(__name__)

DEBUG = True
REALM = os.environ.get('REALM', 'local')

PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "e239163aa2008311405b2eae0c4c617ae88d49075c31119c0d2b59141e294e94")

BIN_TTL = int(os.environ.get("BIN_TTL", timedelta(days=2).total_seconds()))
EXTENDED_TTL = int(os.environ.get("EXTENDED_TTL", timedelta(days=5 * 365).total_seconds()))

MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
IGNORE_HEADERS = []
MAX_REQUESTS = 20
CLEANUP_INTERVAL = 3600

STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    _LOG.warning("Using Redis: {}".format(REDIS_URL))

    STORAGE_BACKEND = "requestbin.storage.redis.RedisStorage"
    REDIS_PREFIX = "requestbin"

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)

    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
