#[macro_export]
macro_rules! anyhow {
    ($msg:literal $(,)?) => {
        $crate::common::log::LogError::log(anyhow::anyhow!($msg))
    };

    ($err:expr $(,)?) => {
        $crate::common::log::LogError::log(anyhow::anyhow!($err))
    };

    ($fmt:expr, $($arg:tt)*) => {
        $crate::common::log::LogError::log(anyhow::anyhow!($fmt, $($arg)*))
    };
}

#[macro_export]
macro_rules! bail {
    ($msg:literal $(,)?) => {
        return Err($crate::anyhow!($msg))
    };

    ($err:expr $(,)?) => {
        return Err($crate::anyhow!($err))
    };

    ($fmt:expr, $($arg:tt)*) => {
        return Err($crate::anyhow!($fmt, $($arg)*))
    };
}

#[macro_export]
macro_rules! ensure {
    ($cond:expr $(,)?) => {
        if !$cond {
            return Err($crate::anyhow!(concat!(
                "Condition failed: `",
                stringify!($cond),
                "`"
            )));
        }
    };
}
