use std::io::{IsTerminal, Write};
use std::path::Path;
use std::process::{Command, Stdio};

use anyhow::Result;

use crate::common::log::LogResult;

pub fn commit<S>(message: S) -> Result<()>
where
    S: AsRef<str>,
{
    let mut cmd = Command::new("git");
    cmd.args(["commit", "--file=-"])
        .stdin(Stdio::piped())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    let mut child = cmd.spawn()?;
    child
        .stdin
        .as_ref()
        .unwrap()
        .write_all(message.as_ref().as_bytes())
        .log()?;
    let status = child.wait().log()?;
    crate::ensure!(status.success());
    Ok(())
}

pub fn diff<I, S>(exclude: I) -> Result<String>
where
    I: IntoIterator<Item = S>,
    S: AsRef<Path>,
{
    let mut cmd = Command::new("git");
    cmd.args(["diff", "--cached"]);
    exclude.into_iter().for_each(|p| {
        cmd.arg(format!(":(exclude){}", p.as_ref().to_str().unwrap()));
    });
    cmd.stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit());
    let output = cmd.output().log()?;
    crate::ensure!(output.status.success());
    String::from_utf8(output.stdout).log()
}

pub fn status<I, S>(exclude: I) -> Result<()>
where
    I: IntoIterator<Item = S>,
    S: AsRef<Path>,
{
    let mut cmd = Command::new("git");
    if std::io::stdout().is_terminal() {
        cmd.args(["-c", "color.status=always"]);
    }
    cmd.args(["status"]);
    exclude.into_iter().for_each(|p| {
        cmd.arg(format!(":(exclude){}", p.as_ref().to_str().unwrap()));
    });
    cmd.stdin(Stdio::null())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit());
    let status = cmd.status().log()?;
    crate::ensure!(status.success());
    Ok(())
}
