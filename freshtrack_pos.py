"""
Project: FreshTrack POS System
Build: 9.9.9.NISHU
Developer: Nosrat Jahan
Architecture: Modular Tkinter Interface with JSON Persistence
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import ctypes
from typing import Dict, List, Any


# --- HIGH-DPI SCALING ENABLER (Windows Integration) ---
def enable_high_dpi_scaling():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


# --- SYSTEM GLOBALS ---
CONFIG = {
    "APP_NAME": "FreshTrack POS 🛒",  # অ্যাপের নাম পরিবর্তন করা হয়েছে
    "VERSION": "9.9.9.NISHU",
    "DEVELOPER": "Nosrat Jahan",
    "DATABASE": "pos_data.json",
    "THEME": {
        "primary_bg": "#0B1120",
        "sidebar_bg": "#111827",
        "accent": "#F59E0B",  # Industrial Dark Orange
        "card_bg": "#1F2937",
        "text_main": "#F9FAFB",
        "text_muted": "#9CA3AF"
    }
}


class POSController:
    """Handles all data persistence and business logic."""

    @staticmethod
    def initialize_storage() -> Dict[str, Any]:
        """Loads system data from JSON storage."""
        if os.path.exists(CONFIG["DATABASE"]):
            try:
                with open(CONFIG["DATABASE"], 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        return {"inventory": [], "sales": []}

    @staticmethod
    def sync_storage(data: Dict[str, Any]):
        """Writes current application state to physical storage."""
        try:
            with open(CONFIG["DATABASE"], 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"I/O Operation Failed: {e}")


class SmartPOSApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{CONFIG['APP_NAME']} | Runtime: {CONFIG['VERSION']}")
        self.root.geometry("1150x780")
        self.root.configure(bg=CONFIG["THEME"]["primary_bg"])

        # Data initialization
        self.app_data = POSController.initialize_storage()

        self._build_sidebar()
        self._build_viewport()
        self.navigate("DASHBOARD")

    def _build_sidebar(self):
        """Constructs the primary navigation interface."""
        self.sidebar = tk.Frame(self.root, bg=CONFIG["THEME"]["sidebar_bg"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Identity (Sidebar Header)
        tk.Label(self.sidebar, text="FreshTrack", font=("Segoe UI", 22, "bold"),
                 bg=CONFIG["THEME"]["sidebar_bg"], fg=CONFIG["THEME"]["accent"]).pack(pady=45)

        # Navigational Router
        nav_items = [
            ("📊 Dashboard", "DASHBOARD"),
            ("➕ Add Product", "ADD_ITEM"),
            ("📦 Inventory", "INVENTORY"),
            ("🛒 POS Terminal", "TERMINAL"),
            ("ℹ️ About System", "ABOUT")
        ]

        for label, target in nav_items:
            btn = tk.Button(self.sidebar, text=f"   {label}", font=("Segoe UI", 11),
                            bg=CONFIG["THEME"]["sidebar_bg"], fg=CONFIG["THEME"]["text_muted"],
                            bd=0, anchor="w", padx=25, pady=16, cursor="hand2",
                            command=lambda t=target: self.navigate(t))
            btn.pack(fill="x")
            # Hover effect logic
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1F2937", fg="white"))
            btn.bind("<Leave>",
                     lambda e, b=btn: b.config(bg=CONFIG["THEME"]["sidebar_bg"], fg=CONFIG["THEME"]["text_muted"]))

        # Version Attribution
        tk.Label(self.sidebar, text=f"Release: {CONFIG['VERSION']}", font=("Consolas", 9),
                 bg=CONFIG["THEME"]["sidebar_bg"], fg="#4B5563").pack(side="bottom", pady=15)

    def _build_viewport(self):
        """Initializes the main content area."""
        self.viewport = tk.Frame(self.root, bg=CONFIG["THEME"]["primary_bg"])
        self.viewport.pack(side="right", expand=True, fill="both")

    def navigate(self, target: str):
        """Standard routing engine for view switching."""
        for widget in self.viewport.winfo_children():
            widget.destroy()

        if target == "DASHBOARD":
            self.render_dashboard()
        elif target == "ADD_ITEM":
            self.render_entry_form()
        elif target == "INVENTORY":
            self.render_inventory()
        elif target == "TERMINAL":
            self.render_terminal()
        elif target == "ABOUT":
            self.render_about()

    # --- VIEW RENDERING METHODS ---

    def render_dashboard(self):
        tk.Label(self.viewport, text="System Statistics", font=("Segoe UI", 22, "bold"),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["text_main"]).pack(anchor="w", padx=45, pady=35)

        card_row = tk.Frame(self.viewport, bg=CONFIG["THEME"]["primary_bg"])
        card_row.pack(fill="x", padx=45)

        rev = sum(s['sell_price'] for s in self.app_data['sales'])
        prof = sum(s['profit'] for s in self.app_data['sales'])

        self._create_metric_card(card_row, 0, "TOTAL REVENUE", f"৳ {rev:,.2f}")
        self._create_metric_card(card_row, 1, "NET PROFIT", f"৳ {prof:,.2f}")
        self._create_metric_card(card_row, 2, "ACTIVE BUILD", CONFIG["VERSION"])

    def _create_metric_card(self, parent, col, title, val):
        card = tk.Frame(parent, bg=CONFIG["THEME"]["card_bg"], padx=25, pady=30,
                        highlightthickness=1, highlightbackground="#374151")
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), bg=CONFIG["THEME"]["card_bg"],
                 fg=CONFIG["THEME"]["text_muted"]).pack(anchor="w")
        tk.Label(card, text=val, font=("Segoe UI", 18, "bold"), bg=CONFIG["THEME"]["card_bg"],
                 fg=CONFIG["THEME"]["accent"]).pack(anchor="w", pady=(12, 0))
        parent.grid_columnconfigure(col, weight=1)

    def render_entry_form(self):
        container = tk.Frame(self.viewport, bg=CONFIG["THEME"]["primary_bg"], padx=55, pady=45)
        container.pack(fill="both")

        tk.Label(container, text="Inventory Entry", font=("Segoe UI", 20, "bold"),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["text_main"]).grid(row=0, columnspan=2,
                                                                                         pady=(0, 35), sticky="w")

        fields = ["Product Name:", "Buy Price (৳):", "Sell Price (৳):", "Stock Qty:"]
        self.inputs = []

        for i, label in enumerate(fields):
            tk.Label(container, text=label, font=("Segoe UI", 11), bg=CONFIG["THEME"]["primary_bg"],
                     fg=CONFIG["THEME"]["text_muted"]).grid(row=i + 1, column=0, pady=14, sticky="w")
            ent = tk.Entry(container, font=("Segoe UI", 12), bg=CONFIG["THEME"]["card_bg"], fg="white", bd=0,
                           insertbackground="white", highlightthickness=1, highlightbackground="#374151")
            ent.grid(row=i + 1, column=1, pady=14, padx=25, ipady=9, sticky="ew")

            # Key-binding for rapid data entry
            if i < len(fields) - 1:
                ent.bind("<Return>", lambda e, idx=i: self.inputs[idx + 1].focus())
            else:
                ent.bind("<Return>", lambda e: self.commit_product())
            self.inputs.append(ent)

        self.inputs[0].focus_set()
        tk.Button(container, text="COMMIT TO DATABASE", bg=CONFIG["THEME"]["accent"], fg="white",
                  font=("Segoe UI", 11, "bold"), padx=45, pady=16, bd=0, cursor="hand2",
                  command=self.commit_product).grid(row=5, column=1, pady=35, sticky="e")

    def commit_product(self):
        raw = [e.get() for e in self.inputs]
        if all(raw):
            try:
                new_entry = {"name": raw[0], "buy_price": float(raw[1]), "sell_price": float(raw[2]),
                             "stock": int(raw[3])}
                self.app_data["inventory"].append(new_entry)
                POSController.sync_storage(self.app_data)
                messagebox.showinfo("POS Engine", f"Successfully indexed: {raw[0]}")
                self.navigate("INVENTORY")
            except ValueError:
                messagebox.showerror("Type Conflict", "Numeric fields require valid numbers.")
        else:
            messagebox.showwarning("Validation Error", "Incomplete payload. All fields required.")

    def render_inventory(self):
        tk.Label(self.viewport, text="Warehouse Ledger", font=("Segoe UI", 18, "bold"),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["text_main"]).pack(anchor="w", padx=45, pady=35)

        table_wrap = tk.Frame(self.viewport, bg=CONFIG["THEME"]["card_bg"])
        table_wrap.pack(fill="both", expand=True, padx=45, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=CONFIG["THEME"]["card_bg"], foreground="white",
                        fieldbackground=CONFIG["THEME"]["card_bg"], rowheight=38)
        style.configure("Treeview.Heading", background="#111827", foreground=CONFIG["THEME"]["accent"],
                        font=("Segoe UI", 11, "bold"))

        tree = ttk.Treeview(table_wrap, columns=("N", "B", "S", "Q"), show="headings")
        for cid, text in [("N", "Name"), ("B", "Cost"), ("S", "Retail"), ("Q", "Stock")]:
            tree.heading(cid, text=text);
            tree.column(cid, anchor="center")

        for item in self.app_data["inventory"]:
            tree.insert("", "end", values=(item['name'], item['buy_price'], item['sell_price'], item['stock']))
        tree.pack(fill="both", expand=True)

    def render_terminal(self):
        tk.Label(self.viewport, text="Sales Interface", font=("Segoe UI", 18, "bold"),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["text_main"]).pack(anchor="w", padx=45, pady=35)
        grid = tk.Frame(self.viewport, bg=CONFIG["THEME"]["primary_bg"])
        grid.pack(fill="both", expand=True, padx=45)

        for i, item in enumerate(self.app_data["inventory"]):
            tk.Button(grid, text=f"{item['name']}\n৳{item['sell_price']}", bg=CONFIG["THEME"]["card_bg"], fg="white",
                      font=("Segoe UI", 10, "bold"), width=19, height=4, bd=0,
                      command=lambda x=item: self.execute_sale(x)).grid(row=i // 4, column=i % 4, padx=12, pady=12)

    def execute_sale(self, item):
        if item['stock'] > 0:
            profit = item['sell_price'] - item['buy_price']
            self.app_data["sales"].append({"name": item['name'], "sell_price": item['sell_price'], "profit": profit})
            for i in self.app_data["inventory"]:
                if i['name'] == item['name']: i['stock'] -= 1
            POSController.sync_storage(self.app_data)
            self.navigate("DASHBOARD")
        else:
            messagebox.showerror("Availability Error", "Insufficient stock for this SKU.")

    def render_about(self):
        container = tk.Frame(self.viewport, bg=CONFIG["THEME"]["primary_bg"], padx=65, pady=65)
        container.pack(expand=True)

        tk.Label(container, text=CONFIG["APP_NAME"], font=("Segoe UI", 30, "bold"),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["accent"]).pack()
        tk.Label(container, text=f"Deployment Version: {CONFIG['VERSION']}", font=("Segoe UI", 13),
                 bg=CONFIG["THEME"]["primary_bg"], fg=CONFIG["THEME"]["text_main"]).pack(pady=(5, 25))

        meta_card = tk.Frame(container, bg=CONFIG["THEME"]["card_bg"], padx=45, pady=45,
                             highlightthickness=1, highlightbackground="#374151")
        meta_card.pack()

        logs = [
            ("Lead Developer", CONFIG["DEVELOPER"]),
            ("System Build", CONFIG["VERSION"]),
            ("Backend Stack", "Python Core / JSON Data Stream"),
            ("License", "Proprietary Commercial"),
            ("Origin", "Neuronix Engineering Laboratory")
        ]

        for label, val in logs:
            row = tk.Frame(meta_card, bg=CONFIG["THEME"]["card_bg"], pady=10)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 11, "bold"),
                     bg=CONFIG["THEME"]["card_bg"], fg=CONFIG["THEME"]["text_muted"]).pack(side="left")
            tk.Label(row, text=val, font=("Segoe UI", 11),
                     bg=CONFIG["THEME"]["card_bg"], fg=CONFIG["THEME"]["text_main"]).pack(side="right", padx=(35, 0))


if __name__ == "__main__":
    enable_high_dpi_scaling()
    app_root = tk.Tk()
    application = SmartPOSApp(app_root)
    app_root.mainloop()
