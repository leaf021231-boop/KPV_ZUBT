import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import uuid

# ==========================================
# 独立工具 UI 样式 (复用主游戏的设定)
# ==========================================
COLORS = {
    "bg": "#F2F3F7", "card": "#FFFFFF", "primary": "#4A6CF7",
    "text": "#1C1C1E", "subtext": "#6E6E73", "border": "#E1E3E8",
    "danger": "#EF4444"
}
F_HEAD = ("Microsoft YaHei UI", 16, "bold")
F_SUB = ("Microsoft YaHei UI", 12, "bold")
F_BODY = ("Microsoft YaHei UI", 11)
F_SMALL = ("Microsoft YaHei UI", 10)

def make_scrollable(parent):
    wrap = tk.Frame(parent, bg=COLORS["bg"])
    canvas = tk.Canvas(wrap, bg=COLORS["bg"], highlightthickness=0)
    sb = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    inner = tk.Frame(canvas, bg=COLORS["bg"])
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    return wrap, inner

def Card(parent):
    outer = tk.Frame(parent, bg=COLORS["bg"])
    inner = tk.Frame(outer, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
    inner.pack(fill="both", expand=True)
    return outer, inner

# ==========================================
# 剧本编辑器 App
# ==========================================
class ScenarioCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI人生重开 - 自定义剧本工坊")
        self.geometry("800x800")
        self.configure(bg=COLORS["bg"])
        
        # 内部数据
        self.talents = []
        self.mod_rows = []
        
        self._build_ui()

    def _build_ui(self):
        # 头部
        header = tk.Frame(self, bg=COLORS["card"], height=60, highlightbackground=COLORS["border"], highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="✨ 剧本创作工坊 (Scenario Creator)", bg=COLORS["card"], fg=COLORS["text"], font=F_HEAD).pack(side="left", padx=20, pady=15)
        ttk.Button(header, text="📤 导出为 JSON 剧本包", command=self.export_json).pack(side="right", padx=20, pady=15)

        wrap, body = make_scrollable(self)
        wrap.pack(fill="both", expand=True, padx=20, pady=10)

        # ============ 1. 剧本基础设定 ============
        outer, card = Card(body)
        outer.pack(fill="x", pady=5)
        tk.Label(card, text="1. 世界观基础设定", bg=COLORS["card"], font=F_SUB).grid(row=0, column=0, sticky="w", padx=10, pady=10, columnspan=2)
        
        def _lbl(r, txt): tk.Label(card, text=txt, bg=COLORS["card"], font=F_BODY).grid(row=r, column=0, sticky="ne", padx=10, pady=5)
        
        _lbl(1, "剧本 ID (英文/拼音)")
        self.e_id = ttk.Entry(card, width=40)
        self.e_id.grid(row=1, column=1, sticky="w", pady=5)
        self.e_id.insert(0, f"custom_{uuid.uuid4().hex[:6]}")

        _lbl(2, "剧本名称 (UI显示)")
        self.e_name = ttk.Entry(card, width=40)
        self.e_name.grid(row=2, column=1, sticky="w", pady=5)

        _lbl(3, "剧本 Tag (核心关联词)")
        self.e_tag = ttk.Entry(card, width=40)
        self.e_tag.grid(row=3, column=1, sticky="w", pady=5)
        
        _lbl(4, "包含义务教育?")
        self.v_edu = tk.BooleanVar(value=False)
        tk.Checkbutton(card, text="是 (AI会自动执行 1-18 岁教育检定)", variable=self.v_edu, bg=COLORS["card"]).grid(row=4, column=1, sticky="w")

        _lbl(5, "世界观描述")
        self.t_desc = scrolledtext.ScrolledText(card, height=4, width=50, font=F_BODY)
        self.t_desc.grid(row=5, column=1, sticky="w", pady=5)

        # ============ 2. 剧本专属天赋 ============
        outer, card2 = Card(body)
        outer.pack(fill="x", pady=10)
        
        head2 = tk.Frame(card2, bg=COLORS["card"])
        head2.pack(fill="x", padx=10, pady=10)
        tk.Label(head2, text="2. 剧本专属天赋池", bg=COLORS["card"], font=F_SUB).pack(side="left")
        
        self.list_frame = tk.Frame(card2, bg=COLORS["card"])
        self.list_frame.pack(fill="x", padx=10)
        self.refresh_talents()

        # ============ 3. 添加新天赋表单 ============
        outer, form = Card(body)
        outer.pack(fill="x", pady=5)
        tk.Label(form, text="添加新天赋到本剧本", bg=COLORS["card"], font=F_SUB).grid(row=0, column=0, sticky="w", padx=10, pady=10, columnspan=2)

        def _flbl(r, txt): tk.Label(form, text=txt, bg=COLORS["card"], font=F_BODY).grid(row=r, column=0, sticky="ne", padx=10, pady=5)

        _flbl(1, "天赋名称")
        self.te_name = ttk.Entry(form, width=30)
        self.te_name.grid(row=1, column=1, sticky="w", pady=5)

        _flbl(2, "稀有度")
        self.v_rarity = tk.StringVar(value="common")
        rf = tk.Frame(form, bg=COLORS["card"])
        rf.grid(row=2, column=1, sticky="w")
        for r, l in [("negative", "负面"), ("common", "普通"), ("rare", "稀有"), ("legendary", "传奇"), ("wildcard", "特殊")]:
            tk.Radiobutton(rf, text=l, variable=self.v_rarity, value=r, bg=COLORS["card"]).pack(side="left")

        _flbl(3, "适用模式")
        self.v_mode = tk.StringVar(value="Normal")
        mf = tk.Frame(form, bg=COLORS["card"])
        mf.grid(row=3, column=1, sticky="w")
        for m, l in [("Normal", "普通"), ("Store", "通马桶")]:
            tk.Radiobutton(mf, text=l, variable=self.v_mode, value=m, bg=COLORS["card"]).pack(side="left")

        _flbl(4, "描述")
        self.te_desc = ttk.Entry(form, width=50)
        self.te_desc.grid(row=4, column=1, sticky="w", pady=5)

        _flbl(5, "叙事")
        self.te_narr = ttk.Entry(form, width=50)
        self.te_narr.grid(row=5, column=1, sticky="w", pady=5)

        _flbl(6, "属性加成")
        mod_f = tk.Frame(form, bg=COLORS["card"])
        mod_f.grid(row=6, column=1, sticky="w", pady=5)
        self.mod_container = tk.Frame(mod_f, bg=COLORS["card"])
        self.mod_container.pack(fill="x")
        ttk.Button(mod_f, text="+ 添加属性加成 (如 STR, +10)", command=self.add_mod_row).pack(anchor="w", pady=2)

        ttk.Button(form, text="📥 将此天赋保存到剧本", command=self.save_talent).grid(row=7, column=1, sticky="w", pady=15)

    def add_mod_row(self):
        row = tk.Frame(self.mod_container, bg=COLORS["card"])
        row.pack(fill="x", pady=2)
        v_attr = tk.StringVar()
        v_val = tk.StringVar()
        ttk.Entry(row, textvariable=v_attr, width=8).pack(side="left", padx=2)
        ttk.Entry(row, textvariable=v_val, width=12).pack(side="left", padx=2)
        ttk.Button(row, text="X", width=2, command=lambda: self.remove_mod_row(row)).pack(side="left")
        self.mod_rows.append((v_attr, v_val, row))

    def remove_mod_row(self, row):
        self.mod_rows = [m for m in self.mod_rows if m[2] != row]
        row.destroy()

    def save_talent(self):
        name = self.te_name.get().strip()
        if not name: return messagebox.showwarning("提示", "天赋名不能为空")
        
        mods = []
        for v_attr, v_val, _ in self.mod_rows:
            a, v = v_attr.get().strip(), v_val.get().strip()
            if a and v: mods.append([a, v])

        # 强制绑定到当前填写的 scenario_tag
        cur_tag = self.e_tag.get().strip() or "custom_tag"

        t = {
            "name": name,
            "rarity": self.v_rarity.get(),
            "mode": self.v_mode.get(),
            "scenarios": [cur_tag],  # 自动绑定
            "desc": self.te_desc.get().strip(),
            "narrative": self.te_narr.get().strip(),
            "modifiers": mods
        }
        self.talents.append(t)
        
        # 清空表单
        self.te_name.delete(0, 'end')
        self.te_desc.delete(0, 'end')
        self.te_narr.delete(0, 'end')
        for _, _, r in self.mod_rows: r.destroy()
        self.mod_rows = []
        self.refresh_talents()

    def del_talent(self, idx):
        del self.talents[idx]
        self.refresh_talents()

    def refresh_talents(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        if not self.talents:
            tk.Label(self.list_frame, text="暂无天赋", bg=COLORS["card"], fg=COLORS["subtext"]).pack()
            return
        for i, t in enumerate(self.talents):
            f = tk.Frame(self.list_frame, bg=COLORS["bg"])
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"[{t['mode']} | {t['rarity']}] {t['name']}", bg=COLORS["bg"]).pack(side="left", padx=5)
            ttk.Button(f, text="删", width=3, command=lambda idx=i: self.del_talent(idx)).pack(side="right")

    def export_json(self):
        sid = self.e_id.get().strip()
        name = self.e_name.get().strip()
        tag = self.e_tag.get().strip()
        desc = self.t_desc.get("1.0", "end").strip()

        if not name or not tag:
            return messagebox.showwarning("错误", "剧本名称和 Tag 不能为空！")

        scenario_def = {
            "id": sid,
            "name": name,
            "scenario_tag": tag,
            "has_edu": self.v_edu.get(),
            "desc": desc
        }

        # 更新所有天赋的 Tag 为最终 Tag
        for t in self.talents:
            t["scenarios"] = [tag]

        export_data = {
            "scenario_def": scenario_def,
            "talents": self.talents
        }

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"scenario_{tag}.json",
            filetypes=[("JSON 剧本包", "*.json")],
            title="导出剧本"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", f"剧本 {name} 导出成功！\n请在游戏主程序中导入。")

if __name__ == "__main__":
    ScenarioCreator().mainloop()