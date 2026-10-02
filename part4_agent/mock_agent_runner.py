import csv
import json
import sys
from pathlib import Path

# Import Part 2 functions without modifying them
PART2_DIR = Path(__file__).resolve().parent.parent / "part2_engine"
sys.path.insert(0, str(PART2_DIR))

from growth_engine import validate_feed, mom_growth, is_flagged


BASE_DIR = Path(__file__).resolve().parent.parent
FEED_PATH = BASE_DIR / "part2_engine" / "fixtures" / "monthly_category_revenue.csv"
PROMPT_PATH = BASE_DIR / "part3_narrative" / "prompt_pack.md"


def load_feed(csv_path):
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_month_order(month):
    order = {
        "April": 1,
        "May": 2,
        "June": 3
    }
    return order[month]


def previous_month(month):
    order = {
        "May": "April",
        "June": "May"
    }

    if month not in order:
        raise ValueError("Only May and June are supported for this capstone run.")

    return order[month]


def load_prompt_pack():
    return PROMPT_PATH.read_text(encoding="utf-8")


def fill_narrative(
    prompt_pack,
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    month,
    prev_month
):
    required_placeholders = [
        "{category}",
        "{previous_revenue}",
        "{current_revenue}",
        "{mom_pct}",
        "{month}",
        "{prev_month}",
    ]

    for placeholder in required_placeholders:
        if placeholder not in prompt_pack:
            raise ValueError(
                f"Missing required placeholder in prompt_pack.md: {placeholder}"
            )

    filled = (
        prompt_pack
        .replace("{category}", category)
        .replace("{previous_revenue}", f"{previous_revenue:.2f}")
        .replace("{current_revenue}", f"{current_revenue:.2f}")
        .replace("{mom_pct}", f"{mom_pct:.2f}")
        .replace("{month}", month)
        .replace("{prev_month}", prev_month)
    )

    # Deterministic offline narrative based only on verified inputs.
    if mom_pct > 0:
        implication = (
            "**HYPOTHESIS:** The increase may be related to changes in customer "
            "demand, promotional activity, or seasonal purchasing patterns. "
            "The category manager should review available business data to "
            "identify the verified cause and decide whether the growth should "
            "be sustained."
        )
    else:
        implication = (
            "**HYPOTHESIS:** The decrease may be related to changes in customer "
            "demand, promotional activity, or product availability. "
            "The category manager should review available business data to "
            "identify the verified cause and determine an appropriate follow-up action."
        )

    return (
        f"### Context\n"
        f"{category} revenue changed from INR {previous_revenue:.2f} "
        f"in {prev_month} to INR {current_revenue:.2f} in {month}.\n\n"
        f"### Insight\n"
        f"**FACT:** {category} recorded a Month-over-Month growth of "
        f"**{mom_pct:.2f}%** from {prev_month} to {month}.\n\n"
        f"### Implication\n"
        f"{implication}"
    )


def run_agent(run_month):
    # 1. Load feed
    rows = load_feed(FEED_PATH)

    # 2. Validate feed
    valid, errors = validate_feed(str(FEED_PATH))

    # 3. Hard stop if invalid
    if not valid:
        return {
            "run_month": run_month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    prev = previous_month(run_month)

    current_rows = {
        row["category"]: row
        for row in rows
        if row["month"] == run_month
    }

    previous_rows = {
        row["category"]: row
        for row in rows
        if row["month"] == prev
    }

    prompt_pack = load_prompt_pack()

    flagged = []
    escalated = []

    # 4, 5. Calculate MoM and flag every category
    for category in current_rows:
        current_revenue = float(current_rows[category]["revenue"])
        previous_revenue_value = float(previous_rows[category]["revenue"])

        mom_pct = mom_growth(previous_revenue_value, current_revenue)
        status = is_flagged(mom_pct)

        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue_value,
            "current_revenue": current_revenue,
        }

        if status == "flagged":
            flagged.append(item)

        elif status == "escalate_exact_boundary":
            escalated.append(item)

    # 6. Sort flagged categories by absolute MoM magnitude
    flagged.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # 6b. Draft only top 3
    top_three = flagged[:3]
    remaining = flagged[3:]

    flagged_output = []

    for item in top_three:
        message = fill_narrative(
            prompt_pack,
            item["category"],
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
            run_month,
            prev,
        )

        flagged_output.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": message,
        })

    # 7. Suppress remaining flagged categories
    suppressed_output = []

    for item in remaining:
        suppressed_output.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "status": "suppressed, review manually",
        })

    # 7b. Exact-boundary categories stay separate
    escalated_output = []

    for item in escalated:
        escalated_output.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "status": "escalate_exact_boundary",
        })

    # 8. Emit one structured JSON object
    result = {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output,
        "suppressed_categories": suppressed_output,
        "escalated_categories": escalated_output,
        "action_taken": "drafted_for_human_approval",
    }

    return result


if __name__ == "__main__":
    month = "May"

    if len(sys.argv) > 1:
        month = sys.argv[1]

    result = run_agent(month)

    print(json.dumps(result, indent=2))