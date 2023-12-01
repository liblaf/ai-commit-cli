use std::panic::Location;

pub trait LogError {
    #[track_caller]
    fn log(self) -> anyhow::Error;
}

pub trait LogResult<T> {
    #[track_caller]
    fn log(self) -> anyhow::Result<T>;
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
