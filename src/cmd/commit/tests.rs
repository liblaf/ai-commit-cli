#[test]
fn test_sanitize_no_scope_no_breaking() {
    let message = "feat: Add new feature";
    let expected = Some("feat: add new feature".to_string());
    assert_eq!(super::sanitize(message), expected);
}

#[test]
fn test_sanitize_with_scope_no_breaking() {
    let message = "feat(UI): improve user interface";
    let expected = Some("feat(ui): improve user interface".to_string());
    assert_eq!(super::sanitize(message), expected);
}

#[test]
fn test_sanitize_no_scope_with_breaking() {
    let message = "feat!: add breaking change";
    let expected = Some("feat!: add breaking change".to_string());
    assert_eq!(super::sanitize(message), expected);
}

#[test]
fn test_sanitize_with_scope_with_breaking() {
    let message = "feat(ui)!: introduce breaking change in UI";
    let expected = Some("feat(ui)!: introduce breaking change in UI".to_string());
    assert_eq!(super::sanitize(message), expected);
}

#[test]
fn test_sanitize_invalid_message() {
    let message = "invalid commit message";
    let expected = None;
    assert_eq!(super::sanitize(message), expected);
}

#[test]
fn test_sanitize_multiline_message() {
    let message = "feat: add new feature\n\nfeat: This is a multiline commit message";
    let expected =
        Some("feat: add new feature\n\nfeat: this is a multiline commit message".to_string());
    assert_eq!(super::sanitize(message), expected);
}
