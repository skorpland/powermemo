import logging
import uuid

LOG = logging.getLogger("powermemo")


def string_to_uuid(s: str, salt="powermemo_client") -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, s + salt))
