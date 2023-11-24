use std::io::IsTerminal;
use std::process::{Command, Stdio};

use anyhow::Result;

use crate::common::log::LogResult;

pub fn run() -> Result<()> {
    let mut cmd = Command::new("pre-commit");
    cmd.arg("run");
    if std::io::stdout().is_terminal() {
        cmd.arg("--color=always");
    }
    cmd.stdin(Stdio::null())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    let status = cmd.status().log()?;
    crate::ensure!(status.success());
    Ok(())
}
