# Introduction #

There are a few "magic" values in the isolate and swarming server. Also some dimensions and state values have special meaning.


# client tools environment variables #

  * `ISOLATE_SERVER` sets the default value of --isolate-server.
  * `ISOLATE_DEBUG` sets --verbose verbosity.
  * `SWARMING_SERVER` sets the default value for --swarming.


# run\_isolated #

`run_isolated.py/.zip` understands the following. This value should be set in the `command` section of the .isolate file.

  * `${ISOLATED_OUTDIR}`: If found on command line argument, replaced by the temporary directory that is uploaded back to the server after the task execution. This causes `run_isolated` to print a `[run_isolated_out_hack]` statement after the task.


# Swarming #


## Task execution environment ##

When a Swarming bot is running a task, the following environment variables are always set:

  * `SWARMING_HEADLESS=1` is always set.
  * `SWARMING_BOT_ID` is set to the bot id.


## dimensions ##

  * `id`: must be a single value in the list, which also must be unique. It's what uniquely identify the bot.
  * `quarantined`: if present, it specifies the bot self-quarantined, as it found out it needs manual sysadmin assistance before being able to accept any task. An example is that it doesn't enough free disk space.


## state ##

  * `cost_usd_hour`: reports the base cost of this bot in $USD/hour.
  * `periodic_reboot_secs`: when set to a integer, instructs the server to send a reboot command after this period. The actual period is fuzzed with a 10% delta.
  * `quarantined`: has the same meaning than in `dimensions`. It's also supported as a state.