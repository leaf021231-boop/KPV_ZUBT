"""
Creative Commons Legal Code
CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.
"""


# main.py
import threading
import random
import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from openai import OpenAI
import data as normal_data
import hornidata
import storedata
import finedata
import sv_ttk

from data import (
    SCENES, GENDERS, RARITY_CONFIG,
    ASSET_TIERS, FAME_TIERS, EXPE_TIERS, KNOW_TIERS,
    get_tier, roll_dice, parse_ai_json,
    load_config, save_config, clear_config,
    MODE_TEST, MODE_IRONMAN,
    MODE_HORNY_MILD, MODE_HORNY_INTENSE,
)

from storedata import (
    KEEPER_ARCHETYPES,
    get_keeper_archetype_by_id,
    init_store_state,
)

VERSION = "v0.7.1.1 YAWNINGLION"

TALENT_USER_PATH = os.path.join(os.path.expanduser("~"), ".ai_life_remake_talents.json")


def load_user_talents():
    try:
        with open(TALENT_USER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        talents = data.get("talents", [])
        # 修复 modifiers 形态：JSON 反序列化后是 list，draw 时也能用，但保险起见统一一下
        for t in talents:
            t["modifiers"] = [tuple(m) if isinstance(m, list) else m
                              for m in t.get("modifiers", [])]
        return talents
    except Exception:
        return []


def save_user_talents(talents):
    try:
        out = []
        for t in talents:
            tt = dict(t)
            tt["modifiers"] = [list(m) for m in t.get("modifiers", [])]
            out.append(tt)
        with open(TALENT_USER_PATH, "w", encoding="utf-8") as f:
            json.dump({"talents": out}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ============================================================
# Mode routing
# ============================================================

CONTENT_NORMAL = "normal"
CONTENT_HORNY = MODE_HORNY_MILD
CONTENT_STORE = "store"

# Fine Mode is now a modifier, not a content mode.
CONTENT_FINE = "fine"  # kept only for old-save compatibility; do not expose as content mode

DIFF_STANDARD = "standard"
DIFF_TEST = MODE_TEST
DIFF_IRONMAN = MODE_IRONMAN

CONTENT_MODE_MODULES = {
    CONTENT_NORMAL: normal_data,
    CONTENT_HORNY: hornidata,
    CONTENT_STORE: storedata,
}

# Note: keys match the strings stored on the character.
# All lookup code uses the "label" field, so do NOT rename it back to "ui".
FINE_TIMESTAMP_PRESETS = {
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
    "weekly": {
        "label": "每周",
        "tick_label": "周",
        "age_step": 1 / 52,
    },
}


def get_data_module(c):
    """
    Return the data module for the selected content mode.
    If missing/unknown, default to normal data.py.
    """
    return CONTENT_MODE_MODULES.get(c.get("content_mode", CONTENT_NORMAL), normal_data)


def build_mode_display(c):
    parts = []

    cm = c.get("content_mode", CONTENT_NORMAL)

    if cm == CONTENT_NORMAL:
        parts.append("普通人生")
    elif cm == CONTENT_HORNY:
        parts.append("性压抑模式")
    elif cm == CONTENT_STORE:
        parts.append("Store Mode")
    elif cm == CONTENT_FINE:
        parts.append("Fine Mode（旧内容模式）")
    else:
        parts.append(str(cm))

    diff = c.get("difficulty", DIFF_STANDARD)

    if diff == DIFF_TEST:
        parts.append("测试")
    elif diff == DIFF_IRONMAN:
        parts.append("铁人")
    else:
        parts.append("标准")

    if c.get("fast_mode"):
        parts.append("快速40岁收束")

    if c.get("fine_enabled"):
        fs = c.get("fine_settings", {})
        start_age = fs.get("start_age", "?")
        end_age = fs.get("end_age", "?")
        ts = fs.get("timestamp", "year")
        ts_ui = FINE_TIMESTAMP_PRESETS.get(ts, {}).get("label", ts)
        parts.append(f"Fine {start_age}→{end_age}岁 / {ts_ui}")

    return " / ".join(parts)


# ============================================================
# UI theme
# ============================================================

COLORS = {
    "bg": "#F2F3F7",
    "card": "#FFFFFF",
    "primary": "#4A6CF7",
    "primary_d": "#3A55C9",
    "text": "#1C1C1E",
    "subtext": "#6E6E73",
    "border": "#E1E3E8",
    "success": "#22C55E",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "muted": "#9CA3AF",
}

FONT_FAM = "Microsoft YaHei UI"
F_HEAD = (FONT_FAM, 16, "bold")
F_SUB = (FONT_FAM, 12, "bold")
F_BODY = (FONT_FAM, 11)
F_SMALL = (FONT_FAM, 10)
F_MONO = ("Consolas", 10)


def apply_style(root):
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure(".", background=COLORS["bg"], foreground=COLORS["text"], font=F_BODY)
    s.configure("TFrame", background=COLORS["bg"])
    s.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=F_BODY)

    s.configure(
        "Primary.TButton",
        background=COLORS["primary"],
        foreground="white",
        font=(FONT_FAM, 11, "bold"),
        borderwidth=0,
        padding=(16, 8),
    )
    s.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_d"]), ("disabled", "#B6BFD9")],
        foreground=[("disabled", "#EEEEEE")],
    )

    s.configure(
        "Secondary.TButton",
        background="#E8EAF1",
        foreground=COLORS["text"],
        font=F_BODY,
        borderwidth=0,
        padding=(14, 7),
    )
    s.map("Secondary.TButton", background=[("active", "#D6DAE6")])

    s.configure(
        "Danger.TButton",
        background="#FEE2E2",
        foreground=COLORS["danger"],
        font=F_BODY,
        borderwidth=0,
        padding=(12, 6),
    )
    s.map("Danger.TButton", background=[("active", "#FECACA")])

    s.configure(
        "Ghost.TButton",
        background=COLORS["bg"],
        foreground=COLORS["primary"],
        font=F_BODY,
        borderwidth=0,
        padding=(8, 4),
    )
    s.map("Ghost.TButton", background=[("active", "#E8EAF1")])

    s.configure("TEntry", fieldbackground=COLORS["card"], borderwidth=1, relief="solid", padding=6)

    s.configure("Card.TCheckbutton", background=COLORS["card"], foreground=COLORS["text"], font=F_BODY)
    s.configure("Card.TRadiobutton", background=COLORS["card"], foreground=COLORS["text"], font=F_BODY)


def make_scrollable(parent, bg=None):
    bg = bg or COLORS["bg"]

    wrap = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(wrap, bg=bg, highlightthickness=0)
    sb = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)

    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    inner = tk.Frame(canvas, bg=bg)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

    def _wheel(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(int(-event.delta / 120), "units")

    def _bind(_):
        canvas.bind_all("<MouseWheel>", _wheel)
        canvas.bind_all("<Button-4>", _wheel)
        canvas.bind_all("<Button-5>", _wheel)

    def _unbind(_):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)

    return wrap, inner


def auto_wrap(label, padding=40):
    label.bind("<Configure>", lambda e: label.config(wraplength=max(120, e.width - padding)))


def Card(parent):
    outer = tk.Frame(parent, bg=COLORS["bg"])
    inner = tk.Frame(
        outer,
        bg=COLORS["card"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
    )
    inner.pack(fill="both", expand=True)
    return outer, inner


def make_bottom(parent):
    bottom = tk.Frame(parent, bg=COLORS["bg"])
    bottom.pack(side="bottom", fill="x", padx=40, pady=(0, 20))
    return bottom

# ============================================================
# Talent Editor
# ============================================================

class TalentEditor(tk.Toplevel):
    SCENARIO_TAGS = ["citywalk", "dragonfire", "flyaway", "loneblade"]
    RARITY_OPTIONS = [
        ("negative", "负面"), ("common", "普通"),
        ("rare", "稀有"), ("legendary", "传奇"), ("wildcard", "特殊"),
    ]
    #MODE_OPTIONS = [("Normal", "普通"), ("Horni", "性压抑")]
    MODE_OPTIONS = [("Normal", "普通"), ("store", "通马桶模式")]

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("自定义天赋编辑器")
        self.geometry("760x780")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)

        self.talents = load_user_talents()
        self.editing_index = None

        self.name_var = tk.StringVar()
        self.rarity_var = tk.StringVar(value="common")
        self.mode_var = tk.StringVar(value="Normal")
        self.scenario_any_var = tk.BooleanVar(value=True)
        self.scenario_vars = {tag: tk.BooleanVar() for tag in self.SCENARIO_TAGS}
        self.modifier_rows = []

        self._build()
        self._reset_form()
        self._refresh_list()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(header, text="✨ 自定义天赋编辑器",
                 bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD).pack(anchor="w")

        info_lbl = tk.Label(
            header,
            text="自定义天赋将与默认天赋池合并参与抽取。修改后立即生效，文件保存在用户目录。",
            bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL, justify="left",
        )
        info_lbl.pack(anchor="w", fill="x", pady=(0, 8))
        auto_wrap(info_lbl)

        wrap, body = make_scrollable(self)
        wrap.pack(fill="both", expand=True, padx=16, pady=4)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, pady=4)

        # === 列表 ===
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        head = tk.Frame(card, bg=COLORS["card"])
        head.pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(head, text="已保存天赋", bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(side="left")

        ttk.Button(head, text="🗑 全部清空",
                   style="Danger.TButton", command=self._clear_all).pack(side="right")

        self.list_frame = tk.Frame(card, bg=COLORS["card"])
        self.list_frame.pack(fill="x", padx=14, pady=(0, 12))

        # === 表单 ===
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(card, text="新建 / 编辑", bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(12, 6)
        )

        form = tk.Frame(card, bg=COLORS["card"])
        form.pack(fill="x", padx=14, pady=(0, 12))
        form.grid_columnconfigure(1, weight=1)

        def _label(r, txt):
            tk.Label(form, text=txt, bg=COLORS["card"], fg=COLORS["text"],
                     font=F_BODY).grid(row=r, column=0, sticky="ne",
                                        padx=(0, 10), pady=4)

        _label(0, "名称")
        ttk.Entry(form, textvariable=self.name_var).grid(row=0, column=1, sticky="we", pady=4)

        _label(1, "稀有度")
        rar_frame = tk.Frame(form, bg=COLORS["card"])
        rar_frame.grid(row=1, column=1, sticky="w", pady=4)
        for code, label in self.RARITY_OPTIONS:
            ttk.Radiobutton(rar_frame, text=label, variable=self.rarity_var,
                            value=code, style="Card.TRadiobutton").pack(side="left", padx=4)

        _label(2, "模式")
        mode_frame = tk.Frame(form, bg=COLORS["card"])
        mode_frame.grid(row=2, column=1, sticky="w", pady=4)
        for code, label in self.MODE_OPTIONS:
            ttk.Radiobutton(mode_frame, text=label, variable=self.mode_var,
                            value=code, style="Card.TRadiobutton").pack(side="left", padx=4)

        _label(3, "场景")
        sc_frame = tk.Frame(form, bg=COLORS["card"])
        sc_frame.grid(row=3, column=1, sticky="w", pady=4)
        ttk.Checkbutton(
            sc_frame, text="any（全部）", variable=self.scenario_any_var,
            style="Card.TCheckbutton", command=self._toggle_any,
        ).pack(side="left", padx=4)
        for tag in self.SCENARIO_TAGS:
            ttk.Checkbutton(
                sc_frame, text=tag, variable=self.scenario_vars[tag],
                style="Card.TCheckbutton",
                command=lambda: self.scenario_any_var.set(False),
            ).pack(side="left", padx=4)

        _label(4, "描述")
        self.desc_text = tk.Text(form, height=2, font=F_BODY, bg="#FAFBFE",
                                  relief="flat", highlightbackground=COLORS["border"],
                                  highlightthickness=1, wrap="word")
        self.desc_text.grid(row=4, column=1, sticky="we", pady=4)

        _label(5, "叙事")
        self.narr_text = tk.Text(form, height=2, font=F_BODY, bg="#FAFBFE",
                                  relief="flat", highlightbackground=COLORS["border"],
                                  highlightthickness=1, wrap="word")
        self.narr_text.grid(row=5, column=1, sticky="we", pady=4)

        _label(6, "属性加成")
        mod_outer = tk.Frame(form, bg=COLORS["card"])
        mod_outer.grid(row=6, column=1, sticky="we", pady=4)

        self.mod_container = tk.Frame(mod_outer, bg=COLORS["card"])
        self.mod_container.pack(fill="x")

        ttk.Button(
            mod_outer, text="+ 添加加成", style="Ghost.TButton",
            command=lambda: self._add_modifier_row(),
        ).pack(anchor="w", pady=4)

        tip = tk.Label(
            form,
            text="加成示例：+1d6  /  -1d2*5  /  +10  /  -2*5",
            bg=COLORS["card"], fg=COLORS["muted"], font=F_SMALL,
        )
        tip.grid(row=7, column=1, sticky="w", pady=(0, 6))

        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 14))

        ttk.Button(btn_row, text="清空表单", style="Secondary.TButton",
                   command=self._reset_form).pack(side="left")
        ttk.Button(btn_row, text="💾 保存", style="Primary.TButton",
                   command=self._save_current).pack(side="right")

    def _toggle_any(self):
        if self.scenario_any_var.get():
            for v in self.scenario_vars.values():
                v.set(False)

    def _add_modifier_row(self, attr="STR", dice="+1d6"):
        row = tk.Frame(self.mod_container, bg=COLORS["card"])
        row.pack(fill="x", pady=2)

        attrs_all = ["STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "CRE", "LUCK",
                     "LIB", "TEC", "END", "SEN", "LOV", "EXP", "HMR"]

        attr_var = tk.StringVar(value=attr)
        ttk.Combobox(row, textvariable=attr_var, values=attrs_all,
                     width=8, state="readonly").pack(side="left", padx=2)

        dice_var = tk.StringVar(value=dice)
        ttk.Entry(row, textvariable=dice_var, width=18).pack(side="left", padx=2)

        ttk.Button(row, text="−", style="Danger.TButton", width=3,
                   command=lambda: self._remove_modifier_row(row)).pack(side="left", padx=2)

        self.modifier_rows.append((attr_var, dice_var, row))

    def _remove_modifier_row(self, row):
        for entry in list(self.modifier_rows):
            if entry[2] is row:
                self.modifier_rows.remove(entry)
                break
        row.destroy()

    def _reset_form(self):
        self.editing_index = None
        self.name_var.set("")
        self.rarity_var.set("common")
        self.mode_var.set("Normal")
        self.scenario_any_var.set(True)
        for v in self.scenario_vars.values():
            v.set(False)
        self.desc_text.delete("1.0", "end")
        self.narr_text.delete("1.0", "end")
        for _, _, row in self.modifier_rows:
            row.destroy()
        self.modifier_rows = []

    def _load_for_edit(self, idx):
        self._reset_form()
        t = self.talents[idx]
        self.editing_index = idx
        self.name_var.set(t.get("name", ""))
        self.rarity_var.set(t.get("rarity", "common"))
        self.mode_var.set(t.get("mode", "Normal"))

        scs = t.get("scenarios", ["any"])
        if "any" in scs:
            self.scenario_any_var.set(True)
        else:
            self.scenario_any_var.set(False)
            for tag in scs:
                if tag in self.scenario_vars:
                    self.scenario_vars[tag].set(True)

        self.desc_text.insert("1.0", t.get("desc", ""))
        self.narr_text.insert("1.0", t.get("narrative", ""))
        for attr, dice in t.get("modifiers", []):
            self._add_modifier_row(attr, dice)

    def _save_current(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("提示", "请填写天赋名称。")
            return

        modifiers = []
        for attr_var, dice_var, _ in self.modifier_rows:
            attr = attr_var.get().strip()
            dice = dice_var.get().strip()
            if not attr or not dice:
                continue
            try:
                roll_dice(dice)
            except Exception:
                messagebox.showwarning(
                    "提示",
                    f"加成「{attr} {dice}」无法解析。例：+1d6, -2*5, +1d2*5",
                )
                return
            modifiers.append([attr, dice])

        if self.scenario_any_var.get():
            scenarios = ["any"]
        else:
            scenarios = [tag for tag, v in self.scenario_vars.items() if v.get()]
            if not scenarios:
                messagebox.showwarning("提示", "请至少选择一个场景，或勾选 any。")
                return

        talent = {
            "name": name,
            "rarity": self.rarity_var.get(),
            "mode": self.mode_var.get(),
            "scenarios": scenarios,
            "desc": self.desc_text.get("1.0", "end").strip(),
            "narrative": self.narr_text.get("1.0", "end").strip(),
            "modifiers": modifiers,
            "user_defined": True,
        }

        if self.editing_index is not None:
            self.talents[self.editing_index] = talent
        else:
            self.talents.append(talent)

        save_user_talents(self.talents)
        self._reset_form()
        self._refresh_list()
        messagebox.showinfo("已保存", f"天赋「{name}」已保存。")

    def _delete(self, idx):
        t = self.talents[idx]
        if not messagebox.askyesno("删除", f"确定删除天赋「{t.get('name','')}」吗？"):
            return
        del self.talents[idx]
        save_user_talents(self.talents)
        self._refresh_list()

    def _clear_all(self):
        if not self.talents:
            return
        if not messagebox.askyesno("清空", "确定清空所有自定义天赋吗？"):
            return
        self.talents = []
        save_user_talents(self.talents)
        self._refresh_list()

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.talents:
            tk.Label(self.list_frame, text="（暂无自定义天赋）",
                     bg=COLORS["card"], fg=COLORS["muted"],
                     font=F_SMALL).pack(anchor="w", pady=8)
            return

        for idx, t in enumerate(self.talents):
            row = tk.Frame(self.list_frame, bg=COLORS["card"])
            row.pack(fill="x", pady=3)

            cfg = RARITY_CONFIG.get(t.get("rarity", "common"), RARITY_CONFIG["common"])

            tk.Label(row, text=cfg["label"], bg=cfg["bg"], fg=cfg["color"],
                     font=(FONT_FAM, 9, "bold"), padx=8, pady=2).pack(side="left")

            mode_text = "(普通)" if t.get("mode") == "Normal" else "(性压抑)"
            scs = "/".join(t.get("scenarios", ["any"]))

            tk.Label(row, text=f"  {t.get('name','')}  {mode_text}  ·  {scs}",
                     bg=COLORS["card"], fg=COLORS["text"],
                     font=F_BODY).pack(side="left")

            ttk.Button(row, text="删除", style="Danger.TButton",
                       command=lambda i=idx: self._delete(i)).pack(side="right", padx=2)
            ttk.Button(row, text="编辑", style="Ghost.TButton",
                       command=lambda i=idx: self._load_for_edit(i)).pack(side="right", padx=2)


# ============================================================
# Global System Prompt Editor
# ============================================================

class GlobalPromptEditor(tk.Toplevel):
    """编辑会被自动追加到所有新角色 system prompt 末尾的全局指令。"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("默认追加提示词")
        self.geometry("680x540")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)

        tk.Label(self, text="🛠 默认追加提示词",
                 bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD).pack(
            anchor="w", padx=16, pady=(14, 4)
        )

        info = ("这里写的内容会自动追加到每次新建角色时的系统提示词末尾。\n"
                "适合写写作风格、长度限制、特定禁忌等通用要求。\n"
                "如果只想改单局，请在游戏中点「🛠 编辑系统提示词」。")
        lbl = tk.Label(self, text=info, bg=COLORS["bg"],
                       fg=COLORS["subtext"], font=F_SMALL, justify="left")
        lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
        auto_wrap(lbl)

        cfg = load_config()
        current = cfg.get("extra_system_prompt", "")

        self.txt = scrolledtext.ScrolledText(self, font=F_MONO, wrap="word", height=18)
        self.txt.pack(fill="both", expand=True, padx=16, pady=8)
        self.txt.insert("1.0", current)

        bottom = tk.Frame(self, bg=COLORS["bg"])
        bottom.pack(fill="x", padx=16, pady=(0, 16))

        def save():
            text = self.txt.get("1.0", "end").rstrip()
            cfg = load_config()
            cfg["extra_system_prompt"] = text
            save_config(cfg)
            messagebox.showinfo("已保存", "默认追加提示词已保存。")
            self.destroy()

        def clear():
            self.txt.delete("1.0", "end")

        ttk.Button(bottom, text="保存", style="Primary.TButton",
                   command=save).pack(side="right")
        ttk.Button(bottom, text="取消", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=8)
        ttk.Button(bottom, text="清空", style="Danger.TButton",
                   command=clear).pack(side="left")
# ============================================================
# Main App
# ============================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"AI人生模拟器 {VERSION}")
        self._auto_size_window()
        self.minsize(560, 640)
        self.resizable(True, True)
        #self.configure(bg=COLORS["bg"])
        #apply_style(self)
        sv_ttk.set_theme("light")

        self.app_state = {"client": None, "model": None, "connected": False}
        self.disclaimer_accepted = False

        self.reset_character()

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (
            DisclaimerPage,
            APIPage,
            ScenePage,
            IdentityPage,
            StoreKeeperPage,
            TalentPage,
            AttributePage,
            FineTrackerPage,
            ConfirmPage,
            GamePage,
            SummaryPage,
        ):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("DisclaimerPage")

    def _auto_size_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        target_h = int(sh * 0.85)
        target_w = int(target_h * 3 / 4)

        if target_w > int(sw * 0.7):
            target_w = int(sw * 0.7)
            target_h = int(target_w * 4 / 3)

        target_w = max(target_w, 620)
        target_h = max(target_h, 720)

        x = max(0, (sw - target_w) // 2)
        y = max(0, (sh - target_h) // 2 - 30)
        self.geometry(f"{target_w}x{target_h}+{x}+{y}")

    def fine_initial_points(self):
        """
        Fine Mode: 18岁以后，每 1 岁获得 1 次自由成长检定。
        如果 start_age < 18，返回 0，跳过分配页面。
        """
        c = self.character
        if not c.get("fine_enabled"):
            return 0

        fs = c.get("fine_settings", {})
        try:
            start_age = float(fs.get("start_age", 0))
        except Exception:
            start_age = 0

        return max(0, int(start_age) - 18)

    def configure_fine_mode(self, enabled, start_age=0, end_age=80, timestamp="year"):
        """
        Stores Fine Mode settings on character.
        Fine Mode is a rules modifier, not a content mode.
        """
        c = self.character

        if not enabled:
            finedata.clear_character(c)
            return

        finedata.configure_character(
            c,
            {
                "start_age": start_age,
                "end_age": end_age,
                "timestamp": timestamp,
            },
        )

        # Reset any previous tracker allocation since the start age may have changed.
        c["initial_trackers"] = {}

    def reset_character(self):
        self.character = {
            "scene_id": None,
            "scene_name": None,
            "scene_desc": "",
            "scenario_tag": "citywalk",
            "has_compulsory_edu": False,

            "gender": None,
            "race": "人类",
            "extra_info": "",

            "content_mode": CONTENT_NORMAL,
            "difficulty": DIFF_STANDARD,
            "fast_mode": False,

            "fine_enabled": False,
            "fine_settings": {},
            "time_config_override": {},
            "initial_trackers": {},

            # Old compatibility key.
            "mode": CONTENT_NORMAL,

            "talents": [],
            "talent_rolls_used": 0,
            "attributes": {},
            "luck": 0,
            "luck_rolls_used": 0,

            "backstory": "",
            "final_attributes": {},
            "roll_log": [],

            "hp": 0,
            "max_hp": 0,

            "alive": True,
            "cause_of_death": None,

            "messages": [],
            "summary": {},
        }

    def mode_data(self):
        return get_data_module(self.character)

    def sync_compat_mode(self):
        c = self.character
        c["mode"] = c.get("content_mode", CONTENT_NORMAL)

    def init_attributes_for_mode(self):
        m = self.mode_data()
        self.character["attributes"] = {a: 30 for a in m.ATTRIBUTES}

    def show_page(self, name):
        page = self.pages[name]
        if hasattr(page, "on_show"):
            page.on_show()
        page.tkraise()

    def reset_all(self, ask=True):
        if ask and not messagebox.askyesno(
            "重置游戏",
            "确定要重置所有进度并返回首页吗？\n（API 设置不会丢）",
        ):
            return

        self.reset_character()

        game = self.pages["GamePage"]
        game.initialized = False
        game.clear_history()
        game.clear_control()

        if not self.disclaimer_accepted:
            self.show_page("DisclaimerPage")
        elif self.app_state.get("connected"):
            self.show_page("ScenePage")
        else:
            self.show_page("APIPage")

    def export_current(self):
        self.pages["SummaryPage"].export_to_txt()

    # ----------------------------------------------------------------
    # Save / Load (new in v0.5.1)
    # ----------------------------------------------------------------

    def save_game_state(self):
        """
        Save the full character state + history text to a JSON file.
        Available any time after the game has started.
        """
        c = self.character

        if not c.get("messages"):
            messagebox.showinfo("提示", "游戏尚未开始，没有可保存的内容。")
            return

        try:
            history = self.pages["GamePage"].history_text.get("1.0", "end")
        except Exception:
            history = ""

        state = {
            "version": VERSION,
            "saved_at": datetime.datetime.now().isoformat(),
            "character": c,
            "history_text": history,
        }

        try:
            age = self.mode_data().get_character_age(c)
        except Exception:
            age = 0

        try:
            age_str = f"{int(age)}"
        except Exception:
            age_str = "?"

        default_name = (
            f"重开手账存档_{c.get('scene_name', '')}"
            f"_{age_str}岁_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=default_name,
            filetypes=[("JSON 存档", "*.json"), ("所有文件", "*.*")],
            title="保存游戏存档",
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2, default=str)
            messagebox.showinfo("存档成功", f"已保存到：\n{path}")
        except Exception as e:
            messagebox.showerror("存档失败", f"出错了：{e}")

    def load_game_state(self):
        """
        Load a saved JSON state and resume the game on GamePage.
        """
        if not self.app_state.get("connected"):
            if not messagebox.askyesno(
                "API 未连接",
                "尚未连接 API。\n你仍可以导入存档查看历史，但下一次推演会失败。\n\n要继续吗？",
            ):
                return

        path = filedialog.askopenfilename(
            filetypes=[("JSON 存档", "*.json"), ("所有文件", "*.*")],
            title="导入游戏存档",
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as e:
            messagebox.showerror("读取失败", f"无法读取存档：{e}")
            return

        if not isinstance(state, dict) or "character" not in state:
            messagebox.showerror("读取失败", "存档格式不正确。")
            return

        loaded_char = state["character"]
        if not isinstance(loaded_char, dict):
            messagebox.showerror("读取失败", "存档中 character 字段格式不正确。")
            return

        # Merge into the default skeleton so missing keys won't crash.
        self.reset_character()
        self.character.update(loaded_char)
        self.sync_compat_mode()

        game = self.pages["GamePage"]
        game.initialized = True
        game.clear_control()

        # Build right panel for the loaded mode.
        game.build_stats_panel()
        game.refresh_panel()

        # Restore the textual history.
        history_text = state.get("history_text", "")
        game.history_text.config(state="normal")
        game.history_text.delete("1.0", "end")
        game.history_text.insert("1.0", history_text)
        game.history_text.see("end")
        game.history_text.config(state="disabled")

        # Update title.
        c = self.character
        m = self.mode_data()
        try:
            if c.get("alive", True):
                game.title_label.config(text=m.format_time(c))
            else:
                game.title_label.config(text=f"💀 享年 {m.get_character_age(c)} 岁")
        except Exception:
            pass

        # Decide what controls to show.
        if not c.get("alive", True):
            if c.get("summary"):
                self.show_page("SummaryPage")
                messagebox.showinfo("导入成功", "存档显示游戏已经结束，已直接载入总结页面。")
                return
            game.handle_death()
        elif game.should_fast_end():
            game.handle_fast_end()
        elif game.should_fine_end():
            game.handle_fine_end()
        else:
            last_choices = self._extract_last_choices()
            if last_choices:
                game.show_choices(last_choices)
            else:
                game.show_next_button()

        self.show_page("GamePage")
        messagebox.showinfo("导入成功", "已恢复游戏进度。")

    def _extract_last_choices(self):
        """
        Look at the most recent assistant JSON in messages.
        If it offered choices, return them so we can rebuild the choice UI.
        """
        msgs = self.character.get("messages", [])
        for msg in reversed(msgs):
            if msg.get("role") == "assistant":
                try:
                    data = parse_ai_json(msg.get("content", ""))
                    if data.get("has_choice") and data.get("choices"):
                        return data["choices"]
                except Exception:
                    pass
                return None
        return None


# ============================================================
# Top bar
# ============================================================

class TopBar(tk.Frame):
    def __init__(self, parent, app, title="", subtitle="", show_save=True):
        super().__init__(
            parent,
            bg=COLORS["card"],
            height=64,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        self.pack_propagate(False)

        left = tk.Frame(self, bg=COLORS["card"])
        left.pack(side="left", fill="y", padx=20)

        tk.Label(
            left,
            text=title,
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=(FONT_FAM, 14, "bold"),
        ).pack(anchor="w", pady=(10, 0))

        if subtitle:
            tk.Label(
                left,
                text=subtitle,
                bg=COLORS["card"],
                fg=COLORS["subtext"],
                font=F_SMALL,
            ).pack(anchor="w")

        right = tk.Frame(self, bg=COLORS["card"])
        right.pack(side="right", fill="y", padx=15)

        ttk.Button(
            right,
            text="🔄 重置",
            style="Danger.TButton",
            command=app.reset_all,
        ).pack(side="right", pady=14)

        ttk.Button(
            right,
            text="📄 导出",
            style="Ghost.TButton",
            command=app.export_current,
        ).pack(side="right", pady=14, padx=4)

        if show_save:
            ttk.Button(
                right,
                text="💾 存档",
                style="Ghost.TButton",
                command=app.save_game_state,
            ).pack(side="right", pady=14, padx=4)


# ============================================================
# 0. Disclaimer
# ============================================================
class DisclaimerPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        TopBar(self, app, title="⚠️ 重要提示", subtitle="step 0 · 请先读完").pack(side="top", fill="x")

        bottom = make_bottom(self)
        self.btn_next = ttk.Button(
            bottom,
            text="同意并继续 →",
            style="Primary.TButton",
            state="disabled",
            command=self._go,
        )
        self.btn_next.pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=30)

        outer, card = Card(inner)
        outer.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="免责声明",
            bg=COLORS["card"],
            fg=COLORS["danger"],
            font=F_HEAD,
        ).pack(anchor="w", padx=24, pady=(20, 10))

        # ============ 1. 免责声明正文 ============
        disclaimer_text = (
            "本程序是部分参考 https://re.maa-ai.com/ 的精神本地版，作者参考了大致的架构并加入了很多自己想要的功能。\n\n"
            "网页版体验更好喵。\n\n"
            "本程序的用户（以下简称你）可以通过切换不同的API来达到使用不同LLM来玩的效果。同时，本程序加入了更多的用户编辑功能。\n\n"
            "这个小程序会需要你填入你的 API 密钥，这是很重要的东西。\n\n"
            "因为这个程序本身基本没有安全防护，而且开放了很多用户编辑自由度，进行恶意修改再重新传播相当简单。请仔细辨别你收到的这一份是否有被恶意修改。\n\n"
            "如果你无法确认这个程序的来源，作者建议你跑一遍杀毒软件或virustotal。（但真的藏有小巧思的话你看到这句话时已经迟了喵。）\n\n"
            "无论如何，作者强烈建议你重新创建一个新的、有消费限制的 API。\n\n"
            "如果你不知道怎么设置 API 限额，建议不要使用此程序。\n\n"
            "本程序本体完全免费。如果你花了钱，恭喜你被坑了。（API自费）\n\n"
            "本程序为玩具，作者不对任何因使用本程序导致的损失负责。\n\n"
            "本程序假设用户为心智完善、情绪稳定的成年人。请确认你是这样的正常成年人。\n\n"
            "本程序已采用 CC0 1.0 (公有领域贡献) 协议释出。\n"
            "作者已放弃所有版权，你可以自由复制、修改、分发，均无需征求许可。\n\n\n\n"
                        "此致，敬礼！\n"
            "               KPV_ZUBT"
        )

        disc_lbl = tk.Label(
            card, text=disclaimer_text, bg=COLORS["card"], fg=COLORS["text"],
            font=F_BODY, justify="left"
        )
        disc_lbl.pack(anchor="w", fill="x", padx=24, pady=(0, 16))
        auto_wrap(disc_lbl)

        # ============ 2. 确认打勾的格子（插在中间） ============
        self.agree_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            card,
            text="我已满十八岁；我确认了此程序的来源；我将会使用有消费上限的、新的 API。",
            variable=self.agree_var,
            style="Card.TCheckbutton",
            command=self._toggle,
        ).pack(anchor="w", padx=24, pady=(8, 20))

        # ============ 3. 分割线与更新日志 ============
        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=24, pady=10)
        
        tk.Label(
            card, text="📜 更新日志", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB
        ).pack(anchor="w", padx=24, pady=(10, 4))

        changelog_text = (
            f"{VERSION} 更新：\n"
            "- 健康发行版，删除和隐藏了部分不合适的内容。\n\n"
            "v0.7.1 RUNGORUN 更新：\n"  
            "- 添加了设置自动保存功能。现在许多设置会自动保存了，你下一次打开游戏不需要重新调试一遍。\n"
            "- 这个功能其实0.7.0就做好了。但是我觉得它太伟大了，不亚于山顶洞人第一次发现石头可以丢。\n"
            "- 所以我给了它一个专门的版本供在更新日志里面。\n"
            "- 优化了UI显示，将软件界面从2016年升级到了2018年。\n\n"
            "v0.7.0 INVITE 更新：\n"   
            "- 正式添加了CC0的协议释出。\n"
            "- 添加了通过传统派3d6*5骰点来配置属性的功能。此功能可以用于所有模式。\n"
            "- 添加了高级功能：省token模式。可以降低一些因为上下文产生的消费。\n"
            "- 添加了高级功能：检查发送给API的内容。方便调试和检查token用量。\n"
            "- 优化了测试模式，添加无上限选择天赋和无限加自由属性点的功能。\n"
            "- 优化了微调模式，现在选择起始岁数会自动根据你的基础数值进行1-18岁属性成长的演算。\n"
            "- 优化了通马桶模式，现在所有的浮动属性都是基于d100并且对游戏有实际影响了。\n"
            "- 优化了返回报错内容，现在里面包含api的话会自动删除。少量提高安全性。\n"
            "- 将JUNIPER版本中更新的计算方法适配进了所有模式中。\n"
            "- 修复了微调模式中“周”的时间单位无法被使用的问题。\n\n"
            "v0.6.9/0.7.0 pre-patch EVOLUTIONERA 更新：\n"   
            "- 添加了AI返回报错时，可以查看返回内容的选项。\n"
            "- 重做了所有名声/资产等属性，现在它们都是基于100的可检定属性了。\n"
            "- 重做了0-18岁的义务教育，资产成长等。现在CRE将会是很重要的属性了。\n"
            "- 优化API保存方法为keyring加密。少量提高安全性。\n"
            "- 优化API链接界面。现在勾选“显示key”的时候，中间的六位字符不会被抓取。少量提高安全性。\n"
            "- 优化API链接界面。可同时保存的api数量减少为两个。\n"
            "- 修复了第一次打开特质编辑器无法看到已有特质的bug。\n"
            "- 通马桶模式暂时还没有做d100适配的浮动属性。\n\n"
            "v0.6.3 YUBIKIRI 更新：\n"   
            "- 修复了BANYAN版本中主动行动（又）无法实际确认行动的问题。\n"
            "- 修复了通马桶模式中出现AttributeError的问题。\n\n"
            "v0.6.2 SAIKA 更新：\n"           
            "- 添加了可以让用户在正常模式中是否启用骰子功能的选择项。\n"
            "- 添加了针对低级自动爬虫抓取本地加密密匙的防护。少量提高安全性。\n"
            "- 修复了POPLAR版本中骰子功能超出代码定义范围的bug。\n\n"
            "v0.6.1 IHATETOTELLYOU 更新：\n"
            "- 对所有模式里的选择检定都做了CARNATION更新中的成功/失败检定功能适配。\n"
            "- 小幅上调所有模式中的自由属性点至180点。\n"
            "- 优化了通马桶模式的技术细节。\n"
            "- 对四个情景都进行了通马桶模式的天赋池适配。\n\n"
            "v0.6.0 REVERSE 更新：\n"
            "- 添加了我要通马桶模式。现在你可以扮演一名神秘npc来接取和解决委托了。\n"
            "- 修复了主动行动无法实际确认行动的问题。\n"
            "- 修复了数个其他bug。\n"
            "- 优化api保存方法为本地加密。少量提高安全性。\n\n"
            "v0.5.5 UTOPIOSPHERE 更新：\n"
            "- 添加了自己填写天赋的能力。\n"
            "- 添加了回合中主动行动的选项。\n"
            "- api链接QOL优化，现在你可以同时保存三个不同的api了。\n"
            "- 优化了界面至clamshell，软件年代从1996进化到了2016。\n"
            "- 修复了AI报错后重试会推进时间线的bug。\n\n"
            "v0.5.1 PLATINUM 更新：\n"
            "- 修复了 Fine Mode 配置时间轴错误的 bug。\n"
            "- 修复了时间刻度显示一直是英文键名的 bug。\n"
            "- 修复了IdentityPage 的「上一步」会跳到错误页面的 bug。\n\n"
            "v0.5.0 UNDO 更新：\n"
            "- 添加了导入记录功能，配合之前的导出记录功能可以实现保存了。\n"
            "- 添加了微调模式，现在你可以调整每回合的时间跨度，起始年龄和结束年龄了！\n"
            "- 铁人模式/测试模式/普通模式现在改为在故事设定之上的调整条件。\n"
            "- QOL改善和底层代码优化。\n\n"
            "v0.4.1 LIGHTPOLLUTION 更新：\n"
            "- 修改了天赋系统-从单纯的抽三变为了抽六选三。\n"
            "- 在一局人生结束之后和游戏进行时都增加了导出记录为.txt的功能。\n"
            "- 小幅上调了两种模式下的属性点数量。\n"
            "- 微调了AI给予选项的频率。\n\n"
            "v0.4.0 NINEPOINTEIGHT 更新：\n"
            "- 第一个新架构的版本\n\n\n\n\n\n\n\n\n\n"
            "我永远喜欢UMP45"
        )

        log_lbl = tk.Label(
            card, text=changelog_text, bg=COLORS["card"], fg=COLORS["subtext"],
            font=F_SMALL, justify="left"
        )
        log_lbl.pack(anchor="w", fill="x", padx=24, pady=(0, 20))
        auto_wrap(log_lbl)

    def _toggle(self):
        self.btn_next.config(state="normal" if self.agree_var.get() else "disabled")

    def _go(self):
        self.app.disclaimer_accepted = True
        self.app.show_page("APIPage")
        


import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
# (Assuming OpenAI, load_config, save_config, Card, TopBar, etc. are imported above)

import os
import json
from cryptography.fernet import Fernet

import keyring
import keyring.errors

# ============================================================
# 1. API 页面 (使用原生 Keyring 安全存储)
# ============================================================
def mask_api_key(key):
    """安全脱敏函数：隐藏 10~16 位，如果太短则隐藏中间"""
    if not key:
        return ""
    if len(key) > 16:
        # [:9] 截取前9位 (index 0~8)，[16:] 保留第17位及以后
        return key[:9] + "••••••" + key[16:]
    elif len(key) > 6:
        return key[:3] + "••••••" + key[-3:]
    else:
        return "••••••"
    
# ============================================================
# 1. API 页面 (脱敏防护 + 系统原生凭据管理)
# ============================================================
class APIPage(tk.Frame):
    NUM_SLOTS = 2
    KEYRING_SERVICE = "AILifeRemake"

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        TopBar(
            self, app,
            title=f"🎮 AI 人生重开手账 {VERSION}",
            subtitle="step 1 · 连接你的 AI（可保存 2 套配置）",
            show_save=False,
        ).pack(side="top", fill="x")
        
        bottom = make_bottom(self)
        ttk.Button(
            bottom, text="清除已保存的 API 信息",
            style="Ghost.TButton", command=self.clear_saved,
        ).pack(side="left")
        self.btn_next = ttk.Button(
            bottom, text="下一步 →",
            style="Primary.TButton", state="disabled",
            command=lambda: self.app.show_page("ScenePage"),
        )
        self.btn_next.pack(side="right")
        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)
        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)
        outer, card = Card(inner)
        outer.pack(fill="x")
        tk.Label(card, text="API 连接", bg=COLORS["card"], fg=COLORS["text"], font=F_HEAD).pack(
            anchor="w", padx=24, pady=(20, 4)
        )
        lbl = tk.Label(
            card,
            text=("可以保存最多 2 套 API 配置（OpenAI 兼容）。\n"
                  "点哪个槽的「测试并启用」，最后成功的那一槽就是当前实际使用的模型。"),
            bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, justify="left",
        )
        lbl.pack(anchor="w", fill="x", padx=24, pady=(0, 16))
        auto_wrap(lbl)
        
        # ---- 加载配置 ----
        cfg = load_config()
        
        if "slots" not in cfg:
            cfg["slots"] = [{
                "base_url": cfg.get("base_url", "https://api.deepseek.com/v1"),
                "model": cfg.get("model", "deepseek-chat"),
            }]
            cfg["active_slot"] = 0
            
        slots = list(cfg.get("slots", []))
        
        # 从操作系统 Keyring 中读取真实的 API Key 存入内存，UI 栏位只显示打码版
        self.real_keys = []
        for i, slot in enumerate(slots):
            os_key = keyring.get_password(self.KEYRING_SERVICE, f"api_key_slot_{i}")
            os_key = os_key if os_key else ""
            self.real_keys.append(os_key)
            slot["api_key"] = mask_api_key(os_key) # <--- UI 栏只显示这串掩码
            
        while len(slots) < self.NUM_SLOTS:
            self.real_keys.append("")
            slots.append({
                "base_url": "https://api.deepseek.com/v1",
                "api_key": "",
                "model": "deepseek-chat",
            })
            
        self.slot_widgets = []
        for i in range(self.NUM_SLOTS):
            self.slot_widgets.append(self._build_slot_card(inner, i, slots[i]))
            
        # ---- 控制区 ----
        outer, card = Card(inner)
        outer.pack(fill="x", pady=10)
        ctl = tk.Frame(card, bg=COLORS["card"])
        ctl.pack(fill="x", padx=18, pady=12)
        self.remember_var = tk.BooleanVar(value=cfg.get("remember", True))
        ttk.Checkbutton(
            ctl, text="记住所有 API 配置（API Key 将通过系统原生凭据管理器加密保存）",
            variable=self.remember_var, style="Card.TCheckbutton",
        ).pack(side="left")
        self.status = tk.Label(
            card, text="（还没测试）", bg=COLORS["card"],
            fg=COLORS["muted"], font=F_SMALL,
        )
        self.status.pack(anchor="w", padx=18, pady=(0, 12))
        
    def _build_slot_card(self, parent, idx, slot_data):
        outer, card = Card(parent)
        outer.pack(fill="x", pady=8)
        head = tk.Frame(card, bg=COLORS["card"])
        head.pack(fill="x", padx=18, pady=(12, 4))
        tk.Label(head, text=f"API链接 #{idx + 1}", bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(side="left")
        active_lbl = tk.Label(head, text="", bg=COLORS["card"],
                              fg=COLORS["success"], font=F_SMALL)
        active_lbl.pack(side="right")
        f = tk.Frame(card, bg=COLORS["card"])
        f.pack(padx=18, pady=4, fill="x")
        f.grid_columnconfigure(1, weight=1)
        
        def _row(label, r, default="", show=None):
            tk.Label(f, text=label, bg=COLORS["card"], fg=COLORS["text"],
                     font=F_BODY).grid(row=r, column=0, sticky="e",
                                        pady=4, padx=(0, 12))
            e = ttk.Entry(f, width=50)
            if show:
                e.config(show=show)
            if default:
                e.insert(0, default)
            e.grid(row=r, column=1, pady=4, sticky="we")
            return e
            
        e_url = _row("Base URL", 0, default=slot_data.get("base_url", ""))
        e_key = _row("API Key", 1, default=slot_data.get("api_key", ""), show="*")
        e_model = _row("模型名", 2, default=slot_data.get("model", ""))
        show_var = tk.BooleanVar(value=False)
        
        def toggle_show():
            # 这里就算点开了显示的也只会是类似 sk-12345••••••789 这种脱敏的 Key
            e_key.config(show="" if show_var.get() else "*")
            
        ttk.Checkbutton(
            f, text="显示 Key", variable=show_var,
            style="Card.TCheckbutton", command=toggle_show,
        ).grid(row=3, column=1, sticky="w", pady=2)
        
        ttk.Button(
            card, text="测试并启用此 API", style="Primary.TButton",
            command=lambda i=idx: self.test_slot(i),
        ).pack(anchor="e", padx=18, pady=(4, 12))
        return {"url": e_url, "key": e_key, "model": e_model, "active_label": active_lbl}
                
    def test_slot(self, idx):
        sw = self.slot_widgets[idx]
        url = sw["url"].get().strip()
        display_key = sw["key"].get().strip()
        model = sw["model"].get().strip()
        
        if not (url and display_key and model):
            messagebox.showwarning("提示", f"槽 #{idx + 1} 三个字段都得填好。")
            return
            
        # 安全验证：如果输入框里是我们在初始化时填进去的打码 Key，说明没改动，提取真实 Key。
        # 如果不是，说明用户重新粘贴了新 Key，那就拿新输入的值。
        actual_key = self.real_keys[idx] if display_key == mask_api_key(self.real_keys[idx]) else display_key
        
        self._update_active_indicator(None)
        self.status.config(text=f"⏳ 正在测试槽 #{idx + 1}……", fg=COLORS["warning"])
        self.btn_next.config(state="disabled")
        
        def worker():
            try:
                client = OpenAI(base_url=url, api_key=actual_key)
                r = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": 'This is a test. Reply with only "1".'}],
                    max_tokens=10, temperature=0,
                )
                reply = r.choices[0].message.content.strip()
                def ok():
                    self.real_keys[idx] = actual_key # 测试成功，更新内存里的真 Key
                    self.app.app_state.update(client=client, model=model, connected=True)
                    self.status.config(text=f"✅ 槽 #{idx + 1} 连接成功！AI 回复：{reply}", fg=COLORS["success"])
                    self.btn_next.config(state="normal")
                    self._update_active_indicator(idx)
                    self._save_config(active=idx)
                self.after(0, ok)
            except Exception as e:
                err = str(e)
                # 终极脱敏：扫描报错文本，如果 OpenAI 库抛出的错误包含真实密钥，将其彻底抹除为打码版
                if actual_key and actual_key in err:
                    err = err.replace(actual_key, mask_api_key(actual_key))
                
                def fail():
                    self.app.app_state["connected"] = False
                    self.status.config(text=f"❌ 槽 #{idx + 1} 失败：{err}", fg=COLORS["danger"])
                self.after(0, fail)
        threading.Thread(target=worker, daemon=True).start()
        
    def _update_active_indicator(self, active_idx):
        for i, sw in enumerate(self.slot_widgets):
            sw["active_label"].config(text="● 当前使用" if i == active_idx else "")
            
    def _save_config(self, active=0):
        cfg = load_config() if self.remember_var.get() else {}
        slots = []
        for i, sw in enumerate(self.slot_widgets):
            display_key = sw["key"].get().strip()
            # 获取真正的 key 用于存储
            actual_key = self.real_keys[i] if display_key == mask_api_key(self.real_keys[i]) else display_key
            
            slots.append({
                "base_url": sw["url"].get().strip(),
                "model": sw["model"].get().strip(),
            })
            
            if self.remember_var.get():
                if actual_key:
                    keyring.set_password(self.KEYRING_SERVICE, f"api_key_slot_{i}", actual_key)
                    self.real_keys[i] = actual_key
            else:
                try:
                    keyring.delete_password(self.KEYRING_SERVICE, f"api_key_slot_{i}")
                except keyring.errors.PasswordDeleteError:
                    pass
            
        if self.remember_var.get():
            cfg["slots"] = slots
            cfg["active_slot"] = active
            cfg["remember"] = True
            save_config(cfg)
        else:
            cfg = load_config()
            cfg.pop("slots", None)
            cfg.pop("active_slot", None)
            cfg["remember"] = False
            save_config(cfg)
            
    def clear_saved(self):
        cfg = load_config()
        cfg.pop("slots", None)
        cfg.pop("active_slot", None)
        save_config(cfg)
        
        for i in range(self.NUM_SLOTS):
            try:
                keyring.delete_password(self.KEYRING_SERVICE, f"api_key_slot_{i}")
            except keyring.errors.PasswordDeleteError:
                pass
             
        messagebox.showinfo("已清除", "API 登录信息已从系统凭据管理器和配置文件中安全删除。")
        
    def on_show(self):
        if self.app.app_state.get("connected"):
            self.btn_next.config(state="normal")


# ============================================================
# 2. Scene 
# ============================================================

class ScenePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.selected = tk.StringVar()

        TopBar(self, app, title="① 选择世界", subtitle="step 2 · 选择故事发生的世界").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=lambda: self.app.show_page("APIPage"),
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="📂 导入存档",
            style="Ghost.TButton",
            command=self.app.load_game_state,
        ).pack(side="left", padx=8)

        ttk.Button(
            bottom,
            text="下一步 →",
            style="Primary.TButton",
            command=self.go_next,
        ).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        # Import banner.
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        head = tk.Frame(card, bg=COLORS["card"])
        head.pack(fill="x", padx=18, pady=(12, 4))

        tk.Label(
            head,
            text="📂 已有存档？",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(side="left")

        ttk.Button(
            head,
            text="导入存档继续游戏",
            style="Primary.TButton",
            command=self.app.load_game_state,
        ).pack(side="right")

        lbl = tk.Label(
            card,
            text=(
                "如果你之前在游戏中点过 💾 存档 按钮保存了 .json 文件，"
                "可以从这里直接读取，跳过角色创建直接继续未完成的人生。"
            ),
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
            justify="left",
        )
        lbl.pack(anchor="w", fill="x", padx=18, pady=(0, 12))
        auto_wrap(lbl)

        # Scenes.
        for sc in SCENES:
            outer, card = Card(inner)
            outer.pack(fill="x", pady=6)

            top = tk.Frame(card, bg=COLORS["card"])
            top.pack(fill="x", padx=18, pady=(12, 4))

            ttk.Radiobutton(
                top,
                text=f"{sc['name']}　[{sc['scenario_tag']}]",
                variable=self.selected,
                value=sc["id"],
                style="Card.TRadiobutton",
            ).pack(anchor="w")

            lbl = tk.Label(
                card,
                text=sc["desc"],
                bg=COLORS["card"],
                fg=COLORS["subtext"],
                font=F_SMALL,
                justify="left",
            )
            lbl.pack(anchor="w", fill="x", padx=42, pady=(0, 12))
            auto_wrap(lbl)

        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(
            card,
            text='自定义世界描述（仅"自定义世界"使用）',
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(anchor="w", padx=18, pady=(12, 4))

        self.custom_text = tk.Text(
            card,
            height=4,
            bd=0,
            font=F_BODY,
            bg="#FAFBFE",
            relief="flat",
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            wrap="word",
        )
        self.custom_text.pack(fill="x", padx=18, pady=(0, 8))

        self.custom_edu_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            card,
            text="自定义世界中存在义务教育",
            variable=self.custom_edu_var,
            style="Card.TCheckbutton",
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # Advanced features card
        outer, card = Card(inner)
        outer.pack(fill="x", pady=10)

        tk.Label(card, text="🔧 高级功能", bg=COLORS["card"],
                fg=COLORS["text"], font=F_SUB).pack(anchor="w", padx=18, pady=(12, 4))

        adv_lbl = tk.Label(
            card,
            text=("自定义天赋会和默认天赋池一起出现在抽取中；"
                "默认追加提示词会附加到所有未来角色的 system prompt 末尾。"),
            bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, justify="left",
        )
        adv_lbl.pack(anchor="w", fill="x", padx=18, pady=(0, 8))
        auto_wrap(adv_lbl)
        
        
        # ========== NEW: 体验设置 Toggle ==========
        cfg_prefs = load_config().get("preferences", {}) # <--- 读取偏好设置
        
        self.adv_save_token_var = tk.BooleanVar(value=cfg_prefs.get("adv_save_token", True))
        ttk.Checkbutton(card, text="省token模式：每一回合开启新对话并提取履历，大量节省词元(推荐)",
                        variable=self.adv_save_token_var, style="Card.TCheckbutton").pack(anchor="w", padx=18, pady=(4, 0))
                        
        self.adv_edit_prompt_var = tk.BooleanVar(value=cfg_prefs.get("adv_edit_prompt", False))
        ttk.Checkbutton(card, text="游戏中允许编辑系统提示词",
                        variable=self.adv_edit_prompt_var, style="Card.TCheckbutton").pack(anchor="w", padx=18, pady=(4, 0))
                        
        self.adv_show_payload_var = tk.BooleanVar(value=cfg_prefs.get("adv_show_payload", False))
        ttk.Checkbutton(card, text="显示每轮对话发送给API的内容",
                        variable=self.adv_show_payload_var, style="Card.TCheckbutton").pack(anchor="w", padx=18, pady=(4, 12))

        adv_row = tk.Frame(card, bg=COLORS["card"])
        adv_row.pack(anchor="w", padx=18, pady=(0, 14))

        ttk.Button(
            adv_row, text="✨ 自定义天赋编辑器", style="Secondary.TButton",
            command=lambda: TalentEditor(self.app, self.app),
        ).pack(side="left", padx=4)

        ttk.Button(
            adv_row, text="🛠 默认提示词编辑器", style="Secondary.TButton",
            command=lambda: GlobalPromptEditor(self.app, self.app),
        ).pack(side="left", padx=4)

    def go_next(self):
        sid = self.selected.get()
        if not sid:
            messagebox.showwarning("提示", "请选择一个世界场景！")
            return

        sc = next(s for s in SCENES if s["id"] == sid)
        c = self.app.character

        c["scene_id"] = sid
        c["scene_name"] = sc["name"]
        c["scenario_tag"] = sc["scenario_tag"]
        
        # 记录高级功能偏好到当前角色
        c["adv_save_token"] = self.adv_save_token_var.get()
        c["adv_edit_prompt"] = self.adv_edit_prompt_var.get()
        c["adv_show_payload"] = self.adv_show_payload_var.get()
        
        # ================= NEW: 保存高级功能到本地配置文件 =================
        cfg = load_config()
        prefs = cfg.setdefault("preferences", {})
        prefs["adv_save_token"] = self.adv_save_token_var.get()
        prefs["adv_edit_prompt"] = self.adv_edit_prompt_var.get()
        prefs["adv_show_payload"] = self.adv_show_payload_var.get()
        save_config(cfg)
        # ===============================================================

        if sid == "custom":
            txt = self.custom_text.get("1.0", "end").strip()
            if not txt:
                messagebox.showwarning("提示", "选择自定义世界请填写描述！")
                return
            c["scene_desc"] = txt
            c["has_compulsory_edu"] = bool(self.custom_edu_var.get())
        else:
            c["scene_desc"] = sc["desc"]
            c["has_compulsory_edu"] = bool(sc.get("has_edu", False))

        self.app.show_page("IdentityPage")

# ============================================================
# 3. Identity + content mode + modifiers
# ============================================================

class IdentityPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        
        cfg_prefs = load_config().get("preferences", {}) # <--- 读取偏好设置

        self.gender_var = tk.StringVar(value="男")
        self.content_var = tk.StringVar(value=cfg_prefs.get("content_mode", CONTENT_NORMAL))
        self.diff_var = tk.StringVar(value=cfg_prefs.get("difficulty", DIFF_STANDARD))

        self.fast_var = tk.BooleanVar(value=cfg_prefs.get("fast_mode", False))
        self.fine_var = tk.BooleanVar(value=cfg_prefs.get("fine_enabled", False))
        
        # Fine Mode 的具体数值也顺手保存一下，方便测试
        self.fine_start_var = tk.StringVar(value=cfg_prefs.get("fine_start", "0"))
        self.fine_end_var = tk.StringVar(value=cfg_prefs.get("fine_end", "80"))
        self.fine_timestamp_var = tk.StringVar(value="year")
        # Display variable for the timestamp combobox.
        self.fine_ts_display_var = tk.StringVar(
            value=FINE_TIMESTAMP_PRESETS["year"]["label"]
        )
        self.fine_widgets = []

        TopBar(self, app, title="② 身份设定", subtitle="step 3 · 身份、内容模式与规则修饰器").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=lambda: self.app.show_page("ScenePage"),  # FIX: was AttributePage
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="下一步 →",
            style="Primary.TButton",
            command=self.go_next,
        ).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        # Gender
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(card, text="性别", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 6)
        )

        gf = tk.Frame(card, bg=COLORS["card"])
        gf.pack(fill="x", padx=18, pady=(0, 12))

        for g in GENDERS:
            ttk.Radiobutton(
                gf,
                text=g,
                variable=self.gender_var,
                value=g,
                style="Card.TRadiobutton",
            ).pack(side="left", padx=5)

        tk.Label(gf, text="自定义：", bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL).pack(
            side="left", padx=(15, 5)
        )

        self.gender_custom = ttk.Entry(gf, width=20)
        self.gender_custom.pack(side="left")

        # Race
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(card, text="种族", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 6)
        )

        self.race_entry = ttk.Entry(card, width=40)
        self.race_entry.insert(0, "人类")
        self.race_entry.pack(anchor="w", padx=18, pady=(0, 12))

        # Extra info
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(
            card,
            text="额外信息（和角色无关的信息，世界观等。）",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(anchor="w", padx=18, pady=(12, 6))

        self.extra_text = tk.Text(
            card,
            height=4,
            bd=0,
            font=F_BODY,
            bg="#FAFBFE",
            relief="flat",
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            wrap="word",
        )
        self.extra_text.pack(fill="x", padx=18, pady=(0, 12))

        # Content mode
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(card, text="内容模式（选择一个 data 文件方向）", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 6)
        )

        content_options = [
            (CONTENT_NORMAL, "普通人生", "世间百态", "normal"),
            #(CONTENT_HORNY, "我有性压抑", "特殊属性和一些独特特质。", "normal"),
            (CONTENT_STORE, "我要通马桶", "扮演神秘NPC接受委托和解决委托。", "normal"),
        ]

        for code, label, desc, state in content_options:
            row = tk.Frame(card, bg=COLORS["card"])
            row.pack(fill="x", padx=18, pady=3)

            ttk.Radiobutton(
                row,
                text=label,
                variable=self.content_var,
                value=code,
                style="Card.TRadiobutton",
                state=state,
            ).pack(anchor="w")

            lbl = tk.Label(row, text="    " + desc, bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, justify="left")
            lbl.pack(anchor="w", fill="x")
            auto_wrap(lbl)

        # Difficulty
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(card, text="难度修饰器", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 6)
        )

        diff_options = [
            (DIFF_STANDARD, "标准", "成功的人生需要一点点运气。"),
            (DIFF_TEST, "测试模式 🧪", "无限抽天赋、无限投幸运。你不是开来作弊的，对吧？"),
            (DIFF_IRONMAN, "铁人模式 ⚙️", "天赋只能抽 1 次，幸运只能投 2 次。真正的勇士敢于直面人生。"),
        ]

        for code, label, desc in diff_options:
            row = tk.Frame(card, bg=COLORS["card"])
            row.pack(fill="x", padx=18, pady=3)

            ttk.Radiobutton(
                row,
                text=label,
                variable=self.diff_var,
                value=code,
                style="Card.TRadiobutton",
            ).pack(anchor="w")

            lbl = tk.Label(row, text="    " + desc, bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, justify="left")
            lbl.pack(anchor="w", fill="x")
            auto_wrap(lbl)

        # Pacing / Fine Mode
        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        tk.Label(
            card,
            text="节奏修饰器",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(anchor="w", padx=18, pady=(12, 6))

        ttk.Checkbutton(
            card,
            text="快速模式 ⚡：角色到 40 岁时收束并生成后日谈",
            variable=self.fast_var,
            style="Card.TCheckbutton",
        ).pack(anchor="w", padx=18, pady=(0, 8))

        ttk.Checkbutton(
            card,
            text="微调模式：自定义开局年龄 / 终止年龄 / 时间刻度",
            variable=self.fine_var,
            style="Card.TCheckbutton",
            command=self._toggle_fine_controls,
        ).pack(anchor="w", padx=18, pady=(4, 8))

        fine_frame = tk.Frame(card, bg=COLORS["card"])
        fine_frame.pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(
            fine_frame,
            text="开局年龄",
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
        ).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)

        e_start = ttk.Entry(fine_frame, textvariable=self.fine_start_var, width=8)
        e_start.grid(row=0, column=1, sticky="w", padx=(0, 16), pady=4)

        tk.Label(
            fine_frame,
            text="终止年龄",
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
        ).grid(row=0, column=2, sticky="w", padx=(0, 6), pady=4)

        e_end = ttk.Entry(fine_frame, textvariable=self.fine_end_var, width=8)
        e_end.grid(row=0, column=3, sticky="w", padx=(0, 16), pady=4)

        tk.Label(
            fine_frame,
            text="时间刻度",
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
        ).grid(row=0, column=4, sticky="w", padx=(0, 6), pady=4)

        # Friendly labels in the dropdown.
        ts_labels = [v["label"] for v in FINE_TIMESTAMP_PRESETS.values()]
        combo_ts = ttk.Combobox(
            fine_frame,
            textvariable=self.fine_ts_display_var,
            values=ts_labels,
            width=12,
            state="readonly",
        )
        combo_ts.grid(row=0, column=5, sticky="w", pady=4)

        help_lbl = tk.Label(
            card,
            text=(
                "微调模式说明：如果开局年龄大于0，角色不会从出生开始。"
                "你会获得等同于开局年龄的经历点，可分配到当前模式的派生追踪项。"
                "AI 会根据这些数值编写开局前的人生经历。" 
            ),
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
            justify="left",
        )
        help_lbl.pack(anchor="w", fill="x", padx=18, pady=(0, 12))
        auto_wrap(help_lbl)

        self.fine_widgets = [e_start, e_end, combo_ts]
        self._toggle_fine_controls()

    def _toggle_fine_controls(self):
        enabled = self.fine_var.get()
        for w in getattr(self, "fine_widgets", []):
            try:
                if isinstance(w, ttk.Combobox):
                    w.config(state="readonly" if enabled else "disabled")
                else:
                    w.config(state="normal" if enabled else "disabled")
            except Exception:
                pass

    def _label_to_timestamp_key(self, label):
        for k, v in FINE_TIMESTAMP_PRESETS.items():
            if v["label"] == label:
                return k
        return "year"

    def go_next(self):
        gender = self.gender_var.get()

        if gender == "自定义":
            cg = self.gender_custom.get().strip()
            if not cg:
                messagebox.showwarning("提示", "选择自定义性别请填写内容！")
                return
            gender = cg

        if self.content_var.get() == CONTENT_STORE:
            if self.fine_var.get():
                if not messagebox.askyesno(
                    "提示",
                    "通马桶模拟器与 Fine Mode 不兼容（时间刻度冲突）。\n点确定将自动关闭 Fine Mode 继续。",
                ):
                    return
                self.fine_var.set(False)

            if self.fast_var.get():
                if not messagebox.askyesno(
                    "提示",
                    "通马桶模拟器与快速模式不兼容（age 单位是天不是年）。\n点确定将自动关闭快速模式继续。",
                ):
                    return
                self.fast_var.set(False)        

        c = self.app.character
        c.update(
            gender=gender,
            race=self.race_entry.get().strip() or "人类",
            extra_info=self.extra_text.get("1.0", "end").strip(),
            content_mode=self.content_var.get(),
            difficulty=self.diff_var.get(),
            fast_mode=bool(self.fast_var.get()),
        )

        if self.fine_var.get():
            try:
                start_age = float(self.fine_start_var.get().strip())
                end_age = float(self.fine_end_var.get().strip())
            except Exception:
                messagebox.showwarning("提示", "Fine Mode 的开局年龄和终止年龄必须是数字。")
                return

            if start_age < 0:
                messagebox.showwarning("提示", "开局年龄不能小于 0。")
                return

            if end_age <= start_age:
                messagebox.showwarning("提示", "终止年龄必须大于开局年龄。")
                return

            ts_key = self._label_to_timestamp_key(self.fine_ts_display_var.get())
            self.fine_timestamp_var.set(ts_key)

            self.app.configure_fine_mode(
                True,
                start_age=start_age,
                end_age=end_age,
                timestamp=ts_key,
            )
        else:
            self.app.configure_fine_mode(False)

        # ================= NEW: 保存模式偏好到本地配置文件 =================
        cfg = load_config()
        prefs = cfg.setdefault("preferences", {})
        prefs["content_mode"] = self.content_var.get()
        prefs["difficulty"] = self.diff_var.get()
        prefs["fast_mode"] = self.fast_var.get()
        prefs["fine_enabled"] = self.fine_var.get()
        if self.fine_var.get():
            prefs["fine_start"] = self.fine_start_var.get().strip()
            prefs["fine_end"] = self.fine_end_var.get().strip()
        save_config(cfg)
        # ===============================================================

        self.app.sync_compat_mode()
        self.app.init_attributes_for_mode()

        if c["content_mode"] == CONTENT_STORE:
            self.app.show_page("StoreKeeperPage")
        else:
            self.app.show_page("TalentPage")

# ============================================================
# 3.5 Store Keeper Identity (only for 通马桶模拟器)
# ============================================================

class StoreKeeperPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.archetype_var = tk.StringVar(value="detective")
        self.custom_name_var = tk.StringVar()

        TopBar(self, app,
               title="②½ 店主原型",
               subtitle="step 3.5 · 通马桶模拟器 · 选择你扮演的神秘 NPC").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(bottom, text="← 上一步", style="Secondary.TButton",
                   command=lambda: self.app.show_page("IdentityPage")).pack(side="left")
        ttk.Button(bottom, text="下一步 →", style="Primary.TButton",
                   command=self.go_next).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        # ---- 原型选择 ----
        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(card, text="选择你的店主原型",
                 bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 8))

        for arch in KEEPER_ARCHETYPES:
            row = tk.Frame(card, bg=COLORS["card"])
            row.pack(fill="x", padx=18, pady=3)
            ttk.Radiobutton(row, text=arch["name"], variable=self.archetype_var,
                            value=arch["id"], style="Card.TRadiobutton",
                            command=self._toggle_custom).pack(anchor="w")
            lbl = tk.Label(row, text="    " + arch["desc"],
                           bg=COLORS["card"], fg=COLORS["subtext"],
                           font=F_SMALL, justify="left")
            lbl.pack(anchor="w", fill="x")
            auto_wrap(lbl)

        # ---- 自定义原型名 ----
        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(card, text="自定义店主原型（仅当上方选了「自定义」时使用）",
                 bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 4))

        self.custom_entry = ttk.Entry(card, textvariable=self.custom_name_var)
        self.custom_entry.pack(fill="x", padx=18, pady=(0, 12))

        # ---- 背景故事（必填） ----
        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        # (在 __init__ 函数的背景故事输入框的逻辑后面加入这块代码：)

        # ---- 营业期限 ----
        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(card, text="店铺营业期限",
                 bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 4))

        info_time = "设定店铺运营的时间。到达期限后游戏将自动结算并生成总评结局。"
        tk.Label(card, text=info_time, bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL).pack(anchor="w", padx=18, pady=(0, 4))
        
        self.end_tick_var = tk.StringVar(value="120")
        f_tick = tk.Frame(card, bg=COLORS["card"])
        f_tick.pack(anchor="w", padx=18, pady=(0, 12))
        ttk.Entry(f_tick, textvariable=self.end_tick_var, width=8).pack(side="left")
        tk.Label(f_tick, text=" 旬", bg=COLORS["card"], fg=COLORS["text"], font=F_BODY).pack(side="left")

        tk.Label(card, text="店主背景故事（必填）",
                 bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=18, pady=(12, 4))

        info = ("通马桶模拟器要求你提供店主的来历。AI 不会自己编：你写什么 AI 就用什么。\n"
                "可以写：你是谁、来自哪里、为什么开店、当下的处境、你的店开在哪。")
        info_lbl = tk.Label(card, text=info, bg=COLORS["card"],
                            fg=COLORS["subtext"], font=F_SMALL, justify="left")
        info_lbl.pack(anchor="w", fill="x", padx=18, pady=(0, 8))
        auto_wrap(info_lbl)

        self.backstory_text = tk.Text(card, height=8, bd=0, font=F_BODY,
                                       bg="#FAFBFE", relief="flat",
                                       highlightbackground=COLORS["border"],
                                       highlightthickness=1, wrap="word")
        self.backstory_text.pack(fill="x", padx=18, pady=(0, 12))

    def _toggle_custom(self):
        self.custom_entry.config(state="normal" if self.archetype_var.get() == "custom" else "disabled")

    def on_show(self):
        c = self.app.character
        if c.get("store_keeper_type"):
            self.archetype_var.set(c["store_keeper_type"])
        if c.get("store_keeper_type_custom"):
            self.custom_name_var.set(c["store_keeper_type_custom"])
        if c.get("store_keeper_backstory"):
            self.backstory_text.delete("1.0", "end")
            self.backstory_text.insert("1.0", c["store_keeper_backstory"])
        # 回显设定的回合数
        if c.get("store_end_tick"):
            self.end_tick_var.set(str(c["store_end_tick"]))
        self._toggle_custom()

    def go_next(self):
        c = self.app.character

        arch_id = self.archetype_var.get()
        backstory = self.backstory_text.get("1.0", "end").strip()

        if not backstory:
            messagebox.showwarning("提示", "店主背景故事必须填写。")
            return
            
        # 校验营业回合
        try:
            end_tick = int(self.end_tick_var.get().strip())
            if end_tick <= 0: raise ValueError
        except Exception:
            messagebox.showwarning("提示", "营业期限必须是大于 0 的整数。")
            return

        if arch_id == "custom":
            custom_name = self.custom_name_var.get().strip()
            if not custom_name:
                messagebox.showwarning("提示", "选了自定义原型必须填写名称。")
                return
            label = custom_name
        else:
            arch = get_keeper_archetype_by_id(arch_id)
            label = arch["name"] if arch else arch_id

        c["store_keeper_type"] = arch_id
        c["store_keeper_type_label"] = label
        c["store_keeper_type_custom"] = self.custom_name_var.get().strip()
        c["store_keeper_backstory"] = backstory
        c["store_end_tick"] = end_tick  # 存入角色数据

        init_store_state(c)
        self.app.show_page("TalentPage")
# ============================================================
# 4. Talents
# ============================================================

class TalentPage(tk.Frame):
    DRAW_COUNT = 6
    PICK_COUNT = 3

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.drawn_talents =[]
        self.selected_indices = set()

        TopBar(
            self,
            app,
            title="③ 天赋抽取",
            subtitle=f"step 4 · 抽 {self.DRAW_COUNT} 选 {self.PICK_COUNT}",
        ).pack(side="top", fill="x")

        bottom = make_bottom(self)
        def _talent_go_back():
            if self.app.character.get("content_mode") == CONTENT_STORE:
                self.app.show_page("StoreKeeperPage")
            else:
                self.app.show_page("IdentityPage")

        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=_talent_go_back,
        ).pack(side="left")

        self.btn_next = ttk.Button(
            bottom,
            text="下一步 →",
            style="Primary.TButton",
            state="disabled",
            command=self.go_next,
        )
        self.btn_next.pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=15)

        top = tk.Frame(inner, bg=COLORS["bg"])
        top.pack(fill="x", pady=4)

        self.label_count = tk.Label(top, text="", bg=COLORS["bg"], fg=COLORS["subtext"], font=F_BODY)
        self.label_count.pack(side="left")

        self.btn_roll = ttk.Button(
            top,
            text=f"🎲 抽取 {self.DRAW_COUNT} 个天赋",
            style="Primary.TButton",
            command=self.roll,
        )
        self.btn_roll.pack(side="right")

        self.label_pick = tk.Label(inner, text="", bg=COLORS["bg"], fg=COLORS["primary"], font=F_SUB)
        self.label_pick.pack(anchor="w", pady=(8, 4))

        legend = tk.Frame(inner, bg=COLORS["bg"])
        legend.pack(fill="x", pady=(2, 8))
        
        ttk.Button(
            legend, text="✨ 编辑自定义天赋",
            style="Ghost.TButton",
            command=lambda: TalentEditor(self.app, self.app),
        ).pack(side="right", padx=10)

        for _, cfg in RARITY_CONFIG.items():
            tk.Label(
                legend,
                text=cfg["label"],
                bg=cfg["bg"],
                fg=cfg["color"],
                font=(FONT_FAM, 9, "bold"),
                padx=10,
                pady=3,
            ).pack(side="left", padx=4)

        tk.Label(
            legend,
            text="（点卡片选中 / 取消选中）",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=F_SMALL,
        ).pack(side="left", padx=10)

        self.list_frame = tk.Frame(inner, bg=COLORS["bg"])
        self.list_frame.pack(fill="both", expand=True, pady=8)

    def _max_rolls(self):
        diff = self.app.character.get("difficulty", DIFF_STANDARD)
        if diff == DIFF_TEST:
            return float("inf")
        if diff == DIFF_IRONMAN:
            return 1
        return 5

    def _mode_str(self):
        diff = self.app.character.get("difficulty", DIFF_STANDARD)
        if diff == DIFF_TEST:
            return "测试模式：无限选取"
        if diff == DIFF_IRONMAN:
            return "铁人模式：只能抽 1 次"
        return "标准模式：最多 5 次"

    def on_show(self):
        c = self.app.character
        is_test = c.get("difficulty") == DIFF_TEST
        
        if is_test:
            self.btn_roll.config(text="✨ [测试] 显示所有可用天赋", state="normal")
        else:
            self.btn_roll.config(text=f"🎲 抽取 {self.DRAW_COUNT} 个天赋")
            self.btn_roll.config(state="normal" if c["talent_rolls_used"] < self._max_rolls() else "disabled")
            
        self.refresh_pickbar()
        self.update_count()

    def update_count(self):
        c = self.app.character
        is_test = c.get("difficulty") == DIFF_TEST
        
        if is_test:
            self.label_count.config(text="测试模式：无限选取")
            return
            
        used = c["talent_rolls_used"]
        mr = self._max_rolls()
        rem = "∞" if mr == float("inf") else max(0, mr - used)
        self.label_count.config(text=f"{self._mode_str()}　·　已抽 {used} 次　·　剩余 {rem}")

    def refresh_pickbar(self):
        is_test = self.app.character.get("difficulty") == DIFF_TEST
        n = len(self.selected_indices)
        
        if is_test:
            self.label_pick.config(text=f"已选 {n} 个（无限制）")
            self.btn_next.config(state="normal")
        else:
            self.label_pick.config(text=f"已选 {n} / {self.PICK_COUNT}")
            self.btn_next.config(state="normal" if n == self.PICK_COUNT else "disabled")

    def roll(self):
        c = self.app.character
        is_test = c.get("difficulty") == DIFF_TEST

        if not is_test and c["talent_rolls_used"] >= self._max_rolls():
            messagebox.showinfo("提示", "抽取次数已用完！")
            return

        m = self.app.mode_data()
        mode_tag = getattr(m, "TALENT_MODE_TAG", "Normal")

        combined_pool = list(m.TALENT_POOL) + load_user_talents()

        if is_test:
            # 测试模式：显示当前场景与模式下所有适用的天赋
            drawn = normal_data.filter_pool(combined_pool, c["scenario_tag"], mode_tag)
        else:
            # 普通抽取
            drawn = normal_data.draw_talents(
                combined_pool,
                c["scenario_tag"],
                mode_tag,
                n=self.DRAW_COUNT,
            )

            if len(drawn) < self.PICK_COUNT:
                messagebox.showwarning(
                    "提示",
                    f"天赋池里满足条件 (mode={mode_tag} & scenario={c['scenario_tag']}) "
                    f"的天赋少于 {self.PICK_COUNT} 个。\n\n"
                    f"请去对应 data 文件里多加几条。",
                )
                return

        self.drawn_talents = drawn
        self.selected_indices = set()
        
        if not is_test:
            c["talent_rolls_used"] += 1
            
        c["talents"] =[]

        self.refresh_list()
        self.refresh_pickbar()
        self.update_count()

        if not is_test and c["talent_rolls_used"] >= self._max_rolls():
            self.btn_roll.config(state="disabled")

    def toggle_select(self, idx):
        is_test = self.app.character.get("difficulty") == DIFF_TEST
        
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
        else:
            if not is_test and len(self.selected_indices) >= self.PICK_COUNT:
                # 超过数量时顶掉第一个
                self.selected_indices = set(list(self.selected_indices)[1:])
            self.selected_indices.add(idx)

        self.refresh_list()
        self.refresh_pickbar()

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.drawn_talents:
            tk.Label(
                self.list_frame,
                text="（点上方按钮抽卡/显示天赋）",
                bg=COLORS["bg"],
                fg=COLORS["muted"],
                font=F_BODY,
            ).pack(pady=20)
            return

        for idx, t in enumerate(self.drawn_talents):
            rarity = t.get("rarity", "common")
            cfg = RARITY_CONFIG.get(rarity, RARITY_CONFIG["common"])
            is_sel = idx in self.selected_indices

            outer = tk.Frame(self.list_frame, bg=COLORS["bg"])
            outer.pack(fill="x", pady=4)

            border = COLORS["primary"] if is_sel else cfg["color"]
            thick = 3 if is_sel else 2
            inside_bg = "#EAF0FE" if is_sel else COLORS["card"]

            inner = tk.Frame(
                outer,
                bg=inside_bg,
                highlightbackground=border,
                highlightthickness=thick,
                cursor="hand2",
            )
            inner.pack(fill="both", expand=True)

            header = tk.Frame(inner, bg=inside_bg)
            header.pack(fill="x", padx=14, pady=(10, 2))

            check = "✅ " if is_sel else ""

            tk.Label(
                header,
                text=cfg["label"],
                bg=cfg["bg"],
                fg=cfg["color"],
                font=(FONT_FAM, 9, "bold"),
                padx=8,
                pady=2,
            ).pack(side="left")

            tk.Label(
                header,
                text=f"  {check}{t['name']}",
                bg=inside_bg,
                fg=cfg["color"],
                font=(FONT_FAM, 12, "bold"),
            ).pack(side="left")

            mods = "  ".join(f"{a}{md}" for a, md in t.get("modifiers",[]))
            if mods:
                tk.Label(header, text=mods, bg=inside_bg, fg=COLORS["subtext"], font=F_SMALL).pack(side="right")

            desc_lbl = tk.Label(
                inner,
                text=t.get("desc", ""),
                bg=inside_bg,
                fg=COLORS["text"],
                font=F_BODY,
                justify="left",
                anchor="w",
            )
            desc_lbl.pack(fill="x", padx=14, pady=(0, 10))
            auto_wrap(desc_lbl)

            self._bind_click_recursive(inner, idx)

    def _bind_click_recursive(self, widget, idx):
        widget.bind("<Button-1>", lambda e, i=idx: self.toggle_select(i))
        for child in widget.winfo_children():
            self._bind_click_recursive(child, idx)

    def go_next(self):
        is_test = self.app.character.get("difficulty") == DIFF_TEST
        if not is_test and len(self.selected_indices) != self.PICK_COUNT:
            messagebox.showwarning("提示", f"请选择 {self.PICK_COUNT} 个天赋！")
            return

        self.app.character["talents"] = [self.drawn_talents[i] for i in sorted(self.selected_indices)]
        self.app.show_page("AttributePage")


# ============================================================
# 5. Attributes
# ============================================================

class AttributePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.attr_labels = {}

        TopBar(self, app, title="④ 属性分配", subtitle="step 5 · 初始属性").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=lambda: self.app.show_page("TalentPage"),
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="下一步 →",
            style="Primary.TButton",
            command=self.go_next,
        ).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)
        
        # 顶部模式切换与测试功能区
        self.top_ctrl = tk.Frame(inner, bg=COLORS["bg"])
        self.top_ctrl.pack(fill="x", pady=(0, 10))
        
        self.btn_toggle_mode = ttk.Button(
            self.top_ctrl,
            text="🎲 试试传统派roll点！",
            style="Ghost.TButton",
            command=self.toggle_roll_mode
        )
        self.btn_toggle_mode.pack(side="left")
        
        self.btn_test_points = ttk.Button(
            self.top_ctrl,
            text="🧪[测试] +50点自由属性",
            style="Ghost.TButton",
            command=self.add_test_points
        )

        top = tk.Frame(inner, bg=COLORS["bg"])
        top.pack(fill="x")

        self.tip_label = tk.Label(top, text="", bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL)
        self.tip_label.pack(side="left")

        self.label_remain = tk.Label(top, text="", bg=COLORS["bg"], fg=COLORS["primary"], font=F_SUB)
        self.label_remain.pack(side="right")

        outer, card = Card(inner)
        outer.pack(fill="x", pady=10)

        self.af = tk.Frame(card, bg=COLORS["card"])
        self.af.pack(padx=18, pady=14, fill="x")

        outer, card = Card(inner)
        outer.pack(fill="x", pady=6)

        head = tk.Frame(card, bg=COLORS["card"])
        head.pack(fill="x", padx=18, pady=(12, 6))

        tk.Label(head, text="幸运 LUCK = (3d6+2)*5", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(side="left")

        body2 = tk.Frame(card, bg=COLORS["card"])
        body2.pack(fill="x", padx=18, pady=(0, 14))

        self.luck_label = tk.Label(
            body2,
            text="未投掷",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=(FONT_FAM, 16, "bold"),
            width=8,
        )
        self.luck_label.pack(side="left", padx=(0, 14))

        self.btn_luck = ttk.Button(body2, text="🎲 投掷幸运", style="Secondary.TButton", command=self.roll_luck)
        self.btn_luck.pack(side="left", padx=8)

        self.luck_count = tk.Label(body2, text="", bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL)
        self.luck_count.pack(side="left", padx=10)

    def _points_pool(self):
        m = self.app.mode_data()
        return getattr(m, "POINTS_POOL_DEFAULT", 180)

    def toggle_roll_mode(self):
        c = self.app.character
        c["is_classic_roll"] = not c.get("is_classic_roll", False)
        
        if c["is_classic_roll"]:
            # 初次切换到 Roll 模式时自动强制 Roll 一次
            if c.get("stat_rolls_used", 0) == 0:
                self.do_classic_roll(force=True)
        else:
            # 切换回点数模式时重置属性为 30
            m = self.app.mode_data()
            for a in m.ATTRIBUTES:
                c["attributes"][a] = 30
                
        self.on_show()

    def add_test_points(self):
        c = self.app.character
        c["test_extra_points"] = c.get("test_extra_points", 0) + 50
        self.on_show()

    def _stat_roll_max(self):
        diff = self.app.character.get("difficulty", DIFF_STANDARD)
        if diff == DIFF_TEST:
            return float("inf")
        if diff == DIFF_IRONMAN:
            return 1
        return 5

    def do_classic_roll(self, force=False):
        c = self.app.character
        max_rolls = self._stat_roll_max()
        
        if not force and c.get("stat_rolls_used", 0) >= max_rolls:
            messagebox.showinfo("提示", "重roll次数已用完！")
            return
            
        m = self.app.mode_data()
        # “每一个属性现在都会变成3d6*5”
        for a in m.ATTRIBUTES:
            c["attributes"][a] = roll_dice("3d6") * 5
            
        if not force:
            c["stat_rolls_used"] = c.get("stat_rolls_used", 0) + 1
            
        self.on_show()

    def on_show(self):
        c = self.app.character
        m = self.app.mode_data()
        
        # 确保变量存在
        if "test_extra_points" not in c:
            c["test_extra_points"] = 0
        if "stat_rolls_used" not in c:
            c["stat_rolls_used"] = 0
        if "is_classic_roll" not in c:
            c["is_classic_roll"] = False

        is_test = c.get("difficulty", DIFF_STANDARD) == DIFF_TEST
        is_classic = c["is_classic_roll"]

        # 测试模式增加额外点数按钮
        if is_test and not is_classic:
            self.btn_test_points.pack(side="left", padx=10)
        else:
            self.btn_test_points.pack_forget()

        if is_classic:
            self.btn_toggle_mode.config(text="🔙 切换回自由分配模式")
        else:
            self.btn_toggle_mode.config(text="🎲 试试传统派roll点！")

        for w in self.af.winfo_children():
            w.destroy()

        self.attr_labels = {}
        
        # =========== 经典 Roll 点模式 ===========
        if is_classic:
            roll_frame = tk.Frame(self.af, bg=COLORS["card"])
            roll_frame.grid(row=0, column=0, sticky="we", pady=(0, 10))
            self.af.grid_columnconfigure(0, weight=1)
            
            mr = self._stat_roll_max()
            used = c["stat_rolls_used"]
            rem = "∞" if mr == float("inf") else max(0, mr - used)
            
            btn_roll = ttk.Button(
                roll_frame, text=f"🎲 重roll所有属性（剩余 {rem} 次）", 
                style="Primary.TButton", command=self.do_classic_roll
            )
            btn_roll.pack(side="left")
            
            if used >= mr and mr != float("inf"):
                btn_roll.config(state="disabled")

            for i, a in enumerate(m.ATTRIBUTES):
                row = tk.Frame(self.af, bg=COLORS["card"])
                row.grid(row=i+1, column=0, sticky="we", pady=4)
                
                tk.Label(row, text=f"{a}　{m.ATTR_DESC[a]}", bg=COLORS["card"], fg=COLORS["text"], font=F_BODY, width=14, anchor="w").pack(side="left")
                desc = tk.Label(row, text=m.ATTR_LONG_DESC[a], bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, anchor="w", justify="left")
                desc.pack(side="left", padx=(0, 10), fill="x", expand=True)
                auto_wrap(desc)
                
                lbl = tk.Label(row, text=str(c["attributes"].get(a, 30)), bg=COLORS["card"], fg=COLORS["primary"], font=(FONT_FAM, 13, "bold"), width=5)
                lbl.pack(side="right", padx=10)
                self.attr_labels[a] = lbl
                
            self.tip_label.config(text="传统派Roll点模式：所有属性变为 3d6*5")
            self.label_remain.config(text="")
            
        # =========== 点数购买模式 ===========
        else:
            for i, a in enumerate(m.ATTRIBUTES):
                row = tk.Frame(self.af, bg=COLORS["card"])
                row.grid(row=i, column=0, sticky="we", pady=4)
                self.af.grid_columnconfigure(0, weight=1)

                tk.Label(
                    row, text=f"{a}　{m.ATTR_DESC[a]}", bg=COLORS["card"], 
                    fg=COLORS["text"], font=F_BODY, width=14, anchor="w"
                ).pack(side="left")

                desc = tk.Label(
                    row, text=m.ATTR_LONG_DESC[a], bg=COLORS["card"], 
                    fg=COLORS["subtext"], font=F_SMALL, anchor="w", justify="left"
                )
                desc.pack(side="left", padx=(0, 10), fill="x", expand=True)
                auto_wrap(desc)

                ttk.Button(row, text="−", width=3, style="Secondary.TButton", command=lambda x=a: self.change(x, -5)).pack(side="left", padx=2)
                lbl = tk.Label(row, text=str(c["attributes"].get(a, 30)), bg=COLORS["card"], fg=COLORS["text"], font=(FONT_FAM, 13, "bold"), width=5)
                lbl.pack(side="left", padx=4)
                self.attr_labels[a] = lbl
                ttk.Button(row, text="+", width=3, style="Secondary.TButton", command=lambda x=a: self.change(x, 5)).pack(side="left", padx=2)

            pool_total = self._points_pool() + c["test_extra_points"]
            self.tip_label.config(text=f"每项 30~85，每次 ±5　|　总池 {pool_total} 点")
            
        self.refresh()
        self.refresh_luck()

    def remaining(self):
        m = self.app.mode_data()
        c = self.app.character
        spent = sum(c["attributes"].values()) - 30 * len(m.ATTRIBUTES)
        pool = self._points_pool() + c.get("test_extra_points", 0)
        return pool - spent

    def change(self, attr, delta):
        c = self.app.character
        new = c["attributes"][attr] + delta

        if new < 30 or new > 85:
            return

        if delta > 0 and self.remaining() < delta:
            messagebox.showinfo("提示", "剩余点数不够！")
            return

        c["attributes"][attr] = new
        self.refresh()

    def refresh(self):
        c = self.app.character
        for a, lbl in self.attr_labels.items():
            lbl.config(text=str(c["attributes"].get(a, 30)))

        if not c.get("is_classic_roll", False):
            rem = self.remaining()
            color = COLORS["primary"] if rem == 0 else (COLORS["warning"] if rem > 0 else COLORS["danger"])
            self.label_remain.config(text=f"剩余可分配点数：{rem}", fg=color)
        else:
            self.label_remain.config(text="")

    def _luck_max(self):
        diff = self.app.character.get("difficulty", DIFF_STANDARD)
        if diff == DIFF_TEST:
            return float("inf")
        if diff == DIFF_IRONMAN:
            return 2
        return 5

    def roll_luck(self):
        c = self.app.character

        if c.get("luck_rolls_used", 0) >= self._luck_max():
            messagebox.showinfo("提示", "幸运投掷次数已用完！")
            return

        c["luck"] = roll_dice("(3d6+2)*5")
        c["luck_rolls_used"] = c.get("luck_rolls_used", 0) + 1
        self.refresh_luck()

    def refresh_luck(self):
        c = self.app.character
        mr = self._luck_max()
        used = c.get("luck_rolls_used", 0)
        rem = "∞" if mr == float("inf") else max(0, mr - used)

        self.luck_label.config(text=str(c.get("luck", 0)) if c.get("luck", 0) else "未投掷")
        self.luck_count.config(text=f"剩余 {rem} 次")
        self.btn_luck.config(state="normal" if rem != 0 else "disabled")

    def go_next(self):
        c = self.app.character

        # 仅在非经典 Roll 点模式下检测点数是否用光
        if not c.get("is_classic_roll", False):
            if self.remaining() != 0:
                if not messagebox.askyesno("确认", f"还剩 {self.remaining()} 点未分配，确定继续吗？"):
                    return

        if c.get("luck", 0) == 0:
            messagebox.showwarning("提示", "请先投掷幸运！")
            return

        if c.get("fine_enabled") and self.app.fine_initial_points() > 0:
            self.app.show_page("FineTrackerPage")
        else:
            self.app.show_page("ConfirmPage")


# ============================================================
# 5.5 Fine Mode initial tracker allocation
# ============================================================

class FineTrackerPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.values = {}
        self.value_labels = {}
        self.remaining_label = None
        self.list_frame = None

        TopBar(
            self,
            app,
            title="④½ 开局前经历分配",
            subtitle="Fine Mode · 用开局前的人生年份换取派生追踪项",
        ).pack(side="top", fill="x")

        bottom = make_bottom(self)

        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=lambda: self.app.show_page("AttributePage"),
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="下一步 →",
            style="Primary.TButton",
            command=self.go_next,
        ).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(
            card,
            text="开局前经历点",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_HEAD,
        ).pack(anchor="w", padx=18, pady=(16, 4))

        # (在 FineTrackerPage.__init__ 中找到这段，替换 info 文本)
        info = (
            "微调模式下，如果开局年龄大于 18 岁，系统会在后台为你自动模拟 1~18 岁的自然成长（含义务教育等）。\n\n"
            "18 岁之后，你每年获得 1 个【自由成长检定】机会。\n"
            "你可以把它们分配到下方的派生属性上，系统会为你进行对应的 COC 成长检定（投掷 d100，大于等于当前属性才成长，有概率失败！）。"
        )

        lbl = tk.Label(
            card,
            text=info,
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            font=F_SMALL,
            justify="left",
        )
        lbl.pack(anchor="w", fill="x", padx=18, pady=(0, 12))
        auto_wrap(lbl)

        self.remaining_label = tk.Label(
            card,
            text="",
            bg=COLORS["card"],
            fg=COLORS["primary"],
            font=F_SUB,
        )
        self.remaining_label.pack(anchor="w", padx=18, pady=(0, 12))

        outer, card = Card(inner)
        outer.pack(fill="x", pady=8)

        tk.Label(
            card,
            text="可分配追踪项",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(anchor="w", padx=18, pady=(14, 6))

        self.list_frame = tk.Frame(card, bg=COLORS["card"])
        self.list_frame.pack(fill="x", padx=18, pady=(0, 16))

    def total_points(self):
        return self.app.fine_initial_points()

    def spent_points(self):
        return sum(max(0, int(v)) for v in self.values.values())

    def remaining_points(self):
        return self.total_points() - self.spent_points()

    def on_show(self):
        c = self.app.character
        m = self.app.mode_data()
        trackers = getattr(m, "TRACKERS", {})

        if not trackers:
            messagebox.showinfo("提示", "当前模式没有定义派生追踪项，跳过 Fine Mode 经历点分配。")
            self.app.show_page("ConfirmPage")
            return

        total = self.total_points()

        if total <= 0:
            c["initial_trackers"] = {}
            self.app.show_page("ConfirmPage")
            return

        keys = list(trackers.keys())
        existing = c.get("initial_trackers") or {}

        self.values = {k: int(existing.get(k, 0)) for k in keys}

        if self.spent_points() > total:
            self.values = {k: 0 for k in keys}

        self.refresh_list()
        self.refresh_remaining()

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        self.value_labels = {}

        m = self.app.mode_data()
        trackers = getattr(m, "TRACKERS", {})

        for key, cfg in trackers.items():
            row = tk.Frame(self.list_frame, bg=COLORS["card"])
            row.pack(fill="x", pady=5)

            label = cfg.get("label", key)
            adj_key = cfg.get("adjustment_key", key)

            left = tk.Frame(row, bg=COLORS["card"])
            left.pack(side="left", fill="x", expand=True)

            tk.Label(
                left,
                text=f"{label}",
                bg=COLORS["card"],
                fg=COLORS["text"],
                font=(FONT_FAM, 11, "bold"),
            ).pack(anchor="w")

            tk.Label(
                left,
                text=f"tracker: {key} / AI adjustment key: {adj_key}",
                bg=COLORS["card"],
                fg=COLORS["subtext"],
                font=F_SMALL,
            ).pack(anchor="w")

            btns = tk.Frame(row, bg=COLORS["card"])
            btns.pack(side="right")

            ttk.Button(
                btns,
                text="−5",
                width=4,
                style="Secondary.TButton",
                command=lambda k=key: self.change(k, -5),
            ).pack(side="left", padx=2)

            ttk.Button(
                btns,
                text="−",
                width=3,
                style="Secondary.TButton",
                command=lambda k=key: self.change(k, -1),
            ).pack(side="left", padx=2)

            val = tk.Label(
                btns,
                text=str(self.values.get(key, 0)),
                bg=COLORS["card"],
                fg=COLORS["primary"],
                font=(FONT_FAM, 13, "bold"),
                width=5,
            )
            val.pack(side="left", padx=6)
            self.value_labels[key] = val

            ttk.Button(
                btns,
                text="+",
                width=3,
                style="Secondary.TButton",
                command=lambda k=key: self.change(k, 1),
            ).pack(side="left", padx=2)

            ttk.Button(
                btns,
                text="+5",
                width=4,
                style="Secondary.TButton",
                command=lambda k=key: self.change(k, 5),
            ).pack(side="left", padx=2)

    def change(self, key, delta):
        cur = int(self.values.get(key, 0))
        new = cur + delta

        if new < 0:
            new = 0

        diff = new - cur

        if diff > 0 and self.remaining_points() < diff:
            messagebox.showinfo("提示", "剩余经历点不够。")
            return

        self.values[key] = new

        if key in self.value_labels:
            self.value_labels[key].config(text=str(new))

        self.refresh_remaining()

    def refresh_remaining(self):
        total = self.total_points()
        spent = self.spent_points()
        rem = total - spent

        color = COLORS["primary"] if rem == 0 else COLORS["warning"]

        self.remaining_label.config(
            text=f"总成长检定次数：{total}　已分配：{spent}　剩余：{rem}",
            fg=color,
        )

    def go_next(self):
        c = self.app.character

        rem = self.remaining_points()
        if rem > 0:
            if not messagebox.askyesno(
                "确认",
                f"还有 {rem} 点经历点未分配，确定继续吗？",
            ):
                return

        c["initial_trackers"] = {
            k: int(v)
            for k, v in self.values.items()
            if int(v) != 0
        }

        self.app.show_page("ConfirmPage")


# ============================================================
# 6. Confirm
# ============================================================

class ConfirmPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        TopBar(self, app, title="⑤ 确认角色", subtitle="step 6 · 最后看一眼").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(
            bottom,
            text="← 上一步",
            style="Secondary.TButton",
            command=self.go_back,
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="✓ 确认创建角色",
            style="Primary.TButton",
            command=self.confirm,
        ).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        outer, card = Card(inner)
        outer.pack(fill="both", expand=True)

        self.display = scrolledtext.ScrolledText(
            card,
            height=18,
            font=F_MONO,
            bd=0,
            relief="flat",
            bg=COLORS["card"],
            padx=14,
            pady=10,
            wrap="word",
        )
        self.display.pack(fill="both", expand=True, padx=4, pady=(8, 4))

        tk.Label(inner, text="角色背景故事（可选）", bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL).pack(
            anchor="w", pady=(8, 4)
        )

        self.backstory = tk.Text(
            inner,
            height=5,
            bd=0,
            font=F_BODY,
            bg=COLORS["card"],
            relief="flat",
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            wrap="word",
        )
        self.backstory.pack(fill="x")
        # --- Skill check checkbox (only for normal/horni modes) ---
        cfg_prefs = load_config().get("preferences", {}) # <--- 读取偏好设置
        self.skill_check_var = tk.BooleanVar(value=cfg_prefs.get("skill_check_enabled", True))
        
        self.skill_check_cb = ttk.Checkbutton(
            inner,   # the inner Frame we already have
            text="使用基于d100的属性检定",
            variable=self.skill_check_var,
            style="Card.TCheckbutton",
        )
        # We will pack it in on_show depending on the mode.

    def go_back(self):
        c = self.app.character
        if c.get("fine_enabled") and self.app.fine_initial_points() > 0:
            self.app.show_page("FineTrackerPage")
        else:
            self.app.show_page("AttributePage")

    def on_show(self):
        c = self.app.character
        m = self.app.mode_data()

        adj = {a: [] for a in m.ATTRIBUTES}
        adj["LUCK"] = []

        for t in c["talents"]:
            for attr, mod in t.get("modifiers", []):
                adj.setdefault(attr, []).append((t["name"], mod))

        lines = [
            f"【世界】 {c['scene_name']}　[{c['scenario_tag']}]",
            f"【性别】 {c['gender']}    【种族】 {c['race']}",
        ]

        if c.get("extra_info"):
            lines.append(f"【额外】 {c['extra_info']}")

        lines.append(f"【模式】 {build_mode_display(c)}")

        if c.get("fine_enabled"):
            fs = c.get("fine_settings", {})
            ts = fs.get("timestamp", "year")
            ts_ui = FINE_TIMESTAMP_PRESETS.get(ts, {}).get("label", ts)
            lines.append(
                f"【Fine】 开局 {fs.get('start_age')} 岁，终止 {fs.get('end_age')} 岁，刻度：{ts_ui}"
            )

        lines.append("")
        lines.append("【属性】（基础 + 天赋调整）")

        for a in m.ATTRIBUTES:
            line = f"  {a}({m.ATTR_DESC[a]}): {c['attributes'][a]}"
            for tn, mod in adj.get(a, []):
                line += f"  {mod}({tn})"
            lines.append(line)

        line = f"  LUCK: {c['luck']}"
        for tn, mod in adj.get("LUCK", []):
            line += f"  {mod}({tn})"
        lines.append(line)

        if c.get("fine_enabled"):
            init_trackers = c.get("initial_trackers") or {}
            if init_trackers:
                lines.append("")
                lines.append("【开局前经历点分配】")
                trackers = getattr(m, "TRACKERS", {})
                for key, val in init_trackers.items():
                    label = trackers.get(key, {}).get("label", key)
                    lines.append(f"  {label}({key}): +{val}")
            else:
                lines.append("")
                lines.append("【开局前经历点分配】 未分配")

        lines.append("")
        lines.append("【天赋】")

        for t in c["talents"]:
            r = RARITY_CONFIG.get(t.get("rarity", "common"), {}).get("label", "")
            lines.append(f"  ★ [{r}] {t['name']}：{t.get('desc', '')}")

        self.display.config(state="normal")
        self.display.delete("1.0", "end")
        self.display.insert("1.0", "\n".join(lines))
        self.display.config(state="disabled")
                # Show skill check checkbox only for normal/horni modes
        c = self.app.character
        if c.get("content_mode") == CONTENT_STORE:
            # Store mode always uses checks – hide and force True
            self.skill_check_var.set(True)
            self.skill_check_cb.pack_forget()
        else:
            self.skill_check_cb.pack(anchor="w", padx=24, pady=(4, 12))

    def confirm(self):
        c = self.app.character
        m = self.app.mode_data()

        final = {a: c["attributes"][a] for a in m.ATTRIBUTES}
        final["LUCK"] = c["luck"]

        log = []

        for t in c["talents"]:
            for attr, mod in t.get("modifiers", []):
                rolled = roll_dice(mod)
                final[attr] = final.get(attr, 0) + rolled
                log.append(f"{t['name']}: {attr} {mod} → {rolled:+d}")

        c["final_attributes"] = final
        c["roll_log"] = log
        c["backstory"] = self.backstory.get("1.0", "end").strip()

        c["max_hp"] = m.calculate_max_hp(final)
        c["hp"] = c["max_hp"]

        # Save the skill check preference
        c["skill_checks_enabled"] = self.skill_check_var.get()
        # Store mode always enabled
        if c.get("content_mode") == CONTENT_STORE:
            c["skill_checks_enabled"] = True
            
        # ================= NEW: 保存检定开关偏好 =================
        cfg = load_config()
        prefs = cfg.setdefault("preferences", {})
        prefs["skill_check_enabled"] = self.skill_check_var.get()
        save_config(cfg)
        # =======================================================

        self.app.show_page("GamePage")


# ============================================================
# 7. Game Page
# ============================================================

class GamePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.initialized = False
        self._pending_retry = None
        self.stats_labels = {}

        TopBar(self, app, title="🌱 人生进行中", subtitle="尽情体验你的一生").pack(side="top", fill="x")

        self.title_label = tk.Label(self, text="", bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD)
        self.title_label.pack(pady=10)

        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=20)

        left_outer = tk.Frame(main, bg=COLORS["bg"], width=230)
        left_outer.pack(side="left", fill="y", padx=(0, 12))
        left_outer.pack_propagate(False)

        outer, card = Card(left_outer)
        outer.pack(fill="both", expand=True)

        tk.Label(card, text="角色面板", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(12, 6)
        )

        self.stats_panel = tk.Frame(card, bg=COLORS["card"])
        self.stats_panel.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        outer, card = Card(right)
        outer.pack(fill="both", expand=True)

        tk.Label(card, text="人生履历", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(12, 4)
        )

        self.history_text = scrolledtext.ScrolledText(
            card,
            height=20,
            font=F_BODY,
            wrap="word",
            bg=COLORS["card"],
            bd=0,
            padx=14,
            pady=8,
            relief="flat",
        )
        self.history_text.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        self.history_text.tag_config("year", font=(FONT_FAM, 11, "bold"), foreground=COLORS["primary"])
        self.history_text.tag_config("adj", foreground=COLORS["muted"])
        self.history_text.tag_config("choice", foreground=COLORS["success"])
        self.history_text.tag_config("death", foreground=COLORS["danger"], font=(FONT_FAM, 11, "bold"))
        self.history_text.config(state="disabled")

        outer, card = Card(self)
        outer.pack(fill="x", padx=20, pady=12)

        self.control_frame = tk.Frame(card, bg=COLORS["card"], height=120)
        self.control_frame.pack(fill="x", padx=14, pady=10)

    def on_show(self):
        if not self.initialized:
            self.initialize_game()
            self.initialized = True

    def clear_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.config(state="disabled")

    def initialize_game(self):
        c = self.app.character
        m = self.app.mode_data()

        c.update(alive=True, cause_of_death=None, event_chance=0.5, history=[])

        m.init_trackers(c)
        m.init_time_state(c)

        fine_start_logs = []
        
        # ==== Fine Mode: 自动模拟 1~18 岁并结算自由成长检定 ====
        if c.get("fine_enabled"):
            fs = c.get("fine_settings", {})
            start_age = int(float(fs.get("start_age", 0)))
            
            if start_age > 0:
                cfg = m.get_time_config(c)
                age_key = cfg["age_key"]
                
                # 1. 记录初始基准值
                trackers = getattr(m, "TRACKERS", {})
                baseline = {k: c.get(k, 0) for k in trackers.keys()}
                
                # 2. 模拟 1 到 min(18, start_age) 岁的自然成长
                original_age = c.get(age_key, 0)
                for y in range(1, min(18, start_age) + 1):
                    c[age_key] = y
                    m.apply_turn_start_effects(c)
                    
                c[age_key] = original_age # 恢复实际年龄
                
                # 总结 1~18 岁模拟结果日志
                for k in trackers.keys():
                    diff = c.get(k, 0) - baseline.get(k, 0)
                    if diff > 0:
                        label = trackers[k].get("label", k)
                        fine_start_logs.append(f"1~18岁自然成长：{label} +{diff}")
                        
                # 3. 结算用户分配的自由成长检定 (18岁以后)
                init_trackers = c.get("initial_trackers") or {}
                for key, checks in init_trackers.items():
                    if key not in trackers or checks <= 0: continue
                    
                    success_count = 0
                    total_gain = 0
                    for _ in range(checks):
                        current_val = c.get(key, 0)
                        # COC 成长骰：投掷 d100，大于等于当前属性才成长
                        if random.randint(1, 100) >= current_val:
                            gain = roll_dice("1d6")
                            # 按照模式里的高等级缩减惩罚
                            if current_val >= 90: gain = max(1, gain // 3)
                            elif current_val >= 70: gain = max(1, gain // 3)
                            elif current_val >= 50: gain = max(1, gain // 2)
                            
                            c[key] = min(100, current_val + gain)
                            success_count += 1
                            total_gain += gain
                            
                    label = trackers[key].get("label", key)
                    if success_count > 0:
                        fine_start_logs.append(f"18岁后历练：{label} 成长检定 {checks} 次，成功 {success_count} 次 (共 +{total_gain})")
                    else:
                        fine_start_logs.append(f"18岁后历练：{label} 成长检定 {checks} 次，全部失败")

        c["_fine_start_logs"] = fine_start_logs

        self.app.sync_compat_mode()

        base_prompt = m.build_system_prompt(c)
        extra_global = load_config().get("extra_system_prompt", "").strip()
        if extra_global:
            base_prompt += "\n\n【玩家自定义全局指令】\n" + extra_global
        if c.get("fine_enabled"):
            base_prompt += self.build_fine_prompt_block()

        prompt = self.wrap_editable_prompt(base_prompt, "")
        c["_base_system_prompt"] = base_prompt
        c["_system_prompt"] = prompt
        c["messages"] = [{"role": "system", "content": prompt}]

        if c.get("fast_mode"):
            c["messages"].append({
                "role": "system",
                "content": "【快速模式】角色到 40 岁时游戏收束，请让 0~40 岁的人生节奏合理。",
            })

        self.build_stats_panel()
        self.refresh_panel()

        # ===== Store Mode 走专属流程 =====
        if c.get("content_mode") == CONTENT_STORE:
            self.append_history(f"━━━ 开张大吉 · {build_mode_display(c)} ━━━", "year")
            self.append_history(
                f"世界：{c['scene_name']}　店主：{c.get('store_keeper_type_label','')}　{c['gender']}·{c['race']}\n"
            )
            c["store_round"] = 0
            self.set_loading("店铺正在开张……")
            self.send_to_ai(m.build_intro_round_prompt(c), self.on_store_intro_response)
            return

        # ===== 普通流程 =====
        self.append_history("━━━ 人生重开 ━━━", "year")
        self.append_history(
            f"世界：{c['scene_name']}　角色：{c['gender']}·{c['race']}　模式：{build_mode_display(c)}\n"
        )

        if c.get("fine_enabled") and self.app.fine_initial_points() > 0:
            self.set_loading("正在生成开局前人生经历……")
            self.send_to_ai(self.build_fine_opening_prompt(), self.on_birth_response)
        else:
            self.set_loading("正在推演出生……")
            self.send_to_ai(
                "请描述角色的出生与时间 0 的起点。介绍家庭、出生环境、童年起点。"
                "本次必须 has_choice=false, alive=true, adjustments 为空。",
                self.on_birth_response,
            )

    def build_fine_prompt_block(self):
        c = self.app.character
        fs = c.get("fine_settings", {})
        ts = fs.get("timestamp", "year")
        ts_ui = FINE_TIMESTAMP_PRESETS.get(ts, {}).get("label", ts)

        return f"""

【Fine Mode / 自定义时间轴】
本局启用了 Fine Mode。
- 角色开局年龄：{fs.get("start_age")} 岁。
- 角色终止年龄：{fs.get("end_age")} 岁。
- 每次玩家点击"下一时间点"，推进：{ts_ui}。
- 如果开局年龄大于 0，请把开局前的人生视为既成事实。
- 不要把角色写成刚出生，除非开局年龄就是 0。
- 开局前经历点已经由玩家分配到派生追踪项中。
- 这些派生追踪项代表角色在开局前已经积累的学历、知识、资产、名气等。
- 请根据这些数值自然编写角色过去的人生经历。
- 核心出生属性仍然是锁定的，不要通过 adjustments 修改核心属性。
"""

    def build_fine_opening_prompt(self):
        c = self.app.character
        m = self.app.mode_data()
        fs = c.get("fine_settings", {})
        trackers = getattr(m, "TRACKERS", {})

        tracker_lines = []

        for key, cfg in trackers.items():
            label = cfg.get("label", key)
            value = c.get(key, cfg.get("initial", 0))

            tiers = cfg.get("tiers")
            if tiers:
                try:
                    tier = get_tier(value, tiers)
                    tracker_lines.append(f"- {label}({key}) = {value}，等级：{tier}")
                except Exception:
                    tracker_lines.append(f"- {label}({key}) = {value}")
            else:
                tracker_lines.append(f"- {label}({key}) = {value}")

        tracker_text = "\n".join(tracker_lines) or "（无派生追踪项）"

        return f"""Fine Mode 开局。
角色当前不是刚出生，而是已经 {fs.get("start_age")} 岁。

请根据以下信息，为角色编写从出生到当前年龄为止的简要人生经历，并描写当前这个时间点的开局状态。

【要求】
- 不要从 0 岁逐年流水账。
- 请概括重要成长经历、家庭背景、教育/历练、关系、经济状态、名声等。
- 请解释为什么角色当前拥有这些派生追踪项数值。
- 如果玩家填写了背景故事，请优先尊重玩家背景故事。
- 本次是开局介绍，必须 has_choice=false。
- 本次不要再额外奖励经历点，adjustments 请保持为空或只写 0。
- alive=true。

【当前派生追踪项】
{tracker_text}

严格输出 JSON：
{{
  "narrative": "开局前人生经历与当前状态，200~500字。",
  "has_choice": false,
  "choices": {{}},
  "adjustments": {{}},
  "alive": true,
  "cause_of_death": null
}}"""

    def wrap_editable_prompt(self, base_prompt, user_area):
        return (
            base_prompt
            + "\n\n"
            + "===== USER EDIT AREA START =====\n"
            + "建议只编辑这两个 marker 之间的区域。\n"
            + "你可以在这里追加给当前 LLM 的写作/格式要求。\n"
            + user_area.strip()
            + "\n===== USER EDIT AREA END =====\n"
        )

    def build_stats_panel(self):
        for w in self.stats_panel.winfo_children():
            w.destroy()

        self.stats_labels = {}

        c = self.app.character
        m = self.app.mode_data()

        for a in list(m.ATTRIBUTES) + ["LUCK"]:
            row = tk.Frame(self.stats_panel, bg=COLORS["card"])
            row.pack(fill="x", pady=2)

            tk.Label(row, text=a, bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL, width=7, anchor="w").pack(
                side="left"
            )

            lbl = tk.Label(row, text="-", bg=COLORS["card"], fg=COLORS["text"], font=(FONT_FAM, 11, "bold"), anchor="w")
            lbl.pack(side="left")
            self.stats_labels[a] = lbl

        ttk.Separator(self.stats_panel, orient="horizontal").pack(fill="x", pady=8)

        hp_row = tk.Frame(self.stats_panel, bg=COLORS["card"])
        hp_row.pack(fill="x", pady=2)

        tk.Label(hp_row, text="❤️ HP", bg=COLORS["card"], fg=COLORS["danger"], font=(FONT_FAM, 11, "bold"), width=7, anchor="w").pack(
            side="left"
        )

        hp_lbl = tk.Label(hp_row, text="-/-", bg=COLORS["card"], fg=COLORS["text"], font=(FONT_FAM, 11, "bold"), anchor="w")
        hp_lbl.pack(side="left")
        self.stats_labels["hp"] = hp_lbl

        ttk.Separator(self.stats_panel, orient="horizontal").pack(fill="x", pady=8)

        for key, cfg in getattr(m, "TRACKERS", {}).items():
            row = tk.Frame(self.stats_panel, bg=COLORS["card"])
            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=cfg.get("label", key),
                bg=COLORS["card"],
                fg=COLORS["subtext"],
                font=F_SMALL,
                width=7,
                anchor="w",
            ).pack(side="left")

            lbl = tk.Label(row, text="-", bg=COLORS["card"], fg=COLORS["text"], font=(FONT_FAM, 11, "bold"), anchor="w")
            lbl.pack(side="left")
            self.stats_labels[key] = lbl
        # Store mode: 客户名册按钮
        if self.app.character.get("content_mode") == CONTENT_STORE:
            ttk.Separator(self.stats_panel, orient="horizontal").pack(fill="x", pady=8)
            ttk.Button(
                self.stats_panel,
                text="📜 客户名册",
                style="Secondary.TButton",
                command=lambda: ClientRosterDialog(self.app, self.app),
            ).pack(fill="x", pady=4)
            ttk.Button(
                self.stats_panel,
                text="📋 当前委托",
                style="Secondary.TButton",
                command=self._show_open_commissions,
            ).pack(fill="x", pady=4)

    def should_fine_end(self):
        return finedata.reached_end_age(self.app.character, self.app.mode_data())

    def handle_fine_end(self):
        c = self.app.character
        m = self.app.mode_data()

        try:
            age = m.get_character_age(c)
        except Exception:
            age = "?"

        self.append_history("\n━━━ 游戏结束！ ━━━", "death")
        self.append_history(f"（Fine Mode · 已到达终止年龄 {age} 岁）")

        self.clear_control()

        ttk.Button(
            self.control_frame,
            text="📜 查看人生总结",
            style="Primary.TButton",
            command=self.request_fine_summary,
        ).pack(pady=14)

    def request_fine_summary(self):
        self.set_loading("AI 正在总结这段人生……")
        self.send_to_ai(
            """Fine Mode 已到达设定的终止年龄。请对角色从开局到现在的人生阶段做出总结。
如果角色仍然活着，请不要写成已经死亡，而是总结其阶段性成就、遗憾和未来可能。
严格输出JSON（只输出JSON）：
{
  "scores": {"legendary": 0, "dramatic": 0, "successful": 0},
  "evaluation": "对这段人生的文字评价（300~600字）"
}""",
            self.on_summary_response,
        )

    def on_birth_response(self, data):
        c = self.app.character
        fine_logs = c.pop("_fine_start_logs", [])
        self.apply_event(data, add_header=True, pre_logs=fine_logs)
        self.show_life_style_choice()

    def show_life_style_choice(self):
        self.clear_control()

        tk.Label(
            self.control_frame,
            text="这一世，你的人生将会……",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=F_SUB,
        ).pack(pady=4)

        bf = tk.Frame(self.control_frame, bg=COLORS["card"])
        bf.pack()

        for label, prob in [
            ("A. 或将波澜壮阔（75%）", 0.75),
            ("B. 老天自有安排（50%）", 0.50),
            ("C. 只愿风平浪静（25%）", 0.25),
        ]:
            ttk.Button(
                bf,
                text=label,
                style="Secondary.TButton",
                command=lambda p=prob: self.set_life_style(p),
            ).pack(side="left", padx=6)

    def set_life_style(self, prob):
        c = self.app.character
        c["event_chance"] = prob

        label = {
            0.75: "或将波澜壮阔",
            0.50: "老天自有安排",
            0.25: "只愿风平浪静",
        }[prob]

        c["messages"].append({
            "role": "system",
            "content": f"【人生基调】玩家选择了「{label}」。请在叙事时配合这个基调。",
        })

        self.show_next_button()

    def show_next_button(self):
        self.clear_control()
        row = tk.Frame(self.control_frame, bg=COLORS["card"])
        row.pack(pady=10)

        ttk.Button(
            row, text="下一时间点 →",
            style="Primary.TButton", command=self.next_tick,
        ).pack(side="left", padx=6)

        ttk.Button(
            row, text="🎯 主动行动",
            style="Secondary.TButton", command=self.do_active_action,
        ).pack(side="left", padx=6)

        c = self.app.character
        if c.get("adv_edit_prompt"):
            ttk.Button(
                row, text="🛠 编辑系统提示词",
                style="Secondary.TButton", command=self.edit_system_prompt,
            ).pack(side="left", padx=6)
            
        if c.get("adv_show_payload"):
            ttk.Button(
                row, text="📄 本轮对话发送内容",
                style="Ghost.TButton", command=self.show_api_payload,
            ).pack(side="left", padx=6)

    def next_tick(self):
        c = self.app.character
        m = self.app.mode_data()

        if c.get("content_mode") == CONTENT_STORE:
            self.next_tick_store()
            return

        m.advance_time(c)
        start_logs = m.apply_turn_start_effects(c)

        if random.random() < c.get("event_chance", 0.5):
            self.set_loading("正在推演下一个时间点……")
            self.send_to_ai(
                f"角色现在处于：{m.format_time(c)}。请推演这个时间点发生的事件。",
                lambda d: self.on_event_response(d, start_logs),
            )
        else:
            self.append_history("\n" + m.format_history_header(c), "year")
            if start_logs:
                self.append_history(f"　〔{' / '.join(start_logs)}〕", "adj")
            self.append_history("　无事发生。")
            self.refresh_panel()

            if self.should_fast_end():
                self.handle_fast_end()
            elif self.should_fine_end():
                self.handle_fine_end()
            else:
                self.show_next_button()

    def on_event_response(self, data, start_logs=None):
        self.apply_event(data, add_header=True, pre_logs=start_logs or [])

        if not self.app.character["alive"]:
            self.handle_death()
        elif self.should_fast_end():
            self.handle_fast_end()
        elif self.should_fine_end():
            self.handle_fine_end()
        elif data.get("has_choice"):
            self.show_choices(data.get("choices") or {})
        else:
            self.show_next_button()

    def should_fast_end(self):
        c = self.app.character
        if c.get("content_mode") == CONTENT_STORE:
            return False
        if not c.get("fast_mode"):
            return False
        try:
            age = self.app.mode_data().get_character_age(c)
        except Exception:
            return False
        return age >= 40

    def should_fine_end(self):
        c = self.app.character
        if c.get("content_mode") == CONTENT_STORE:
            return False
        return finedata.reached_end_age(c, self.app.mode_data())
    
    def show_retry_button(self):
        self.clear_control()
        row = tk.Frame(self.control_frame, bg=COLORS["card"])
        row.pack(pady=10)

        ttk.Button(
            row, text="🔁 重试上一次请求",
            style="Primary.TButton", command=self.do_retry,
        ).pack(side="left", padx=6)

        c = self.app.character
        if c.get("adv_edit_prompt"):
            ttk.Button(
                row, text="🛠 编辑系统提示词",
                style="Secondary.TButton", command=self.edit_system_prompt,
            ).pack(side="left", padx=6)

        ttk.Button(
            row, text="📄 显示原始返回",
            style="Ghost.TButton", command=self.show_raw_response,
        ).pack(side="left", padx=6)
        
        if c.get("adv_show_payload"):
            ttk.Button(
                row, text="📄 完整发送内容",
                style="Ghost.TButton", command=self.show_api_payload,
            ).pack(side="left", padx=6)

        tk.Label(
            self.control_frame,
            text="（上一次 AI 调用失败，时间和事件状态都未推进，点重试会重发同一请求）",
            bg=COLORS["card"], fg=COLORS["muted"], font=F_SMALL,
        ).pack(pady=(4, 0))

    def do_retry(self):
        """重发上一次失败的 AI 请求，不推进时间、不重掷事件骰子。"""
        if not self._pending_retry:
            # 没有挂着的请求，回到正常流程
            self.show_next_button()
            return

        user_msg, callback = self._pending_retry
        self._pending_retry = None
        self.set_loading("正在重试上一次请求……")
        self.send_to_ai(user_msg, callback)

    def show_raw_response(self):
            """弹出一个窗口，显示 AI 最近一次返回的内容。"""
            content = getattr(self, "_last_raw_response", "（没有记录到任何内容）")
            
            win = tk.Toplevel(self.app)
            win.title("AI 原始返回内容")
            win.geometry("640x480")
            win.configure(bg=COLORS["bg"])
            win.transient(self.app)
            
            tk.Label(
                win, text="🔍 原始返回内容", bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD
            ).pack(anchor="w", padx=16, pady=(14, 4))
            
            info = "如果看到下面是一大段普通聊天的文字，说明 AI 忘记输出 JSON 格式了；如果看到拒绝回答，说明触发了审查过滤器；如果是空的一行，说明 API 连接失败。"
            lbl = tk.Label(win, text=info, bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL, justify="left")
            lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
            auto_wrap(lbl)
            
            txt = scrolledtext.ScrolledText(
                win, font=F_MONO, wrap="word", bg=COLORS["card"], bd=0, 
                highlightbackground=COLORS["border"], highlightthickness=1
            )
            txt.pack(fill="both", expand=True, padx=16, pady=8)
            txt.insert("1.0", content)
            txt.config(state="disabled") # 只读模式
            
            bottom = tk.Frame(win, bg=COLORS["bg"])
            bottom.pack(side="bottom", fill="x", padx=16, pady=16)
            ttk.Button(bottom, text="关闭", style="Primary.TButton", command=win.destroy).pack(side="right")
    
    def apply_event(self, data, add_header=True, pre_logs=None):
        c = self.app.character
        m = self.app.mode_data()
        pre_logs = pre_logs or []

        narrative = data.get("narrative", "（AI未提供描述）")

        if add_header:
            self.append_history("\n" + m.format_history_header(c), "year")

        self.append_history(f"　{narrative}")

        log = list(pre_logs)
        ignored = []

        adj = data.get("adjustments") or {}
        locked = set(m.ATTRIBUTES) | {"LUCK"}

        for k, v in adj.items():
            if not isinstance(v, (int, float)) or v == 0:
                continue

            v = int(v)

            if k in locked:
                ignored.append(f"{k}{v:+d}")
                continue

            if k == "HP":
                v = int(v)
                old = c["hp"]
                is_horny = c.get("content_mode") in (MODE_HORNY_MILD, MODE_HORNY_INTENSE)
                
                # Horni 模式特殊抵抗扣血机制
                if v < 0 and is_horny:
                    deduction_checks = abs(v)
                    actual_loss = 0
                    for _ in range(deduction_checks):
                        lib_check = m.perform_skill_check(c, "LIB", difficulty="normal")
                        end_check = m.perform_skill_check(c, "END", difficulty="normal")
                        
                        # 只要有一个成功就免于这 1 点扣血
                        if not (lib_check["success"] or end_check["success"]):
                            actual_loss += 1
                            
                        # 这两个防守检定本身也属于锻炼，享受成长判定
                        for chk in (lib_check, end_check):
                            growth_log = m.apply_skill_check_growth(c, chk)
                            if growth_log:
                                log.append(f"{growth_log}")

                    c["hp"] = max(0, c["hp"] - actual_loss)
                    actual = c["hp"] - old
                    if actual != 0:
                        log.append(f"❤️HP {actual:+d} (抵抗失败)")
                    else:
                        log.append(f"❤️HP 抵抗成功！(未扣血)")
                else:
                    # Normal / Store 模式原生扣血逻辑
                    c["hp"] = min(c["max_hp"], c["hp"] + v)
                    actual = c["hp"] - old
                    if actual != 0:
                        log.append(f"❤️HP {actual:+d}")
                continue

            tracker_log = m.apply_tracker_adjustment(c, k, v)
            if tracker_log:
                log.append(tracker_log)

        if log:
            self.append_history(f"　〔{' / '.join(log)}〕", "adj")

        if ignored:
            print(f"[屏蔽AI对锁定属性的修改] {ignored}")

        ai_alive = data.get("alive", True)

        if not ai_alive or c["hp"] <= 0:
            c["alive"] = False
            cause = data.get("cause_of_death")
            if not cause:
                cause = "重伤不治" if c["hp"] <= 0 else "未知"
            c["cause_of_death"] = cause

            age = m.get_character_age(c)
            self.append_history(f"\n💀 享年 {age} 岁　死因：{cause}", "death")

        self.refresh_panel()

    def filter_valid_checks(self, checks):
            """核心拦截器：打回所有不属于当前模式的非法属性检定"""
            if not checks:
                return[]
                
            m = self.app.mode_data()
            valid = set(m.ATTRIBUTES) | {"LUCK"}
            for key, cfg in getattr(m, "TRACKERS", {}).items():
                valid.add(cfg.get("adjustment_key", key))
            
            filtered =[]
            for attr in checks:
                attr_upper = str(attr).strip().upper()
                if attr_upper in valid:
                    filtered.append(attr_upper)
                else:
                    print(f"[拦截非法检定] AI 给出了不存在的属性：{attr}")
            
            if not filtered and checks:
                fallback = "INT" if "INT" in valid else (m.ATTRIBUTES[0] if m.ATTRIBUTES else "LUCK")
                filtered.append(fallback)
                print(f"[兜底检定] 非法属性替换为：{fallback}")
                
            return filtered

    def show_choices(self, choices):
        c = self.app.character
        if c.get("content_mode") == CONTENT_STORE:
            return self.show_store_choices(choices)

        self.clear_control()

        tk.Label(self.control_frame, text="你的选择是？",
                bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(pady=2)

        bf = tk.Frame(self.control_frame, bg=COLORS["card"])
        bf.pack(fill="x")

        for key in ["A", "B", "C"]:
            if key not in choices:
                continue
            choice = choices[key]
            if isinstance(choice, str):
                desc, checks, difficulty = choice,[], "normal"
            else:
                desc = choice.get("text", "")
                checks = choice.get("checks") or[]
                difficulty = choice.get("difficulty") or "normal"

            if checks:
                check_tag = "/".join(checks)
                diff_zh = {"easy": "易", "normal": "中", "hard": "难"}.get(difficulty, "中")
                label = f"{key}. [{check_tag}|{diff_zh}] {desc}"
            else:
                label = f"{key}. {desc}"

            btn = tk.Button(
                bf, text=label, justify="left", anchor="w",
                bg="#F4F6FB", fg=COLORS["text"], font=F_BODY,
                activebackground="#E8EAF1", bd=0,
                padx=12, pady=6, relief="flat", cursor="hand2",
                command=lambda k=key, d=desc, ch=checks, df=difficulty:
                    self.make_choice(k, d, ch, df),
            )
            btn.pack(fill="x", pady=2)
            auto_wrap(btn, padding=80)

        cf = tk.Frame(self.control_frame, bg=COLORS["card"])
        cf.pack(fill="x", pady=4)

        tk.Label(cf, text="或自己来：", bg=COLORS["card"],
                fg=COLORS["subtext"], font=F_SMALL).pack(side="left")

        self.custom_entry = ttk.Entry(cf)
        self.custom_entry.pack(side="left", fill="x", expand=True, padx=6)

        ttk.Button(cf, text="提交", style="Secondary.TButton",
                command=self.make_custom_choice).pack(side="left")
                
        if c.get("adv_edit_prompt"):
            ttk.Button(cf, text="🛠 提示词", style="Ghost.TButton",
                    command=self.edit_system_prompt).pack(side="left", padx=4)
        if c.get("adv_show_payload"):
            ttk.Button(cf, text="📄 发送内容", style="Ghost.TButton",
                    command=self.show_api_payload).pack(side="left", padx=4)
            
    def make_choice(self, key, desc, checks=None, difficulty="normal"):
        c = self.app.character
        m = self.app.mode_data()

        self.append_history(f"　→ 你选择了 {key}：{desc}", "choice")

        checks = self.filter_valid_checks(checks) # <--- 新增这一行

        # If skill checks are disabled for this run, or the AI gave no checks,
        # just forward to AI for narrative resolution.
        if not c.get("skill_checks_enabled", True) or not checks:
            self.set_loading("正在推演选择的后果……")
            self.send_to_ai(
                f"玩家选择了 {key}：{desc}。请推演这个选择的结果（仍是同一个时间点）。",
                self.on_choice_response,
            )
            return

        # ---- Skill checks are enabled: roll and then narrate ----
        check_results = []
        for attr in checks:
            result = m.perform_skill_check(c, attr, difficulty=difficulty)
            check_results.append(result)
            self.append_history(f"　{m.format_check_log(result)}", "adj")
            growth_log = m.apply_skill_check_growth(c, result)
            if growth_log:
                self.append_history(f"　〔{growth_log}〕", "adj")

        self.refresh_panel()

        self.set_loading("正在推演结果……")
        self.send_to_ai(
            m.build_resolution_prompt(
                c,
                action_summary=f"{key}：{desc}",
                check_results=check_results,
            ),
            self.on_choice_response,
        )

    def make_custom_choice(self):
        text = self.custom_entry.get().strip()
        if not text:
            messagebox.showinfo("提示", "请输入你的选择。")
            return

        self.append_history(f"　→ 你选择了自定义：{text}", "choice")
        self.set_loading("正在分析你的行动……")
        self.send_action_check_normal(text)
    def send_action_check_normal(self, action_text):
        """普通/性压抑模式：先问 AI 用什么属性，再投骰子。"""
        c = self.app.character
        m = self.app.mode_data()

        if not self.app.app_state.get("connected"):
            self.set_loading("正在推演……")
            self.send_to_ai(
                f"玩家选择了自定义行动：{action_text}。请推演结果。",
                self.on_choice_response,
            )
            return

        client = self.app.app_state["client"]
        model = self.app.app_state["model"]
        prompt = m.build_action_check_prompt(c, action_text)

        def worker():
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Return ONLY a JSON object describing skill checks. No prose."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=200,
                )
                data = parse_ai_json(resp.choices[0].message.content)
                checks = data.get("checks") or []
                difficulty = data.get("difficulty") or "normal"
                self.after(0, lambda: self.execute_normal_custom_action(action_text, checks, difficulty))
            except Exception as e:
                err = str(e)

                def fallback():
                    # 失败兜底：不投骰直接推演
                    self.set_loading("正在推演……")
                    self.send_to_ai(
                        f"玩家选择了自定义行动：{action_text}。请推演结果。",
                        self.on_choice_response,
                    )

                self.after(0, fallback)

        threading.Thread(target=worker, daemon=True).start()


    def execute_normal_custom_action(self, action_text, checks, difficulty):
        c = self.app.character
        m = self.app.mode_data()

        checks = self.filter_valid_checks(checks) # <--- 新增这一行

        if not checks:
            # AI 觉得不需要检定 → 直接推演
            self.set_loading("正在推演……")
            self.send_to_ai(
                f"玩家选择了自定义行动：{action_text}。请推演结果。",
                self.on_choice_response,
            )
            return

        check_results = []
        for attr in checks:
            result = m.perform_skill_check(c, attr, difficulty=difficulty)
            check_results.append(result)
            self.append_history(f"　{m.format_check_log(result)}", "adj")
            growth_log = m.apply_skill_check_growth(c, result)
            if growth_log:
                self.append_history(f"　〔{growth_log}〕", "adj")

        self.refresh_panel()

        self.set_loading("正在推演结果……")
        self.send_to_ai(
            m.build_resolution_prompt(c, action_summary=action_text,
                                    check_results=check_results),
            self.on_choice_response,
        )

    def on_choice_response(self, data):
        self.apply_event(data, add_header=False)

        if not self.app.character["alive"]:
            self.handle_death()
        elif self.should_fast_end():
            self.handle_fast_end()
        elif self.should_fine_end():
            self.handle_fine_end()
        elif data.get("has_choice"):
            self.show_choices(data.get("choices") or {})
        else:
                self.show_next_button()
    def do_active_action(self):
            """让玩家在当前时间点输入主动行动。"""
            win = tk.Toplevel(self.app)
            win.title("主动行动")
            win.geometry("560x360")
            win.configure(bg=COLORS["bg"])
            win.transient(self.app)
            win.grab_set()

            # 顶部标题
            tk.Label(win, text="🎯 主动行动",
                    bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD).pack(
                anchor="w", padx=16, pady=(14, 4)
            )

            # 底部按钮区
            bottom = tk.Frame(win, bg=COLORS["bg"])
            bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 16))

            # 中间说明
            info = ("描述你在这个时间点想主动做的事。\n"
                    "AI 会基于角色当前状态推演结果。\n"
                    "（这个动作不会推进时间，可以在同一年里多次主动行动。）")
            lbl = tk.Label(win, text=info, bg=COLORS["bg"], fg=COLORS["subtext"],
                        font=F_SMALL, justify="left")
            lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
            auto_wrap(lbl)

            # 文本框 (now correctly in the outer scope!)
            txt = tk.Text(
                win, height=6, font=F_BODY, wrap="word",
                bg=COLORS["card"], bd=0, padx=10, pady=8,
                highlightbackground=COLORS["border"], highlightthickness=1,
            )
            txt.pack(fill="both", expand=True, padx=16, pady=8)
            txt.focus_set()

            def submit():
                action = txt.get("1.0", "end").strip()
                if not action:
                    messagebox.showwarning("提示", "请描述你的行动。", parent=win)
                    return
                win.destroy()

                c = self.app.character
                self.append_history(f"　→ 主动行动：{action}", "choice")

                # Route to the correct prompt handling based on the mode
                if c.get("content_mode") == CONTENT_STORE:
                    self.set_loading("正在分析你的行动……")
                    self.send_action_check(action)
                else:
                    self.set_loading("正在分析你的行动……")
                    self.send_action_check_normal(action)

            ttk.Button(bottom, text="执行（Enter）", style="Primary.TButton",
                    command=submit).pack(side="right")
            ttk.Button(bottom, text="取消（Esc）", style="Secondary.TButton",
                    command=win.destroy).pack(side="right", padx=8)

            # 快捷键
            win.bind("<Return>", lambda e: (submit(), "break"))
            win.bind("<Control-Return>", lambda e: (submit(), "break"))
            win.bind("<Escape>", lambda e: win.destroy())

    def edit_system_prompt(self):
        c = self.app.character

        if not c.get("messages"):
            messagebox.showinfo("提示", "游戏还没有初始化系统提示词。")
            return

        win = tk.Toplevel(self)
        win.title("编辑系统提示词")
        win.geometry("760x620")
        win.configure(bg=COLORS["bg"])

        tk.Label(
            win,
            text="系统提示词编辑器",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=F_HEAD,
        ).pack(anchor="w", padx=16, pady=(14, 4))

        info = (
            "你正在编辑完整 system prompt。\n"
            "建议只编辑以下两个 marker 之间的区域：\n"
            "===== USER EDIT AREA START ===== 和 ===== USER EDIT AREA END =====\n"
            "如果删坏了，可以点击「恢复默认」。"
        )

        lbl = tk.Label(win, text=info, bg=COLORS["bg"], fg=COLORS["warning"], font=F_SMALL, justify="left")
        lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
        auto_wrap(lbl)

        txt = scrolledtext.ScrolledText(win, font=F_MONO, wrap="word", height=26)
        txt.pack(fill="both", expand=True, padx=16, pady=8)
        txt.insert("1.0", c["messages"][0]["content"])

        bottom = tk.Frame(win, bg=COLORS["bg"])
        bottom.pack(fill="x", padx=16, pady=(0, 16))

        def save():
            new_prompt = txt.get("1.0", "end").strip()
            if not new_prompt:
                messagebox.showwarning("提示", "系统提示词不能为空。")
                return

            c["messages"][0]["content"] = new_prompt
            c["_system_prompt"] = new_prompt
            messagebox.showinfo("已保存", "系统提示词已更新。之后的 AI 请求会使用新的提示词。")
            win.destroy()

        def restore():
            base = c.get("_base_system_prompt") or self.app.mode_data().build_system_prompt(c)
            restored = self.wrap_editable_prompt(base, "")
            txt.delete("1.0", "end")
            txt.insert("1.0", restored)

        ttk.Button(bottom, text="保存", style="Primary.TButton", command=save).pack(side="right")
        ttk.Button(bottom, text="取消", style="Secondary.TButton", command=win.destroy).pack(side="right", padx=8)
        ttk.Button(bottom, text="恢复默认", style="Danger.TButton", command=restore).pack(side="left")

    def handle_death(self):
        self.clear_control()
        ttk.Button(
            self.control_frame,
            text="📜 查看一生总结",
            style="Primary.TButton",
            command=self.request_summary,
        ).pack(pady=14)

    def handle_fast_end(self):
        self.append_history("\n━━━ 游戏结束！ ━━━", "death")
        self.append_history("（快速模式 · 40 岁强制收束）")

        self.clear_control()

        ttk.Button(
            self.control_frame,
            text="📜 查看 40 岁后的人生（后日谈）",
            style="Primary.TButton",
            command=self.request_fast_summary,
        ).pack(pady=14)

    def request_summary(self):
        c = self.app.character
        m = self.app.mode_data()

        if c.get("content_mode") == CONTENT_STORE and hasattr(m, "build_store_summary_prompt"):
            prompt = m.build_store_summary_prompt(c)
            self.set_loading("AI 正在评判这段店铺生涯……")
        else:
            prompt = """角色已离世。请对这一生做出评价与总结。

    严格输出JSON（只输出JSON）：
    {
    "scores": {"legendary": 0, "dramatic": 0, "successful": 0},
    "evaluation": "对这一生的文字评价（200~500字）"
    }"""
            self.set_loading("AI 正在评判你的一生……")

        self.send_to_ai(prompt, self.on_summary_response)

    def request_fast_summary(self):
        self.set_loading("AI 正在描绘 40 岁后的人生……")
        self.send_to_ai(
            """角色 40 岁，快速模式结束。请为角色描绘 40 岁之后的人生总览（后日谈），
包括事业、家庭、晚年、最终结局等。

严格输出JSON（只输出JSON）：
{
  "scores": {"legendary": 0, "dramatic": 0, "successful": 0},
  "evaluation": "对这一生（含后日谈）的总评，300~600字。"
}""",
            self.on_summary_response,
        )

    def on_summary_response(self, data):
        self.app.character["summary"] = data
        self.app.show_page("SummaryPage")

    def clear_control(self):
        for w in self.control_frame.winfo_children():
            w.destroy()

    def set_loading(self, text):
        self.clear_control()
        tk.Label(
            self.control_frame,
            text=f"⏳ {text}",
            bg=COLORS["card"],
            fg=COLORS["warning"],
            font=F_BODY,
        ).pack(pady=18)

    def append_history(self, text, tag=None):
        self.history_text.config(state="normal")
        if tag:
            self.history_text.insert("end", text + "\n", tag)
        else:
            self.history_text.insert("end", text + "\n")
        self.history_text.see("end")
        self.history_text.config(state="disabled")

    def refresh_panel(self):
        c = self.app.character
        m = self.app.mode_data()
        attrs = c.get("final_attributes", {})

        for a in list(m.ATTRIBUTES) + ["LUCK"]:
            if a in self.stats_labels:
                self.stats_labels[a].config(text=str(attrs.get(a, "-")))

        hp = c.get("hp", 0)
        mhp = c.get("max_hp", 0)

        if mhp > 0:
            ratio = hp / mhp
            if hp <= 0 or ratio < 0.3:
                hp_color = COLORS["danger"]
            elif ratio < 0.6:
                hp_color = COLORS["warning"]
            else:
                hp_color = COLORS["success"]

            self.stats_labels["hp"].config(text=f"{hp} / {mhp}", fg=hp_color)
        else:
            self.stats_labels["hp"].config(text="-/-", fg=COLORS["muted"])

        try:
            age = m.get_character_age(c)
        except Exception:
            age = 0

        for key, cfg in getattr(m, "TRACKERS", {}).items():
            if key not in self.stats_labels:
                continue

            value = c.get(key, cfg.get("initial", 0))

            unlock_age = cfg.get("unlock_age")
            if unlock_age is not None and age < unlock_age:
                self.stats_labels[key].config(text=cfg.get("locked_text", "（未解锁）"), fg=COLORS["muted"])
                continue

            tiers = cfg.get("tiers")
            if tiers:
                self.stats_labels[key].config(text=f"{get_tier(value, tiers)} ({value})", fg=COLORS["text"])
            else:
                self.stats_labels[key].config(text=str(value), fg=COLORS["text"])

        if c.get("alive", True):
            try:
                self.title_label.config(text=m.format_time(c))
            except Exception:
                self.title_label.config(text="")
        else:
            try:
                self.title_label.config(text=f"💀 享年 {m.get_character_age(c)} 岁")
            except Exception:
                self.title_label.config(text="💀 已离世")

    def get_state_brief(self):
        c = self.app.character
        m = self.app.mode_data()

        if c.get("content_mode") == CONTENT_STORE:
            attrs = c.get("final_attributes", {})
            attr_str = " ".join(f"{k}={v}" for k, v in attrs.items())
            open_count = len([com for com in c.get("store_commissions", {}).values()
                            if com.get("status") == "open"])
            client_count = len(c.get("store_clients", {}))
            return (
                f"[当前店铺状态] {m.format_time(c)} | {attr_str} | "
                f"❤️HP={c.get('hp', 0)}/{c.get('max_hp', 0)} | "
                f"家底={c.get('assets',0)} | 神秘度={c.get('mystery',0)} | "
                f"名声={c.get('reputation',0)} | 操守={c.get('integrity',0)} | "
                f"风波={c.get('heat',0)}/10 | "
                f"进行中委托={open_count} | 客户名册={client_count} 人"
            )

        attrs = c.get("final_attributes", {})
        attr_str = " ".join(f"{k}={v}" for k, v in attrs.items())
        tracker_parts = []
        for key, cfg in getattr(m, "TRACKERS", {}).items():
            value = c.get(key, cfg.get("initial", 0))
            tiers = cfg.get("tiers")
            label = cfg.get("label", key)
            if tiers:
                tracker_parts.append(f"{label}={get_tier(value, tiers)}({value})")
            else:
                tracker_parts.append(f"{label}={value}")
        edu_world = "有义务教育" if c.get("has_compulsory_edu") else "无义务教育"
        return (
            f"[当前状态] {m.format_time(c)} | {attr_str} | "
            f"❤️HP={c.get('hp', 0)}/{c.get('max_hp', 0)} | "
            f"{' | '.join(tracker_parts)} | 世界规则：{edu_world}"
        )

    def show_api_payload(self):
        """弹出一个窗口，显示即将/刚刚发送给 AI 的完整明文。"""
        content = self.app.character.get("_last_payload",[])
        
        if not content:
            display_text = "（尚未发送过任何请求）"
        else:
            lines =[]
            for msg in content:
                role = msg.get("role", "unknown").upper()
                text = msg.get("content", "")
                lines.append(f"【{role}】\n{text}\n")
            display_text = "-" * 40 + "\n" + ("\n\n".join(lines))
            
        win = tk.Toplevel(self.app)
        win.title("完整发送内容 (API Payload)")
        win.geometry("720x560")
        win.configure(bg=COLORS["bg"])
        win.transient(self.app)
        
        tk.Label(
            win, text="🔍 完整发送内容", bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD
        ).pack(anchor="w", padx=16, pady=(14, 4))
        
        info = "这里显示的是最后一次向 API 实际发出的数据包文本。非常适合排查 AI 为什么发疯或者忘了剧情。"
        lbl = tk.Label(win, text=info, bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL, justify="left")
        lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
        
        txt = scrolledtext.ScrolledText(
            win, font=F_MONO, wrap="word", bg=COLORS["card"], bd=0, 
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        txt.pack(fill="both", expand=True, padx=16, pady=8)
        txt.insert("1.0", display_text)
        txt.config(state="disabled") # 只读模式
        
        bottom = tk.Frame(win, bg=COLORS["bg"])
        bottom.pack(side="bottom", fill="x", padx=16, pady=16)
        ttk.Button(bottom, text="关闭", style="Primary.TButton", command=win.destroy).pack(side="right")

    def send_to_ai(self, user_msg, callback):
        c = self.app.character

        if not self.app.app_state.get("connected"):
            messagebox.showerror("错误", "API 未连接，无法继续推演。")
            self.show_next_button()
            return

        full_msg = f"{self.get_state_brief()}\n\n{user_msg}"
        c["messages"].append({"role": "user", "content": full_msg})

        client = self.app.app_state["client"]
        model = self.app.app_state["model"]
        
        # ========== 省 TOKEN 核心逻辑 ==========
        msgs = c["messages"]
        msgs_to_send =[]
        
        if c.get("adv_save_token", True):
            # 模式开启：提取系统设定 + 最近1200字的纯履历
            system_msgs = [x for x in msgs if x["role"] == "system"]
            hist = self.history_text.get("1.0", "end").strip()
            recent_hist = hist[-1200:] if len(hist) > 1200 else hist
            if recent_hist:
                recent_hist = "...\n" + recent_hist
                
            combined_user_content = f"【最近的人生履历(供参考剧情背景)】\n{recent_hist}\n\n【当前状态与行动指令】\n{full_msg}"
            msgs_to_send = system_msgs +[{"role": "user", "content": combined_user_content}]
        else:
            # 模式关闭：原始的保留上下文法
            if len(msgs) > 40:
                system_msgs =[x for x in msgs if x["role"] == "system"][:4]
                tail = msgs[-30:]
                msgs_to_send = system_msgs + tail
            else:
                msgs_to_send = msgs
                
        c["_last_payload"] = msgs_to_send  # 记录当前即将发送的内容供玩家查看

        def worker():
            raw_text = "（API 请求失败，未获取到返回内容或网络超时）"
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=msgs_to_send,
                    temperature=0.9,
                )

                raw_text = resp.choices[0].message.content
                c["messages"].append({"role": "assistant", "content": raw_text})

                d = parse_ai_json(raw_text)

                self.after(0, lambda: callback(d))

            except Exception as e:
                if c["messages"] and c["messages"][-1]["role"] == "assistant":
                    c["messages"].pop()
                if c["messages"] and c["messages"][-1]["role"] == "user":
                    c["messages"].pop()

                err = str(e)
                self._pending_retry = (user_msg, callback)
                self._last_raw_response = raw_text  

                def show_error():
                    messagebox.showerror(
                        "错误",
                        f"AI 出错或返回格式不对：\n{err}\n\n"
                        f"点「🔁 重试上一次请求」会重新调用 API（不会推进时间、不会重掷事件骰子）。",
                    )
                    self.show_retry_button()

                self.after(0, show_error)

        threading.Thread(target=worker, daemon=True).start()
# ============================================================
# Store Mode (通马桶模拟器) 流程
# ============================================================

    def on_store_intro_response(self, data):
        c = self.app.character
        fine_logs = c.pop("_fine_start_logs", [])
        self.apply_event(data, add_header=True, pre_logs=fine_logs)
        c["store_round"] = 1
        if not c.get("alive", True):
            self.handle_death()
        else:
            self.show_next_button()

    def send_quick_query(self, prompt, callback,
                        system_msg="Return ONLY a JSON object. No prose."):
        """单次 AI 询问，不写入对话历史。"""
        if not self.app.app_state.get("connected"):
            callback(None)
            return

        client = self.app.app_state["client"]
        model = self.app.app_state["model"]
        
        msgs_to_send =[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ]
        self.app.character["_last_payload"] = msgs_to_send

        def worker():
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=msgs_to_send,
                    temperature=0.4,
                    max_tokens=300,
                )
                data = parse_ai_json(resp.choices[0].message.content)
                self.after(0, lambda: callback(data))
            except Exception:
                self.after(0, lambda: callback(None))

        threading.Thread(target=worker, daemon=True).start()


    def attempt_delay_commission(self, com_id):
        c = self.app.character
        m = self.app.mode_data()

        com = c.get("store_commissions", {}).get(com_id)
        if not com:
            return

        if com.get("delays_used", 0) >= m.COMMISSION_AUTO_ABANDON_DELAYS:
            messagebox.showwarning("提示", "这个委托已经拖延太久，下次开始就会自动放弃。")
            return

        if not messagebox.askyesno(
            "拖延委托",
            f"你想拖延委托「{com.get('summary','?')}」吗？\n"
            f"如果客户答应，下次处理享有优势骰。\n"
            f"已拖延 {com.get('delays_used',0)}/{m.COMMISSION_AUTO_ABANDON_DELAYS} 次。",
        ):
            return

        prompt = m.build_delay_check_prompt(c, com_id)
        self.set_loading("正在试探客户……")

        def callback(data):
            self.clear_control()
            self.show_next_button()

            if not data:
                self.append_history("　⏳ 拖延失败：联络中断。", "adj")
                return

            com = c.get("store_commissions", {}).get(com_id)
            if not com:
                return

            narrative = data.get("narrative", "")
            agreed = bool(data.get("agreed", False))

            if agreed:
                com["delays_used"] = com.get("delays_used", 0) + 1
                com["pending_advantage"] = True
                self.append_history(f"　⏳ 拖延：{narrative}", "adj")
                self.append_history("　〔下次处理此委托享有优势骰〕", "adj")
            else:
                self.append_history(f"　⏳ 拖延失败：{narrative}", "adj")

            self.refresh_panel()

        self.send_quick_query(prompt, callback)    

    def next_tick_store(self):
        c = self.app.character
        m = self.app.mode_data()

        m.advance_time(c)
        start_logs = m.apply_turn_start_effects(c)
        
        # ========================================================
        # 检查是否到达预设的营业期限
        # ========================================================
        if c.get("time_tick", 0) >= c.get("store_end_tick", 120):
            self.append_history("\n━━━ 营业期满！ ━━━", "death")
            self.append_history(f"（到达预定结束时间：第 {c['store_end_tick']} 旬）")
            self.refresh_panel()
            self.clear_control()
            ttk.Button(
                self.control_frame,
                text="📜 查看店铺生涯总结",
                style="Primary.TButton",
                command=self.request_summary,
            ).pack(pady=14)
            return

        rnd = c.get("store_round", 0)

        if rnd == 1:
            c["store_round"] = 2
            self.set_loading("第一位客人正在登门……")
            self.send_to_ai(m.build_first_client_prompt(c),
                            lambda d: self.on_store_event_response(d, start_logs))
            return

        if rnd == 2:
            c["store_round"] = 3
            self.append_history("\n" + m.format_history_header(c), "year")
            if start_logs:
                self.append_history(f"　〔{' / '.join(start_logs)}〕", "adj")
            self.append_history("　这一旬风平浪静。请决定你今后的命运。")
            self.refresh_panel()
            self.show_store_tone_choice()
            return

        # ========================================================
        # rnd >= 3 正常循环：新的麻烦判定链 (HEAT -> MYST -> REPT/INTE + HMR)
        # ========================================================
        self.append_history("\n" + m.format_history_header(c), "year")
        if start_logs:
            self.append_history(f"　〔{' / '.join(start_logs)}〕", "adj")

        heat = c.get("heat", 0)
        myst = c.get("mystery", 25)
        
        trouble_hits = False # 记录最终是否触发了麻烦

        # 1. 检定 HEAT (抛 d100，小于等于 HEAT 则被注意到)
        if random.randint(1, 100) <= heat:
            # 被注意到了！
            # 2. 检定 MYSTERY (抛 d100，小于等于 MYST 则成功隐藏)
            if random.randint(1, 100) <= myst:
                self.append_history("　似乎有人在打你的主意，但没抓到你的尾巴。")
            else:
                # 藏不住了，进行最后的摆脱检定
                # 组1：名声(劣势) 或 操守(劣势)
                rept_check = m.perform_skill_check(c, "REPUTATION", advantage_override="disadvantage")
                inte_check = m.perform_skill_check(c, "INTEGRITY", advantage_override="disadvantage")
                group1_pass = rept_check["success"] or inte_check["success"]
                
                # 组2：人脉(普通)
                hmr_check = m.perform_skill_check(c, "HMR", difficulty="normal")
                group2_pass = hmr_check["success"]

                # 打印检定过程给玩家看
                self.append_history("　【遭遇麻烦：危机逃脱检定】", "adj")
                self.append_history(f"　{m.format_check_log(rept_check)}", "adj")
                self.append_history(f"　{m.format_check_log(inte_check)}", "adj")
                self.append_history(f"　{m.format_check_log(hmr_check)}", "adj")

                if group1_pass and group2_pass:
                    # 逃脱成功！找个熟人背书
                    active_clients = m.get_active_clients(c)
                    if active_clients:
                        savior = random.choice(active_clients)
                        savior_name = savior.get("name", "一个老朋友")
                        savior["relationship"] = "感激"
                    else:
                        savior_name = "一个老朋友"
                        
                    self.append_history(f"　麻烦差点找上了你，但是{savior_name}帮你解决了问题。")
                else:
                    # 彻底失败，麻烦上门
                    trouble_hits = True

        if trouble_hits:
            # 将处理权交给 AI
            self.trigger_store_event("k", [])
            return

        # 如果没遇到麻烦，或者成功化解了麻烦，才判断这旬有没有委托
        if random.random() < c.get("event_chance", 0.5):
            kind = m.roll_event_kind(c) # 抽取新客户(n)或老客户(l)
            self.trigger_store_event(kind, [])
        else:
            self.append_history("　风平浪静......你可以自由进行行动。")
            self.refresh_panel()
            self.show_next_button()

    def show_store_tone_choice(self):
        self.clear_control()
        tk.Label(self.control_frame, text="请决定你的命运……",
                bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(pady=4)
        bf = tk.Frame(self.control_frame, bg=COLORS["card"])
        bf.pack()
        for label, prob in [
            ("A. 搅风舞云（事件75%）", 0.75),
            ("B. 放任自然（事件50%）", 0.50),
            ("C. 韬光养晦（事件25%）", 0.25),
        ]:
            ttk.Button(bf, text=label, style="Secondary.TButton",
                    command=lambda p=prob: self.set_store_tone(p)).pack(side="left", padx=6)

    def set_store_tone(self, prob):
        c = self.app.character
        c["event_chance"] = prob
        label = {0.75: "搅风舞云", 0.50: "放任自然", 0.25: "韬光养晦"}[prob]
        c["messages"].append({
            "role": "system",
            "content": f"【店主基调】玩家选择了「{label}」（事件出现几率 {int(prob*100)}%）。"
        })
        self.show_next_button()

    def trigger_store_event(self, kind, start_logs):
        c = self.app.character
        m = self.app.mode_data()

        if kind == "l":
            client = m.pick_old_client_for_visit(c)
            if not client:
                kind = "n"
            else:
                self.set_loading(f"{client.get('name','某位')} 熟客来访……")
                self.send_to_ai(
                    m.build_event_prompt(c, "l", client=client),
                    lambda d: self.on_store_event_response(d, start_logs, expected_client=client),
                )
                return

        if kind == "n":
            self.set_loading("有新客人来访……")
            prompt = m.build_event_prompt(c, "n")
        elif kind == "k":
            self.set_loading("一桩麻烦找上门……")
            prompt = m.build_event_prompt(c, "k")
        else:
            self.set_loading("时光在店里慢慢流淌……")
            prompt = m.build_event_prompt(c, "quiet")

        self.send_to_ai(prompt, lambda d: self.on_store_event_response(d, start_logs))

    def on_store_event_response(self, data, start_logs=None, expected_client=None):
        c = self.app.character
        start_logs = start_logs or []

        self.apply_event(data, add_header=True, pre_logs=start_logs)

        if not c.get("alive", True):
            self.handle_death()
            return

        se = data.get("store_event") or {}
        kind = se.get("kind", "none")

        if kind == "new_client":
            self.handle_new_client_event(se, data)
        elif kind == "old_client":
            self.handle_old_client_event(se, data, expected_client=expected_client)
        elif kind == "trouble":
            self.handle_trouble_event(se, data)
        else:  # quiet / none / resolution etc
            if data.get("has_choice"):
                self.show_store_choices(data.get("choices") or {}, allow_reject=False)
            else:
                self.show_next_button()

    def handle_new_client_event(self, se, data):
        c = self.app.character
        client_data = dict(se.get("client") or {})
        task_data = dict(se.get("task") or {})

        c["_pending_client_data"] = client_data
        c["_pending_task_data"] = task_data
        c["_pending_event_kind"] = "n"
        c["_pending_existing_client_id"] = None

        dlg = NewCommissionDialog(self.app, client_data, task_data, returning=False)
        self.app.wait_window(dlg)

        self.append_history(
            f"　📜 任务标题：{task_data.get('summary','?')}（来访者：{client_data.get('name','?')}）",
            "choice",
        )

        if data.get("has_choice"):
            self.show_store_choices(data.get("choices") or {}, allow_reject=True)
        else:
            self.show_next_button()

    def handle_old_client_event(self, se, data, expected_client=None):
        c = self.app.character
        m = self.app.mode_data()

        client_id = se.get("client_id") or (expected_client.get("id") if expected_client else None)
        if not client_id or client_id not in c.get("store_clients", {}):
            if data.get("has_choice"):
                self.show_store_choices(data.get("choices") or {}, allow_reject=False)
            else:
                self.show_next_button()
            return

        client = c["store_clients"][client_id]
        client["last_seen_tick"] = m.get_time_tick(c)

        follow_up_kind = se.get("follow_up_kind", "")
        task_data = se.get("task")

        if task_data and follow_up_kind in ("new_request", "unfinished_business"):
            c["_pending_client_data"] = client
            c["_pending_task_data"] = dict(task_data)
            c["_pending_event_kind"] = "l"
            c["_pending_existing_client_id"] = client_id

            dlg = NewCommissionDialog(self.app, client, task_data, returning=True)
            self.app.wait_window(dlg)

            self.append_history(
                f"　📜 熟客「{client.get('name','?')}」带新委托：{task_data.get('summary','?')}",
                "choice",
            )

            if data.get("has_choice"):
                self.show_store_choices(data.get("choices") or {}, allow_reject=True)
            else:
                self.show_next_button()
        else:
            c["_active_client_id"] = client_id
            c["_active_event_kind"] = "l"
            if data.get("has_choice"):
                self.show_store_choices(data.get("choices") or {}, allow_reject=False)
            else:
                self.show_next_button()

    def handle_trouble_event(self, se, data):
        c = self.app.character
        c["_active_event_kind"] = "k"
        if data.get("has_choice"):
            self.show_store_choices(data.get("choices") or {}, allow_reject=False)
        else:
            self.show_next_button()

    def _commit_pending_commission(self):
        c = self.app.character
        m = self.app.mode_data()

        if not c.get("_pending_task_data"):
            return

        existing_id = c.get("_pending_existing_client_id")
        if existing_id and existing_id in c.get("store_clients", {}):
            client_id = existing_id
        else:
            client_id = m.add_client(c, dict(c["_pending_client_data"]))

        com_id = m.add_commission(c, dict(c["_pending_task_data"]), client_id=client_id)

        c["_active_commission_id"] = com_id
        c["_active_client_id"] = client_id
        c["_active_event_kind"] = c.get("_pending_event_kind", "n")

        c["_pending_client_data"] = None
        c["_pending_task_data"] = None
        c["_pending_event_kind"] = None
        c["_pending_existing_client_id"] = None

        self.append_history("　✅ 你接下了委托。客户已入名册。", "adj")
        self.refresh_panel()

    def show_store_choices(self, choices, allow_reject=False):
        self.clear_control()

        tk.Label(self.control_frame, text="你的选择是？",
                bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(pady=2)

        bf = tk.Frame(self.control_frame, bg=COLORS["card"])
        bf.pack(fill="x")

        for key in ["A", "B", "C"]:
            if key not in choices:
                continue
            choice = choices[key]
            if isinstance(choice, str):
                desc, checks, difficulty = choice,[], "normal"
            else:
                desc = choice.get("text", "")
                checks = choice.get("checks", []) or[]
                difficulty = choice.get("difficulty", "normal")

            check_tag = "/".join(checks) if checks else "?"
            diff_zh = {"easy": "易", "normal": "中", "hard": "难"}.get(difficulty, "?")
            label = f"{key}. [{check_tag}|{diff_zh}] {desc}"

            btn = tk.Button(
                bf, text=label, justify="left", anchor="w",
                bg="#F4F6FB", fg=COLORS["text"], font=F_BODY,
                activebackground="#E8EAF1", bd=0,
                padx=12, pady=6, relief="flat", cursor="hand2",
                command=lambda k=key, d=desc, ch=checks, df=difficulty:
                    self.make_store_choice(k, d, ch, df),
            )
            btn.pack(fill="x", pady=2)
            auto_wrap(btn, padding=80)

        if allow_reject:
            ttk.Button(bf, text="❌ 拒绝委托", style="Danger.TButton",
                    command=self.reject_pending_commission).pack(fill="x", pady=4)

        cf = tk.Frame(self.control_frame, bg=COLORS["card"])
        cf.pack(fill="x", pady=4)
        tk.Label(cf, text="或自己来：", bg=COLORS["card"],
                fg=COLORS["subtext"], font=F_SMALL).pack(side="left")
        self.custom_entry = ttk.Entry(cf)
        self.custom_entry.pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(cf, text="提交", style="Secondary.TButton",
                command=self.make_store_custom_choice).pack(side="left")
                
        c = self.app.character
        if c.get("adv_edit_prompt"):
            ttk.Button(cf, text="🛠 提示词", style="Ghost.TButton",
                    command=self.edit_system_prompt).pack(side="left", padx=4)
        if c.get("adv_show_payload"):
            ttk.Button(cf, text="📄 发送内容", style="Ghost.TButton",
                    command=self.show_api_payload).pack(side="left", padx=4)

    def make_store_choice(self, key, desc, checks, difficulty):
        c = self.app.character
        m = self.app.mode_data()

        self.append_history(f"　→ 你选择了 {key}：{desc}", "choice")

        if c.get("_pending_task_data"):
            self._commit_pending_commission()

        com_id = c.get("_active_commission_id")
        advantage_override = None
        if com_id and com_id in c.get("store_commissions", {}):
            com = c["store_commissions"][com_id]
            if com.get("pending_advantage"):
                advantage_override = "advantage"
                com["pending_advantage"] = False
        checks = self.filter_valid_checks(checks) # <--- 新增这一行

        if not checks:
            checks = ["INT"]

        check_results = []
        for attr in checks:
            result = m.perform_skill_check(
                c, attr, difficulty=difficulty, advantage_override=advantage_override
            )
            check_results.append(result)
            self.append_history(f"　{m.format_check_log(result)}", "adj")
            growth_log = m.apply_skill_check_growth(c, result)
            if growth_log:
                self.append_history(f"　〔{growth_log}〕", "adj")

        self.refresh_panel()

        self.set_loading("正在推演结果……")
        self.send_to_ai(
            m.build_resolution_prompt(
                c, action_summary=f"{key}：{desc}",
                check_results=check_results,
                commission_id=c.get("_active_commission_id"),
                client_id=c.get("_active_client_id"),
                event_kind=c.get("_active_event_kind"),
            ),
            self.on_store_resolution_response,
        )

    def make_store_custom_choice(self):
        text = self.custom_entry.get().strip()
        if not text:
            messagebox.showinfo("提示", "请输入你的行动。")
            return
        self.append_history(f"　→ 你选择了自定义：{text}", "choice")
        self.set_loading("正在分析你的行动……")
        self.send_action_check(text)

    def send_action_check_normal(self, action_text):
        """普通/性压抑模式：先问 AI 用什么属性，再投骰子。"""
        c = self.app.character
        m = self.app.mode_data()

        if not self.app.app_state.get("connected"):
            self.set_loading("正在推演……")
            self.send_to_ai(
                f"玩家选择了自定义行动：{action_text}。请推演结果。",
                self.on_choice_response,
            )
            return

        client = self.app.app_state["client"]
        model = self.app.app_state["model"]
        prompt = m.build_action_check_prompt(c, action_text)
        
        msgs_to_send =[
            {"role": "system", "content": "Return ONLY a JSON object describing skill checks. No prose."},
            {"role": "user", "content": prompt},
        ]
        c["_last_payload"] = msgs_to_send

        def worker():
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=msgs_to_send,
                    temperature=0.3,
                    max_tokens=200,
                )
                data = parse_ai_json(resp.choices[0].message.content)
                checks = data.get("checks") or[]
                difficulty = data.get("difficulty") or "normal"
                self.after(0, lambda: self.execute_normal_custom_action(action_text, checks, difficulty))
            except Exception as e:
                err = str(e)
                def fallback():
                    self.set_loading("正在推演……")
                    self.send_to_ai(
                        f"玩家选择了自定义行动：{action_text}。请推演结果。",
                        self.on_choice_response,
                    )
                self.after(0, fallback)

        threading.Thread(target=worker, daemon=True).start()

    def execute_custom_action(self, action_text, checks, difficulty):
        c = self.app.character
        m = self.app.mode_data()

        if c.get("_pending_task_data"):
            self._commit_pending_commission()

        com_id = c.get("_active_commission_id")
        advantage_override = None
        if com_id and com_id in c.get("store_commissions", {}):
            com = c["store_commissions"][com_id]
            if com.get("pending_advantage"):
                advantage_override = "advantage"
                com["pending_advantage"] = False
                checks = self.filter_valid_checks(checks) # <--- 新增这一行
                if not checks:
                    checks =["INT"]

        check_results = []
        for attr in checks:
            result = m.perform_skill_check(
                c, attr, difficulty=difficulty, advantage_override=advantage_override
            )
            check_results.append(result)
            self.append_history(f"　{m.format_check_log(result)}", "adj")
            growth_log = m.apply_skill_check_growth(c, result)
            if growth_log:
                self.append_history(f"　〔{growth_log}〕", "adj")

        self.refresh_panel()

        self.set_loading("正在推演结果……")
        self.send_to_ai(
            m.build_resolution_prompt(
                c, action_summary=action_text,
                check_results=check_results,
                commission_id=c.get("_active_commission_id"),
                client_id=c.get("_active_client_id"),
                event_kind=c.get("_active_event_kind"),
            ),
            self.on_store_resolution_response,
        )

    def on_store_resolution_response(self, data):
        c = self.app.character
        m = self.app.mode_data()

        self.apply_event(data, add_header=False)

        if not c.get("alive", True):
            self.handle_death()
            return

        se = data.get("store_event") or {}

        if se.get("kind") == "resolution":
            com_id = se.get("commission_id") or c.get("_active_commission_id")
            if com_id and com_id in c.get("store_commissions", {}):
                com = c["store_commissions"][com_id]
                outcome = se.get("outcome", "ongoing")
                if outcome in ("resolved", "failed", "partial"):
                    # 状态修改
                    com["status"] = outcome if outcome != "partial" else "resolved"
                    com["resolution"] = (data.get("narrative", "") or "")[:160]
                    if outcome == "partial":
                        com["resolution"] = "(部分达成) " + com["resolution"]
                    
                    c["_active_commission_id"] = None
                    
                    # ========================================================
                    # 核心机制：委托结案/失败的硬编码奖惩
                    # ========================================================
                    import random
                    
                    if outcome in ("resolved", "partial"):
                        # 成功完成：HMR, CRE, INT 各获得 1 次 1d6 的成长检定
                        for attr in ["HMR", "CRE", "INT"]:
                            attr_val = c["final_attributes"].get(attr, 30)
                            # COC式成长检定：投掷 d100，大于等于当前属性才成长
                            growth_roll = random.randint(1, 100)
                            if growth_roll >= attr_val:
                                gain = m.roll_dice("1d6")
                                c["final_attributes"][attr] = min(100, attr_val + gain)
                                self.append_history(f"　🌟 结案历练：你的 {attr} 提升了 {gain} 点！", "choice")
                                
                    elif outcome == "failed":
                        # 失败：HEAT 固定增加 1d6，HMR 固定折损 1d6
                        heat_gain = m.roll_dice("1d6")
                        c["heat"] = min(100, c.get("heat", 0) + heat_gain)
                        
                        hmr_loss = m.roll_dice("1d6")
                        c["final_attributes"]["HMR"] = max(1, c["final_attributes"].get("HMR", 30) - hmr_loss)
                        
                        self.append_history(f"　⚠️ 委托失败：风波(HEAT) 增加了 {heat_gain} 点，人脉(HMR) 折损了 {hmr_loss} 点！", "death")

            # 处理客户关系变化
            client_id = c.get("_active_client_id")
            if client_id and client_id in c.get("store_clients", {}):
                rel = se.get("client_relationship_after")
                if rel:
                    c["store_clients"][client_id]["relationship"] = rel
                    c["store_clients"][client_id]["last_seen_tick"] = m.get_time_tick(c)

        if data.get("has_choice"):
            self.show_store_choices(data.get("choices") or {}, allow_reject=False)
        else:
            c["_active_commission_id"] = None
            c["_active_client_id"] = None
            c["_active_event_kind"] = None
            self.refresh_panel()
            self.show_next_button()

    def reject_pending_commission(self):
        c = self.app.character
        m = self.app.mode_data()

        pending_name = "客户"
        if c.get("_pending_client_data"):
            pending_name = c["_pending_client_data"].get("name", "客户")

        c["_pending_client_data"] = None
        c["_pending_task_data"] = None
        c["_pending_event_kind"] = None
        c["_pending_existing_client_id"] = None

        self.append_history(f"　→ 你拒绝了 {pending_name} 的委托", "choice")

        if c.get("store_round", 0) <= 2:
            prompt = m.build_reject_first_client_prompt(c)
        else:
            prompt = m.build_reject_normal_prompt(c, pending_name)

        self.set_loading("处理拒绝……")
        self.send_to_ai(prompt, self.on_reject_response)

    def on_reject_response(self, data):
        self.apply_event(data, add_header=False)
        if not self.app.character.get("alive", True):
            self.handle_death()
        else:
            self.show_next_button()    

    def _show_open_commissions(self):
        c = self.app.character
        m = self.app.mode_data()
        open_coms = m.get_open_commissions(c)

        win = tk.Toplevel(self.app)
        win.title("当前委托")
        win.geometry("640x480")
        win.configure(bg=COLORS["bg"])
        win.transient(self.app)

        tk.Label(win, text="📋 当前进行中的委托",
                bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD).pack(
            anchor="w", padx=16, pady=(14, 4))

        bottom = tk.Frame(win, bg=COLORS["bg"])
        bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 16))
        ttk.Button(bottom, text="关闭", style="Primary.TButton",
                command=win.destroy).pack(side="right")

        wrap, body = make_scrollable(win)
        wrap.pack(fill="both", expand=True, padx=16, pady=4)
        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, pady=4)

        if not open_coms:
            tk.Label(inner, text="（暂无进行中委托）", bg=COLORS["bg"],
                    fg=COLORS["muted"], font=F_BODY).pack(pady=20)
            return

        for com in open_coms:
            outer, card = Card(inner)
            outer.pack(fill="x", pady=4)

            cid = com.get("client_id")
            client = c.get("store_clients", {}).get(cid, {})
            adv = "（已享有优势骰）" if com.get("pending_advantage") else ""

            tk.Label(card, text=f"📜 {com.get('summary','?')}{adv}",
                    bg=COLORS["card"], fg=COLORS["text"],
                    font=F_SUB).pack(anchor="w", padx=14, pady=(12, 4))

            tk.Label(card,
                    text=(f"客户：{client.get('name','未知')}  ·  "
                        f"建立于第 {com.get('created_tick', 0)} 旬  ·  "
                        f"延期 {com.get('delays_used', 0)}/{m.COMMISSION_AUTO_ABANDON_DELAYS}"),
                    bg=COLORS["card"], fg=COLORS["subtext"], font=F_SMALL).pack(
                anchor="w", padx=14)

            details_lbl = tk.Label(card, text=com.get("details", ""),
                                bg=COLORS["card"], fg=COLORS["text"],
                                font=F_BODY, justify="left")
            details_lbl.pack(anchor="w", fill="x", padx=14, pady=(4, 12))
            # 拖延按钮
            btn_row = tk.Frame(card, bg=COLORS["card"])
            btn_row.pack(fill="x", padx=14, pady=(0, 12))

            delay_state = "normal"
            if com.get("delays_used", 0) >= m.COMMISSION_AUTO_ABANDON_DELAYS - 1:
                delay_state = "disabled"

            def _delay(cid=com["id"], wnd=win):
                wnd.destroy()
                self.attempt_delay_commission(cid)

            ttk.Button(
                btn_row,
                text=f"⏳ 拖延（{com.get('delays_used',0)}/{m.COMMISSION_AUTO_ABANDON_DELAYS}）",
                style="Secondary.TButton",
                state=delay_state,
                command=_delay,
            ).pack(side="left", padx=2)

            auto_wrap(details_lbl)

# ============================================================
# 8. Summary
# ============================================================

class SummaryPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        TopBar(self, app, title="✦ 一生总结 ✦", subtitle="盖棺定论").pack(side="top", fill="x")

        bottom = make_bottom(self)
        ttk.Button(bottom, text="🔄 再来一世", style="Primary.TButton", command=self.restart).pack(side="left")
        ttk.Button(bottom, text="📄 导出记录 (.txt)", style="Secondary.TButton", command=self.export_to_txt).pack(
            side="left", padx=8
        )
        ttk.Button(bottom, text="退出", style="Secondary.TButton", command=self.app.quit).pack(side="right")

        wrap, body = make_scrollable(self)
        wrap.pack(side="top", fill="both", expand=True)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        self.scores_frame = tk.Frame(inner, bg=COLORS["bg"])
        self.scores_frame.pack(pady=16)

        outer, card = Card(inner)
        outer.pack(fill="both", expand=True, pady=10)

        tk.Label(card, text="—— AI 评价 ——", bg=COLORS["card"], fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(10, 4)
        )

        self.eval_text = scrolledtext.ScrolledText(
            card,
            height=12,
            font=F_BODY,
            wrap="word",
            bd=0,
            bg=COLORS["card"],
            padx=12,
            pady=8,
            relief="flat",
        )
        self.eval_text.pack(fill="both", expand=True, padx=4, pady=(0, 10))

    def on_show(self):
        for w in self.scores_frame.winfo_children():
            w.destroy()

        summary = self.app.character.get("summary", {})
        scores = summary.get("scores", {})

        for label, key, color in [
            ("🌟 传奇性", "legendary", "#A855F7"),
            ("🎭 戏剧性", "dramatic", "#3B82F6"),
            ("👑 成功性", "successful", "#22C55E"),
        ]:
            f = tk.Frame(self.scores_frame, bg=COLORS["bg"])
            f.pack(side="left", padx=30)

            tk.Label(f, text=label, bg=COLORS["bg"], fg=COLORS["subtext"], font=F_BODY).pack()
            tk.Label(
                f,
                text=str(scores.get(key, "?")),
                bg=COLORS["bg"],
                fg=color,
                font=(FONT_FAM, 32, "bold"),
            ).pack()

        evaluation = summary.get("evaluation", "（AI未提供评价 / 或游戏尚未结束）")

        self.eval_text.config(state="normal")
        self.eval_text.delete("1.0", "end")
        self.eval_text.insert("1.0", evaluation)
        self.eval_text.config(state="disabled")

    def restart(self):
        self.app.reset_character()

        game = self.app.pages["GamePage"]
        game.initialized = False
        game._pending_retry = None
        game.clear_history()
        game.clear_control()

        self.app.show_page("ScenePage")

    def export_to_txt(self):
        c = self.app.character
        m = get_data_module(c)

        try:
            age = m.get_character_age(c)
        except Exception:
            age = 0

        try:
            age_str = f"{int(age)}"
        except Exception:
            age_str = "?"

        default_name = (
            f"重开手账_{c.get('gender', '')}_{c.get('scene_name', '')}_"
            f"{age_str}岁_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        )

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="导出人生记录",
        )

        if not path:
            return

        try:
            content = self._build_export_text()
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            messagebox.showinfo("导出成功", f"已保存到：\n{path}")

        except Exception as e:
            messagebox.showerror("导出失败", f"出错了：{e}")

    def _build_export_text(self):
        c = self.app.character
        m = get_data_module(c)

        L = []
        sep = "═" * 60
        sub = "─" * 60

        L.append(sep)
        L.append(f"  AI 人生重开手账 {VERSION} · 人生记录")
        L.append(sep)
        L.append(f"导出时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        L.append("")

        L.append("【角色信息】")
        L.append(sub)
        L.append(f"世界：{c.get('scene_name', '?')}　[{c.get('scenario_tag', '?')}]")

        if c.get("scene_desc"):
            L.append(f"世界设定：{c['scene_desc']}")

        L.append(f"性别：{c.get('gender', '?')}　种族：{c.get('race', '?')}")

        if c.get("extra_info"):
            L.append(f"额外设定：{c['extra_info']}")

        L.append(f"游戏模式：{build_mode_display(c)}")

        if c.get("fine_enabled"):
            fs = c.get("fine_settings", {})
            ts = fs.get("timestamp", "year")
            ts_ui = FINE_TIMESTAMP_PRESETS.get(ts, {}).get("label", ts)
            L.append(f"Fine Mode：开局 {fs.get('start_age')} 岁，终止 {fs.get('end_age')} 岁，刻度 {ts_ui}")

            init_trackers = c.get("initial_trackers") or {}
            if init_trackers:
                L.append("开局前经历点分配：")
                trackers = getattr(m, "TRACKERS", {})
                for key, val in init_trackers.items():
                    label = trackers.get(key, {}).get("label", key)
                    L.append(f"  {label}({key}) +{val}")

        L.append(f"义务教育：{'是' if c.get('has_compulsory_edu') else '否'}")

        if c.get("backstory"):
            L.append(f"背景故事：{c['backstory']}")

        L.append("")

        L.append("【出生属性】（含天赋调整）")
        L.append(sub)

        attrs = c.get("final_attributes", {})
        ordered_keys = list(getattr(m, "ATTRIBUTES", [])) + ["LUCK"]

        for k in ordered_keys:
            if k in attrs:
                desc = getattr(m, "ATTR_DESC", {}).get(k, "幸运" if k == "LUCK" else "")
                L.append(f"  {k:<5}{desc:<6} = {attrs[k]}")

        for k, v in attrs.items():
            if k not in ordered_keys:
                L.append(f"  {k:<5}        = {v}")

        if c.get("max_hp"):
            L.append(f"  HP_MAX        = {c['max_hp']}")

        L.append("")

        L.append("【天赋】")
        L.append(sub)

        if c.get("talents"):
            for t in c.get("talents", []):
                rarity_label = RARITY_CONFIG.get(t.get("rarity", "common"), {}).get("label", "")
                L.append(f"  ★ [{rarity_label}] {t.get('name', '未知天赋')}")
                if t.get("desc"):
                    L.append(f"      {t['desc']}")
                if t.get("narrative"):
                    L.append(f"      叙事：{t['narrative']}")
        else:
            L.append("（尚未选择天赋）")

        L.append("")

        if c.get("roll_log"):
            L.append("【天赋骰点明细】")
            L.append(sub)
            for entry in c["roll_log"]:
                L.append(f"  {entry}")
            L.append("")

        L.append("【人生履历】")
        L.append(sub)

        try:
            game_page = self.app.pages["GamePage"]
            history = game_page.history_text.get("1.0", "end").rstrip()
        except Exception:
            history = ""

        L.append(history if history else "（人生履历尚未开始）")
        L.append("")

        L.append("【最终状态】")
        L.append(sub)

        try:
            L.append(f"时间：{m.format_time(c)}")
            age = m.get_character_age(c)
        except Exception:
            age = 0
            L.append("时间：未知")

        if c.get("alive", True):
            L.append(f"年龄：{age} 岁（仍在世 / 或尚未结束）")
        else:
            L.append(f"享年：{age} 岁")
            L.append(f"死因：{c.get('cause_of_death', '未知')}")

        L.append(f"HP：{c.get('hp', 0)} / {c.get('max_hp', 0)}")

        for key, cfg in getattr(m, "TRACKERS", {}).items():
            value = c.get(key, cfg.get("initial", 0))
            label = cfg.get("label", key)
            tiers = cfg.get("tiers")

            if tiers:
                L.append(f"{label}：{get_tier(value, tiers)} ({value})")
            else:
                L.append(f"{label}：{value}")

        L.append("")

        summary = c.get("summary", {})

        if summary:
            L.append("【AI 评价】")
            L.append(sub)

            scores = summary.get("scores", {})
            L.append(f"  🌟 传奇性：{scores.get('legendary', '?')}")
            L.append(f"  🎭 戏剧性：{scores.get('dramatic', '?')}")
            L.append(f"  👑 成功性：{scores.get('successful', '?')}")
            L.append("")
            L.append("【评语】")
            L.append(summary.get("evaluation", "（无）"))
            L.append("")

        L.append(sep)
        L.append(f"  导出自 AI 人生重开手账 {VERSION}")
        L.append(sep)

        return "\n".join(L)

# ============================================================
# Store Mode dialogs
# ============================================================

class NewCommissionDialog(tk.Toplevel):
    """新委托弹窗（单弹窗双栏）。"""

    def __init__(self, parent, client_data, task_data, returning=False):
        super().__init__(parent)
        self.title("新委托" if not returning else "熟客委托")
        self.geometry("820x520")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)
        self.grab_set()

        title_text = "📜 新委托登门" if not returning else "📜 熟客带委托上门"
        tk.Label(self, text=title_text, bg=COLORS["bg"],
                 fg=COLORS["text"], font=F_HEAD).pack(anchor="w", padx=16, pady=(14, 4))

        info_text = ("一位新客人首次登门。请阅读两份简报，"
                     "回到主界面用按钮决定如何处理。") if not returning else \
                    "熟客带着新的请求回来了。"
        info_lbl = tk.Label(self, text=info_text, bg=COLORS["bg"],
                            fg=COLORS["subtext"], font=F_SMALL, justify="left")
        info_lbl.pack(anchor="w", fill="x", padx=16, pady=(0, 8))
        auto_wrap(info_lbl)

        # 底部按钮先 pack
        bottom = tk.Frame(self, bg=COLORS["bg"])
        bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 16))
        ttk.Button(bottom, text="关闭并选择行动 → ",
                   style="Primary.TButton", command=self.destroy).pack(side="right")

        # 双栏内容
        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=4)

        # 左栏：任务简报
        left_outer, left_card = Card(body)
        left_outer.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(left_card, text="📋 任务简报", bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(12, 6))

        self._field(left_card, "概要", task_data.get("summary", "?"))
        self._field(left_card, "详情", task_data.get("details", "?"))
        self._field(left_card, "报酬", task_data.get("reward", "?"))
        danger = task_data.get("danger", "?")
        if isinstance(danger, int):
            danger_text = "★" * max(0, min(5, danger)) + f"（{danger}/5）"
        else:
            danger_text = str(danger)
        self._field(left_card, "危险度", danger_text)

        # 右栏：客户简报
        right_outer, right_card = Card(body)
        right_outer.pack(side="left", fill="both", expand=True, padx=(6, 0))

        tk.Label(right_card, text="👤 客户简报", bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(
            anchor="w", padx=14, pady=(12, 6))

        self._field(right_card, "姓名", client_data.get("name", "?"))
        self._field(right_card, "原型", client_data.get("archetype", "?"))
        if client_data.get("appearance"):
            self._field(right_card, "外表", client_data["appearance"])
        if client_data.get("first_impression"):
            self._field(right_card, "第一印象", client_data["first_impression"])
        if returning:
            self._field(right_card, "目前关系", client_data.get("relationship", "中立"))
            if client_data.get("notes"):
                self._field(right_card, "玩家备注", client_data["notes"])

        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self.destroy())

    def _field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLORS["card"])
        row.pack(fill="x", padx=14, pady=2)
        tk.Label(row, text=f"{label}：", bg=COLORS["card"],
                 fg=COLORS["subtext"], font=F_SMALL,
                 width=8, anchor="ne").pack(side="left", anchor="n")
        val_lbl = tk.Label(row, text=str(value), bg=COLORS["card"],
                           fg=COLORS["text"], font=F_BODY,
                           justify="left", anchor="nw")
        val_lbl.pack(side="left", fill="x", expand=True, anchor="n")
        auto_wrap(val_lbl, padding=20)


class ClientRosterDialog(tk.Toplevel):
    """客户名册：浏览、备注、重点关注、拉黑。"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("📜 客户名册")
        self.geometry("820x640")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)

        c = app.character
        m = app.mode_data()

        tk.Label(self, text="📜 客户名册",
                 bg=COLORS["bg"], fg=COLORS["text"], font=F_HEAD).pack(
            anchor="w", padx=16, pady=(14, 4))

        clients = list(c.get("store_clients", {}).values())
        pri = c.get("store_priority_ids", [])
        bl = c.get("store_blacklist_ids", [])

        info_lbl = tk.Label(self,
                            text=(f"共 {len(clients)} 位客户  ·  "
                                  f"⭐重点关注 {len(pri)}/{m.PRIORITY_CLIENTS_MAX}  ·  "
                                  f"🚫拉黑 {len(bl)}"),
                            bg=COLORS["bg"], fg=COLORS["subtext"], font=F_SMALL)
        info_lbl.pack(anchor="w", padx=16, pady=(0, 8))

        # 底部
        bottom = tk.Frame(self, bg=COLORS["bg"])
        bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 16))
        ttk.Button(bottom, text="关闭", style="Primary.TButton",
                   command=self.destroy).pack(side="right")

        # 列表
        wrap, body = make_scrollable(self)
        wrap.pack(fill="both", expand=True, padx=16, pady=4)

        inner = tk.Frame(body, bg=COLORS["bg"])
        inner.pack(fill="both", expand=True, pady=4)

        if not clients:
            tk.Label(inner, text="（暂无客户）", bg=COLORS["bg"],
                     fg=COLORS["muted"], font=F_BODY).pack(pady=20)
            return

        # 排序：重点关注在前
        pri_set = set(pri)
        clients.sort(key=lambda cl: (0 if cl.get("id") in pri_set else 1,
                                      -cl.get("last_seen_tick", 0)))

        for client in clients:
            self._build_card(inner, client, c, m)

    def _build_card(self, parent, client, c, m):
        outer, card = Card(parent)
        outer.pack(fill="x", pady=4)

        cid = client.get("id")
        is_pri = cid in c.get("store_priority_ids", [])
        is_bl = cid in c.get("store_blacklist_ids", [])

        head = tk.Frame(card, bg=COLORS["card"])
        head.pack(fill="x", padx=14, pady=(12, 4))

        tags = []
        if is_pri:
            tags.append("⭐重点")
        if is_bl:
            tags.append("🚫拉黑")
        tag_text = " ".join(tags)

        title_str = f"{client.get('name','?')}  ·  {client.get('archetype','')}"
        if tag_text:
            title_str = f"{tag_text}  {title_str}"

        tk.Label(head, text=title_str, bg=COLORS["card"],
                 fg=COLORS["text"], font=F_SUB).pack(side="left")

        info_text = (f"目前关系：{client.get('relationship', '中立')}  ·  "
                     f"上次见面：第 {client.get('last_seen_tick', 0)} 旬  ·  "
                     f"档案 ID：{cid}")
        tk.Label(card, text=info_text, bg=COLORS["card"],
                 fg=COLORS["subtext"], font=F_SMALL).pack(anchor="w", padx=14)

        # 备注
        notes_frame = tk.Frame(card, bg=COLORS["card"])
        notes_frame.pack(fill="x", padx=14, pady=(8, 4))

        tk.Label(notes_frame, text="玩家备注：", bg=COLORS["card"],
                 fg=COLORS["subtext"], font=F_SMALL).pack(anchor="w")

        notes_text = tk.Text(notes_frame, height=2, font=F_BODY,
                              bg="#FAFBFE", relief="flat",
                              highlightbackground=COLORS["border"],
                              highlightthickness=1, wrap="word")
        notes_text.insert("1.0", client.get("notes", ""))
        notes_text.pack(fill="x")

        # 按钮
        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(fill="x", padx=14, pady=(4, 12))

        def save_notes():
            new_notes = notes_text.get("1.0", "end").rstrip()
            c["store_clients"][cid]["notes"] = new_notes
            messagebox.showinfo("已保存", "备注已保存。", parent=self)

        ttk.Button(btn_row, text="💾 保存备注",
                   style="Secondary.TButton",
                   command=save_notes).pack(side="left", padx=2)

        def toggle_pri():
            result = m.toggle_priority(c, cid)
            if result is None:
                messagebox.showwarning(
                    "提示",
                    f"重点关注名单已满（最多 {m.PRIORITY_CLIENTS_MAX} 位）。",
                    parent=self,
                )
            else:
                self._refresh()

        if not is_bl:
            ttk.Button(btn_row,
                       text=("取消重点" if is_pri else "⭐ 重点关注"),
                       style="Secondary.TButton",
                       command=toggle_pri).pack(side="left", padx=2)

        def toggle_bl():
            m.toggle_blacklist(c, cid)
            self._refresh()

        ttk.Button(btn_row,
                   text=("取消拉黑" if is_bl else "🚫 拉黑"),
                   style="Danger.TButton",
                   command=toggle_bl).pack(side="left", padx=2)

    def _refresh(self):
        # 简单粗暴：销毁后重开
        app = self.app
        self.destroy()
        ClientRosterDialog(app, app)
# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    App().mainloop()