"""Local translation review helpers.

No scraping, browser automation, or network access belongs here.
"""

import json
from pathlib import Path


APPROVED_STATUS = "approved"
APPROVED_STATUSES = {APPROVED_STATUS, "starter_approved"}


def load_translation_reviews(path="data/translation_reviews.json"):
    review_path = Path(path)
    if not review_path.exists():
        return []
    data = json.loads(review_path.read_text(encoding="utf-8"))
    return data.get("reviews", [])


def review_key(review):
    return (
        review.get("pasuk_id"),
        review.get("token_index"),
        review.get("surface"),
    )


def build_review_index(reviews):
    return {review_key(review): review for review in reviews}


def choose_context_translation(proposed_context, review=None):
    if (
        review
        and review.get("review_status") in APPROVED_STATUSES
        and review.get("approved_context")
    ):
        return review["approved_context"]
    return proposed_context


def find_review_for_analysis(analysis, reviews):
    surface = analysis.get("surface") or analysis.get("word")
    source_refs = set(analysis.get("source_refs") or [])

    for review in reviews:
        if review.get("surface") != surface:
            continue
        if source_refs and review.get("pasuk_id") not in source_refs:
            continue
        return review

    for review in reviews:
        if review.get("surface") == surface:
            return review

    return None


def apply_review(analysis, review):
    updated = dict(analysis)
    proposed_context = (
        updated.get("translation_context")
        or updated.get("context_translation")
        or updated.get("translation")
    )
    context = choose_context_translation(proposed_context, review)
    if context:
        updated["translation_context"] = context
        updated["context_translation"] = context
    if review:
        updated["review_status"] = review.get("review_status")
        updated["authority_source"] = review.get("authority_source")
    return updated
