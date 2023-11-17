use std::path::PathBuf;

use anyhow::Result;
use async_openai::config::OpenAIConfig;
use async_openai::types::{
    ChatCompletionRequestSystemMessageArgs, ChatCompletionRequestUserMessageArgs,
    CreateChatCompletionRequestArgs,
};
use async_openai::Client;
use clap::Args;
use colored::Colorize;
use inquire::Select;

use crate::cmd::Run;
use crate::common::log::LogResult;

#[derive(Debug, Args)]
pub struct Cmd {
    #[arg(short, long, env = "OPENAI_API_KEY")]
    api_key: Option<String>,

    #[arg(short, long)]
    exclude: Vec<PathBuf>,

    #[arg(long, default_value = "gpt-3.5-turbo-16k")]
    model: String,

    #[arg(long, default_value_t = 500)]
    max_tokens: u16,

    #[arg(short, default_value_t = 1)]
    n: u8,

    #[arg(long, default_value_t = 0.0)]
    temperature: f32,

    #[arg(long, default_value_t = 0.1)]
    top_p: f32,
}

const EXCLUDE: &[&str] = &["*-lock.*", "*.lock"];

impl Cmd {
    fn api_key(&self) -> Result<String> {
        if let Some(api_key) = self.api_key.as_ref() {
            return Ok(api_key.to_string());
        }
        if let Ok(api_key) = crate::external::bitwarden::get_notes("OPENAI_KEY") {
            return Ok(api_key);
        }
        crate::bail!("OPENAI_API_KEY is not provided");
    }
}

#[async_trait::async_trait]
impl Run for Cmd {
    async fn run(&self) -> anyhow::Result<()> {
        let mut exclude: Vec<_> = EXCLUDE.iter().map(PathBuf::from).collect();
        self.exclude
            .iter()
            .for_each(|f| exclude.push(f.to_path_buf()));
        crate::external::git::status(&exclude)?;
        let diff = crate::external::git::diff(exclude)?;
        crate::ensure!(!diff.trim().is_empty());
        let client = Client::with_config(OpenAIConfig::new().with_api_key(self.api_key()?));
        let request = CreateChatCompletionRequestArgs::default()
            .messages([
                ChatCompletionRequestSystemMessageArgs::default()
                    .content(include_str!(concat!(
                        env!("CARGO_MANIFEST_DIR"),
                        "/res/prompt.md"
                    )))
                    .build()
                    .log()?
                    .into(),
                ChatCompletionRequestUserMessageArgs::default()
                    .content(diff)
                    .build()
                    .log()?
                    .into(),
            ])
            .model(&self.model)
            .max_tokens(self.max_tokens)
            .n(self.n)
            .temperature(self.temperature)
            .top_p(self.top_p)
            .build()
            .log()?;
        let response = client.chat().create(request).await.log()?;
        let select = Select::new(
            &format!(
                "Pick a commit message to use: {}",
                "(Ctrl+C to exit)".dimmed()
            ),
            response
                .choices
                .iter()
                .filter_map(|c| c.message.content.as_deref())
                .collect(),
        )
        .prompt()
        .log()?;
        crate::external::git::commit(select)
    }
}
