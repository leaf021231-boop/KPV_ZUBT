# storedata.py —— 通马桶模拟器
# 玩家扮演接三教九流委托的"神秘 NPC"。
# 客户与委托数据由程序持有；AI 只负责讲故事 + 标注鉴定属性/难度。
# 鉴定（1d100 vs 属性）由程序投，结果反馈给 AI 写叙事。

import os
import json
import uuid
import random

import data as base
from data import (
    SCENES, GENDERS,
    RARITY_CONFIG, RARITY_WEIGHTS,
    roll_dice, filter_pool, draw_talents,
    parse_ai_json,
    ASSET_TIERS as BASE_ASSET_TIERS,
    get_tier,
    perform_skill_check, apply_skill_check_growth,
    resolve_multi_check, format_check_log,
)


# ============================================================
# 模式标识
# ============================================================

MODE_ID = "store"
MODE_LABEL = "通马桶模拟器"
MODE_DESCRIPTION = "扮演游戏里面的神秘NPC！由你接下三教九流的委托。"
TALENT_MODE_TAG = "Store"


# ============================================================
# 6 个属性
# ============================================================

ATTRIBUTES = ["STR", "CRE", "HMR", "INT", "APP", "END"]

ATTR_DESC = {
    "STR": "武力",
    "CRE": "资金",
    "HMR": "人脉",
    "INT": "经验",
    "APP": "亲和",
    "END": "精力",
}

ATTR_LONG_DESC = {
    "STR": "武力值。拳头是一个好东西，稳定，可信赖，能解决大部分的麻烦。",
    "CRE": "资金值。只要有足够的金钱，几乎没有什么是买不到的。",
    "HMR": "人脉值。金钱买不到的东西，说不定缺的是和对的人的那杯咖啡。",
    "INT": "经验值。你需要足够的经验才能八面玲珑、不留尾巴。",
    "APP": "亲和力。有时一个温暖的微笑价值千金。",
    "END": "精力值。一个成功的行动不仅需要能力，还需要充沛的精力坚持到底。",
}

# 6 个属性，每项基础 30，初始池 150 → 平均 +25/属性
POINTS_POOL_DEFAULT = 150
POINTS_POOL_INTENSE = 200  # 兼容字段，目前不使用


# ============================================================
# 派生数值的等级
# ============================================================

# ============================================================
# 派生数值的等级 (基于 D100 系统，平均起点为 50)
# ============================================================

# 神秘度：低=人尽皆知，高=见首不见尾 (公式计算范围通常在 25~75)
MYSTERY_TIERS = [
    (20, "人尽皆知"), (40, "众所周知"), (60, "略有耳闻"),
    (80, "神秘莫测"), (100, "见首不见尾"), (float("inf"), "传说不存在"),
]

# 名声：低=残忍邪恶，高=仁义无双 (起点 50+)
REPUTATION_TIERS = [
    (20, "残忍邪恶"), (40, "不择手段"), (60, "亦正亦邪"),
    (80, "古道热肠"), (100, "除魔卫道"), (float("inf"), "仁义无双"),
]

# 操守：低=背信弃义，高=一诺千金 (起点 50+)
INTEGRITY_TIERS = [
    (20, "背信弃义"), (40, "见利忘义"), (60, "为人圆滑"),
    (80, "言而有信"), (100, "重信守诺"), (float("inf"), "千金一诺"),
]


# ============================================================
# TRACKERS（GamePage 右侧面板用）
# ============================================================

TRACKERS = {
    "assets": {
        "label": "家底",
        "adjustment_key": "ASSET",
        "initial": 0,
        "tiers": BASE_ASSET_TIERS,
    },
    "mystery": {
        "label": "神秘度",
        "adjustment_key": "MYSTERY",
        "initial": 10,
        "tiers": MYSTERY_TIERS,
    },
    "reputation": {
        "label": "名声",
        "adjustment_key": "REPUTATION",
        "initial": 0,
        "tiers": REPUTATION_TIERS,
    },
    "integrity": {
        "label": "操守",
        "adjustment_key": "INTEGRITY",
        "initial": 0,
        "tiers": INTEGRITY_TIERS,
    },
    "heat": {
        "label": "风波",
        "adjustment_key": "HEAT",
        "initial": 0,
        "tiers": None,        # 直接显示 0~10
        "min": 0,
        "max": 10,
    },
}

PRIORITY_CLIENTS_MAX = 5
COMMISSION_AUTO_ABANDON_DELAYS = 3


# ============================================================
# 店主原型
# ============================================================

KEEPER_ARCHETYPES = [
    {"id": "detective",     "name": "私家侦探",
     "desc": "暗巷与窗台是你的办公室，烟雾缭绕里你能看清人心。"},
    {"id": "info_broker",   "name": "情报贩子",
     "desc": "你不卖货物，只卖秘密。一句话千两金，一个名字十条命。"},
    {"id": "occultist",     "name": "游方术士",
     "desc": "你借符箓与卦象之名而活。是真灵验还是装神弄鬼，没人说得清。"},
    {"id": "monster_hunter","name": "猎魔人",
     "desc": "村民锁紧门窗的夜里，你是他们最后的希望。"},
    {"id": "fixer",         "name": "黑市掮客",
     "desc": "你能搞到一切——只要价钱合适，问题别问。"},
    {"id": "doctor",        "name": "黑医",
     "desc": "正派大夫不愿沾的病人都来你这。"},
    {"id": "custom",        "name": "自定义",
     "desc": "你是其他什么角色——必须自己填写描述。"},
]


def get_keeper_archetype_by_id(aid):
    for a in KEEPER_ARCHETYPES:
        if a["id"] == aid:
            return a
    return None


# ============================================================
# 时间：1 旬 = 15 天
# ============================================================

TIME_CONFIG = {
    "tick_key": "time_tick",
    "age_key": "age_value",
    "tick_label": "旬",
    "age_label": "天",
    "start_tick": 0,
    "start_age": 0,
    "tick_step": 1,
    "age_step": 15,
}


def get_time_config(c):
    cfg = dict(TIME_CONFIG)
    cfg.update(c.get("time_config_override") or {})
    return cfg


def init_time_state(c):
    cfg = get_time_config(c)
    c[cfg["tick_key"]] = cfg["start_tick"]
    c[cfg["age_key"]] = cfg["start_age"]


def advance_time(c):
    cfg = get_time_config(c)
    c[cfg["tick_key"]] = c.get(cfg["tick_key"], cfg["start_tick"]) + cfg["tick_step"]
    c[cfg["age_key"]] = c.get(cfg["age_key"], cfg["start_age"]) + cfg["age_step"]


def get_character_age(c):
    cfg = get_time_config(c)
    return c.get(cfg["age_key"], cfg["start_age"])


def get_time_tick(c):
    cfg = get_time_config(c)
    return c.get(cfg["tick_key"], cfg["start_tick"])


def _fmt(x):
    try:
        return str(int(x)) if float(x).is_integer() else f"{float(x):.2f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def format_time(c):
    return f"开张第 {_fmt(get_time_tick(c))} 旬 · 第 {_fmt(get_character_age(c))} 天"


def format_history_header(c):
    return f"开张第 {_fmt(get_time_tick(c))}旬（第 {_fmt(get_character_age(c))} 天）"


# ============================================================
# 状态初始化与 HP
# ============================================================

def init_trackers(c):
    for key, cfg in TRACKERS.items():
        c[key] = cfg.get("initial", 0)
    init_store_state(c)


def init_store_state(c):
    """通马桶模拟器特有的角色状态。"""
    c.setdefault("store_clients", {})         # client_id -> client dict
    c.setdefault("store_commissions", {})     # commission_id -> commission dict
    c.setdefault("store_priority_ids", [])    # 重点关注的 client_id 列表
    c.setdefault("store_blacklist_ids", [])   # 拉黑的 client_id 列表
    c.setdefault("store_round", 0)            # 0=未开始 1=R1已演 2=R2已演 3=R3已演 4+=正常
    c.setdefault("store_keeper_type", "")
    c.setdefault("store_keeper_type_label", "")
    c.setdefault("store_keeper_backstory", "")


def calculate_max_hp(final_attributes):
    return max(1, (final_attributes.get("END", 50) + final_attributes.get("STR", 50)) // 10)


def apply_turn_start_effects(c):
    logs = []
    if c.get("hp", 0) < c.get("max_hp", 0):
        old = c["hp"]
        c["hp"] = min(c["max_hp"], c["hp"] + 1)
        if c["hp"] != old:
            logs.append(f"❤️HP +{c['hp'] - old}")

    # 自动放弃过期委托
    expired = auto_abandon_expired_commissions(c)
    for com in expired:
        client_name = "未知"
        if com.get("client_id") and com["client_id"] in c["store_clients"]:
            client_name = c["store_clients"][com["client_id"]].get("name", "未知")
        logs.append(f"⌛ 委托过期：{client_name} 的「{com.get('summary','?')}」自动放弃")

    return logs


def apply_tracker_adjustment(c, adjustment_key, value):
    value = int(value)
    for tracker_key, cfg in TRACKERS.items():
        if cfg.get("adjustment_key") != adjustment_key:
            continue
        old = c.get(tracker_key, 0)
        new = old + value
        if cfg.get("min") is not None:
            new = max(cfg["min"], new)
        if cfg.get("max") is not None:
            new = min(cfg["max"], new)
        actual = new - old
        if actual == 0:
            return None
        c[tracker_key] = new
        return f"{cfg['label']} {actual:+d}"
    return None


# ============================================================
# 客户 / 委托 数据操作
# ============================================================

def add_client(c, client_data):
    cid = client_data.get("id") or str(uuid.uuid4())[:8]
    client_data["id"] = cid
    client_data.setdefault("notes", "")
    client_data.setdefault("relationship", "中立")
    client_data.setdefault("created_tick", get_time_tick(c))
    client_data.setdefault("last_seen_tick", get_time_tick(c))
    c["store_clients"][cid] = client_data
    return cid


def add_commission(c, commission_data, client_id=None):
    com_id = commission_data.get("id") or str(uuid.uuid4())[:8]
    commission_data["id"] = com_id
    commission_data["client_id"] = client_id
    commission_data.setdefault("status", "open")     # open/resolved/failed/abandoned
    commission_data.setdefault("created_tick", get_time_tick(c))
    commission_data.setdefault("last_action_tick", get_time_tick(c))
    commission_data.setdefault("delays_used", 0)
    commission_data.setdefault("pending_advantage", False)  # 上一次延期客户答应了
    c["store_commissions"][com_id] = commission_data
    return com_id


def get_open_commissions(c):
    return [com for com in c.get("store_commissions", {}).values()
            if com.get("status") == "open"]


def get_active_clients(c):
    """非黑名单客户。"""
    bl = set(c.get("store_blacklist_ids", []))
    return [cl for cl in c.get("store_clients", {}).values()
            if cl.get("id") not in bl]


def is_priority(c, client_id):
    return client_id in c.get("store_priority_ids", [])


def toggle_priority(c, client_id):
    """返回新的状态。受 PRIORITY_CLIENTS_MAX 上限约束。"""
    pri = c.setdefault("store_priority_ids", [])
    if client_id in pri:
        pri.remove(client_id)
        return False
    if len(pri) >= PRIORITY_CLIENTS_MAX:
        return None  # 满了
    pri.append(client_id)
    return True


def toggle_blacklist(c, client_id):
    bl = c.setdefault("store_blacklist_ids", [])
    if client_id in bl:
        bl.remove(client_id)
        return False
    bl.append(client_id)
    # 拉黑同时取消重点关注
    pri = c.setdefault("store_priority_ids", [])
    if client_id in pri:
        pri.remove(client_id)
    return True


def auto_abandon_expired_commissions(c, max_delay=COMMISSION_AUTO_ABANDON_DELAYS):
    abandoned = []
    for com in c.get("store_commissions", {}).values():
        if com.get("status") != "open":
            continue
        if com.get("delays_used", 0) >= max_delay:
            com["status"] = "abandoned"
            com["resolution"] = "委托过期，自动放弃"
            abandoned.append(com)
    return abandoned


# ============================================================
# 事件类型抽取
# ============================================================

def roll_event_kind(c):
    """
    在"今旬有事发生"这个前提下，决定事件类型。
    返回 'k' / 'n' / 'l' 之一。
    """
    heat = c.get("heat", 0)
    p_k = min(0.06 * heat, 0.6)
    remaining = 1.0 - p_k

    x = len(get_active_clients(c))
    new_appetite = max(0.3, 0.9 - 0.03 * x)

    p_n = new_appetite * remaining
    p_l = (1.0 - new_appetite) * remaining

    # 没有老客户时，把 P(l) 全部转给 P(n)
    if x == 0:
        p_n += p_l
        p_l = 0.0

    r = random.random()
    if r < p_k:
        return "k"
    if r < p_k + p_n:
        return "n"
    return "l"


def pick_old_client_for_visit(c):
    """50% 从重点关注池，50% 从普通池。任一池为空时退化为另一池。"""
    active = get_active_clients(c)
    if not active:
        return None

    pri_ids = set(c.get("store_priority_ids", []))
    pool_a = [cl for cl in active if cl.get("id") in pri_ids]
    pool_b = [cl for cl in active if cl.get("id") not in pri_ids]

    if pool_a and pool_b:
        return random.choice(pool_a if random.random() < 0.5 else pool_b)
    if pool_a:
        return random.choice(pool_a)
    if pool_b:
        return random.choice(pool_b)
    return None


# ============================================================
# 鉴定系统（程序投骰，不交给 AI）
# ============================================================

# ============================================================
# 提示词构建
# ============================================================

def _talents_block(c):
    return "\n".join(
        f"  - 【{RARITY_CONFIG.get(t.get('rarity','common'),{}).get('label','')}】"
        f"{t['name']}：{t.get('narrative', t.get('desc',''))}"
        for t in c["talents"]
    ) or "  （无）"


def _reputation_block(c):
    parts = []
    for tk in ("mystery", "reputation", "integrity"):
        cfg = TRACKERS[tk]
        val = c.get(tk, cfg["initial"])
        parts.append(f"  - {cfg['label']}：{get_tier(val, cfg['tiers'])} ({val})")
    parts.append(f"  - 风波：{c.get('heat', 0)} / 10")
    return "\n".join(parts)


def _open_commissions_block(c):
    open_coms = get_open_commissions(c)
    if not open_coms:
        return "  （目前没有进行中的委托）"
    out = []
    for com in open_coms:
        cid = com.get("client_id")
        cname = c.get("store_clients", {}).get(cid, {}).get("name", "未知")
        adv = "（享有优势骰）" if com.get("pending_advantage") else ""
        out.append(f"  - 委托 {com['id']} | 来自 {cname} | "
                   f"内容：{com.get('summary','?')} | 拖延 {com.get('delays_used',0)}/{COMMISSION_AUTO_ABANDON_DELAYS}{adv}")
    return "\n".join(out)


def _recent_resolved_block(c):
    coms = [com for com in c.get("store_commissions", {}).values()
            if com.get("status") in ("resolved", "failed", "abandoned")]
    coms.sort(key=lambda x: x.get("created_tick", 0), reverse=True)
    if not coms:
        return "  （还没结过案）"
    out = []
    for com in coms[:5]:
        cid = com.get("client_id")
        cname = c.get("store_clients", {}).get(cid, {}).get("name", "未知")
        out.append(f"  - {com.get('summary','?')}（{cname}）→ "
                   f"{com.get('status')}：{com.get('resolution','')}")
    return "\n".join(out)


def _client_roster_block(c, max_show=10):
    clients = get_active_clients(c)
    if not clients:
        return "  （还没有客户）"
    pri = set(c.get("store_priority_ids", []))
    out = []
    for cl in clients[:max_show]:
        tag = "⭐" if cl["id"] in pri else "  "
        out.append(f"  {tag} [{cl['id']}] {cl.get('name','?')} - "
                   f"{cl.get('archetype','')} - {cl.get('relationship','中立')}")
    if len(clients) > max_show:
        out.append(f"  …还有 {len(clients) - max_show} 位")
    return "\n".join(out)


def build_system_prompt(c):
    attrs = c["final_attributes"]
    attr_text = "  ".join(f"{k}={v}" for k, v in attrs.items())
    extra = f"\n额外设定：{c['extra_info']}" if c.get("extra_info") else ""
    backstory = (c.get("store_keeper_backstory") or c.get("backstory") or "").strip()
    backstory_block = f"\n背景故事：{backstory}" if backstory else "\n背景故事：（玩家未填）"
    keeper_type = (c.get("store_keeper_type_label") or c.get("store_keeper_type") or "").strip()
    keeper_block = f"\n店主原型：{keeper_type}" if keeper_type else ""
    max_hp = calculate_max_hp(attrs)

    return f"""你是「通马桶模拟器」的叙事 AI。
玩家扮演一个三教九流间替人办事的"神秘 NPC"——可能是侦探、情报贩子、游方术士、猎魔人、黑医、黑市掮客。

【世界设定】
{c['scene_name']}：{c['scene_desc']}

【店主基本信息】
性别：{c['gender']}　种族：{c['race']}{keeper_block}{extra}{backstory_block}

【当前属性（出生时已锁定，由系统在鉴定成功时 +1d6，**你不要写进 adjustments**）】
{attr_text}
最大生命/精力 HP_MAX = (END + STR) // 10 = {max_hp}

【天赋】
{_talents_block(c)}

【🎲 鉴定系统（核心机制）】
本模式由程序投 1d100 vs 属性来决定成败，**你不再决定胜负**。
- 你给出的每个选项必须包含两个字段：checks（1-2 个属性键）和 difficulty。
- 难度对应的程序行为：
    * "easy"   = 双骰取优（更容易过）
    * "normal" = 单骰（标准）
    * "hard"   = 双骰取劣（极难，**只用在真正棘手的情境**）
- 鉴定本身已经代表"有一定难度的事"，所以 hard 必须节制使用。
- 程序投完之后会回传「完胜/险胜/完败」，你**只负责按这个结果写故事**。
- 不要在叙事里让玩家自动成功；一切胜负由骰子决定。

【📋 委托与客户（程序持有，不要乱编）】
- 客户名册和委托清单**由程序保存**。
- 当系统让你引入新客户时，按 store_event.kind="new_client" 输出。
- 当系统指定老客户回访时，会在 user 消息里给出客户信息，按 kind="old_client"。
- 当系统触发风波事件时，按 kind="trouble"。
- 当系统说"无事"时，按 kind="quiet"，简短描写日常。
- 不要凭空虚构名册以外的客户也不要假装某个委托还在进行。

【📦 委托状态】
- open / resolved / failed / abandoned。
- 玩家可以在客户答应的前提下"拖延"委托获得下一次的优势骰，3 次之后系统强制 abandoned。
- 玩家可主动放弃委托。

【🌡️ 风波 HEAT（0-10）】
- 办事不干净 / 露出马脚 / 留活口都会让 HEAT 上升。
- HEAT 越高越容易被盯上（受害者家属、同行、官府）。
- 由 adjustments.HEAT 调节。

【🎭 名声 / 神秘度 / 操守】
- 神秘度 MYSTERY：低=人尽皆知，高=见首不见尾。低调办事 ↑，张扬办事 ↓。
- 名声 REPUTATION：低=残忍邪恶，高=仁义无双。
- 操守 INTEGRITY：低=背信弃义，高=一诺千金。
- 都用 adjustments 中的整数 ±。

【❤️ HP】
- HP_MAX = (END + STR) // 10。
- 每旬自动 +1。
- HP ≤ 0 即死亡。死亡只发生于剧情，不会因衰老死。

【⛔ 规则】
- adjustments **不能**包含 STR/CRE/HMR/INT/APP/END，这些只能由鉴定成功的 +1d6 触发。
- adjustments **可以**包含：HP / ASSET / MYSTERY / REPUTATION / INTEGRITY / HEAT。

【📖 进行中的委托】
{_open_commissions_block(c)}

【📚 最近结案的委托】
{_recent_resolved_block(c)}

【👥 当前客户名册】（共 {len(get_active_clients(c))} 人，最多展示 10）
{_client_roster_block(c)}

【🎭 当前店主声誉】
{_reputation_block(c)}

【输出格式】（严格 JSON，只输出 JSON）
通用骨架：
{{
  "narrative": "本时间点的叙事（一句话到 400 字）",
  "has_choice": true,
  "choices": {{
    "A": {{"text": "选项A描述", "checks": ["STR"], "difficulty": "normal"}},
    "B": {{"text": "选项B描述", "checks": ["CRE"], "difficulty": "easy"}},
    "C": {{"text": "选项C描述", "checks": ["INT","APP"], "difficulty": "hard"}}
  }},
  "adjustments": {{"HP": 0, "ASSET": 0, "MYSTERY": 0, "REPUTATION": 0, "INTEGRITY": 0, "HEAT": 0}},
  "alive": true,
  "cause_of_death": null,
  "store_event": {{"kind": "none"}}
}}

store_event 的可选形态：

· new_client（系统要求引入新客户时）：
{{
  "kind": "new_client",
  "client": {{
    "name": "...", "archetype": "...", "first_impression": "...",
    "danger": 1, "appearance": "..."
  }},
  "task": {{
    "summary": "一句话标题", "details": "...",
    "reward": "...", "danger": 1
  }}
}}

· old_client（系统已经告诉你具体客户）：
{{
  "kind": "old_client",
  "client_id": "（系统给的，原样回填）",
  "follow_up_kind": "thanks | grudge | new_request | unfinished_business",
  "task": {{ ... 仅在 new_request / unfinished_business 时填 ... }}
}}

· trouble（HEAT 触发的麻烦）：
{{
  "kind": "trouble",
  "trouble_type": "...",
  "summary": "..."
}}

· resolution（玩家行动结束后判定结果）：
{{
  "kind": "resolution",
  "commission_id": "（如果是结案，填委托ID）",
  "outcome": "resolved | failed | partial | ongoing",
  "client_relationship_after": "感激 | 敌视 | 死亡 | 失联 | 中立"
}}

· quiet / none：
{{ "kind": "quiet" }} 或 {{ "kind": "none" }}
"""


# ============================================================
# 各种事件的 user 消息构建
# ============================================================

def build_intro_round_prompt(c):
    """R1：根据玩家自填的店主类型 + 背景，渲染开场。"""
    return f"""第 1 旬开场：请基于玩家提供的设定写一段开场旁白（150~300字）。

玩家选择的店主原型：{c.get('store_keeper_type_label') or c.get('store_keeper_type') or '未指定'}
玩家提供的店主背景：{c.get('store_keeper_backstory','（玩家没填）')}

要求：
- 仅基于以上设定渲染当前店铺、地点、生活状态。
- **不要**引入客户，**不要**触发委托。
- has_choice = false。
- store_event.kind = "none"。
- adjustments 全 0。
- alive = true。
"""


def build_first_client_prompt(c):
    """R2：强制引入第一个客户，且必须是简单到接近滑稽的小事。"""
    return f"""第 2 旬：请引入店主开张以来的**第一位客户**。

要求：
- 这必须是一件**简单到接近滑稽**的小事（字面意义的通马桶、找猫、修门、找钥匙），符合店主原型的方向但不要太严肃。
- choices 必须是 3 个，每个的 difficulty 只能是 "easy" 或 "normal"，**不允许 hard**。
- store_event.kind = "new_client"，必须包含 client 与 task。
- has_choice = true。
- 叙事重点放在客户登门拜访的画面和气氛。
- adjustments 全 0（接不接由后续判定）。
"""


def build_event_prompt(c, kind, **kwargs):
    """R4 起的常规事件 prompt。"""
    if kind == "n":
        return f"""请引入一位**新客户**和他的委托。
- 委托类型应符合当前店主声誉 / 风波 / 名声的氛围。
- difficulty 自由选择，但 hard 仅用于真正棘手的事情。
- store_event.kind = "new_client"。
- has_choice = true（3 个选项）。
"""
    if kind == "l":
        client = kwargs.get("client", {})
        cid = client.get("id", "")
        notes = client.get("notes", "")
        last_seen = client.get("last_seen_tick", 0)
        rel = client.get("relationship", "中立")
        return f"""请处理一次**老客户回访**。

客户档案：
  ID：{cid}
  姓名：{client.get('name','?')}
  原型：{client.get('archetype','?')}
  目前关系：{rel}
  上次见面：第 {last_seen} 旬
  玩家备注：{notes or '（无）'}

请从以下 follow_up_kind 里选一种：
  - thanks（专程来道谢/送礼）
  - grudge（带着旧账上门讨说法）
  - new_request（带新委托）
  - unfinished_business（之前有遗留问题）

要求：
- store_event.kind = "old_client"。
- store_event.client_id 必须等于 "{cid}"，不要新建客户。
- 如果选 new_request 或 unfinished_business，需要附 task。
- has_choice = true。
"""
    if kind == "k":
        heat = c.get("heat", 0)
        return f"""HEAT 触发了**风波**事件。当前 HEAT={heat}/10。
请描述一桩主动找上门的麻烦：受害者家属、同行嫉妒、官府盘查、债主、被记仇的旧客户等。
- store_event.kind = "trouble"。
- has_choice = true（3 个处理方案）。
- difficulty 自由，麻烦本身可以 normal 或 hard。
"""
    if kind == "quiet":
        return """这一旬没有事情发生。
- 简短描写店主的日常 50~150 字（看店、整理货品、温酒读书等）。
- store_event.kind = "quiet"。
- has_choice = false。
- adjustments 可以全 0 或微小数字。
"""
    return ""


def build_action_check_prompt(c, action_text):
    """玩家自定义行动 → 先问 AI 用啥属性。"""
    return f"""玩家想在当前时间点主动做一件事。
你只需要判断它需要哪些属性鉴定，然后**只返回一个 JSON**，不要写故事。

玩家行动：{action_text}

可用属性：STR(武力)、CRE(资金)、HMR(人脉)、INT(经验)、APP(亲和)、END(精力)

判定原则：
- 简单的小事（凑近聊天、随便看看）→ 1 个属性，难度 easy。
- 一般行动 → 1 个属性，难度 normal。
- 涉及多种能力或非常困难的事情 → 2 个属性，难度 normal 或 hard。
- "鉴定"本身已经代表事情有难度，**只在真正棘手时用 hard**。

严格只返回如下 JSON：
{{
  "checks": ["STR"],
  "difficulty": "normal",
  "reasoning": "一句话理由"
}}
"""


def build_resolution_prompt(c, action_summary, check_results,
                            commission_id=None, client_id=None,
                            event_kind=None):
    """玩家行动 + 鉴定结果都齐了，让 AI 写结局叙事。"""
    overall = resolve_multi_check(check_results)

    lines = []
    for r in check_results:
        rule_zh = {"advantage": "（双骰取优）",
                   "disadvantage": "（双骰取劣）",
                   "normal": ""}[r["rule"]]
        rolls_text = "+".join(str(x) for x in r["rolls"])
        mark = "✅成功" if r["success"] else "❌失败"
        lines.append(f"  - {r['attribute']} 鉴定（属性值 {r['value']}）{rule_zh}："
                     f"投出 [{rolls_text}]，采用 {r['kept']} → {mark}")
    check_text = "\n".join(lines)

    overall_zh = {
        "full_success": "完胜（所有鉴定都通过）",
        "partial_success": "险胜（有部分鉴定失败，必须付出代价才能办成）",
        "full_failure": "完败（鉴定都失败）",
    }[overall]

    extra_hint = ""
    if commission_id:
        extra_hint += f"\n这次行动针对的是委托 {commission_id}。"
        extra_hint += "\nstore_event.kind = \"resolution\"，commission_id 原样回填。"
        extra_hint += "\n- 完胜 → outcome 一般为 \"resolved\"。"
        extra_hint += "\n- 险胜 → 可以 \"partial\" 或 \"resolved\"（带代价）。"
        extra_hint += "\n- 完败 → 通常是 \"failed\"，也可以 \"ongoing\" 让玩家继续挣扎。"
    if client_id:
        extra_hint += f"\n本次互动的客户 ID 是 {client_id}，请在 client_relationship_after 中给出关系变化。"
    if event_kind == "k":
        extra_hint += "\n这是 HEAT 触发的麻烦事件，完败一般会让 HEAT +1~+2。"

    return f"""玩家这一次的行动是：{action_summary}

【鉴定结果】
{check_text}

【综合判定】{overall_zh}

请基于以上结果写一段 200~400 字的叙事。要求：
- 叙事必须吻合判定结果。完胜不能写失败，完败不能写成功。
- 险胜：办成了，但要付明显代价（HP / ASSET / MYSTERY / REPUTATION / INTEGRITY 之一显著损失）。
- 完败：失利。HEAT +1 是默认，可叠加其他损失。
- 如果这件事还能继续往下推（同一委托没结案或剧情有续），可以 has_choice=true 给后续。
- 否则 has_choice=false。
{extra_hint}
"""


def build_reject_first_client_prompt(c):
    """玩家拒绝了第一个客户（首单无代价）。"""
    return """玩家拒绝了第一位客户的委托。
请用 60~150 字描写客户离开的场景。
- 这是开张第一单的拒绝，是教程性的，**不要扣任何属性 / 不要 +HEAT / 不要 -名声**。
- adjustments 全 0。
- store_event.kind = "none"。
- has_choice = false。
"""


def build_reject_normal_prompt(c, client_name="客户"):
    """普通情境下拒绝委托。"""
    return f"""玩家拒绝了 {client_name} 的委托。
请用 100~200 字描写拒绝场景。
- 拒绝可能影响神秘度 / 名声 / 操守，请合理小幅调整。
- adjustments 不要超过 ±2。
- store_event.kind = "none"。
- has_choice = false。
"""


# ============================================================
# 天赋池（占位，后面慢慢补）
# ============================================================

TALENT_POOL_ANY = [
    # ============ NEGATIVE (12个) ============
    {"name": "酒鬼", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "没有酒，你什么都干不了。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "酒桌上的朋友不叫朋友，但酒桌外你连话都说不利索。"},
    {"name": "体弱多病", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你从小身体就不好。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "躺在床上的日子里，你读完了别人一辈子都读不完的东西。"},
    {"name": "面部疤痕", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "一道横贯面容的伤疤。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "镜子里的那个人让小孩哭闹，也让敌人三思。"},
    {"name": "赌徒", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你总是输得比赢得多。",
     "modifiers": [("CRE", "-1d3*5")],
     "narrative": "下一把，下一把一定能翻本。"},
    {"name": "独行者", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你习惯一个人。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "人群让你疲惫，独处让你清醒。"},
    {"name": "欠债累累", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你欠了一屁股债。",
     "modifiers": [("CRE", "-1d2*5"), ("END", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "债主遍布天下——某种意义上，这也是一种人脉。"},
    {"name": "臭名昭著", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你的名声不太好。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "人们提起你的名字时总会压低声音。但这也意味着——他们记得你。"},
    {"name": "口吃", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你说话不太利索。",
     "modifiers": [("APP", "-1d3*5")],
     "narrative": "你、你有话要说，但、但舌头总是跟不上脑子。"},
    {"name": "懒散成性", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "能躺着绝不坐着。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("APP", "+1d1*5")],
     "narrative": "你笑容可掬地拒绝了每一份需要出力的工作。"},
    {"name": "旧伤缠身", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你的身体记得每一场雨。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那些伤疤会在最不合时宜的时候提醒你：你已经不是年轻时候的自己了。"},
    {"name": "一贫如洗", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "你身上只剩几个铜板。",
     "modifiers": [("CRE", "-1d3*5")],
     "narrative": "口袋里的风比外面的还大。"},
    {"name": "社交恐惧", "rarity": "negative", "mode": "Store", "scenarios": ["any"],
     "desc": "陌生人让你冒汗。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("END", "+1d1*5")],
     "narrative": "打招呼前你要在心里排练十遍，然后还是会说错。"},
    {"name": "笨拙", "rarity": "NEGATIVE", "mode": "Store", "scenarios": ["any"],
     "desc": "你有一身力气，但举止粗鲁吓人。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d3*5")],
     "narrative": "你撞翻的东西比搬运的多。"},
    {"name": "挥霍无度", "rarity": "NEGATIVE", "mode": "Store", "scenarios": ["any"],
     "desc": "你手上总有点小钱，但来得快去得也快。",
     "modifiers": [("CRE", "+1d1*5"), ("END", "-1d2*5"), ("HMR", "-1d1*5")],
     "narrative": "今朝有酒今朝醉，千金散尽不复来。"},
    {"name": "轻信于人", "rarity": "NEGATIVE", "mode": "Store", "scenarios": ["any"],
     "desc": "你待人真诚，却容易被花言巧语蒙骗。",
     "modifiers": [("APP", "+1d1*5"), ("HMR", "-1d3*5")],
     "narrative": "你帮过的人不少，坑过你的人更多。"},
    {"name": "冷血无情", "rarity": "NEGATIVE", "mode": "Store", "scenarios": ["any"],
     "desc": "自认极度理性，计算精准，但缺乏人情味，让人不敢亲近。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d3*5")],
     "narrative": "你自觉你解决问题的方式总是最优解——只是没人愿意承认。"},
    # ============ COMMON (12个) ============
    {"name": "街头混混", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "年轻时混过一阵子。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你打过几次群架，也挨过几次揍。至少学会了怎么握拳头。"},
    {"name": "游手好闲", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你见过形形色色的人。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你没赚到什么钱，但认识了三教九流。"},
    {"name": "勤恳踏实", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你做事认真。",
     "modifiers": [("END", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你相信只要埋头干活，总会有回报。虽然这并不总是对的。"},
    {"name": "健谈", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你嘴皮子利索。",
     "modifiers": [("APP", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "君子动口不动手——不是因为君子，是因为动手打不过。"},
    {"name": "沉默寡言", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你话不多。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "别人说话的时候你在听。听比说更有用。"},
    {"name": "省吃俭用", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你攒下了一点家底。",
     "modifiers": [("CRE", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "一顿好饭你能分成三天吃。"},
    {"name": "平凡出身", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "没什么特别的背景。",
     "modifiers": [],
     "narrative": "你出生在一个普通家庭，过着普通日子，直到普通日子过不下去。"},
    {"name": "老好人", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你脾气好，大家都愿意找你。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "'下次请你吃饭'是你最常收到的承诺，也是最常被遗忘的承诺。"},
    {"name": "孤儿", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你从小无父无母。",
     "modifiers": [("END", "+1d1*5"), ("HMR", "-1d1*5")],
     "narrative": "没有家让你失望，也没有家能让你依靠。"},
    {"name": "浪子回头", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你曾经荒唐过。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "那些年的荒唐教会你的，比任何书本都多。"},
    {"name": "市井智慧", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你懂得察言观色。",
     "modifiers": [],
     "narrative": "你没读过什么书，但人情世故这本书你翻得比谁都勤。"},
    {"name": "身强体健", "rarity": "common", "mode": "Store", "scenarios": ["any"],
     "desc": "你体格不错。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "父母给的好身板是你最大的财产。"},
    # ============ RARE (8个) ============
    {"name": "走南闯北", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你去过很多地方。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "每一个地方都留下了你的一小部分，也给了你一小部分。"},
    {"name": "天生魅力", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你天生招人喜欢。",
     "modifiers": [("APP", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你只是笑了笑，而对方已经愿意为你做很多事。"},
    {"name": "精力旺盛", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你仿佛有用不完的劲。",
     "modifiers": [("END", "+1d2*5"), ("STR", "+1d1*5")],
     "narrative": "别人累瘫的时候，你才刚刚开始活过来。"},
    {"name": "博闻强记", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你记性极好。",
     "modifiers": [("INT", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "十年前的闲谈，二十年前的一张脸，你都记得清清楚楚。"},
    {"name": "察言观色", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你能看穿人心。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "一个人的眼神停留多久，嘴角抽动的方向，都在对你讲话。"},
    {"name": "积蓄颇丰", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你攒下了不小的一笔。",
     "modifiers": [("CRE", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "多年的节俭和精明让你有了一个不错的起点。"},
    {"name": "身经百战", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你见过真正的血。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "每一次劫后余生都让你更加清楚——活着本身就是一种胜利。"},
    {"name": "八面玲珑", "rarity": "rare", "mode": "Store", "scenarios": ["any"],
     "desc": "你跟谁都能说上话。",
     "modifiers": [("APP", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "贵人面前你恭谨，泼皮面前你痞气，老人面前你稳重，孩童面前你温和。"},
    # ============ LEGENDARY (4个) ============
    {"name": "天纵奇才", "rarity": "legendary", "mode": "Store", "scenarios": ["any"],
     "desc": "你是百年一遇的聪明人。",
     "modifiers": [("INT", "+2d2*5"), ("APP", "+1d2*5")],
     "narrative": "别人用十年琢磨的道理，你一眼就看穿。剩下的九年零十一个月，你用来想该怎么利用这个道理。"},
    {"name": "名动一方", "rarity": "legendary", "mode": "Store", "scenarios": ["any"],
     "desc": "你的名字，在某个圈子里无人不知。",
     "modifiers": [("HMR", "+2d3*5")],
     "narrative": "一封署上你名字的信，可以打开很多扇门。"},
    {"name": "钢筋铁骨", "rarity": "legendary", "mode": "Store", "scenarios": ["any"],
     "desc": "你的身体是真正的武器。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d2*5")],
     "narrative": "你拳头落下的时候，连空气都要让路。"},
    {"name": "万人迷", "rarity": "legendary", "mode": "Store", "scenarios": ["any"],
     "desc": "你的魅力超乎常理。",
     "modifiers": [("APP", "+2d3*5")],
     "narrative": "你走进房间的那一刻，所有人的目光都会不自觉地转过来——然后，就很难移开了。"},
    {"name": "不死身", "rarity": "LEGENDARY", "mode": "Store", "scenarios": ["any"],
     "desc": "你曾经死里逃生的次数比大多数人吃饭还多，练就了钢铁之躯和超凡毅力。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d2*5")],
     "narrative": "阎王爷懒得翻你的名字册。"},
    {"name": "传奇人物", "rarity": "LEGENDARY", "mode": "Store", "scenarios": ["any"],
     "desc": "你曾是某个传说故事的中心，至今余辉犹在。",
     "modifiers": [("STR", "+2d2*5"), ("APP", "+1d2*5")],
     "narrative": "江湖上还流传着你曾经的故事。"},
    # ============ WILDCARD (4个) ============
    {"name": "疯癫智者", "rarity": "wildcard", "mode": "Store", "scenarios": ["any"],
     "desc": "你的脑子和别人不一样。",
     "modifiers": [("INT", "+2d3*5"), ("APP", "-1d3*5"), ("HMR", "-1d3*5")],
     "narrative": "你看得见别人看不见的东西，也说些别人听不懂的话。他们说你疯了。也许吧，但疯子往往最先看清真相。"},
    {"name": "金玉其外", "rarity": "wildcard", "mode": "Store", "scenarios": ["any"],
     "desc": "你看起来光鲜，口袋却空空。",
     "modifiers": [("APP", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "你身上最后一件体面衣服，是用来掩盖你已经三天没吃饭的事实。"},
    {"name": "独狼武者", "rarity": "wildcard", "mode": "Store", "scenarios": ["any"],
     "desc": "你是孤独的强者。",
     "modifiers": [("STR", "+2d3*5"), ("HMR", "-2d3*5")],
     "narrative": "你不需要朋友，你的拳头就是你最忠诚的同伴。代价是——当你真正需要帮手时，没有人会来。"},
    {"name": "背负血债", "rarity": "wildcard", "mode": "Store", "scenarios": ["any"],
     "desc": "你曾经做过一些事，至今仍在追着你。",
     "modifiers": [("INT", "+1d3*5"), ("STR", "+1d3*5"), ("END", "-1d3*5"), ("HMR", "-1d3*5")],
     "narrative": "那些事教会了你如何在阴影里生存。但每到夜深人静，那些面孔就会回来，让你一夜无眠。"},
    {"name": "双重人格", "rarity": "WILDCARD", "mode": "Store", "scenarios": ["any"],
     "desc": "夜幕降临，另一个你接管一切，长袖善舞，然而每次切换都会消耗大量心力。",
     "modifiers": [("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你不记得昨晚酒宴上与总督称兄道弟的那人是不是自己，但早上的偏头痛在提醒你代价。"},

         # ============ NEGATIVE (8个) ============
    {"name": "996幸存者", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "上一份工作把你榨干了。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你攒下了一点遣散费，还有一身再也治不好的颈椎病和黑眼圈。"},

    {"name": "网贷缠身", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你的手机每天响个不停。",
     "modifiers": [("CRE", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你学会了所有催收话术——因为你听了太多遍了。"},

    {"name": "黑户", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你的身份有些问题。",
     "modifiers": [("HMR", "-1d2*5"), ("CRE", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "办什么都要绕路走,但你也因此认识了一堆同样绕路走的人。"},

    {"name": "前科", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你的档案上有一笔。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "进去的那段日子你学到的东西，比外面十年都多——虽然没一样是好事。"},

    {"name": "夜班综合征", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你的生物钟已经彻底乱了。",
     "modifiers": [("END", "-1d3*5")],
     "narrative": "白天你是行尸走肉，凌晨三点你精神抖擞。"},

    {"name": "小镇做题家", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "除了做题，你什么都不会。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你来到大城市才发现，这里的规则完全不在考纲内。"},

    {"name": "社畜", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你还没从上一份工作里缓过来。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "PPT、周报、KPI——这些词你闭着眼都能念。问题是你闭着眼的时候也在念。"},

    {"name": "啃老族", "rarity": "negative", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你习惯了伸手。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你爸妈留下的那点钱还能撑一阵，但他们每次打电话都让你心虚。"},

    # ============ COMMON (10个) ============
    {"name": "外卖常客", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你认识这片所有的骑手。",
     "modifiers": [("HMR", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "三条街内哪家店出餐快，哪家老板抠门，你门儿清。"},

    {"name": "夜店常客", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你是夜生活的一部分。",
     "modifiers": [("APP", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "DJ认识你,保安认识你,服务员认识你——只有你早上醒来认不出自己。"},

    {"name": "健身爱好者", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你有一张健身卡。",
     "modifiers": [("STR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "虽然去的次数不多，但胸肌是真的练出来一点。"},

    {"name": "社交媒体达人", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你在网上有点小名气。",
     "modifiers": [("HMR", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "几千个粉丝，算不上大V,但也够你在饭局上拿出来说一说。"},

    {"name": "普通上班族", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你朝九晚五过了几年。",
     "modifiers": [],
     "narrative": "地铁、工位、外卖，循环往复。直到有一天你决定换个活法。"},

    {"name": "驾照党", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你开车比走路多。",
     "modifiers": [("END", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "城市的每一条小路、每一个违章摄像头的位置，你都熟稔于心。"},

    {"name": "毕业生", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你刚离开校园。",
     "modifiers": [("INT", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "一肚子知识，空口袋，和一份怎么也找不到的工作。"},

    {"name": "房东的儿女", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你家在城中村有几间出租屋。",
     "modifiers": [("CRE", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "你不用担心房租，但每个月要去收租的时候还是很头疼。"},

    {"name": "宅家一族", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你熟悉网络的每个角落。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "现实世界让你疲惫，但屏幕后面你如鱼得水。"},

    {"name": "跑腿小哥", "rarity": "common", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你靠送东西为生。",
     "modifiers": [("END", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "风里来雨里去，手机电量和你的生活都岌岌可危。"},

    # ============ RARE (5个) ============
    {"name": "程序员", "rarity": "rare", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你懂代码。",
     "modifiers": [("INT", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "在这个时代,会写代码意味着会一门现代魔法。"},

    {"name": "体制内出身", "rarity": "rare", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你父母是公务员。",
     "modifiers": [("HMR", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "饭桌上听到的事情比你这辈子遇到的还多。你知道每件事背后的规矩。"},

    {"name": "私家车主", "rarity": "rare", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你有一辆还不错的车。",
     "modifiers": [("CRE", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "车是男人的第二张脸,你的这张脸还算体面。"},

    {"name": "前警察", "rarity": "rare", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你曾穿过制服。",
     "modifiers": [("STR", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "辞职的原因你不愿多谈,但那身本事还在。办案的直觉也还在。"},

    {"name": "医学世家", "rarity": "rare", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你家三代行医。",
     "modifiers": [("INT", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "小时候你以为全天下的人都会看病。长大后你发现,能救人的本事在这个时代依然珍贵。"},

    # ============ LEGENDARY (4个) ============
    {"name": "富二代", "rarity": "legendary", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你家里不差钱。",
     "modifiers": [("CRE", "+2d2*5"), ("HMR", "+1d2*5")],
     "narrative": "你从小接触的圈子,别人一辈子也挤不进去。你只是没决定要不要接手家业。"},

    {"name": "网红", "rarity": "legendary", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你有几百万粉丝。",
     "modifiers": [("APP", "+1d3*5"), ("HMR", "+1d3*5")],
     "narrative": "陌生人在街上叫你的名字,商家排队送你免费的东西。这个时代,流量就是权力。"},

    {"name": "海归精英", "rarity": "legendary", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "常春藤毕业,见过世面。",
     "modifiers": [("INT", "+2d2*5"), ("APP", "+1d2*5")],
     "narrative": "你说话偶尔会夹几个英文单词,但你确实有那个底气。"},

    {"name": "特种兵退役", "rarity": "legendary", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你受过最严酷的训练。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d3*5")],
     "narrative": "那些年的经历你不会告诉任何人。但你的身体记得每一种杀人和自保的方法。"},

    # ============ WILDCARD (3个) ============
    {"name": "暗网常客", "rarity": "wildcard", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你混迹于互联网的阴影面。",
     "modifiers": [("INT", "+1d3*5"), ("APP", "-2d3*5"), ("HMR", "+1d3*5")],
     "narrative": "你知道很多不该知道的事情,也因此成了一个让人不舒服的人。人们愿意付钱给你,但不愿意跟你吃饭。"},

    {"name": "过气明星", "rarity": "wildcard", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你曾经红过,现在没人记得。",
     "modifiers": [("APP", "+1d3*5"), ("CRE", "-1d3*5"), ("HMR", "+1d3*5")],
     "narrative": "偶尔还会有人认出你,但更多时候你是在怀念镁光灯的感觉——和那些早就花光的代言费。"},

    {"name": "地下拳手", "rarity": "wildcard", "mode": "Store", "scenarios": ["citywalk"],
     "desc": "你在某个地下室里打出过名堂。",
     "modifiers": [("STR", "+1d3*5"), ("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "没有规则,没有裁判,只有钱和血。你赢了很多场,代价是一身的旧伤。"},

     # ============ NEGATIVE (8个) ============
    {"name": "灵根残缺", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你的灵根有缺陷。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "修炼之路对你格外崎岖,但你也因此比别人更早明白:光靠天赋不行。"},

    {"name": "走火入魔", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你曾经修炼出了岔子。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那次之后你再不敢轻易运功。经脉里的隐痛会在阴天提醒你:修仙不是闹着玩的。"},

    {"name": "被逐出山门", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你犯了门规,被师门除名。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "当年的师兄弟如今见你绕道走。但你学到的那些东西,没人能从你脑子里拿走。"},

    {"name": "天煞孤星", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你克亲克友,无人敢近。",
     "modifiers": [("HMR", "-1d3*5")],
     "narrative": "相士看你一眼就摇头。你不信命,但身边的人一个接一个离开,由不得你不信。"},

    {"name": "散修出身", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你无门无派,一切全靠自己。",
     "modifiers": [("HMR", "-1d2*5"), ("CRE", "-1d1*5"), ("END", "+1d1*5")],
     "narrative": "没有传承,没有靠山,每一个突破都是踩着自己的血路走出来的。"},

    {"name": "心魔未除", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你心里住着一个东西。",
     "modifiers": [("APP", "-1d2*5"), ("END", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "夜深人静时它会说话。你听久了,偶尔会怀疑究竟是你还是它在做决定。"},

    {"name": "丹毒缠身", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你年轻时服丹无度。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "那些快速提升境界的丹药让你付出了代价。身体是一笔借贷,总有到期的一天。"},

    {"name": "寿元将近", "rarity": "negative", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你的寿命所剩无几。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "修士一怕境界止步,二怕寿元将尽。你不幸两样都占了一点。所以你做事,有种别人没有的急迫。"},

    # ============ COMMON (10个) ============
    {"name": "药庐学徒", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你在药庐里打过下手。",
     "modifiers": [("INT", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "百草之性你认得大半,虽然自己还炼不出什么像样的丹。"},

    {"name": "山门杂役", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你在某个宗门做过杂役。",
     "modifiers": [("HMR", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "端茶送水的几年让你认识了不少人物。道心未必坚,八卦倒是听了不少。"},

    {"name": "炼气境", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你小有修为,堪堪入门。",
     "modifiers": [("END", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "放在凡人中你是高手,放在修士中你是蝼蚁。但这点本事已经够你吃饭了。"},

    {"name": "剑修", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你练的是剑。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "一剑在手,话就少了。剑修多执拗,你也不例外。"},

    {"name": "游方道士", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你四处云游,居无定所。",
     "modifiers": [("INT", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "山是你的床,风是你的被。脚下的路长过脑子里的答案。"},

    {"name": "世俗出身", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你本是凡人,后来才踏上修行。",
     "modifiers": [],
     "narrative": "你记得没有灵力时的生活。这份记忆让你更懂人间烟火,也更知修行不易。"},

    {"name": "驭兽少年", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你从小与灵兽打交道。",
     "modifiers": [("HMR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "灵兽比人好懂。至少它们不会背叛你——除非你亏待了它们。"},

    {"name": "符箓学徒", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你会画些简单的符。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "画符靠的是手稳心静。你画得不多,但够用。"},

    {"name": "寒门弟子", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你出身贫寒,却踏上了修行路。",
     "modifiers": [("END", "+1d1*5"), ("HMR", "-1d1*5")],
     "narrative": "别人一粒丹药进境,你靠一呼一吸苦熬。这条路你走得比谁都明白。"},

    {"name": "阵法爱好者", "rarity": "common", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你钻研过一些阵法。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "天地之间的规律让你着迷,以至于你经常对着一块地发呆半天。"},

    # ============ RARE (5个) ============
    {"name": "仙家血脉", "rarity": "rare", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你身上流着不凡的血。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "你的先祖中有人飞升,留下的余泽让你比常人强上几分。虽然也就几分。"},

    {"name": "名门之后", "rarity": "rare", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你出身修真大族。",
     "modifiers": [("HMR", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "报出家族名号,大部分场合你都能少几分麻烦——除非遇上家族的仇人。"},

    {"name": "炼丹有成", "rarity": "rare", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你是个合格的丹师。",
     "modifiers": [("INT", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "三品之下的丹药对你来说并非难事。光是这一手,就足以让你衣食无忧。"},

    {"name": "筑基圆满", "rarity": "rare", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你修为不俗,筑基已至圆满。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "在凡俗之地你已是翻云覆雨的人物。只是在真正的修行界,你才刚刚入门。"},

    {"name": "剑心通明", "rarity": "rare", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你的剑道直指本心。",
     "modifiers": [("STR", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "他人修剑是练招,你修剑是问心。一念之动,剑已至千里。"},

    # ============ LEGENDARY (4个) ============
    {"name": "天灵根", "rarity": "legendary", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "万中无一的修道之资。",
     "modifiers": [("END", "+2d2*5"), ("STR", "+2d2*5")],
     "narrative": "你修炼的速度是别人的数倍。天地似乎格外眷顾你——这份眷顾,也是一种负担。"},

    {"name": "散修楷模", "rarity": "legendary", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你已是散修中的塔顶。",
     "modifiers": [("INT", "+2d2*5"), ("STR", "+1d2*5"), ("HMR", "+1d3*5")],
     "narrative": "你活过的岁月比大多数国家的历史都长。凡俗的喜怒哀乐对你而言,不过是又一场似曾相识的戏。"},

    {"name": "仙缘深厚", "rarity": "legendary", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你总能遇到贵人。",
     "modifiers": [("HMR", "+2d2*5"), ("APP", "+2d2*5")],
     "narrative": "无论走到哪里,总有前辈高人愿意点拨你两句。这不是运气,这是命格。"},

    {"name": "太上忘情", "rarity": "legendary", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你修的是绝情之道。",
     "modifiers": [("INT", "+2d2*5"), ("END", "+2d2*5")],
     "narrative": "七情六欲对你如隔靴搔痒。旁人看你冷漠,唯有你自己知道——这是修成的,也是失去的。"},

    # ============ WILDCARD (3个) ============
    {"name": "魔道余孽", "rarity": "wildcard", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你修的不是正道功法。",
     "modifiers": [("STR", "+2d3*5"), ("HMR", "-2d3*5")],
     "narrative": "你的功法见效极快,代价是正道中人人得而诛之。你早已习惯在阴影中行走。"},

    {"name": "转世重修", "rarity": "wildcard", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你隐约记得前世的事。",
     "modifiers": [("INT", "+2d3*5"), ("END", "-1d3*5"), ("STR","-1d3*5")],
     "narrative": "前世的记忆碎片让你见识远超同辈,但这份记忆也在一点点消磨你这具身子的根基。"},

    {"name": "容颜不老", "rarity": "wildcard", "mode": "Store", "scenarios": ["flyaway"],
     "desc": "你保持着最美好的模样。",
     "modifiers": [("APP", "+2d3*5"), ("CRE", "-2d3*5")],
     "narrative": "你的容貌让无数人趋之若鹜——也让同样多的人对你起了歹意。护这张脸花了你太多钱。"},
         # ============ NEGATIVE (8个) ============
    {"name": "法术反噬", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你曾被自己的法术伤过。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那道疤是你自己咒出来的。从那以后你对魔法多了几分敬畏,也少了几分力量。"},

    {"name": "通缉犯", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "某个王国悬赏你的脑袋。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "你的画像贴在每个小镇的酒馆外。画得不太像,但足够让你每次进城都要拉低兜帽。"},

    {"name": "异端血统", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你身上有非人的血。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "教会的人看你的眼神让你浑身不自在。那点血脉给了你力量,也给了你一生的麻烦。"},

    {"name": "破产骑士", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你曾是骑士,如今一无所有。",
     "modifiers": [("CRE", "-1d2*5"), ("END", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "盔甲早就当了,马也卖了。但那柄剑你怎么也不肯放手——因为它是你最后的体面。"},

    {"name": "诅咒缠身", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "有什么东西跟着你。",
     "modifiers": [("END", "-1d3*5")],
     "narrative": "你不记得自己做错了什么。但从某个月圆夜开始,坏事就没停过。"},

    {"name": "魔法学徒的失败", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你没能通过魔法学院的考核。",
     "modifiers": [("CRE", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "学费是家里东拼西凑的。你不敢回去,只能在外面流浪,靠着那点没学完的本事讨生活。"},

    {"name": "瘟疫幸存者", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你从黑死病中活了下来。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "一整个村子只剩你一个。你学会了如何辨认瘟疫的迹象——代价是再也睡不了安稳觉。"},

    {"name": "农奴出身", "rarity": "negative", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你从泥里爬出来的。",
     "modifiers": [("HMR", "-1d2*5"), ("INT", "-1d1*5"), ("END", "+1d1*5")],
     "narrative": "贵族老爷们看你像看牲口。你逃出来了,但身份是抹不掉的烙印。"},

    # ============ COMMON (10个) ============
    {"name": "见习冒险者", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你在冒险者公会挂了名。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "铜牌一块,够你接点跑腿的活。距离真正的冒险者还差十几块金牌的距离。"},

    {"name": "酒馆常客", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你在酒馆里度过了大半青春。",
     "modifiers": [("HMR", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "吟游诗人的歌你听过三百首,冒险者的吹嘘你听过三千个。大部分都是假的,但细节很有用。"},

    {"name": "民兵出身", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你在村镇民兵里服过役。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你会用长矛和弓,会列队,会站岗。没打过什么大仗,倒是哥布林杀了不少。"},

    {"name": "猎人", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你在森林里长大。",
     "modifiers": [("END", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "野兽的脚印你看一眼就懂。人类的心思你至今看不明白。"},

    {"name": "识字的平民", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "在这个时代,识字就是本事。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "大部分人签名都要按手印。你能读能写,这让你在市井里也算半个先生。"},

    {"name": "流浪者", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你四海为家。",
     "modifiers": [],
     "narrative": "你见过海,见过山,见过烧毁的村庄和盛大的节日。但你没见过自己的归处。"},

    {"name": "教会孤儿", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你在修道院长大。",
     "modifiers": [("INT", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "修士们教了你读经和几句祷词。至于信仰——你自己有自己的想法。"},

    {"name": "佣兵学徒", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你跟过几支佣兵团。",
     "modifiers": [("STR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你学会了打仗,也学会了跑。最重要的是学会了在发饷前不要跟队长翻脸。"},

    {"name": "小偷的手艺", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你的手指比一般人灵活。",
     "modifiers": [("HMR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "几个贫民窟的熟面孔是你的朋友——或者至少,不会在你背后捅刀。"},

    {"name": "铁匠学徒", "rarity": "common", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你抡过几年大锤。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你认得好铁和烂铁,也能分辨什么样的剑能杀人,什么样的剑只能挂墙。"},

    # ============ RARE (5个) ============
    {"name": "魔法天赋", "rarity": "rare", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你能感知并操控法力。",
     "modifiers": [("INT", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "在这个大部分人一辈子都碰不到魔法的世界,你天生就与秘源相连。这让你与众不同。"},

    {"name": "贵族私生子", "rarity": "rare", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你有一个不能明说的父亲。",
     "modifiers": [("HMR", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "你从未被承认过,但那位老爷偶尔会派人送些钱来。血脉带来的便利和耻辱,你都尝过。"},

    {"name": "商队护卫老手", "rarity": "rare", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你护送过无数商队穿过蛮荒之地。",
     "modifiers": [("STR", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "大陆上的商人老板们有一半都认识你。他们知道——你不是最便宜的,但你能让货物活着到达。"},

    {"name": "游吟诗人", "rarity": "rare", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你走到哪里都能唱出一首好歌。",
     "modifiers": [("APP", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你能在贵族厅堂和农民篝火旁同样受欢迎。一首歌有时候比一把剑更能打开门。"},

    {"name": "前圣骑士", "rarity": "rare", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你曾是神的仆从。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "不知何故,你离开了教会。但那些训练和信仰的痕迹,还在你的举手投足间。"},

    # ============ LEGENDARY (4个) ============
    {"name": "屠龙者", "rarity": "legendary", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你真的杀过一条龙。",
     "modifiers": [("STR", "+2d2*5"), ("HMR", "+1d2*5")],
     "narrative": "没人完全相信那是你干的,但你身上那块鳞片甲片不会说谎。从此之后,你报名字时没人敢不给面子。"},

    {"name": "大法师的弟子", "rarity": "legendary", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你师从当世最强法师之一。",
     "modifiers": [("INT", "+2d2*5"), ("HMR", "+1d2*5")],
     "narrative": "老师给你的东西比大多数魔法学院一辈子教的都多。代价是,你有时候会替他收拾烂摊子。"},

    {"name": "精灵血裔", "rarity": "legendary", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你身上流着高贵的精灵血。",
     "modifiers": [("APP", "+2d2*5"), ("INT", "+1d2*5")],
     "narrative": "你的眉眼、你的灵敏、你对魔法的亲和——都是那份血脉的馈赠。凡人看你,像看月光。"},

    {"name": "王室血脉", "rarity": "legendary", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你是某个王族的旁支。",
     "modifiers": [("HMR", "+2d2*5"), ("CRE", "+2d2*5")],
     "narrative": "你不在继承序列里,但这个身份已经足够让半个大陆的贵族对你以礼相待——以及让另一半想让你消失。"},

    # ============ WILDCARD (3个) ============
    {"name": "恶魔契约", "rarity": "wildcard", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你签下了某份不该签的契约。",
     "modifiers": [("STR", "+2d3*5"), ("END", "-2d3*5")],
     "narrative": "你得到了远超凡人的力量。但每过一段时间,你会从梦中醒来,发现自己离那个东西又近了一步。"},

    {"name": "亡灵术士之名", "rarity": "wildcard", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你懂得与死者对话的学问。",
     "modifiers": [("INT", "+2d3*5"), ("APP", "-1d3*5"), ("HMR", "-1d3*5")],
     "narrative": "你掌握的知识让你能解开无数秘密,也让每个听说你名字的人下意识地后退一步。"},

    {"name": "德鲁伊隐修", "rarity": "wildcard", "mode": "Store", "scenarios": ["dragonfire"],
     "desc": "你曾在密林深处独居多年。",
     "modifiers": [("END", "+2d3*5"), ("HMR", "-2d3*5")],
     "narrative": "你懂草木,懂野兽,懂风雨的预兆。但你已经太久没跟人说过话,开口时总让人觉得哪里不对劲。"},
     # ============ NEGATIVE (8个) ============
    {"name": "灭门余生", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你是家破人亡的独苗。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "那一夜的血腥你一辈子忘不掉。活下来的人,欠着死去的人一个交代。"},

    {"name": "通缉要犯", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "朝廷的海捕文书上有你的名字。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "你改了名,换了脸,但那张画像总让你在进城时多绕两条街。"},

    {"name": "内伤难愈", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你的经脉里埋着旧伤。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那一掌打进去的内力至今还没化掉。阴雨天,它会提醒你:这条命是借来的。"},

    {"name": "被逐出师门", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你背叛了师门,或被师门背叛。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "当年的师兄弟见你要么动手,要么转身。那些功夫没人能夺走,但门派的庇护再也没有了。"},

    {"name": "仇家遍地", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你年轻时得罪了太多人。",
     "modifiers": [("APP", "-1d3*5")],
     "narrative": "你睡觉时手里都握着刀。江湖路远,你不知道下一个拐角等着你的是熟人还是敌人。"},

    {"name": "青楼出身", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你从风月场走出来。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你见识了人心最深处的东西。这份见识让你通透,也让你再不能完全信任谁。"},

    {"name": "赌场常败", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你一辈子的银子都在赌坊里。",
     "modifiers": [("CRE", "-1d3*5")],
     "narrative": "骰子一响,什么豪情壮志都化作白水。你知道自己不对,但手就是停不下来。"},

    {"name": "断指之仇", "rarity": "negative", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你少了一根手指。",
     "modifiers": [("STR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那根手指是抵了一笔账。从那以后,你学会了用另一只手握刀——也学会了永远不再欠账。"},

    # ============ COMMON (10个) ============
    {"name": "镖局弟子", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你在镖局里走过几年。",
     "modifiers": [("HMR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "各地的黑白两道你都认得几个。喊一声'借过',倒也真有人给面子。"},

    {"name": "落魄书生", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你屡试不第,流落江湖。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "四书五经烂熟于心,可惜考官不赏识。你的笔现在写的是代写书信和讼词。"},

    {"name": "衙门杂役", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你在官府当过差。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你知道县太爷的脾气,知道捕头要什么孝敬。这些东西比功夫有用。"},

    {"name": "走江湖的郎中", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你背着药箱走过大江南北。",
     "modifiers": [("INT", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "刀伤、内伤、慢性病你都见过。救人的事你做过,眼睁睁看人死的事你也做过。"},

    {"name": "三脚猫功夫", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你会点拳脚,但算不上高手。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "打地痞够用,遇到真正的江湖人物你就得跑。这点本事,吃不了饭,但能保命。"},

    {"name": "市井长大", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你在集市巷陌里长大。",
     "modifiers": [],
     "narrative": "哪家店老板爱占便宜,哪条巷子入夜不能走,你比本地人还清楚。"},

    {"name": "跑堂小二", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你在酒楼客栈打过杂。",
     "modifiers": [("APP", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "见人说人话,见鬼说鬼话。在柜台后头站几年,人心你也看了个七八分。"},

    {"name": "行脚商人", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你挑过担子,走过远路。",
     "modifiers": [("END", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "脚底的老茧是你的勋章。走得多了,看得多了,话就少了。"},

    {"name": "戏班出身", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你从小学戏。",
     "modifiers": [("APP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "生旦净末丑你都能演上两段。你知道:人生如戏,但戏假不了情。"},

    {"name": "绿林出身", "rarity": "common", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你在山寨里混过。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "劫富济贫是说给外人听的,兄弟义气才是真的。你下山了,但那几年的规矩还刻在骨子里。"},

    # ============ RARE (5个) ============
    {"name": "名门正派", "rarity": "rare", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你出身江湖大派。",
     "modifiers": [("HMR", "+1d2*5"), ("STR", "+1d1*5")],
     "narrative": "报出师门名号,江湖上大半人要敬你三分。这份底气不是自己挣的,但确实好用。"},

    {"name": "江南富商之后", "rarity": "rare", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你家在苏杭有些家业。",
     "modifiers": [("CRE", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "你自小穿绫罗,吃精馔。但你不满足于账房先生的日子——所以你上路了。"},

    {"name": "少年英侠", "rarity": "rare", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你年纪轻轻就有些名声。",
     "modifiers": [("STR", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "茶楼说书的偶尔会提到你的名字。你知道故事被夸大了十倍,但你不拆穿——好名声难得。"},

    {"name": "暗器高手", "rarity": "rare", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你的袖中藏着百样机巧。",
     "modifiers": [("STR", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "你很少正面动手。手指一弹,胜负已分——这就是你的规矩。"},

    {"name": "御前行走后人", "rarity": "rare", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你父辈在朝中有关系。",
     "modifiers": [("HMR", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "家里的旧人脉还能用几次。你在江湖行走,偶尔拿出一块牌子,就能让衙门高抬贵手。"},

    # ============ LEGENDARY (4个) ============
    {"name": "一代宗师传人", "rarity": "legendary", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你的师父是武林中的传奇。",
     "modifiers": [("STR", "+2d2*5"), ("HMR", "+1d2*5")],
     "narrative": "老头子教了你十几年。他留给你的不只是武功,还有整个江湖对他那一辈人的敬意。"},

    {"name": "江湖百晓生", "rarity": "legendary", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "江湖上的事,你知道得比谁都多。",
     "modifiers": [("INT", "+2d2*5"), ("HMR", "+2d2*5")],
     "narrative": "谁跟谁有仇,谁跟谁上过床,哪个门派的掌门有几个私生子——你都记着。这些东西,比刀子好用。"},

    {"name": "倾国之姿", "rarity": "legendary", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你的容貌惊艳一世。",
     "modifiers": [("APP", "+2d3*5")],
     "narrative": "见过你的人都会记一辈子。这份容貌是你最大的本钱——也是最大的负担。"},

    {"name": "武林世家嫡脉", "rarity": "legendary", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你是某个武林大家族的继承人。",
     "modifiers": [("STR", "+2d2*5"), ("HMR", "+1d2*5")],
     "narrative": "家传武学,祖宅产业,门生故旧——这些你生下来就有。代价是,整个家族的担子也在你肩上。"},

    # ============ WILDCARD (3个) ============
    {"name": "传奇杀手", "rarity": "wildcard", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你曾是一名传奇杀手。",
     "modifiers": [("STR", "+2d3*5"), ("APP", "-1d3*5"), ("HMR", "-2d3*5")],
     "narrative": "你金盆洗手了,但那段日子教你的东西还在。也因此,凡是认识你的人,都不敢真正靠近你。"},

    {"name": "魔教叛徒", "rarity": "wildcard", "mode": "Store", "scenarios": ["loneblade"],
     "desc": "你从邪教里逃了出来。",
     "modifiers": [("INT", "+2d3*5"), ("HMR", "-2d3*5")],
     "narrative": "你知道的秘密能让整个武林翻天。但也正因如此,正邪两道都想要你的命。"},
]

# ============================================================
# 拖延 / 死亡总结
# ============================================================

def build_delay_check_prompt(c, commission_id):
    """问 AI：这位客户同不同意拖延？"""
    com = c.get("store_commissions", {}).get(commission_id, {})
    client = c.get("store_clients", {}).get(com.get("client_id"), {})
    return f"""玩家想拖延一个委托，希望客户答应延期换取下次的优势骰。

【委托】{com.get('summary','?')} - {com.get('details','')}
【客户】{client.get('name','?')}（{client.get('archetype','?')}）
【目前关系】{client.get('relationship','中立')}
【已拖延次数】{com.get('delays_used',0)} / {COMMISSION_AUTO_ABANDON_DELAYS}

请判断客户是否答应延期。综合考虑紧迫程度、委托性质、已拖延次数、当前关系等。

严格只返回如下 JSON：
{{
  "agreed": true,
  "narrative": "客户的反应（30~80字）"
}}
"""


def build_store_summary_prompt(c):
    return f"""店主已离世。请对这一段店铺生涯做出评价与总结。

请围绕以下方面：
- 接过的委托数量与类型
- 客户名册的厚度
- 在江湖/坊间的名声、神秘度、操守
- 店主的传奇程度
- 死因与最终归宿

严格只返回如下 JSON：
{{
  "scores": {{"legendary": 0, "dramatic": 0, "successful": 0}},
  "evaluation": "对这段店铺生涯的文字评价（300~600字）"
}}
"""