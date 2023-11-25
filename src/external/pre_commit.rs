use std::io::IsTerminal;
use std::process::{Command, Stdio};

use anyhow::Result;

use crate::common::log::LogError;

pub fn run() -> Result<()> {
    let mut cmd = Command::new("pre-commit");
    cmd.arg("run");
    if std::io::stdout().is_terminal() {
        cmd.arg("--color=always");
    }
    cmd.stdin(Stdio::null())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    tracing::debug!("{:?}", cmd);
    let status = match cmd.status() {
        Ok(status) => status,
        Err(e) => {
            if e.kind() == std::io::ErrorKind::NotFound {
                return Ok(());
            } else {
                return Err(e.log());
            }
        }
    };
    crate::ensure!(status.success());
    Ok(())
}
