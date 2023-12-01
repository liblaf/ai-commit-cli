#[macro_export]
macro_rules! anyhow {
    ($err:expr $(,)?) => {
        $crate::common::log::LogError::log(anyhow::anyhow!($err))
    };
}

#[macro_export]
macro_rules! bail {
    ($err:expr $(,)?) => {
        return Err($crate::anyhow!($err))
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
