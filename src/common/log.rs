use std::{fmt::Display, panic::Location};

use clap::ValueEnum;

#[derive(Clone, Debug, ValueEnum, PartialEq, PartialOrd)]
pub enum Level {
    Trace,
    Debug,
    Info,
    Warn,
    Error,
}

pub trait LogError {
    #[track_caller]
    fn log(self) -> anyhow::Error;
}

pub trait LogResult<T> {
    #[track_caller]
    fn log(self) -> anyhow::Result<T>;
}

impl Display for Level {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Trace => write!(f, "trace"),
            Self::Debug => write!(f, "debug"),
            Self::Info => write!(f, "info"),
            Self::Warn => write!(f, "warn"),
            Self::Error => write!(f, "error"),
        }
    }
}

impl Level {
    pub fn as_level(&self) -> tracing::Level {
        match self {
            Self::Trace => tracing::Level::TRACE,
            Self::Debug => tracing::Level::DEBUG,
            Self::Info => tracing::Level::INFO,
            Self::Warn => tracing::Level::WARN,
            Self::Error => tracing::Level::ERROR,
        }
    }
}

impl<E> LogError for E
where
    E: Into<anyhow::Error>,
{
    #[track_caller]
    fn log(self) -> anyhow::Error {
        let e = self.into();
        let mut message = e.to_string();
        let sources = e
            .chain()
            .skip(1)
            .enumerate()
            .map(|(i, e)| format!("{:>5}: {}", i, e))
            .collect::<Vec<_>>()
            .join("\n");
        if !sources.is_empty() {
            message += "\nCaused by:\n";
            message += &sources;
            message += "\n";
        }
        let location = Location::caller();
        tracing::error!(
            { location = format!("{}:{}", location.file(), location.line()) },
            "{}",
            message
        );
        e
    }
}

impl<T, E> LogResult<T> for Result<T, E>
where
    E: Into<anyhow::Error>,
{
    #[track_caller]
    fn log(self) -> anyhow::Result<T> {
        match self {
            Ok(t) => Ok(t),
            Err(e) => Err(e.log()),
        }
    }
}
