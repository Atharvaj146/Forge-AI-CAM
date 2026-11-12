
import pytest

from exercises.pushup.rep_counter import PushUpRepCounter


def test_initial_state():
    counter = PushUpRepCounter()

    assert counter.rep_count == 0
    assert counter.state == "WAITING_FOR_TOP"


def test_one_complete_pushup():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP"
    ]

    result = None

    for phase in phases:
        result = counter.update(phase)

    assert result["rep_count"] == 1
    assert result["rep_completed"] is True
    assert result["state"] == "READY"


def test_incomplete_pushup_not_counted():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM"
    ]

    for phase in phases:
        counter.update(phase)

    assert counter.rep_count == 0


def test_aborted_pushup_not_counted():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "TOP"
    ]

    for phase in phases:
        counter.update(phase)

    assert counter.rep_count == 0
    assert counter.state == "READY"


def test_multiple_pushups():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP",

        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP",

        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP"
    ]

    for phase in phases:
        counter.update(phase)

    assert counter.rep_count == 3


def test_tracking_loss_resets_incomplete_rep():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "TRACKING_LOST"
    ]

    for phase in phases:
        counter.update(phase)

    assert counter.rep_count == 0
    assert counter.state == "WAITING_FOR_TOP"


def test_tracking_recovery_requires_top():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "TRACKING_LOST",
        "ASCENDING"
    ]

    for phase in phases:
        counter.update(phase)

    # ASCENDING cannot start a new repetition.
    assert counter.rep_count == 0
    assert counter.state == "WAITING_FOR_TOP"


def test_unknown_phase_is_ignored():
    counter = PushUpRepCounter()

    counter.update("TOP")
    counter.update("UNKNOWN")

    assert counter.rep_count == 0
    assert counter.state == "READY"


def test_rep_completed_only_once():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP",
        "TOP",
        "TOP"
    ]

    completed_events = []

    for phase in phases:
        result = counter.update(phase)
        completed_events.append(result["rep_completed"])

    assert counter.rep_count == 1
    assert completed_events.count(True) == 1


def test_reset():
    counter = PushUpRepCounter()

    phases = [
        "TOP",
        "DESCENDING",
        "BOTTOM",
        "ASCENDING",
        "TOP"
    ]

    for phase in phases:
        counter.update(phase)

    counter.reset()

    assert counter.rep_count == 0
    assert counter.state == "WAITING_FOR_TOP"


def test_bottom_without_descent_is_not_counted():
    counter = PushUpRepCounter()

    counter.update("TOP")
    counter.update("BOTTOM")
    counter.update("ASCENDING")
    counter.update("TOP")

    assert counter.rep_count == 0
