#[macro_export]
macro_rules! bail {
    ($msg:literal $(,)?) => {
        return Err(anyhow::anyhow!($msg)).log()
    };

    ($err:expr $(,)?) => {
        return Err(anyhow::anyhow!($err)).log()
    };

    ($fmt:expr, $($arg:tt)*) => {
        return Err(anyhow::anyhow!($fmt, $($arg)*)).log()
    };
}

#[macro_export]
macro_rules! ensure {
    ($cond:expr $(,)?) => {
        if !$cond {
            return Err(anyhow::anyhow!(concat!(
                "Condition failed: `",
                stringify!($cond),
                "`"
            )))
            .log();
        }
    };
}
