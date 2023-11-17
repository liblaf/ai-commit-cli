use anyhow::Result;
use clap::Parser;
use cmd::Run;

mod cmd;
mod common;
mod external;

#[tokio::main]
async fn main() -> Result<()> {
    let cmd = cmd::Cmd::parse();
    cmd.run().await
}
