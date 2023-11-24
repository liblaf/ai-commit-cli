use std::process::{Command, Stdio};

use anyhow::Result;

use crate::common::log::LogResult;

pub fn get_notes<S>(id: S) -> Result<String>
where
    S: AsRef<str>,
{
    let mut cmd = Command::new("bw");
    cmd.args(["--nointeraction", "get", "notes", id.as_ref()]);
    cmd.stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit());
    let output = cmd.output().log()?;
    crate::ensure!(output.status.success());
    String::from_utf8(output.stdout).log()
}
