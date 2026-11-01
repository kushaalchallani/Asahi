from types import SimpleNamespace
from mission.engine import choose_mission, explain_mission_score, build_recommendation_result, infer_energy_preference, format_mission_reasons, score_mission, build_feedback_history, score_feedback
import mission.engine as engine


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
        recent_feedback={1: ["not_for_me"]},
    )

    assert result.id == 2

def test_repeated_low_mood_prefers_low_energy_mission():
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
    feedback_rows = [
        SimpleNamespace(mission_id=1, feedback="not_for_me"),
        SimpleNamespace(mission_id=2, feedback="helpful"),
        SimpleNamespace(mission_id=1, feedback="helpful"),
    ]

    result = build_feedback_history(feedback_rows)

    assert result == {
        1: ["not_for_me", "helpful"],
        2: ["helpful"],
    }

def test_helpful_feedback_favours_mission():
    check_in = make_check_in("I'm doing okay")

    mission_1 = make_mission(1)
    mission_2 = make_mission(2)

    result = choose_mission(
        check_in,
        [],
        [mission_1, mission_2],
        recent_feedback={1: ["helpful"]},
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
            1: ["not_for_me"],
            2: ["helpful"],
        },
    )

    assert result.id == 2

def test_falls_back_when_low_mood_filter_has_no_matches():
    check_in = make_check_in("A little low")

    only_available_mission = make_mission(
        1,
        category="reflection",
        energy_required="medium",
        social_required=False,
    )

    result = choose_mission(
        check_in,
        [],
        [only_available_mission],
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
        recent_feedback={2: ["not_for_me"]},
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
        recent_feedback={1: ["not_for_me"]},
        recent_check_ins=[
            make_check_in("Tired"),
            make_check_in("Sad"),
        ],
    )

    assert result is None

def test_explain_mission_score_reports_suitability_reasons():
    mission = SimpleNamespace(
        id=1,
        energy_required="low",
        social_required=False,
        category="regulation",
    )

    reasons = explain_mission_score(
        mission=mission,
        is_low_mood=True,
        is_stressed=False,
        is_lonely=False,
        repeated_low_mood=False,
        feedback_by_mission={},
    )

    assert "low_energy" in reasons
    assert "non_social" in reasons
    assert "low_energy_for_low_mood" in reasons

def test_build_recommendation_result_contains_mission_score_and_reasons():
    mission = SimpleNamespace(
        id=1,
        energy_required="low",
        social_required=False,
        category="regulation",
    )

    result = build_recommendation_result(
        mission=mission,
        is_low_mood=True,
        is_stressed=False,
        is_lonely=False,
        repeated_low_mood=False,
        feedback_by_mission={},
    )

    assert result["mission"] is mission
    assert isinstance(result["score"], int)
    assert "low_energy" in result["reasons"]
    assert "non_social" in result["reasons"]


def test_ml_ranking_can_change_selected_mission(monkeypatch):
    check_in = make_check_in("I'm doing okay")

    mission_one = make_mission(
        1,
        category="reflection",
        energy_required="medium",
        social_required=False,
    )

    mission_two = make_mission(
        2,
        category="reflection",
        energy_required="medium",
        social_required=False,
    )

    class FakeModel:
        pass

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        lambda: FakeModel(),
    )

    scores = {
        1: 0.1,
        2: 0.9,
    }

    def fake_predict(model, mission, energy_preference, recently_seen=False):
        return scores[mission.id]

    monkeypatch.setattr(
        engine,
        "predict_mission_match",
        fake_predict,
    )

    result = engine.choose_mission(
        check_in,
        [],
        [mission_one, mission_two],
    )

    assert result.id == 2


def test_rule_based_ranking_works_when_ml_model_unavailable(monkeypatch):
    check_in = make_check_in("I'm doing okay")

    mission_one = make_mission(
        1,
        category="reflection",
        energy_required="low",
        social_required=False,
    )

    mission_two = make_mission(
        2,
        category="reflection",
        energy_required="medium",
        social_required=True,
    )

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        lambda: None,
    )

    result = engine.choose_mission(
        check_in,
        [],
        [mission_one, mission_two],
    )

    assert result.id == 1

def test_infers_low_energy_from_explicit_low_energy_note():
    check_in = make_check_in(
        "I'm doing okay",
        "I'm exhausted and have very little energy today",
    )

    assert infer_energy_preference(check_in) == "low"


def test_infers_high_energy_from_explicit_high_energy_note():
    check_in = make_check_in(
        "I'm doing okay",
        "I feel energetic and ready to be active",
    )

    assert infer_energy_preference(check_in) == "high"


def test_defaults_to_medium_when_energy_is_unclear():
    check_in = make_check_in("I'm doing okay", "Just checking in")

    assert infer_energy_preference(check_in) == "medium"


def test_handles_missing_note():
    check_in = make_check_in("I'm doing okay")

    assert infer_energy_preference(check_in) == "medium"


def test_ml_ranking_receives_inferred_energy_preference(monkeypatch):
    check_in = make_check_in(
        "I'm doing okay",
        "I'm exhausted and have very little energy today",
    )
    mission = make_mission(1)

    received = {}

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        lambda: object(),
    )

    def fake_predict(
        model,
        selected_mission,
        energy_preference,
        recently_seen=False,
    ):
        received["energy_preference"] = energy_preference
        return 0.5

    monkeypatch.setattr(
        engine,
        "predict_mission_match",
        fake_predict,
    )

    engine.choose_mission(check_in, [], [mission])

    assert received["energy_preference"] == "low"

def test_ml_does_not_override_not_for_me_feedback(monkeypatch):
    check_in = make_check_in("I'm doing okay")

    disliked_mission = make_mission(1)
    alternative_mission = make_mission(2)

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        lambda: object(),
    )
    monkeypatch.setattr(
        engine,
        "predict_mission_match",
        lambda model, mission, energy_preference, recently_seen=False:
            1.0 if mission.id == 1 else 0.0,
    )

    result = engine.choose_mission(
        check_in,
        [],
        [disliked_mission, alternative_mission],
        recent_feedback={1: ["not_for_me"]},
    )

    assert result.id == 2


def test_ml_does_not_override_low_energy_suitability(monkeypatch):
    check_in = make_check_in("A little low")

    high_energy_mission = make_mission(
        1,
        energy_required="high",
        social_required=True,
    )
    low_energy_mission = make_mission(
        2,
        energy_required="low",
        social_required=False,
    )

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        lambda: object(),
    )
    monkeypatch.setattr(
        engine,
        "predict_mission_match",
        lambda model, mission, energy_preference, recently_seen=False:
            1.0 if mission.id == 1 else 0.0,
    )

    result = engine.choose_mission(
        check_in,
        [],
        [high_energy_mission, low_energy_mission],
    )

    assert result.id == 2

def test_format_mission_reasons():
    reasons = [
        "low_energy",
        "connection_for_loneliness",
        "unknown_reason",
    ]

    messages = format_mission_reasons(reasons)

    assert "This activity requires little energy." in messages
    assert (
        "This activity offers an opportunity for connection."
        in messages
    )
    assert len(messages) == 2

def test_rule_based_ranking_works_when_model_fails(monkeypatch):
    check_in = make_check_in("I'm doing okay")

    mission_one = make_mission(
        1,
        category="reflection",
        energy_required="medium",
        social_required=False,
    )

    mission_two = make_mission(
        2,
        category="reflection",
        energy_required="low",
        social_required=False,
    )

    def fail_to_load_model():
        raise RuntimeError("Model unavailable")

    monkeypatch.setattr(
        engine,
        "load_mission_model",
        fail_to_load_model,
    )

    result = engine.choose_mission(
        check_in,
        [],
        [mission_one, mission_two],
    )

    assert result is not None
    assert result.id == 2

def test_loneliness_bonus_applies_to_low_energy_non_social_connection_mission():
    mission = SimpleNamespace(
        id=10,
        category="connection",
        energy_required="low",
        social_required=False,
    )

    score = score_mission(
        mission,
        is_low_mood=False,
        is_stressed=False,
        is_lonely=True,
        repeated_low_mood=False,
        feedback_by_mission={},
    )

    assert score == 6

def test_build_feedback_history_uses_latest_feedback():
    feedback_rows = [
        SimpleNamespace(mission_id=1, feedback="not_for_me"),
        SimpleNamespace(mission_id=1, feedback="helpful"),
        SimpleNamespace(mission_id=2, feedback="helpful"),
    ]

    result = build_feedback_history(feedback_rows)

    assert result == {
        1: ["not_for_me", "helpful"],
        2: ["helpful"],
    }


def test_score_feedback_returns_zero_for_empty_history():
    assert score_feedback([]) == 0


def test_score_feedback_rewards_helpful_feedback():
    assert score_feedback(["helpful"]) == 3


def test_score_feedback_penalizes_not_for_me_feedback():
    assert score_feedback(["not_for_me"]) == -3


def test_score_feedback_gives_more_weight_to_latest_feedback():
    assert score_feedback(["not_for_me", "helpful"]) == -1


def test_score_feedback_caps_positive_score():
    assert score_feedback(
        ["helpful", "helpful", "helpful", "helpful", "helpful"]
    ) == 6


def test_score_feedback_caps_negative_score():
    assert score_feedback(
        ["not_for_me", "not_for_me", "not_for_me", "not_for_me", "not_for_me"]
    ) == -6

def test_low_mood_and_stress_apply_both_filters():
    missions = [
        make_mission(1, category="regulation"),
        make_mission(2, category="connection"),
        make_mission(3, category="regulation", energy_required="medium"),
        make_mission(4, category="reflection", social_required=True),
    ]

    result = engine.filter_suitable_missions(
        missions,
        is_low_mood=True,
        is_stressed=True,
        is_lonely=False,
    )

    assert [mission.id for mission in result] == [1]


def test_loneliness_and_stress_apply_both_filters():
    missions = [
        make_mission(1, category="environment"),
        make_mission(2, category="connection"),
        make_mission(3, category="reflection", energy_required="high"),
    ]

    result = engine.filter_suitable_missions(
        missions,
        is_low_mood=False,
        is_stressed=True,
        is_lonely=True,
    )

    assert [mission.id for mission in result] == [1]


def test_no_mood_signals_returns_all_missions():
    missions = [
        make_mission(1),
        make_mission(2, category="connection", energy_required="high"),
    ]

    result = engine.filter_suitable_missions(
        missions,
        is_low_mood=False,
        is_stressed=False,
        is_lonely=False,
    )

    assert result == missions

def test_positive_feedback_history_is_not_overridden_by_latest_negative_feedback():
    check_in = make_check_in("I'm doing okay")

    mission_1 = make_mission(1)
    mission_2 = make_mission(2)

    result = engine.choose_mission(
        check_in,
        [],
        [mission_1, mission_2],
        recent_feedback={
            1: ["not_for_me", "helpful", "helpful", "helpful"],
        },
    )

    assert result.id == 1

def test_negated_mood_words_do_not_trigger_low_mood():
    check_in = make_check_in("I'm doing okay", "I'm not sad or overwhelmed.")

    result = engine.detect_mood(check_in)

    assert result["is_low_mood"] is False