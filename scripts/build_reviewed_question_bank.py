from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    active_pesukim_records,
    active_pasuk_record_for_text,
    active_pasuk_ref_payload,
    active_scope_gold_annotation_for_pasuk_id,
    data_path,
    load_corpus_manifest,
    question_matches_gold_skill_record,
    resolve_repo_path,
)
from engine import flow_builder
from pasuk_flow_generator import analyze_pasuk as runtime_analyze_pasuk
from runtime.question_flow import validate_question_for_serve
from torah_parser.word_bank_adapter import normalize_hebrew_key

OUTPUT_PATH = data_path("active_scope_reviewed_questions.json")
SUMMARY_PATH = data_path("validation", "reviewed_question_bank_summary.json")
HIGH_FREQUENCY_LEXICON_PATH = data_path(
    "lexicon",
    "high_frequency",
    "high_frequency_lexicon.seed.v1.json",
)

TRANSLATION_TARGET_COUNT = 25
SHORESH_TARGET_COUNT = 25
TENSE_TARGET_COUNT = 25
AFFIX_TARGET_COUNT = 25

REVIEWED_BACKFILL_MORPHOLOGY_SUPPORT_ADDITIONS = (
    "וַתּוֹצֵא",
    "וַיִּתֵּן",
    "וַיִּבְרָא",
    "וַיִּשְׁבֹּת",
    "עֲשׂוֹת",
    "יִצְמָח",
    "וַיִּיצֶר",
    "וַיִּטַּע",
    "יִפָּרֵד",
    "וַיְצַו",
    "אֶעֱשֶׂה",
    "וַיִּקַּח",
    "וַיִּבֶן",
    "תַּדְשֵׁא",
    "יִשְׁרְצוּ",
)

# Narrow, gold-backed role/context lifts inside the current active scope.
# These are deliberately limited to richer approved targets that materially
# strengthen comprehension support without widening the skill surface.
REVIEWED_ROLE_CONTEXT_LIFTS = {
    "subject_identification": (
        {"pasuk_id": "bereishis_1_17", "target_index": 0},
        {"pasuk_id": "bereishis_1_21", "target_index": 0},
        {"pasuk_id": "bereishis_1_22", "target_index": 0},
        {"pasuk_id": "bereishis_1_25", "target_index": 0},
        {"pasuk_id": "bereishis_1_31", "target_index": 0},
        {"pasuk_id": "bereishis_2_2", "target_index": 0},
        {"pasuk_id": "bereishis_2_9", "target_index": 0},
    ),
    "object_identification": (
        {"pasuk_id": "bereishis_1_21", "target_index": 0},
        {"pasuk_id": "bereishis_1_22", "target_index": 0},
        {"pasuk_id": "bereishis_1_25", "target_index": 0},
        {"pasuk_id": "bereishis_1_31", "target_index": 0},
    ),
    "phrase_translation": (
        {
            "pasuk_id": "bereishis_1_17",
            "target_index": 0,
            "distractors": [
                "God blessed them",
                "God created them",
                "God placed the light",
            ],
        },
        {
            "pasuk_id": "bereishis_1_21",
            "target_index": 0,
            "distractors": [
                "God blessed the great sea creatures",
                "God created the two great lights",
                "God saw the great sea creatures",
            ],
        },
        {
            "pasuk_id": "bereishis_1_22",
            "target_index": 0,
            "distractors": [
                "God created them",
                "God blessed the earth",
                "God placed them",
            ],
        },
        {
            "pasuk_id": "bereishis_1_25",
            "target_index": 0,
            "distractors": [
                "God blessed the beasts of the earth",
                "God made the great sea creatures",
                "God saw the beasts of the earth",
            ],
        },
        {
            "pasuk_id": "bereishis_1_31",
            "target_index": 0,
            "distractors": [
                "God made all that He had seen",
                "God saw the beasts of the earth",
                "God blessed all that He had made",
            ],
        },
        {
            "pasuk_id": "bereishis_2_2",
            "target_index": 0,
            "distractors": [
                "God blessed",
                "God created",
                "God rested",
            ],
        },
        {
            "pasuk_id": "bereishis_2_9",
            "target_index": 0,
            "distractors": [
                "the LORD God planted every tree",
                "God caused every tree to grow",
                "the LORD God caused every beast to grow",
            ],
        },
    ),
}

# Conservative reviewed-foundation lifts drawn from the current-scope hand audit.
# These promote a small set of already-clean meaning/POS targets so runtime can
# prefer reviewed support over thinner generated fallbacks.
REVIEWED_FOUNDATION_LIFTS = {
    "translation": (
        {
            "pasuk_id": "bereishis_1_5",
            "token": "וַיִּקְרָא",
        },
        {
            "pasuk_id": "bereishis_1_6",
            "token": "וִיהִי",
            "extra_distractors": (
                "and there was",
                "and he said",
                "and let it appear",
            ),
        },
        {
            "pasuk_id": "bereishis_2_4",
            "token": "עֲשׂוֹת",
            "extra_distractors": (
                "to see",
                "to build",
                "to call",
            ),
        },
        {
            "pasuk_id": "bereishis_2_23",
            "token": "וַיֹּאמֶר",
            "extra_distractors": (
                "and he saw",
                "and he built",
                "and he planted",
            ),
        },
        {
            "pasuk_id": "bereishis_2_15",
            "token": "\u05d5\u05b7\u05d9\u05bc\u05b4\u05e7\u05bc\u05b7\u05d7",
        },
        {
            "pasuk_id": "bereishis_1_4",
            "token": "\u05d5\u05b7\u05d9\u05bc\u05b7\u05e8\u05b0\u05d0",
        },
        {
            "pasuk_id": "bereishis_1_4",
            "token": "\u05d5\u05b7\u05d9\u05bc\u05b7\u05d1\u05b0\u05d3\u05bc\u05b5\u05dc",
        },
        {
            "pasuk_id": "bereishis_3_1",
            "token": "\u05d4\u05b8\u05d9\u05b8\u05d4",
        },
        {
            "pasuk_id": "bereishis_3_1",
            "token": "\u05ea\u05b9\u05d0\u05db\u05b0\u05dc\u05d5\u05bc",
        },
        {
            "pasuk_id": "bereishis_3_1",
            "token": "\u05e2\u05b8\u05e9\u05b8\u05c2\u05d4",
        },
        {
            "pasuk_id": "bereishis_3_3",
            "token": "\u05ea\u05b0\u05bc\u05de\u05bb\u05ea\u05d5\u05bc\u05df",
        },
        {
            "pasuk_id": "bereishis_3_3",
            "token": "\u05ea\u05b4\u05d2\u05b0\u05bc\u05e2\u05d5\u05bc",
        },
        {
            "pasuk_id": "bereishis_3_6",
            "token": "\u05dc\u05b0\u05d4\u05b7\u05e9\u05b0\u05c2\u05db\u05b4\u05bc\u05d9\u05dc",
        },
        {
            "pasuk_id": "bereishis_3_5",
            "token": "\u05d9\u05b9\u05d3\u05b5\u05e2\u05b7",
        },
        {
            "pasuk_id": "bereishis_3_7",
            "token": "\u05ea\u05b0\u05d0\u05b5\u05e0\u05b8\u05d4",
        },
        {
            "pasuk_id": "bereishis_3_7",
            "token": "\u05d7\u05b2\u05d2\u05b9\u05e8\u05b9\u05ea",
        },
        {
            "pasuk_id": "bereishis_3_7",
            "token": "\u05d5\u05b7\u05d9\u05b4\u05bc\u05ea\u05b0\u05e4\u05b0\u05bc\u05e8\u05d5\u05bc",
        },
        {
            "pasuk_id": "bereishis_3_8",
            "token": "\u05de\u05b4\u05ea\u05b0\u05d4\u05b7\u05dc\u05b5\u05bc\u05da\u05b0",
        },
        {
            "pasuk_id": "bereishis_3_8",
            "token": "\u05d5\u05b7\u05d9\u05bc\u05b4\u05ea\u05b0\u05d7\u05b7\u05d1\u05b5\u05bc\u05d0",
        },
        {
            "pasuk_id": "bereishis_3_8",
            "token": "\u05e2\u05b5\u05e5",
        },
    ),
    "part_of_speech": (
        {"pasuk_id": "bereishis_1_3", "token": "וַיְהִי"},
        {"pasuk_id": "bereishis_1_4", "token": "וַיַּבְדֵּל"},
        {"pasuk_id": "bereishis_1_9", "token": "וְתֵרָאֶה"},
        {"pasuk_id": "bereishis_1_10", "token": "וַיִּקְרָא"},
        {"pasuk_id": "bereishis_1_12", "token": "וַיַּרְא"},
        {"pasuk_id": "bereishis_1_11", "token": "עֵץ"},
        {"pasuk_id": "bereishis_2_8", "token": "וַיִּטַּע"},
        {"pasuk_id": "bereishis_2_23", "token": "וַיֹּאמֶר"},
        {"pasuk_id": "bereishis_3_8", "token": "קוֹל"},
    ),
}

LEXICON_TIER_BONUS = {
    "A": 3.5,
    "B": 2.0,
    "C": 1.0,
    "D": 0.0,
}

AWKWARD_SHORESH_ROOTS = {
    "יקדש",
    "יקח",
    "יצו",
    "יישן",
    "יבאה",
    "יהי",
}
GENERIC_PHRASE_TRANSLATIONS = {
    "and God said",
    "and God saw",
    "and God made",
}
SHORESH_ROOT_CAPS = {
    "היה": 1,
    "אמר": 2,
    "ראה": 2,
    "קרא": 2,
    "עשה": 2,
}
DEFAULT_SHORESH_ROOT_CAP = 2
DEFAULT_SHORESH_TOKEN_CAP = 2
TENSE_TOKEN_CAPS = {
    normalize_hebrew_key("וַיְהִי"): 2,
    normalize_hebrew_key("וַיֹּאמֶר"): 2,
    normalize_hebrew_key("וַיַּרְא"): 2,
    normalize_hebrew_key("וַיִּקְרָא"): 2,
    normalize_hebrew_key("וַיַּעַשׂ"): 2,
    normalize_hebrew_key("וַיַּבְדֵּל"): 2,
}
DEFAULT_TENSE_TOKEN_CAP = 2
TENSE_CODE_CAPS = {
    "vav_consecutive_past": 17,
    "future": 6,
    "future_jussive": 4,
    "infinitive": 3,
}
SHORESH_PRIORITY_TOKENS_BY_PASUK = {
    "bereishis_1_9": ("יִקָּווּ",),
    "bereishis_1_12": ("וַתּוֹצֵא",),
    "bereishis_1_17": ("וַיִּתֵּן",),
    "bereishis_1_21": ("וַיִּבְרָא",),
    "bereishis_2_2": ("וַיִּשְׁבֹּת",),
    "bereishis_2_5": ("יִצְמָח",),
    "bereishis_2_7": ("וַיִּיצֶר",),
    "bereishis_2_8": ("וַיִּטַּע",),
    "bereishis_2_10": ("יִפָּרֵד",),
    "bereishis_2_16": ("וַיְצַו",),
    "bereishis_2_18": ("אֶעֱשֶׂה",),
    "bereishis_2_21": ("וַיִּקַּח",),
    "bereishis_2_22": ("וַיִּבֶן",),
}
TENSE_PRIORITY_TOKENS_BY_PASUK = {
    "bereishis_1_6": ("וִיהִי",),
    "bereishis_1_9": ("וְתֵרָאֶה", "יִקָּווּ"),
    "bereishis_1_12": ("וַתּוֹצֵא",),
    "bereishis_1_17": ("וַיִּתֵּן",),
    "bereishis_1_20": ("יִשְׁרְצוּ",),
    "bereishis_2_2": ("וַיִּשְׁבֹּת",),
    "bereishis_2_4": ("עֲשׂוֹת",),
    "bereishis_2_5": ("יִצְמָח",),
    "bereishis_2_7": ("וַיִּיצֶר",),
    "bereishis_2_10": ("יִפָּרֵד",),
    "bereishis_2_18": ("אֶעֱשֶׂה",),
    "bereishis_2_21": ("וַיִּקַּח",),
    "bereishis_2_22": ("וַיִּבֶן",),
}
TRANSLATION_PRIORITY_TOKENS_BY_PASUK = {
    "bereishis_2_7": ("נִשְׁמַת",),
}
REMAINING_SHORTFALL_EXPLANATIONS = {
    "shoresh": [
        "Remaining active-scope verb targets were skipped because they stayed too duplicate-feel, object-suffix heavy, or morphologically weak under the current fail-closed validator.",
    ],
    "tense": [
        "Remaining active-scope tense targets were skipped because they stayed too duplicate-feel, morphologically weak, or context-dependent under the current fail-closed validator.",
    ],
}


def normalized_english(text: str | None) -> str:
    rendered = " ".join(str(text or "").split()).lower()
    if not rendered:
        return ""
    if rendered not in {"god", "the lord", "the lord god"}:
        for prefix in ("the ", "a ", "an "):
            if rendered.startswith(prefix):
                rendered = rendered[len(prefix):]
                break
    return rendered


@lru_cache(maxsize=1)
def high_frequency_lexicon_index():
    payload = json.loads(HIGH_FREQUENCY_LEXICON_PATH.read_text(encoding="utf-8"))
    index = {}
    for entry in payload.get("seed_entries", []):
        tier = str(entry.get("tier") or "").strip().upper()
        hebrew = str(entry.get("hebrew") or "").strip()
        if not hebrew or not tier:
            continue
        for variant in re.split(r"\s*/\s*", hebrew):
            key = normalize_hebrew_key(variant)
            if key:
                index[key] = tier
    return index


def lexicon_tier_for_token_entry(token: str, entry: dict | None):
    index = high_frequency_lexicon_index()
    candidates = [
        normalize_hebrew_key(token),
        normalize_hebrew_key((entry or {}).get("lemma") or ""),
        normalize_hebrew_key(flow_builder.clean_shoresh_value((entry or {}).get("shoresh")) or ""),
    ]
    best = None
    for candidate in candidates:
        tier = index.get(candidate)
        if not tier:
            continue
        if best is None or LEXICON_TIER_BONUS.get(tier, 0.0) > LEXICON_TIER_BONUS.get(best, 0.0):
            best = tier
    return best


def stable_fragment(value: str | None) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unknown"


def reviewed_id(family: str, skill: str, pasuk_id: str, target: str, *, question_type: str = "", correct_answer: str = "") -> str:
    normalized_target = normalize_hebrew_key(target or "") or "no_target"
    normalized_type = stable_fragment(question_type or skill or "")
    normalized_answer = normalize_hebrew_key(correct_answer or "") or stable_fragment(correct_answer or "")
    return f"{family}_{skill}_{pasuk_id}_{normalized_type}_{normalized_target}_{normalized_answer}"


def target_signature(question):
    return normalize_hebrew_key(question.get("selected_word") or question.get("word") or "")


def question_repeat_key(question):
    return (
        question.get("question_type") or question.get("skill"),
        target_signature(question),
        normalized_english(question.get("correct_answer")),
    )


def token_priority_bonus(record, token, priorities):
    if not record or not token:
        return 0.0
    preferred_tokens = priorities.get(record.get("pasuk_id")) or ()
    token_key = normalize_hebrew_key(token)
    for index, preferred_token in enumerate(preferred_tokens):
        if token_key == normalize_hebrew_key(preferred_token):
            return max(len(preferred_tokens) - index, 1) * 4.0
    return 0.0


def lane_counts_from_payload(payload):
    lane_counts = Counter()
    for item in payload.get("questions", []):
        lane_counts[item.get("review_family") or "unknown"] += 1
    return dict(lane_counts)


def reviewed_bank_duplicate_key(question):
    return (
        question.get("review_family") or question.get("skill") or "unknown",
        question.get("skill"),
        question.get("pasuk_id"),
        normalize_hebrew_key(question.get("selected_word") or question.get("word") or ""),
        normalized_english(question.get("correct_answer")),
    )


def active_scope_reviewed_seed_paths():
    manifest = load_corpus_manifest()
    paths = []
    for corpus in manifest.get("parsed_corpora", []):
        reviewed_path = (corpus.get("parsed_files") or {}).get("reviewed_questions")
        if not reviewed_path:
            continue
        resolved = resolve_repo_path(reviewed_path)
        if resolved.exists():
            paths.append(resolved)
    return paths


def gold_suppresses_reviewed_skill(pasuk_id: str | None, skill: str | None) -> bool:
    if not pasuk_id or not skill:
        return False
    annotation = active_scope_gold_annotation_for_pasuk_id(pasuk_id) or {}
    skill_record = (annotation.get("skills") or {}).get(str(skill))
    return bool(skill_record and skill_record.get("status") == "suppressed")


def load_promoted_seed_questions():
    active_ids = {
        record.get("pasuk_id")
        for record in active_pesukim_records()
        if record.get("pasuk_id")
    }
    imported = []
    for path in active_scope_reviewed_seed_paths():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for question in payload.get("questions", []):
            if question.get("pasuk_id") not in active_ids:
                continue
            if gold_suppresses_reviewed_skill(question.get("pasuk_id"), question.get("skill")):
                continue
            validation = validate_question_for_serve(
                deepcopy(question),
                fallback_text=question.get("pasuk"),
                validation_path="reviewed_bank_promoted_seed",
                trusted_active_scope=True,
            )
            if not validation["valid"]:
                continue
            item = deepcopy(validation["question"])
            family = str(item.get("review_family") or question.get("review_family") or item.get("skill") or "unknown")
            alias_skills = [str(value).strip() for value in question.get("alias_skills") or [] if str(value).strip()]
            if family == "tense" and item.get("skill") == "identify_tense" and "verb_tense" not in alias_skills:
                alias_skills.append("verb_tense")
            item["review_family"] = family
            item["alias_skills"] = alias_skills
            item["reviewed_id"] = reviewed_id(
                family,
                str(item.get("skill") or ""),
                str(item.get("pasuk_id") or ""),
                str(item.get("selected_word") or item.get("word") or item.get("correct_answer") or ""),
                question_type=str(item.get("question_type") or ""),
                correct_answer=str(item.get("correct_answer") or ""),
            )
            item["source"] = "active scope reviewed bank"
            item["analysis_source"] = "promoted_staged_reviewed_support"
            imported.append(item)
    return imported


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validated_question(question, *, pasuk_text: str, validation_path: str):
    if not question or question.get("status") == "skipped":
        return None
    validation = validate_question_for_serve(
        deepcopy(question),
        fallback_text=pasuk_text,
        validation_path=validation_path,
        trusted_active_scope=True,
    )
    if not validation["valid"]:
        return None
    return validation["question"]


def build_generated_question(skill: str, pasuk_text: str, *, target_token: str | None = None, prefix_level: int | None = None):
    kwargs = {}
    if prefix_level is not None:
        kwargs["prefix_level"] = prefix_level
    try:
        with patch.object(flow_builder, "reviewed_question_for_pasuk_skill", return_value=None):
            if target_token:
                with patch.object(flow_builder, "pick_word_for_skill", return_value=target_token):
                    question = flow_builder.generate_question(skill, pasuk_text, **kwargs)
            else:
                question = flow_builder.generate_question(skill, pasuk_text, **kwargs)
    except Exception:
        return None
    return validated_question(question, pasuk_text=pasuk_text, validation_path="reviewed_bank_build")


def active_record_for_pasuk_id(pasuk_id: str):
    return next(
        (record for record in active_pesukim_records() if record.get("pasuk_id") == pasuk_id),
        None,
    )


def gold_skill_target_for_pasuk(pasuk_id: str, skill: str, target_index: int = 0):
    annotation = active_scope_gold_annotation_for_pasuk_id(pasuk_id) or {}
    skill_record = (annotation.get("skills") or {}).get(skill) or {}
    if skill_record.get("status") != "approved":
        return None
    approved_targets = list(skill_record.get("approved_targets") or [])
    if not approved_targets:
        return None
    if target_index >= len(approved_targets):
        return None
    return skill_record, deepcopy(approved_targets[target_index])


def role_entity_defaults(translation: str):
    lowered = normalized_english(translation)
    if "lord god" in lowered or lowered == "god" or lowered == "the lord":
        return {
            "semantic_group": "divine",
            "entity_type": "divine_being",
        }
    return {
        "semantic_group": "person",
        "entity_type": "person",
    }


def build_gold_subject_reviewed_question(record, target):
    action_token = target.get("main_verb_token")
    surface = target.get("surface")
    translation = target.get("translation")
    if not action_token or not surface or not translation:
        return None
    entity_defaults = role_entity_defaults(translation)
    question = flow_builder.skill_question_payload(
        "subject_identification",
        {
            "token": surface,
            "entry": flow_builder.override_target_entry(
                surface,
                translation,
                semantic_group=entity_defaults["semantic_group"],
                role_hint="subject_candidate",
                entity_type=entity_defaults["entity_type"],
            ),
            "source_pasuk": record["text"],
        },
        f"Who is doing the action in {action_token}?",
        flow_builder.build_parallel_choices(
            translation,
            flow_builder.override_distractors(
                flow_builder.SUBJECT_OVERRIDE_DISTRACTOR_POOL,
                translation,
            ),
            f"{record['pasuk_id']}|reviewed_subject",
            token=surface,
        ),
        translation,
        f"In {action_token}, {surface} is doing the action.",
        action_token=action_token,
        role_focus="subject",
    )
    question = validated_question(
        question,
        pasuk_text=record["text"],
        validation_path="reviewed_bank_gold_subject",
    )
    if not question:
        return None
    skill_record = (active_scope_gold_annotation_for_pasuk_id(record["pasuk_id"]) or {}).get("skills", {}).get("subject_identification")
    if not question_matches_gold_skill_record(question, skill_record):
        return None
    return question


def build_gold_object_reviewed_question(record, target):
    action_token = target.get("main_verb_token")
    surface = target.get("surface")
    translation = target.get("translation")
    role_focus = target.get("role") or "direct_object"
    if not action_token or not surface or not translation:
        return None
    question = flow_builder.skill_question_payload(
        "object_identification",
        {
            "token": surface,
            "entry": flow_builder.override_target_entry(
                surface,
                translation,
                semantic_group="object",
                role_hint="object_candidate",
                entity_type="common_noun",
            ),
            "source_pasuk": record["text"],
        },
        (
            f"Who receives the action in {action_token}?"
            if role_focus == "recipient"
            else f"What receives the action in {action_token}?"
        ),
        flow_builder.build_parallel_choices(
            translation,
            flow_builder.override_distractors(
                flow_builder.RECIPIENT_OVERRIDE_DISTRACTOR_POOL if role_focus == "recipient" else flow_builder.OBJECT_OVERRIDE_DISTRACTOR_POOL,
                translation,
            ),
            f"{record['pasuk_id']}|reviewed_object|{role_focus}",
            token=surface,
        ),
        translation,
        (
            f"In {action_token}, {surface} is the one receiving the action."
            if role_focus == "recipient"
            else f"In {action_token}, {surface} is what receives the action."
        ),
        action_token=action_token,
        role_focus=role_focus,
    )
    question = validated_question(
        question,
        pasuk_text=record["text"],
        validation_path="reviewed_bank_gold_object",
    )
    if not question:
        return None
    skill_record = (active_scope_gold_annotation_for_pasuk_id(record["pasuk_id"]) or {}).get("skills", {}).get("object_identification")
    if not question_matches_gold_skill_record(question, skill_record):
        return None
    return question


def build_gold_phrase_reviewed_question(record, target, distractors):
    surface = target.get("surface")
    translation = target.get("translation")
    if not surface or not translation:
        return None
    question = flow_builder.skill_question_payload(
        "phrase_translation",
        {
            "token": surface,
            "entry": {
                "translation": translation,
                "type": "phrase",
                "part_of_speech": "phrase",
            },
            "source_pasuk": record["text"],
        },
        "What does this phrase mean?",
        flow_builder.build_parallel_choices(
            translation,
            list(distractors or []),
            f"{record['pasuk_id']}|reviewed_phrase",
            token=surface,
        ),
        translation,
        f"Here, {surface} means '{translation}'.",
    )
    question = validated_question(
        question,
        pasuk_text=record["text"],
        validation_path="reviewed_bank_gold_phrase",
    )
    if not question:
        return None
    skill_record = (active_scope_gold_annotation_for_pasuk_id(record["pasuk_id"]) or {}).get("skills", {}).get("phrase_translation")
    if not question_matches_gold_skill_record(question, skill_record):
        return None
    return question


def build_gold_role_context_reviewed_items():
    questions = []

    for spec in REVIEWED_ROLE_CONTEXT_LIFTS["subject_identification"]:
        record = active_record_for_pasuk_id(spec["pasuk_id"])
        target_data = gold_skill_target_for_pasuk(
            spec["pasuk_id"],
            "subject_identification",
            spec.get("target_index", 0),
        )
        if not record or not target_data:
            continue
        _skill_record, target = target_data
        question = build_gold_subject_reviewed_question(record, target)
        if question:
            questions.append((question, "role", []))

    for spec in REVIEWED_ROLE_CONTEXT_LIFTS["object_identification"]:
        record = active_record_for_pasuk_id(spec["pasuk_id"])
        target_data = gold_skill_target_for_pasuk(
            spec["pasuk_id"],
            "object_identification",
            spec.get("target_index", 0),
        )
        if not record or not target_data:
            continue
        _skill_record, target = target_data
        question = build_gold_object_reviewed_question(record, target)
        if question:
            questions.append((question, "role", []))

    for spec in REVIEWED_ROLE_CONTEXT_LIFTS["phrase_translation"]:
        record = active_record_for_pasuk_id(spec["pasuk_id"])
        target_data = gold_skill_target_for_pasuk(
            spec["pasuk_id"],
            "phrase_translation",
            spec.get("target_index", 0),
        )
        if not record or not target_data:
            continue
        _skill_record, target = target_data
        question = build_gold_phrase_reviewed_question(
            record,
            target,
            spec.get("distractors") or [],
        )
        if question:
            questions.append((question, "translation", []))

    return questions


def preferred_runtime_analysis_entry(item):
    analyses = list(item.get("analyses") or [])
    if not analyses and isinstance(item.get("entry"), dict):
        analyses = [item["entry"]]
    for analysis in analyses:
        if analysis.get("confidence") == "generated_alternate":
            continue
        if (
            analysis.get("part_of_speech") not in {"", None, "unknown"}
            or analysis.get("tense")
            or analysis.get("shoresh")
            or analysis.get("prefixes")
            or analysis.get("suffixes")
        ):
            return deepcopy(analysis)
    for analysis in analyses:
        if analysis.get("confidence") != "generated_alternate":
            return deepcopy(analysis)
    return deepcopy(analyses[0]) if analyses else {}


def analyzed_items_for_record(record):
    items = []
    for item in runtime_analyze_pasuk(record["text"]):
        token = item.get("word") or item.get("token") or item.get("surface")
        entry = preferred_runtime_analysis_entry(item)
        if token and entry:
            items.append({"token": token, "entry": entry})
    return items


def analyzed_item_for_record_token(record, token):
    token_key = normalize_hebrew_key(token)
    for item in analyzed_items_for_record(record):
        if normalize_hebrew_key(item["token"]) == token_key:
            return item
    return None


def build_manual_shoresh_question(record, item, word_bank):
    token = item["token"]
    entry = item["entry"]
    validation = flow_builder.validate_question_candidate("shoresh", token, entry)
    if not validation["valid"]:
        return None
    correct = flow_builder.clean_shoresh_value(entry.get("shoresh"))
    if not correct:
        return None
    distractors = [
        value
        for value in flow_builder.shoresh_distractors(correct, word_bank)
        if normalize_hebrew_key(value) != normalize_hebrew_key(correct)
    ]
    if len(distractors) < 3:
        return None
    question = flow_builder.skill_question_payload(
        "shoresh",
        {"token": token, "entry": entry, "source_pasuk": record["text"]},
        f"What is the shoresh of {token}?",
        [correct] + distractors[:3],
        correct,
        f"The shoresh of {token} is {correct}.",
    )
    return validated_question(question, pasuk_text=record["text"], validation_path="reviewed_bank_build")


def build_manual_tense_question(record, item):
    token = item["token"]
    entry = item["entry"]
    correct = flow_builder.runtime_tense_label(entry, token)
    if not correct:
        return None
    choices = flow_builder.fair_tense_choice_codes(correct)
    if not choices:
        return None
    details = flow_builder.tense_form_details(correct, token)
    question = flow_builder.skill_question_payload(
        "identify_tense",
        {"token": token, "entry": entry, "source_pasuk": record["text"]},
        "What form is shown?",
        choices,
        correct,
        flow_builder.tense_question_explanation({"token": token, "entry": entry}, correct),
        tense_display_phrase=details.get("display_phrase"),
        base_conjugation=details.get("base_conjugation"),
        vav_prefix_type=details.get("vav_prefix_type"),
        accepted_answer_aliases=details.get("accepted_answer_aliases"),
        tense_code=details.get("canonical_code"),
        tense=correct,
    )
    return validated_question(question, pasuk_text=record["text"], validation_path="reviewed_bank_build")


def build_manual_translation_question(record, item, word_bank, by_group, *, extra_distractors=()):
    token = item["token"]
    entry = item["entry"]
    if not flow_builder.standalone_translation_target(entry, token):
        return None
    correct = flow_builder.usable_translation(entry, token)
    if not correct:
        return None
    distractors = flow_builder.translation_distractors(
        correct,
        entry,
        by_group,
        word_bank,
        require_quality_count=3,
    )
    try:
        choices = flow_builder.build_parallel_choices(
            correct,
            distractors,
            f"{record['pasuk_id']}|reviewed_translation|{normalize_hebrew_key(token)}",
            extra=list(extra_distractors or []),
            token=token,
        )
    except ValueError:
        return None
    question = flow_builder.skill_question_payload(
        "translation",
        {"token": token, "entry": entry, "source_pasuk": record["text"]},
        f"What does {token} mean?",
        choices,
        correct,
        f"{token} means '{correct}'.",
    )
    return validated_question(question, pasuk_text=record["text"], validation_path="reviewed_bank_build")


def build_manual_part_of_speech_question(record, item):
    token = item["token"]
    entry = item["entry"]
    if not flow_builder.part_of_speech_target_supported(entry, token):
        return None
    correct = flow_builder.entry_type(entry)
    student_correct = flow_builder.student_part_of_speech_label(correct)
    choices = flow_builder.cohort_safe_part_of_speech_choices(correct)
    if not student_correct or choices is None:
        return None
    word_gloss = flow_builder.usable_translation(entry, token)
    explanation = (
        f"{token} means '{word_gloss}', so here it is {flow_builder.part_of_speech_with_article(student_correct)}."
        if word_gloss
        else f"{token} is {flow_builder.part_of_speech_with_article(student_correct)}."
    )
    question = flow_builder.skill_question_payload(
        "part_of_speech",
        {"token": token, "entry": entry, "source_pasuk": record["text"]},
        f"What kind of word is {token}?",
        choices,
        student_correct,
        explanation,
    )
    return validated_question(question, pasuk_text=record["text"], validation_path="reviewed_bank_build")


def build_reviewed_foundation_items(word_bank, by_group):
    questions = []
    for spec in REVIEWED_FOUNDATION_LIFTS["translation"]:
        record = active_record_for_pasuk_id(spec["pasuk_id"])
        if not record:
            continue
        item = analyzed_item_for_record_token(record, spec["token"])
        if not item:
            continue
        question = build_manual_translation_question(
            record,
            item,
            word_bank,
            by_group,
            extra_distractors=spec.get("extra_distractors", ()),
        )
        if question:
            questions.append((question, "translation", []))

    for spec in REVIEWED_FOUNDATION_LIFTS["part_of_speech"]:
        record = active_record_for_pasuk_id(spec["pasuk_id"])
        if not record:
            continue
        item = analyzed_item_for_record_token(record, spec["token"])
        if not item:
            continue
        question = build_manual_part_of_speech_question(record, item)
        if question:
            questions.append((question, "part_of_speech", []))

    return questions


def phrase_candidates():
    candidates = []
    for record in active_pesukim_records():
        question = build_generated_question("phrase_translation", record["text"])
        if not question:
            continue
        correct = normalized_english(question.get("correct_answer"))
        score = len(str(question.get("selected_word") or "").split()) + len(correct.split())
        if correct in GENERIC_PHRASE_TRANSLATIONS:
            score -= 4
        candidates.append(
            {
                "record": record,
                "question": question,
                "correct_key": correct,
                "score": score,
            }
        )
    candidates.sort(
        key=lambda item: (
            -item["score"],
            item["correct_key"],
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def translation_candidates(word_bank):
    candidates = []
    for record in active_pesukim_records():
        analyzed = flow_builder.analyze_pasuk(record["text"], word_bank)
        for item in analyzed:
            token = item["token"]
            entry = item["entry"]
            if not flow_builder.standalone_translation_target(entry, token):
                continue
            gloss = flow_builder.usable_translation(entry, token)
            kind = flow_builder.entry_type(entry)
            if not gloss or kind == "prep":
                continue
            score = 0.0
            if kind in {"noun", "adjective", "pronoun", "adverb"}:
                score += 3.0
            if kind == "verb":
                score -= 1.0
            if str(gloss).lower().startswith("and "):
                score -= 1.0
            lexicon_tier = lexicon_tier_for_token_entry(token, entry)
            score += LEXICON_TIER_BONUS.get(lexicon_tier, 0.0)
            semantic_group = entry.get("semantic_group") or ""
            if semantic_group in {"object", "place", "abstract", "description", "quantity", "person_reference"}:
                score += 1.5
            if semantic_group == "divine":
                score -= 2.0
            if normalized_english(gloss) in {"god", "the lord", "the lord god"}:
                score -= 5.0
            score += token_priority_bonus(record, token, TRANSLATION_PRIORITY_TOKENS_BY_PASUK)
            candidates.append(
                {
                    "record": record,
                    "token": token,
                    "gloss": gloss,
                    "kind": kind,
                    "lexicon_tier": lexicon_tier,
                    "meaning_key": normalized_english(gloss),
                    "semantic_group": semantic_group,
                    "score": score,
                }
            )
    candidates.sort(
        key=lambda item: (
            -item["score"],
            item["meaning_key"],
            normalize_hebrew_key(item["token"]),
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def manual_shoresh_candidates(word_bank):
    candidates = []
    seen = set()
    for record in active_pesukim_records():
        for item in analyzed_items_for_record(record):
            token = item["token"]
            entry = item["entry"]
            if flow_builder.entry_type(entry) != "verb":
                continue
            root = flow_builder.clean_shoresh_value(entry.get("shoresh"))
            if not root:
                continue
            if normalize_hebrew_key(root) in {normalize_hebrew_key(value) for value in AWKWARD_SHORESH_ROOTS}:
                continue
            question = build_manual_shoresh_question(record, item, word_bank)
            if not question:
                continue
            candidate_key = (record["pasuk_id"], normalize_hebrew_key(token), normalize_hebrew_key(root))
            if candidate_key in seen:
                continue
            seen.add(candidate_key)
            normalized_token = normalize_hebrew_key(token)
            score = 0.0
            if not normalized_token.startswith("ו"):
                score += 2.0
            elif normalized_token.startswith(("וי", "ות")):
                score -= 1.5
            else:
                score -= 1.0
            root_key = normalize_hebrew_key(root)
            if root_key == normalize_hebrew_key("היה"):
                score -= 1.0
            if root_key not in {
                normalize_hebrew_key("אמר"),
                normalize_hebrew_key("היה"),
                normalize_hebrew_key("ראה"),
                normalize_hebrew_key("קרא"),
                normalize_hebrew_key("עשה"),
            }:
                score += 1.0
            score += token_priority_bonus(record, token, SHORESH_PRIORITY_TOKENS_BY_PASUK)
            candidates.append(
                {
                    "record": record,
                    "question": question,
                    "token": token,
                    "root": root,
                    "root_key": root_key,
                    "score": score,
                }
            )
    candidates.sort(
        key=lambda item: (
            -item["score"],
            normalize_hebrew_key(item["root"]),
            normalize_hebrew_key(item["token"]),
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def manual_tense_candidates():
    candidates = []
    seen = set()
    for record in active_pesukim_records():
        for item in analyzed_items_for_record(record):
            token = item["token"]
            entry = item["entry"]
            if flow_builder.entry_type(entry) != "verb":
                continue
            question = build_manual_tense_question(record, item)
            if not question:
                continue
            displayed_label = str(question.get("correct_answer") or "")
            tense_code = str(question.get("tense_code") or "")
            candidate_key = (
                record["pasuk_id"],
                normalize_hebrew_key(token),
                displayed_label,
                tense_code,
            )
            if candidate_key in seen:
                continue
            seen.add(candidate_key)
            normalized_token = normalize_hebrew_key(token)
            score = 0.0
            if displayed_label == "to do form":
                score += 5.0
            elif displayed_label == "future":
                score += 4.0
            if not normalized_token.startswith("ו"):
                score += 1.0
            elif tense_code == "vav_consecutive_past":
                score -= 0.5
            score += token_priority_bonus(record, token, TENSE_PRIORITY_TOKENS_BY_PASUK)
            candidates.append(
                {
                    "record": record,
                    "question": question,
                    "token": token,
                    "displayed_label": displayed_label,
                    "tense_code": tense_code,
                    "score": score,
                }
            )
    candidates.sort(
        key=lambda item: (
            -item["score"],
            item["displayed_label"],
            normalize_hebrew_key(item["token"]),
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def prefix_candidates(word_bank, level: int):
    candidates = []
    for record in active_pesukim_records():
        analyzed = flow_builder.analyze_pasuk(record["text"], word_bank)
        for item in analyzed:
            token = item["token"]
            entry = deepcopy(item["entry"])
            flow_builder.apply_prefix_metadata(token, entry, word_bank)
            result = flow_builder.validate_question_candidate("identify_prefix_meaning", token, entry)
            if not result["valid"]:
                continue
            prefix = entry.get("prefix") or flow_builder.extract_prefix(token, word_bank)
            meaning = flow_builder.PREFIX_MEANINGS.get(prefix)
            if not prefix or not meaning:
                continue
            score = 0.0
            if prefix != "ו":
                score += 2.0
            if level >= 2 and prefix in {"ל", "ב", "מ"}:
                score += 1.5
            if level == 3 and flow_builder.entry_type(entry) in {"noun", "verb"}:
                score += 1.0
            candidates.append(
                {
                    "record": record,
                    "token": token,
                    "prefix": prefix,
                    "score": score,
                    "level": level,
                }
            )
    candidates.sort(
        key=lambda item: (
            -item["score"],
            item["prefix"],
            normalize_hebrew_key(item["token"]),
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def suffix_candidates(skill: str):
    candidates = []
    for record in active_pesukim_records():
        question = build_generated_question(skill, record["text"])
        if not question:
            continue
        candidates.append(
            {
                "record": record,
                "question": question,
                "token": question.get("selected_word") or question.get("word"),
                "correct": question.get("correct_answer"),
            }
        )
    candidates.sort(
        key=lambda item: (
            normalized_english(item["correct"]),
            normalize_hebrew_key(item["token"]),
            item["record"]["ref"]["perek"],
            item["record"]["ref"]["pasuk"],
        )
    )
    return candidates


def select_translation_family(word_bank):
    selected = []
    used_meanings = set()
    used_tokens = set()
    divine_used = False
    used_pasuks = set()

    for candidate in translation_candidates(word_bank):
        if candidate["record"]["pasuk_id"] in used_pasuks:
            continue
        if candidate["meaning_key"] in used_meanings or candidate["token"] in used_tokens:
            continue
        if candidate["semantic_group"] == "divine" and divine_used:
            continue
        question = build_generated_question("translation", candidate["record"]["text"], target_token=candidate["token"])
        if not question or question.get("selected_word") != candidate["token"]:
            continue
        selected.append((question, "translation", []))
        used_meanings.add(candidate["meaning_key"])
        used_tokens.add(candidate["token"])
        used_pasuks.add(candidate["record"]["pasuk_id"])
        divine_used = divine_used or candidate["semantic_group"] == "divine"
        if len(selected) >= 10:
            break

    used_phrase_meanings = set()
    for candidate in phrase_candidates():
        question = candidate["question"]
        correct_key = candidate["correct_key"]
        if candidate["record"]["pasuk_id"] in used_pasuks:
            continue
        if correct_key in used_phrase_meanings:
            continue
        used_phrase_meanings.add(correct_key)
        used_pasuks.add(candidate["record"]["pasuk_id"])
        selected.append((question, "translation", []))
        if len(selected) >= TRANSLATION_TARGET_COUNT:
            break

    return selected


def select_shoresh_family(word_bank):
    selected = []
    root_counts = Counter()
    token_counts = Counter()
    used_pasuks = set()
    for candidate in manual_shoresh_candidates(word_bank):
        question = candidate["question"]
        root = candidate["root"]
        token = target_signature(question)
        root_key = candidate["root_key"]
        if candidate["record"]["pasuk_id"] in used_pasuks:
            continue
        if token_counts[token] >= DEFAULT_SHORESH_TOKEN_CAP:
            continue
        if root_counts[root_key] >= SHORESH_ROOT_CAPS.get(root_key, DEFAULT_SHORESH_ROOT_CAP):
            continue
        selected.append((question, "shoresh", []))
        used_pasuks.add(candidate["record"]["pasuk_id"])
        token_counts[token] += 1
        root_counts[root_key] += 1
        if len(selected) >= SHORESH_TARGET_COUNT:
            break
    return selected


def select_tense_family():
    selected = []
    token_counts = Counter()
    answer_counts = Counter()
    tense_code_counts = Counter()
    used_pasuks = set()
    for candidate in manual_tense_candidates():
        question = candidate["question"]
        token = target_signature(question)
        answer_key = normalized_english(question.get("correct_answer"))
        tense_code = str(question.get("tense_code") or "")
        if candidate["record"]["pasuk_id"] in used_pasuks:
            continue
        if token_counts[token] >= TENSE_TOKEN_CAPS.get(token, DEFAULT_TENSE_TOKEN_CAP):
            continue
        if tense_code and tense_code_counts[tense_code] >= TENSE_CODE_CAPS.get(tense_code, TENSE_TARGET_COUNT):
            continue
        if answer_key == "future" and answer_counts[answer_key] >= 10:
            continue
        selected.append((question, "tense", ["verb_tense"]))
        used_pasuks.add(candidate["record"]["pasuk_id"])
        token_counts[token] += 1
        answer_counts[answer_key] += 1
        if tense_code:
            tense_code_counts[tense_code] += 1
        if len(selected) >= TENSE_TARGET_COUNT:
            break
    return selected


def select_affix_family(word_bank):
    selected = []
    seen = set()

    for level, limit in ((1, 8), (2, 4), (3, 3)):
        taken = 0
        prefix_counts = Counter()
        for candidate in prefix_candidates(word_bank, level):
            token_key = (level, normalize_hebrew_key(candidate["token"]))
            if token_key in seen:
                continue
            if prefix_counts[candidate["prefix"]] >= 2:
                continue
            question = build_generated_question(
                "identify_prefix_meaning",
                candidate["record"]["text"],
                target_token=candidate["token"],
                prefix_level=level,
            )
            if not question or question.get("selected_word") != candidate["token"]:
                continue
            if int(question.get("prefix_level") or 1) != level:
                continue
            selected.append((question, "affix", []))
            seen.add(token_key)
            prefix_counts[candidate["prefix"]] += 1
            taken += 1
            if taken >= limit:
                break

    for skill, limit in (("identify_suffix_meaning", 5), ("identify_pronoun_suffix", 5)):
        taken = 0
        for candidate in suffix_candidates(skill):
            token_key = (skill, normalize_hebrew_key(candidate["token"]), normalized_english(candidate["correct"]))
            if token_key in seen:
                continue
            selected.append((candidate["question"], "affix", []))
            seen.add(token_key)
            taken += 1
            if taken >= limit:
                break

    return selected[:AFFIX_TARGET_COUNT]


def build_reviewed_items(*, baseline_lane_counts=None):
    word_bank, by_group = flow_builder.load_word_bank()
    questions = []
    lane_counts = Counter()
    skill_counts = Counter()
    seen_duplicate_keys = set()
    imported_promoted_seed_count = 0
    family_pasuks_with_single_slot = {"shoresh", "tense"}
    seen_single_slot_family_pasuks = set()

    def append_reviewed_item(item):
        family = item.get("review_family") or item.get("skill") or "unknown"
        pasuk_id = item.get("pasuk_id")
        skill = item.get("skill")
        duplicate_key = reviewed_bank_duplicate_key(item)
        family_pasuk_key = (family, pasuk_id)
        if gold_suppresses_reviewed_skill(pasuk_id, skill):
            return False
        if duplicate_key in seen_duplicate_keys:
            return False
        if family in family_pasuks_with_single_slot and family_pasuk_key in seen_single_slot_family_pasuks:
            return False
        questions.append(item)
        lane_counts[family] += 1
        skill_counts[item.get("skill") or "unknown"] += 1
        seen_duplicate_keys.add(duplicate_key)
        if family in family_pasuks_with_single_slot:
            seen_single_slot_family_pasuks.add(family_pasuk_key)
        return True

    for item in load_promoted_seed_questions():
        if append_reviewed_item(item):
            imported_promoted_seed_count += 1

    for question, family, alias_skills in build_gold_role_context_reviewed_items():
        record = active_pasuk_record_for_text(question.get("pasuk"))
        if not record:
            continue
        item = deepcopy(question)
        item.pop("id", None)
        item.pop("_debug_trace", None)
        item["reviewed_id"] = reviewed_id(
            family,
            str(item.get("skill") or ""),
            record.get("pasuk_id"),
            str(item.get("selected_word") or item.get("word") or item.get("correct_answer") or ""),
            question_type=str(item.get("question_type") or ""),
            correct_answer=str(item.get("correct_answer") or ""),
        )
        item["review_family"] = family
        item["alias_skills"] = list(alias_skills)
        item["pasuk_id"] = record.get("pasuk_id")
        item["pasuk_ref"] = active_pasuk_ref_payload(record)
        item["source"] = "active scope reviewed bank"
        item["analysis_source"] = "active_scope_reviewed_bank"
        append_reviewed_item(item)

    for question, family, alias_skills in build_reviewed_foundation_items(word_bank, by_group):
        record = active_pasuk_record_for_text(question.get("pasuk"))
        if not record:
            continue
        item = deepcopy(question)
        item.pop("id", None)
        item.pop("_debug_trace", None)
        item["reviewed_id"] = reviewed_id(
            family,
            str(item.get("skill") or ""),
            record.get("pasuk_id"),
            str(item.get("selected_word") or item.get("word") or item.get("correct_answer") or ""),
            question_type=str(item.get("question_type") or ""),
            correct_answer=str(item.get("correct_answer") or ""),
        )
        item["review_family"] = family
        item["alias_skills"] = list(alias_skills)
        item["pasuk_id"] = record.get("pasuk_id")
        item["pasuk_ref"] = active_pasuk_ref_payload(record)
        item["source"] = "active scope reviewed bank"
        item["analysis_source"] = "active_scope_reviewed_bank"
        append_reviewed_item(item)

    families = [
        *select_translation_family(word_bank),
        *select_shoresh_family(word_bank),
        *select_tense_family(),
        *select_affix_family(word_bank),
    ]

    for index, (question, family, alias_skills) in enumerate(families, start=1):
        record = active_pasuk_record_for_text(question.get("pasuk"))
        if not record:
            continue
        item = deepcopy(question)
        item.pop("id", None)
        item.pop("_debug_trace", None)
        item["reviewed_id"] = reviewed_id(
            family,
            str(item.get("skill") or ""),
            record.get("pasuk_id"),
            str(item.get("selected_word") or item.get("word") or item.get("correct_answer") or index),
            question_type=str(item.get("question_type") or ""),
            correct_answer=str(item.get("correct_answer") or ""),
        )
        item["review_family"] = family
        item["alias_skills"] = list(alias_skills)
        item["pasuk_id"] = record.get("pasuk_id")
        item["pasuk_ref"] = active_pasuk_ref_payload(record)
        item["source"] = "active scope reviewed bank"
        item["analysis_source"] = "active_scope_reviewed_bank"
        append_reviewed_item(item)

    payload = {
        "metadata": {
            "title": "Active Scope Reviewed Questions",
            "scope_id": ACTIVE_ASSESSMENT_SCOPE,
            "status": "active",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "notes": [
                "This file is a repo-curated reviewed question bank for the current active runtime scope.",
                "The runtime may prefer these questions over merely generated candidates when the requested lane matches.",
                "Alias skills are used only where student-facing lane content is intentionally shared, such as tense-family items.",
                "Imported promoted staged reviewed-support items are kept when they still validate inside the active runtime scope.",
            ],
            "backfill_baseline_lane_counts": dict(baseline_lane_counts or {}),
            "morphology_support_additions": list(REVIEWED_BACKFILL_MORPHOLOGY_SUPPORT_ADDITIONS),
            "imported_promoted_seed_count": imported_promoted_seed_count,
            "lane_counts": dict(lane_counts),
            "skill_counts": dict(skill_counts),
        },
        "questions": questions,
    }
    return payload


def validate_reviewed_bank(payload, *, baseline_lane_counts=None):
    issues = []
    lane_counts = Counter()
    skill_counts = Counter()
    duplicate_keys = Counter()
    reviewed_ids = Counter()
    target_duplicates = Counter()
    lane_targets = Counter()
    for item in payload.get("questions", []):
        family = item.get("review_family") or "unknown"
        lane_counts[family] += 1
        skill_counts[item.get("skill") or "unknown"] += 1
        reviewed_ids[item.get("reviewed_id") or ""] += 1
        duplicate_keys[
            (
                family,
                item.get("skill"),
                item.get("pasuk_id"),
                normalize_hebrew_key(item.get("selected_word") or item.get("word") or ""),
                normalized_english(item.get("correct_answer")),
            )
        ] += 1
        target_duplicates[(family, normalize_hebrew_key(item.get("selected_word") or item.get("word") or ""))] += 1
        lane_targets[family] += 1
        validation = validate_question_for_serve(
            deepcopy(item),
            fallback_text=item.get("pasuk"),
            validation_path="reviewed_bank_validation",
            trusted_active_scope=True,
        )
        if not validation["valid"]:
            issues.append(
                {
                    "reviewed_id": item.get("reviewed_id"),
                    "rejection_codes": list(validation.get("rejection_codes") or []),
                }
            )
    duplicate_items = [
        {"key": list(key), "count": count}
        for key, count in duplicate_keys.items()
        if count > 1
    ]
    duplicate_reviewed_ids = [
        {"reviewed_id": reviewed_id_value, "count": count}
        for reviewed_id_value, count in reviewed_ids.items()
        if reviewed_id_value and count > 1
    ]
    repeated_targets = [
        {"family": family, "target": target, "count": count}
        for (family, target), count in target_duplicates.items()
        if count > 1
    ]
    promoted_slice_questions = [
        item
        for item in payload.get("questions", [])
        if str(item.get("pasuk_id") or "").startswith("bereishis_3_")
    ]
    promoted_slice_lane_counts = Counter(
        item.get("review_family") or "unknown"
        for item in promoted_slice_questions
    )
    expected_targets = {
        "translation": TRANSLATION_TARGET_COUNT,
        "shoresh": SHORESH_TARGET_COUNT,
        "tense": TENSE_TARGET_COUNT,
        "affix": AFFIX_TARGET_COUNT,
    }
    shortfalls = {
        family: {
            "expected": expected,
            "actual": lane_counts.get(family, 0),
        }
        for family, expected in expected_targets.items()
        if lane_counts.get(family, 0) < expected
    }
    baseline = dict(
        baseline_lane_counts
        or payload.get("metadata", {}).get("backfill_baseline_lane_counts")
        or {}
    )
    lane_count_delta = {
        family: lane_counts.get(family, 0) - int(baseline.get(family, 0) or 0)
        for family in ("translation", "shoresh", "tense", "affix")
    }
    remaining_shortfall_reasons = {
        family: REMAINING_SHORTFALL_EXPLANATIONS.get(family, [])
        for family in shortfalls
    }
    return {
        "scope_id": payload.get("metadata", {}).get("scope_id"),
        "question_count": len(payload.get("questions", [])),
        "baseline_lane_counts": baseline,
        "lane_counts": dict(lane_counts),
        "lane_count_delta": lane_count_delta,
        "skill_counts": dict(skill_counts),
        "issues": issues,
        "duplicate_items": duplicate_items,
        "duplicate_reviewed_ids": duplicate_reviewed_ids,
        "repeated_targets": repeated_targets,
        "shortfalls": shortfalls,
        "remaining_shortfall_reasons": remaining_shortfall_reasons,
        "morphology_support_additions": list(
            payload.get("metadata", {}).get("morphology_support_additions")
            or REVIEWED_BACKFILL_MORPHOLOGY_SUPPORT_ADDITIONS
        ),
        "imported_promoted_seed_count": int(payload.get("metadata", {}).get("imported_promoted_seed_count") or 0),
        "promoted_slice_question_count": len(promoted_slice_questions),
        "promoted_slice_lane_counts": dict(promoted_slice_lane_counts),
        "valid": not issues and not duplicate_items and not duplicate_reviewed_ids,
    }


def main():
    parser = argparse.ArgumentParser(description="Build and validate the active-scope reviewed question bank.")
    parser.add_argument("--validate-only", action="store_true", help="Validate the existing bank instead of rebuilding it.")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Reviewed-bank JSON output path.")
    parser.add_argument("--summary-output", default=str(SUMMARY_PATH), help="Validation summary JSON output path.")
    args = parser.parse_args()

    output_path = Path(args.output)
    summary_path = Path(args.summary_output)

    existing_payload = None
    baseline_lane_counts = {}
    if output_path.exists():
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
        baseline_lane_counts = dict(
            existing_payload.get("metadata", {}).get("backfill_baseline_lane_counts")
            or lane_counts_from_payload(existing_payload)
        )

    if args.validate_only:
        payload = existing_payload or json.loads(output_path.read_text(encoding="utf-8"))
    else:
        payload = build_reviewed_items(baseline_lane_counts=baseline_lane_counts)
        write_json(output_path, payload)

    summary = validate_reviewed_bank(payload, baseline_lane_counts=baseline_lane_counts)
    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
