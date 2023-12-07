from ai_commit_cli import commit


def test_matches_is_none() -> None:
    message: str = "This is a test message"
    assert commit.sanitize_line(message) == message


def test_scope_is_none() -> None:
    message: str = "fix: This is a test message"
    expected: str = "fix: this is a test message"
    assert commit.sanitize_line(message) == expected


def test_breaking_is_none() -> None:
    message: str = "feat(TEST): This is a test message"
    expected: str = "feat(test): this is a test message"
    assert commit.sanitize_line(message) == expected


def test_all_groups_present() -> None:
    message: str = "feat(TEST)!:  This is a test message"
    expected: str = "feat(test)!: this is a test message"
    assert commit.sanitize_line(message) == expected
