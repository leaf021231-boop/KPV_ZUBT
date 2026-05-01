# finedata.py —— Fine Mode modifier helper

TIMESTAMP_PRESETS = {
    "year": {
        "label": "每年",
        "tick_label": "年",
        "age_step": 1,
    },
    "half_year": {
        "label": "每半年",
        "tick_label": "半年",
        "age_step": 0.5,
    },
    "month": {
        "label": "每月",
        "tick_label": "月",
        "age_step": 1 / 12,
    },
    "weekly": {               # <--- 新增这段
        "label": "每周",
        "tick_label": "周",
        "age_step": 1 / 52,
    },
}


def is_enabled(c):
    return bool(c.get("fine_enabled"))


def normalize_settings(settings):
    """
    Returns a safe Fine Mode settings dict.
    """
    settings = settings or {}

    start_age = float(settings.get("start_age", 0))
    end_age = float(settings.get("end_age", 80))
    timestamp = settings.get("timestamp", "year")

    if timestamp not in TIMESTAMP_PRESETS:
        timestamp = "year"

    if start_age < 0:
        start_age = 0

    if end_age <= start_age:
        end_age = start_age + 1

    preset = TIMESTAMP_PRESETS[timestamp]

    return {
        "enabled": True,
        "start_age": start_age,
        "end_age": end_age,
        "timestamp": timestamp,
        "timestamp_label": preset["label"],
        "tick_label": preset["tick_label"],
        "age_step": preset["age_step"],
    }


def configure_character(c, settings):
    """
    Applies Fine Mode settings onto character.
    main.py should call this after the user confirms identity settings.
    """
    s = normalize_settings(settings)

    c["fine_enabled"] = True
    c["fine_settings"] = s

    # This is the clean bridge into data.py / hornidata.py time functions.
    c["time_config_override"] = {
        "start_tick": 0,
        "start_age": s["start_age"],
        "tick_step": 1,
        "age_step": s["age_step"],
        "tick_label": s["tick_label"],
        "age_label": "岁",
    }


def clear_character(c):
    c["fine_enabled"] = False
    c["fine_settings"] = {}
    c["time_config_override"] = {}
    c["initial_trackers"] = {}


def build_prompt_block(c):
    """
    Extra system prompt text appended to the current content mode prompt.
    """
    if not is_enabled(c):
        return ""

    s = c.get("fine_settings", {})

    return f"""

【Fine Mode / 细节时间模式】
本局启用了自定义时间轴。
- 角色不是必须从 0 岁出生逐年开始。
- 开局年龄：{s.get("start_age")} 岁。
- 终止年龄：{s.get("end_age")} 岁。
- 每次玩家点击“下一时间点”，时间推进：{s.get("timestamp_label")}。
- 如果开局年龄大于 0，请把开局前的人生经历视为已经发生过的背景。
- 不要把角色写成刚出生，除非开局年龄就是 0。
- 请根据当前年龄描写符合年龄阶段的生活处境、社会身份、身体状态、家庭状态与人生压力。
"""


def build_initial_user_prompt(c):
    """
    Replaces the default birth prompt when Fine Mode starts above age 0.
    """
    if not is_enabled(c):
        return None

    s = c.get("fine_settings", {})
    start_age = float(s.get("start_age", 0))

    if start_age <= 0:
        return None

    return (
        f"角色当前开局年龄为 {start_age:g} 岁。"
        f"请不要描写出生，而是概述角色从出生到现在的关键经历，"
        f"并描写当前这个时间点的人生起点。"
        f"本次必须 has_choice=false, alive=true。"
        f"adjustments 可以为空；如确实需要，只允许使用 HP / ASSET / FAME / KNOWLEDGE / EDU。"
    )


def reached_end_age(c, data_module):
    if not is_enabled(c):
        return False

    s = c.get("fine_settings", {})
    end_age = float(s.get("end_age", 80))

    try:
        age = float(data_module.get_character_age(c))
    except Exception:
        return False

    return age >= end_age


def apply_starting_experience(c):
    """
    Optional deterministic baseline boost for years lived before game start.

    This should affect derived trackers, not locked base attributes.
    Returns log strings.
    """
    if not is_enabled(c):
        return []

    if c.get("_fine_starting_experience_applied"):
        return []

    s = c.get("fine_settings", {})
    start_age = int(float(s.get("start_age", 0)))

    if start_age <= 0:
        c["_fine_starting_experience_applied"] = True
        return []

    logs = []

    # Baseline education before start.
    # If the world has compulsory education, simulate normal schooling from 1 to 18.
    if c.get("has_compulsory_edu"):
        edu_gain = min(start_age, 18)
        if edu_gain > 0:
            c["edu"] = c.get("edu", 0) + edu_gain
            logs.append(f"开局前受教育 +{edu_gain}")
    else:
        # In non-modern worlds, do not force EDU too much.
        edu_gain = min(start_age // 4, 6)
        if edu_gain > 0:
            c["edu"] = c.get("edu", 0) + edu_gain
            logs.append(f"开局前历练/开蒙 +{edu_gain}")

    # General life knowledge.
    knowledge_gain = max(0, start_age // 5)
    if knowledge_gain:
        c["knowledge"] = c.get("knowledge", 0) + knowledge_gain
        logs.append(f"开局前知识 +{knowledge_gain}")

    # Adult years may accumulate some assets, but very slowly.
    adult_years = max(0, start_age - 18)
    asset_gain = adult_years // 5
    if asset_gain:
        c["assets"] = c.get("assets", 0) + asset_gain
        logs.append(f"开局前资产 +{asset_gain}")

    c["_fine_starting_experience_applied"] = True
    return logs