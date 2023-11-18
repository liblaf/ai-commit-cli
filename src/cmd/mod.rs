use anyhow::Result;
use clap::builder::styling::AnsiColor;
use clap::builder::Styles;
use clap::{Parser, Subcommand};
use tracing::Level;

mod commit;
mod complete;

#[derive(Debug, Parser)]
#[command(version, author, styles = STYLES)]
pub struct Cmd {
    #[command(subcommand)]
    sub_cmd: SubCmd,

    #[arg(short, long, default_value_t = Level::INFO)]
    log_level: Level,
}

#[async_trait::async_trait]
pub trait Run {
    async fn run(&self) -> Result<()>;
}

const STYLES: Styles = Styles::styled()
    .header(AnsiColor::Blue.on_default().bold())
    .usage(AnsiColor::Cyan.on_default().bold())
    .literal(AnsiColor::Green.on_default().bold())
    .placeholder(AnsiColor::Magenta.on_default().bold());

#[derive(Debug, Subcommand)]
enum SubCmd {
    Commit(commit::Cmd),
    Complete(complete::Cmd),
}

#[async_trait::async_trait]
impl Run for Cmd {
    async fn run(&self) -> Result<()> {
        tracing_subscriber::fmt()
            .pretty()
            .with_max_level(self.log_level)
            .init();
        match &self.sub_cmd {
            SubCmd::Commit(cmd) => cmd.run().await,
            SubCmd::Complete(cmd) => cmd.run().await,
        }
    }
}
