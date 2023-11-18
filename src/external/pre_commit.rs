use std::io::IsTerminal;
use std::process::Command;

use crate::common::log::LogResult;
use anyhow::Result;

pub fn run() -> Result<()> {
    let mut cmd = Command::new("pre-commit");
    cmd.arg("run");
    if std::io::stdout().is_terminal() {
        cmd.arg("--color=always");
    }
    let status = cmd.status()?;
    crate::ensure!(status.success());
    Ok(())
}
