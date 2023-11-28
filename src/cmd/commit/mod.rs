#[cfg(test)]
mod tests;

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
    /// If not provided, will use `bw get notes OPENAI_API_KEY`
    #[arg(short, long, env = "OPENAI_API_KEY")]
    api_key: Option<String>,

    #[arg(short, long, default_values = EXCLUDE)]
    exclude: Vec<PathBuf>,

    #[arg(short, long)]
    include: Vec<PathBuf>,

    #[arg(long, default_value_t = false)]
    no_pre_commit: bool,

    #[arg(short, long)]
    prompt: Option<String>,

    #[arg(long)]
    prompt_file: Option<PathBuf>,

    /// ID of the model to use
    #[arg(long, default_value = "gpt-3.5-turbo-16k")]
    model: String,

    /// The maximum number of tokens to generate in the chat completion
    #[arg(long, default_value_t = 500)]
    max_tokens: u16,

    /// How many chat completion choices to generate for each input message
    #[arg(short, default_value_t = 1)]
    n: u8,

    /// What sampling temperature to use, between 0 and 2
    #[arg(long, default_value_t = 0.0)]
    temperature: f32,

    /// An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass
    #[arg(long, default_value_t = 0.1)]
    top_p: f32,
}

const EXCLUDE: &[&str] = &["*-lock.*", "*.lock"];

impl Cmd {
    fn api_key(&self) -> Result<String> {
        if let Some(api_key) = self.api_key.as_deref() {
            return Ok(api_key.to_string());
        }
        if let Ok(api_key) = crate::external::bitwarden::get_notes("OPENAI_API_KEY") {
            return Ok(api_key);
        }
        crate::bail!("OPENAI_API_KEY is not provided");
    }

    fn prompt(&self) -> Result<String> {
        if let Some(prompt) = self.prompt.as_deref() {
            return Ok(prompt.to_string());
        }
        if let Some(prompt_file) = self.prompt_file.as_deref() {
            return std::fs::read_to_string(prompt_file).log();
        }
        Ok(include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/res/prompt.md")).to_string())
    }
}

#[async_trait::async_trait]
impl Run for Cmd {
    async fn run(&self) -> anyhow::Result<()> {
        if !self.no_pre_commit {
            crate::external::pre_commit::run()?;
        }
        crate::external::git::status(&self.exclude, &self.include)?;
        let diff = crate::external::git::diff(&self.exclude, &self.include)?;
        if diff.trim().is_empty() {
            crate::bail!("no changes added to commit (use \"git add\" and/or \"git commit -a\")");
        }
        let client = Client::with_config(OpenAIConfig::new().with_api_key(self.api_key()?));
        let request = CreateChatCompletionRequestArgs::default()
            .messages([
                ChatCompletionRequestSystemMessageArgs::default()
                    .content(self.prompt()?)
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
        tracing::debug!("{:#?}", request);
        let response = client.chat().create(request).await.log()?;
        tracing::debug!("{:#?}", response);
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
    let lines: Vec<_> = message.trim().split('\n').map(sanitize_line).collect();
    if validate(lines.first()?) {
        Some(lines.join("\n"))
    } else {
        None
    }
}

fn sanitize_line<S>(message: S) -> String
where
    S: AsRef<str>,
{
    let message = message.as_ref();
    let pattern: Regex =
        Regex::new(r"(?P<type>\w+)(?:\((?P<scope>[^\)]+)\))?(?P<breaking>!)?: (?P<description>.+)")
            .log()
            .unwrap();
    let matches = match pattern.captures(message) {
        Some(matches) => matches,
        None => return message.to_string(),
    };
    let type_ = matches.name("type").unwrap().as_str();
    let scope = matches.name("scope").map(|s| s.as_str().to_lowercase());
    let breaking = matches.name("breaking").is_some();
    let description = matches.name("description").unwrap().as_str();
    let description = description
        .chars()
        .next()
        .unwrap()
        .to_lowercase()
        .to_string()
        + &description[1..];
    let mut subject = type_.to_string();
    if let Some(scope) = scope {
        subject += &format!("({})", scope);
    }
    if breaking {
        subject += "!";
    }
    subject += ": ";
    subject += &description;
    subject
}

fn validate<S>(message: S) -> bool
where
    S: AsRef<str>,
{
    let message = message.as_ref();
    let pattern: Regex =
        Regex::new(r"(?P<type>\w+)(?:\((?P<scope>[^\)]+)\))?(?P<breaking>!)?: (?P<description>.+)")
            .log()
            .unwrap();
    pattern.is_match(message)
}
