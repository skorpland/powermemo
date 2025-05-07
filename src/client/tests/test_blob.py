import pytest
from powermemo.core.blob import DocBlob, ChatBlob
from powermemo.error import ServerError
from powermemo.core.blob import BlobType


def test_blob_curd_client(api_client):
    a = api_client
    blob = DocBlob(content="test", fields={"1": "fool"})
    u = a.add_user()
    print(u)
    ud = a.get_user(u)

    b = ud.insert(blob)
    print(ud.get(b))
    print(ud.delete(b))
    with pytest.raises(ServerError):
        ud.get(b)


def test_blob_get_all(api_client):
    a = api_client
    blob = DocBlob(content="test", fields={"1": "fool"})
    u = a.add_user()
    print(u)
    ud = a.get_user(u)

    b = ud.insert(blob)
    b = ud.insert(blob)
    b = ud.insert(blob)
    b = ud.insert(blob)
    r = ud.get_all(BlobType.doc)
    print(ud.delete(b))
    assert len(r) == 4
    with pytest.raises(ServerError):
        ud.get(b)
    a.delete_user(u)


def test_flush_curd_client(api_client):
    mb = api_client
    uid = mb.add_user({"me": "test"})
    u = mb.get_user(uid)
    print(u.profile(need_json=True))
    u.insert(
        ChatBlob(
            messages=[
                {
                    "role": "user",
                    "content": "Hello, I'm Gus",
                },
                {
                    "role": "assistant",
                    "content": "Hi, nice to meet you, Gus!",
                },
            ]
        )
    )
    u.flush()
    ps = u.profile()
    print(u.profile(need_json=True))
    print([p.describe for p in ps])
    print(u.event())
    mb.delete_user(uid)
    print("Deleted user")
