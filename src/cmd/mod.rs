mod commit;
mod complete;

use anyhow::Result;
use clap::builder::styling::AnsiColor;
use clap::builder::Styles;
use clap::{Parser, Subcommand};
use clap_verbosity_flag::{InfoLevel, Verbosity};

#[async_trait::async_trait]
pub trait Run {
    async fn run(&self) -> Result<()>;
}

#[derive(Debug, Parser)]
#[command(version, author, styles = STYLES)]
pub struct Cmd {
    #[command(subcommand)]
    sub_cmd: SubCmd,

    #[command(flatten)]
    verbosity: Verbosity<InfoLevel>,
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
        let level = self.verbosity.log_level().map(|level| match level {
            clap_verbosity_flag::Level::Error => tracing::Level::ERROR,
            clap_verbosity_flag::Level::Warn => tracing::Level::WARN,
            clap_verbosity_flag::Level::Info => tracing::Level::INFO,
            clap_verbosity_flag::Level::Debug => tracing::Level::DEBUG,
            clap_verbosity_flag::Level::Trace => tracing::Level::TRACE,
        });
        if let Some(level) = level {
            if level < tracing::Level::DEBUG {
                tracing_subscriber::fmt()
                    .pretty()
                    .with_file(false)
                    .with_line_number(false)
                    .with_max_level(level)
                    .with_target(false)
                    .without_time()
                    .init();
            } else {
                tracing_subscriber::fmt()
                    .pretty()
                    .with_max_level(level)
                    .init();
            }
        }
        match &self.sub_cmd {
            SubCmd::Commit(cmd) => cmd.run().await,
            SubCmd::Complete(cmd) => cmd.run().await,
        }
    }
}
