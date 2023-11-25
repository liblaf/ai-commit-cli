use clap::{builder::PossibleValue, Args, CommandFactory, ValueEnum};
use clap_complete::Shell;

use crate::cmd::Run;

/// Generate tab-completion scripts for your shell
///
/// $ ai-commit-cli complete fish >$HOME/.local/share/fish/vendor_completions.d
/// $ ai-commit-cli complete fish >/usr/local/share/fish/vendor_completions.d
#[derive(Debug, Args)]
pub struct Cmd {
    shell: Generator,
}

#[derive(Clone, Debug)]
enum Generator {
    Markdown,
    Shell(Shell),
}

impl ValueEnum for Generator {
    fn value_variants<'a>() -> &'a [Self] {
        &[
            Self::Markdown,
            Self::Shell(Shell::Bash),
            Self::Shell(Shell::Elvish),
            Self::Shell(Shell::Fish),
            Self::Shell(Shell::PowerShell),
            Self::Shell(Shell::Zsh),
        ]
    }

    fn to_possible_value(&self) -> Option<clap::builder::PossibleValue> {
        match self {
            Self::Markdown => Some(PossibleValue::new("markdown")),
            Self::Shell(shell) => shell.to_possible_value(),
        }
    }
}

#[async_trait::async_trait]
impl Run for Cmd {
    async fn run(&self) -> anyhow::Result<()> {
        let cmd = &mut crate::cmd::Cmd::command();
        match self.shell {
            Generator::Markdown => clap_markdown::print_help_markdown::<crate::cmd::Cmd>(),
            Generator::Shell(shell) => clap_complete::generate(
                shell,
                cmd,
                cmd.get_name().to_string(),
                &mut std::io::stdout(),
            ),
        }
        Ok(())
    }
}
