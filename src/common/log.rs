use std::fmt::Display;
use std::panic::Location;

use clap::ValueEnum;
use tracing::level_filters::LevelFilter;

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

impl From<Level> for LevelFilter {
    fn from(value: Level) -> LevelFilter {
        match value {
            Level::Trace => tracing::Level::TRACE.into(),
            Level::Debug => tracing::Level::DEBUG.into(),
            Level::Info => tracing::Level::INFO.into(),
            Level::Warn => tracing::Level::WARN.into(),
            Level::Error => tracing::Level::ERROR.into(),
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
