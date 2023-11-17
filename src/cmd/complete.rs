use clap::{Args, CommandFactory};
use clap_complete::Shell;

use crate::cmd::Run;

#[derive(Debug, Args)]
pub struct Cmd {
    shell: Shell,
}

#[async_trait::async_trait]
impl Run for Cmd {
    async fn run(&self) -> anyhow::Result<()> {
        let cmd = &mut crate::cmd::Cmd::command();
        clap_complete::generate(
            self.shell,
            cmd,
            cmd.get_name().to_string(),
            &mut std::io::stdout(),
        );
        Ok(())
    }
}
