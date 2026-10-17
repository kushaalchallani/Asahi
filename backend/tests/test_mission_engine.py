
from types import SimpleNamespace

from mission.engine import choose_mission


def make_mission(
    mission_id,
    *,
    category="reflection",
    difficulty="low",
    social_required=False,
    energy_required="low",
):
    return SimpleNamespace(
        id=mission_id,
        title=f"Mission {mission_id}",
        category=category,
        difficulty=difficulty,
        social_required=social_required,
        energy_required=energy_required,
    )


def make_check_in(feeling, note=None):
    return SimpleNamespace(feeling=feeling, note=note)


def test_returns_none_when_no_missions_exist():
    check_in = make_check_in("I'm doing okay")

    assert choose_mission(check_in, [], []) is None


def test_low_energy_check_in_prefers_low_energy_non_social_mission():
    check_in = make_check_in("A little low")

    social_mission = make_mission(
        1,
        social_required=True,
        energy_required="high",
    )
    suitable_mission = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [social_mission, suitable_mission],
    )

    assert result.id == 2


def test_avoids_recent_missions_when_alternatives_exist():
    check_in = make_check_in("I'm doing okay")
    recent_mission = make_mission(1)
    alternative_mission = make_mission(2)

    result = choose_mission(
        check_in,
        [recent_mission],
        [recent_mission, alternative_mission],
    )

    assert result.id == 2


def test_loneliness_does_not_force_social_mission():
    check_in = make_check_in("Lonely")

    social_mission = make_mission(
        1,
        category="connection",
        social_required=True,
        energy_required="high",
    )
    quiet_mission = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [social_mission, quiet_mission],
    )

    assert result.id == 2

def test_avoids_mission_marked_not_for_me_when_alternative_exists():
    check_in = make_check_in("I'm doing okay")

    disliked_mission = make_mission(1)
    alternative_mission = make_mission(2)

    result = choose_mission(
        check_in,
        [disliked_mission],
        [disliked_mission, alternative_mission],
    )

    assert result.id == 2

def test_not_for_me_feedback_penalizes_mission():
    check_in = make_check_in("I'm doing okay")

    mission_1 = make_mission(1)
    mission_2 = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [mission_1, mission_2],
        recent_feedback={1: "not_for_me"},
    )

    assert result.id == 2

def test_repeated_low_mood_prefers_low_energy_mission():
    from types import SimpleNamespace

    current_check_in = SimpleNamespace(
        feeling="I'm doing okay",
        note="",
    )

    recent_check_ins = [
        SimpleNamespace(feeling="A little low"),
        SimpleNamespace(feeling="Tired"),
        SimpleNamespace(feeling="Sad"),
    ]

    low_energy_mission = SimpleNamespace(
        id=1,
        energy_required="low",
        social_required=False,
        category="regulation",
    )

    high_energy_mission = SimpleNamespace(
        id=2,
        energy_required="high",
        social_required=True,
        category="connection",
    )

    result = choose_mission(
        current_check_in=current_check_in,
        recent_missions=[],
        missions=[high_energy_mission, low_energy_mission],
        recent_check_ins=recent_check_ins,
    )

    assert result.id == 1

def test_repeated_low_mood_in_notes_prefers_low_energy_mission():
    from types import SimpleNamespace

    current_check_in = SimpleNamespace(
        feeling="I'm doing okay",
        note="",
    )

    recent_check_ins = [
        SimpleNamespace(
            feeling="I'm doing okay",
            note="I've been feeling sad lately",
        ),
        SimpleNamespace(
            feeling="I'm doing okay",
            note="I'm tired of everything",
        ),
    ]

    low_energy_mission = SimpleNamespace(
        id=1,
        energy_required="low",
        social_required=False,
        category="regulation",
    )

    high_energy_mission = SimpleNamespace(
        id=2,
        energy_required="high",
        social_required=True,
        category="connection",
    )

    result = choose_mission(
        current_check_in=current_check_in,
        recent_missions=[],
        missions=[
            high_energy_mission,
            low_energy_mission,
        ],
        recent_check_ins=recent_check_ins,
    )

    assert result.id == 1

def test_feedback_history_keeps_latest_feedback_for_each_mission():
    from types import SimpleNamespace
    from mission.engine import build_feedback_history

    feedback_rows = [
        SimpleNamespace(mission_id=1, feedback="not_for_me"),
        SimpleNamespace(mission_id=2, feedback="helpful"),
        SimpleNamespace(mission_id=1, feedback="helpful"),
    ]

    result = build_feedback_history(feedback_rows)

    assert result == {
        1: "not_for_me",
        2: "helpful",
    }

def test_helpful_feedback_favours_mission():
    check_in = make_check_in("I'm doing okay")

    mission_1 = make_mission(1)
    mission_2 = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [mission_1, mission_2],
        recent_feedback={1: "helpful"},
    )

    assert result.id == 1


def test_not_for_me_feedback_loses_to_helpful_feedback():
    check_in = make_check_in("I'm doing okay")

    disliked_mission = make_mission(1)
    helpful_mission = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [disliked_mission, helpful_mission],
        recent_feedback={
            1: "not_for_me",
            2: "helpful",
        },
    )

    assert result.id == 2

def test_falls_back_when_low_mood_filter_has_no_matches():
    check_in = make_check_in("A little low")

    only_available_mission = make_mission(
        1,
        category="reflection",
        energy_required="medium",
        social_required=False
    )

    result = choose_mission(
        check_in,
        [],
        [only_available_mission]
    )

    assert result.id == 1

def test_low_mood_and_feedback_choose_suitable_alternative():
    check_in = make_check_in("A little low")

    recently_assigned = make_mission(
        1,
        energy_required="low",
        social_required=False,
    )
    disliked_mission = make_mission(
        2,
        energy_required="low",
        social_required=False,
    )
    suitable_alternative = make_mission(
        3,
        category="regulation",
        energy_required="low",
        social_required=False,
    )

    result = choose_mission(
        check_in,
        [recently_assigned],
        [
            recently_assigned,
            disliked_mission,
            suitable_alternative,
        ],
        recent_feedback={2: "not_for_me"},
    )

    assert result.id == 3

def test_returns_a_mission_when_all_candidates_were_recently_assigned():
    check_in = make_check_in("I'm doing okay")

    mission_1 = make_mission(1)
    mission_2 = make_mission(2)

    result = choose_mission(
        check_in,
        [mission_1, mission_2],
        [mission_1, mission_2],
    )

    assert result is not None
    assert result.id in {1, 2}

def test_empty_missions_returns_none_with_other_context():
    check_in = make_check_in("A little low")

    result = choose_mission(
        check_in,
        [],
        [],
        recent_feedback={1: "not_for_me"},
        recent_check_ins=[
            make_check_in("Tired"),
            make_check_in("Sad"),
        ],
    )

    assert result is None