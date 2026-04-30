from db import (
    init_schema,
    save_player,
    get_cached_player,
    save_uid_mapping,
    get_cached_uid,
    is_fresh,
)

def check(condition, message):
    """Raise AssertionError if condition is False, print message if it is."""
    if not condition:
        raise AssertionError(f"FAIL: {message}")
    print(f"  ✓ {message}")


def test_save_and_load_player():
    print("test_save_and_load_player:")
    fake_player = {
        "uid": "test-99999",
        "name": "SanityCheckPlayer",
        "level": 42,
        "rank": "Bronze",
    }
    uid = save_player(fake_player)
    check(uid == "test-99999", "save_player returns the UID")

    cached = get_cached_player("test-99999")
    check(cached is not None, "get_cached_player finds the saved player")
    check(cached["username"] == "SanityCheckPlayer", "username matches")
    check(cached["is_fresh"] is True, "freshly-saved data is marked fresh")


def test_save_and_load_uid_mapping():
    print("test_save_and_load_uid_mapping:")
    save_uid_mapping("SanityCheckPlayer", "test-99999")
    cached_uid = get_cached_uid("SanityCheckPlayer")
    check(cached_uid == "test-99999", "saved UID mapping can be retrieved")

    missing = get_cached_uid("NobodyEverLookedUpThisName")
    check(missing is None, "missing username returns None")


def test_freshness_check():
    print("test_freshness_check:")
    check(is_fresh(None) is False, "None timestamp is not fresh")
    # is_fresh format: '2026-04-29 23:51:50'
    check(is_fresh("2020-01-01 00:00:00") is False, "very old timestamp is stale")


if __name__ == "__main__":
    print("Initializing schema...")
    init_schema()
    print()
    test_save_and_load_player()
    test_save_and_load_uid_mapping()
    test_freshness_check()
    print()
    print("All sanity checks passed.")