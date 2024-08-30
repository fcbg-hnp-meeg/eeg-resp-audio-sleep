from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import psychtoolbox as ptb

from ..utils._checks import check_type
from ..utils._docs import fill_doc
from ..utils.logs import logger
from ..utils.time import high_precision_sleep
from ._config import OUTLIER_PERC, SOUND_DURATION, TARGET_DELAY, TRIGGER_TASKS, TRIGGERS
from ._utils import create_sounds, create_trigger, generate_sequence

if TYPE_CHECKING:
    from numpy.typing import NDArray


@fill_doc
def asynchronous(
    peaks: NDArray[np.float64],
    *,
    target: float,
    deviant: float,
) -> None:
    """Asynchronous blocks where a synchronous sequence is repeated.

    Parameters
    ----------
    %(peaks)s
    %(fq_target)s
    %(fq_deviant)s
    """  # noqa: D401
    check_type(peaks, (np.ndarray,), "peaks")
    if peaks.ndim != 1:
        raise ValueError("The peaks array must be one-dimensional.")
    logger.info("Starting asynchronous block.")
    # create sound stimuli, trigger and sequence
    sounds = create_sounds()
    trigger = create_trigger()
    sequence = generate_sequence(target, deviant)
    # the sequence, sound and trigger generation validates the trigger dictionary, thus
    # we can safely map the target and deviant frequencies to their corresponding
    # trigger values and sounds.
    stimulus = {
        TRIGGERS[f"target/{target}"]: sounds[str(target)],
        TRIGGERS[f"deviant/{deviant}"]: sounds[str(deviant)],
    }
    # generate delays between peaks
    rng = np.random.default_rng()
    delays = np.diff(peaks)
    edges = np.percentile(delays, [OUTLIER_PERC, 100 - OUTLIER_PERC])
    delays = delays[np.where((edges[0] < delays) & (delays < edges[1]))]
    delays = rng.choice(delays, size=sequence.size, replace=True)
    # main loop
    counter = 0
    trigger.signal(TRIGGER_TASKS["asynchronous"][0])
    while counter <= sequence.size - 1:
        start = ptb.GetSecs()
        stimulus.get(sequence[counter]).play(when=start + TARGET_DELAY)
        logger.debug("Triggering %i in %.2f ms.", sequence[counter], TARGET_DELAY)
        high_precision_sleep(TARGET_DELAY)
        trigger.signal(sequence[counter])
        logger.info("Stimulus %i / %i complete.", counter + 1, sequence.size)
        # note that if the delays are too short, the value 'wait' could end up negative
        # which (1) makes no sense and (2) would raise in the sleep function.
        wait = start + delays[counter] - ptb.GetSecs()
        high_precision_sleep(wait)
        counter += 1
    # wait for the last sound to finish
    if wait < 1.1 * SOUND_DURATION:
        high_precision_sleep(1.1 * SOUND_DURATION - wait)
    trigger.signal(TRIGGER_TASKS["asynchronous"][1])
    logger.info("Asynchronous block complete.")
