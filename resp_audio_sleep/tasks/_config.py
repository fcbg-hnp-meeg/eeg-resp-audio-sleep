# triggers are defined in the format 'target|deviant/frequency' with frequency as float
TRIGGERS: dict[str, int] = {
    "target/1000.0": 1,
    "target/2000.0": 2,
    "deviant/1000.0": 11,
    "deviant/2000.0": 12,
}
TRIGGER_TYPE: str = "arduino"
TRIGGER_ARGS: str | None = None
# sound settings
N_TARGET: int = 25
N_DEVIANT: int = 5
SOUND_DURATION: float = 0.2
# sequence and task settings
BASELINE_DURATION: float = 60
EDGE_PERC: float = 10  # percentage between 0 and 100
# detector settings
ECG_HEIGHT: float = 0.99
ECG_DISTANCE: float = 0.3
RESP_PROMINENCE: float = 20
RESP_DISTANCE: float = 0.8
# target timing
TARGET_DELAY: float = 0.2


# TODO: Define a configuration class to handle all configuration elements.
class ConfigRepr:  # noqa: D101
    def __repr__(self) -> str:  # noqa: D401
        """String representation of the configuration."""
        repr_str = "Configuration of the system:\n"
        repr_str += len(repr_str.strip()) * "-" + "\n"
        # triggers
        repr_str += f"Triggers:\n  type: {TRIGGER_TYPE}\n"
        if TRIGGER_ARGS is not None:
            repr_str += f"  args: {TRIGGER_ARGS}\n"
        repr_str += "  codes:\n"
        for key, value in TRIGGERS.items():
            repr_str += f"    {key}: {value}\n"
        # sounds
        repr_str += (
            f"Sounds:\n  number of targets: {N_TARGET}\n  "
            f"number of deviants: {N_DEVIANT}\n"
        )
        repr_str += f"  duration: {SOUND_DURATION} s\n"
        # sequence settings
        repr_str += f"Sequence/Task settings:\n  edge percentage: {EDGE_PERC}%\n"
        repr_str += f"  baseline duration: {BASELINE_DURATION} s\n"
        # detector settings
        repr_str += f"Detector settings:\n  ECG height: {ECG_HEIGHT}\n"
        repr_str += f"  ECG distance: {ECG_DISTANCE}\n"
        repr_str += f"  respiration prominence: {RESP_PROMINENCE}\n"
        repr_str += f"  respiration distance: {RESP_DISTANCE}\n"
        return repr_str
