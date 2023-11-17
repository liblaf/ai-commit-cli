use std::panic::Location;

pub trait LogResult<T> {
    #[track_caller]
    fn log(self) -> anyhow::Result<T>;
}

pub trait LogError {
    #[track_caller]
    fn log(self) -> anyhow::Error;
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

impl<E> LogError for E
where
    E: Into<anyhow::Error>,
{
    #[track_caller]
    fn log(self) -> anyhow::Error {
        let e = self.into();
        let mut message = e.to_string() + "\n";
        let sources = e
            .chain()
            .skip(1)
            .enumerate()
            .map(|(i, e)| format!("{:>5}: {}\n", i, e))
            .collect::<Vec<String>>()
            .join("");
        if !sources.is_empty() {
            message += "Caused by:\n";
            message += &sources;
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
