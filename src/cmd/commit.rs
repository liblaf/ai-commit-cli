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
use regex::Regex;

use crate::cmd::Run;
use crate::common::log::LogResult;

#[derive(Debug, Args)]
pub struct Cmd {
    #[arg(short, long, env = "OPENAI_API_KEY")]
    api_key: Option<String>,

    #[arg(short, long)]
    exclude: Vec<PathBuf>,

    #[arg(short, long)]
    include: Vec<PathBuf>,

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
        crate::external::pre_commit::run()?;
        let mut exclude: Vec<_> = EXCLUDE.iter().map(PathBuf::from).collect();
        self.exclude
            .iter()
            .for_each(|f| exclude.push(f.to_path_buf()));
        crate::external::git::status(&exclude, &self.include)?;
        let diff = crate::external::git::diff(exclude, &self.include)?;
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
        if let Some(usage) = response.usage {
            println!(
                "Tokens: {} (prompt) + {} (completion) = {} (total)",
                usage.prompt_tokens.to_string().bold().cyan(),
                usage.completion_tokens.to_string().bold().cyan(),
                usage.total_tokens.to_string().bold().cyan()
            );
        }
        let select = Select::new(
            &format!(
                "Pick a commit message to use: {}",
                "(Ctrl+C to exit)".dimmed()
            ),
            response
                .choices
                .iter()
                .filter_map(|c| c.message.content.as_deref())
                .filter_map(sanitize)
                .collect(),
        )
        .prompt()
        .log()?;
        crate::external::git::commit(select)
    }
}

fn sanitize<S>(message: S) -> Option<String>
where
    S: AsRef<str>,
{
    let message = message.as_ref();
    let mut lines: Vec<_> = message.trim().split('\n').collect();
    let subject = lines[0].trim();
    let pattern: Regex =
        Regex::new(r"(?P<type>\w+)(?:\((?P<scope>\w+)\))?(?P<breaking>!)?: (?P<description>.+)")
            .log()
            .unwrap();
    let matches = pattern.captures(subject)?;
    let type_ = matches.name("type")?.as_str();
    let scope = matches.name("scope").map(|s| s.as_str().to_lowercase());
    let breaking = matches.name("breaking").is_some();
    let description = matches.name("description")?.as_str();
    let description = description.chars().next()?.to_lowercase().to_string() + &description[1..];
    let mut subject = type_.to_string();
    if let Some(scope) = scope {
        subject += &format!("({})", scope);
    }
    if breaking {
        subject += "!";
    }
    subject += ": ";
    subject += &description;
    lines[0] = &subject;
    Some(lines.join("\n"))
}
