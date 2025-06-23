#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
גרסה פשוטה של מחולל פרומפטים ליצירת תמונות
Simple Prompt Generator for AI Images
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
from enum import Enum
from dataclasses import dataclass


# הגדרת מבנה הנתונים למסגרת 8 האלמנטים
@dataclass
class PromptElements:
    """מסגרת 8 האלמנטים ליצירת פרומפט מקצועי"""

    subject: str = ""  # נושא - מה/מי בתמונה
    composition: str = ""  # קומפוזיציה - איך מסודר
    style: str = ""  # סגנון - איזה מראה
    lighting: str = ""  # תאורה - איזה אור
    color: str = ""  # צבע - אילו צבעים
    mood: str = ""  # מצב רוח - איזו תחושה
    details: str = ""  # פרטים - מה לכלול/להשמיט
    context: str = ""  # הקשר - למה זה מיועד


class StyleCategory(Enum):
    """קטגוריות סגנונות זמינות"""

    REALISTIC = "realistic"
    CARTOON = "cartoon"
    WATERCOLOR = "watercolor"
    OIL_PAINTING = "oil painting"
    SKETCH = "sketch"
    RENDER_3D = "3D render"
    MINIMALIST = "minimalist"
    VINTAGE = "vintage"
    MODERN = "modern"
    PHOTOGRAPHY = "professional photography"


class LightingType(Enum):
    """סוגי תאורה זמינים"""

    SOFT_MORNING = "soft morning light"
    DRAMATIC_SUNSET = "dramatic sunset"
    STUDIO = "studio lighting"
    NATURAL_DAYLIGHT = "natural daylight"
    MOODY_SHADOWS = "moody shadows"
    BRIGHT_AIRY = "bright and airy"


class MoodType(Enum):
    """סוגי מצבי רוח"""

    ENERGETIC = "energetic"
    CALM = "calm"
    MYSTERIOUS = "mysterious"
    PROFESSIONAL = "professional"
    PLAYFUL = "playful"
    ELEGANT = "elegant"
    RUSTIC = "rustic"
    FUTURISTIC = "futuristic"


class CompositionType(Enum):
    """סוגי קומפוזיציה"""

    CLOSE_UP = "close-up portrait"
    WIDE_ANGLE = "wide angle"
    BIRDS_EYE = "bird's eye view"
    LOW_ANGLE = "low angle"
    SYMMETRICAL = "symmetrical"
    RULE_OF_THIRDS = "rule of thirds"


class SimplePromptGeneratorGUI:
    """ממשק גרפי פשוט למחולל פרומפטים"""

    def __init__(self, root):
        self.root = root
        self.root.title("מחולל פרומפטים פשוט - Simple AI Image Prompt Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # יצירת הממשק
        self.create_widgets()

        # סגנון
        self.setup_styles()

    def setup_styles(self):
        """הגדרת סגנונות הממשק"""
        style = ttk.Style()
        style.theme_use("clam")

        # צבעים מותאמים
        style.configure(
            "Title.TLabel", font=("Arial", 16, "bold"), foreground="#2c3e50"
        )
        style.configure(
            "Header.TLabel", font=("Arial", 12, "bold"), foreground="#34495e"
        )
        style.configure("Generate.TButton", font=("Arial", 12, "bold"))

    def create_widgets(self):
        """יצירת רכיבי הממשק"""
        # כותרת ראשית
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="🎨 מחולל פרומפטים פשוט ליצירת תמונות",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50",
        )
        title_label.pack(pady=15)

        # מסגרת ראשית
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # מסגרת 8 האלמנטים
        self.create_elements_frame(main_frame)

        # מסגרת פרומפטים
        self.create_output_frame(main_frame)

    def create_elements_frame(self, parent):
        """יצירת מסגרת 8 האלמנטים"""
        elements_frame = ttk.LabelFrame(parent, text="🎯 מסגרת 8 האלמנטים", padding=10)
        elements_frame.pack(fill="x", pady=(0, 10))

        # יצירת שתי עמודות
        left_frame = tk.Frame(elements_frame, bg="#f8f9fa")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        right_frame = tk.Frame(elements_frame, bg="#f8f9fa")
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # עמודה שמאל
        self.create_element_input(
            left_frame, "1. נושא (Subject) *", "subject", 0, required=True
        )
        self.create_element_combobox(
            left_frame,
            "2. קומפוזיציה (Composition)",
            "composition",
            1,
            [c.value for c in CompositionType],
        )
        self.create_element_combobox(
            left_frame, "3. סגנון (Style)", "style", 2, [s.value for s in StyleCategory]
        )
        self.create_element_combobox(
            left_frame,
            "4. תאורה (Lighting)",
            "lighting",
            3,
            [l.value for l in LightingType],
        )

        # עמודה ימין
        self.create_element_input(right_frame, "5. צבעים (Colors)", "color", 0)
        self.create_element_combobox(
            right_frame, "6. מצב רוח (Mood)", "mood", 1, [m.value for m in MoodType]
        )
        self.create_element_input(right_frame, "7. פרטים (Details)", "details", 2)
        self.create_element_input(right_frame, "8. הקשר (Context)", "context", 3)

        # כפתורי פעולה
        actions_frame = tk.Frame(elements_frame, bg="#f8f9fa")
        actions_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            actions_frame, text="💾 שמור תבנית", command=self.save_template
        ).pack(side="left", padx=(0, 5))
        ttk.Button(actions_frame, text="📁 טען תבנית", command=self.load_template).pack(
            side="left", padx=(0, 5)
        )
        ttk.Button(actions_frame, text="🗑️ נקה הכל", command=self.clear_all).pack(
            side="left", padx=(0, 5)
        )

        # דוגמאות מהירות
        examples_frame = tk.Frame(actions_frame, bg="#f8f9fa")
        examples_frame.pack(side="right")

        tk.Label(
            examples_frame, text="דוגמאות מהירות:", font=("Arial", 9), bg="#f8f9fa"
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            examples_frame, text="חתול", command=lambda: self.load_example("cat")
        ).pack(side="left", padx=2)
        ttk.Button(
            examples_frame, text="לוגו", command=lambda: self.load_example("logo")
        ).pack(side="left", padx=2)
        ttk.Button(
            examples_frame, text="נוף", command=lambda: self.load_example("landscape")
        ).pack(side="left", padx=2)

    def create_element_input(self, parent, label_text, var_name, row, required=False):
        """יצירת שדה קלט לאלמנט"""
        color = "#e74c3c" if required else "#34495e"
        label = tk.Label(
            parent, text=label_text, font=("Arial", 10, "bold"), fg=color, bg="#f8f9fa"
        )
        label.grid(row=row * 2, column=0, sticky="w", pady=(5, 2))

        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)

        entry = tk.Entry(parent, textvariable=var, width=40, font=("Arial", 10))
        entry.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(0, 10))

        parent.columnconfigure(0, weight=1)

    def create_element_combobox(self, parent, label_text, var_name, row, values):
        """יצירת רשימה נפתחת לאלמנט"""
        label = tk.Label(
            parent,
            text=label_text,
            font=("Arial", 10, "bold"),
            fg="#34495e",
            bg="#f8f9fa",
        )
        label.grid(row=row * 2, column=0, sticky="w", pady=(5, 2))

        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)

        combo = ttk.Combobox(
            parent,
            textvariable=var,
            values=[""] + values,
            width=37,
            font=("Arial", 10),
            state="readonly",
        )
        combo.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(0, 10))

        parent.columnconfigure(0, weight=1)

    def create_output_frame(self, parent):
        """יצירת מסגרת פלטים"""
        output_frame = tk.Frame(parent, bg="#f0f0f0")
        output_frame.pack(fill="both", expand=True)

        # מסגרת פרומפטים
        prompt_frame = ttk.LabelFrame(output_frame, text="📝 פרומפטים", padding=10)
        prompt_frame.pack(fill="both", expand=True)

        # כפתורי יצירה
        buttons_frame = tk.Frame(prompt_frame, bg="white")
        buttons_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            buttons_frame,
            text="🔄 צור פרומפט",
            command=self.generate_prompt,
            style="Generate.TButton",
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            buttons_frame,
            text="📋 העתק לקליפבורד",
            command=self.copy_to_clipboard,
            style="Generate.TButton",
        ).pack(side="left", padx=(0, 5))

        # טקסט פרומפט
        tk.Label(prompt_frame, text="פרומפט:", font=("Arial", 10, "bold")).pack(
            anchor="w"
        )
        self.prompt_text = scrolledtext.ScrolledText(
            prompt_frame, height=10, font=("Arial", 10)
        )
        self.prompt_text.pack(fill="both", expand=True, pady=(5, 10))

        # הסבר
        explanation_frame = ttk.LabelFrame(output_frame, text="ℹ️ הסבר", padding=10)
        explanation_frame.pack(fill="both", expand=True, pady=(10, 0))

        explanation_text = """
מחולל הפרומפטים הפשוט מאפשר לך ליצור פרומפטים מובנים ליצירת תמונות AI.

איך להשתמש:
1. מלא את השדות של 8 האלמנטים (לפחות את שדה הנושא)
2. לחץ על "צור פרומפט" כדי ליצור פרומפט מובנה
3. העתק את הפרומפט והשתמש בו במחולל תמונות AI כמו DALL-E, Midjourney או Stable Diffusion

טיפים:
• ככל שהפרטים ספציפיים יותר, התוצאה טובה יותר
• השתמש במילות מפתח איכות כמו "high quality", "detailed", "professional"
• שמור תבניות שאתה אוהב לשימוש חוזר
        """

        explanation_label = tk.Label(
            explanation_frame,
            text=explanation_text,
            justify="left",
            bg="white",
            padx=10,
            pady=10,
        )
        explanation_label.pack(fill="both", expand=True)

        # פס סטטוס
        self.status_var = tk.StringVar(value="מוכן לשימוש")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            bg="#ecf0f1",
        )
        status_bar.pack(side="bottom", fill="x")

    def get_elements(self):
        """קבלת הערכים מהממשק"""
        return PromptElements(
            subject=self.subject_var.get().strip(),
            composition=self.composition_var.get().strip(),
            style=self.style_var.get().strip(),
            lighting=self.lighting_var.get().strip(),
            color=self.color_var.get().strip(),
            mood=self.mood_var.get().strip(),
            details=self.details_var.get().strip(),
            context=self.context_var.get().strip(),
        )

    def set_elements(self, elements):
        """עדכון הממשק עם ערכים"""
        self.subject_var.set(elements.subject)
        self.composition_var.set(elements.composition)
        self.style_var.set(elements.style)
        self.lighting_var.set(elements.lighting)
        self.color_var.set(elements.color)
        self.mood_var.set(elements.mood)
        self.details_var.set(elements.details)
        self.context_var.set(elements.context)

    def create_basic_prompt(self, elements):
        """יצירת פרומפט בסיסי מאלמנטים"""
        prompt_parts = []

        # נושא (חובה)
        if elements.subject:
            prompt_parts.append(elements.subject)

        # קומפוזיציה
        if elements.composition:
            prompt_parts.append(f"composition: {elements.composition}")

        # סגנון
        if elements.style:
            prompt_parts.append(f"style: {elements.style}")

        # תאורה
        if elements.lighting:
            prompt_parts.append(f"lighting: {elements.lighting}")

        # צבעים
        if elements.color:
            prompt_parts.append(f"colors: {elements.color}")

        # מצב רוח
        if elements.mood:
            prompt_parts.append(f"mood: {elements.mood}")

        # פרטים נוספים
        if elements.details:
            prompt_parts.append(f"details: {elements.details}")

        # הקשר
        if elements.context:
            prompt_parts.append(f"for: {elements.context}")

        # הוספת משפרי איכות
        prompt_parts.extend(["high quality", "detailed", "professional"])

        return ", ".join(prompt_parts)

    def generate_prompt(self):
        """יצירת פרומפט"""
        elements = self.get_elements()
        if not elements.subject:
            messagebox.showerror("שגיאה", "נא להזין לפחות נושא לתמונה")
            return

        try:
            prompt = self.create_basic_prompt(elements)
            self.prompt_text.delete(1.0, tk.END)
            self.prompt_text.insert(1.0, prompt)
            self.status_var.set("פרומפט נוצר בהצלחה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה ביצירת הפרומפט: {str(e)}")

    def copy_to_clipboard(self):
        """העתקת הפרומפט ללוח"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not prompt:
            messagebox.showerror("שגיאה", "אין פרומפט להעתקה")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.status_var.set("הפרומפט הועתק ללוח")

    def save_template(self):
        """שמירת תבנית"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if filename:
            try:
                elements = self.get_elements()
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(elements.__dict__, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("הצלחה", f"התבנית נשמרה ב: {filename}")
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בשמירת התבנית: {str(e)}")

    def load_template(self):
        """טעינת תבנית"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    elements = PromptElements(**data)

                self.set_elements(elements)
                messagebox.showinfo("הצלחה", "התבנית נטענה בהצלחה")
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בטעינת התבנית: {str(e)}")

    def clear_all(self):
        """ניקוי כל השדות"""
        empty_elements = PromptElements()
        self.set_elements(empty_elements)
        self.prompt_text.delete(1.0, tk.END)
        self.status_var.set("השדות נוקו")

    def load_example(self, example_type):
        """טעינת דוגמאות מהירות"""
        examples = {
            "cat": PromptElements(
                subject="חתול פרסי לבן",
                composition="close-up portrait",
                style="professional photography",
                lighting="soft morning light",
                color="גוונים חמים",
                mood="calm",
                details="עיניים כחולות, פרווה רכה",
                context="צילום מקצועי",
            ),
            "logo": PromptElements(
                subject="לוגו מינימליסטי",
                composition="symmetrical",
                style="minimalist",
                lighting="clean lighting",
                color="כחול וצבעי אמון",
                mood="professional",
                details="פשוט וזכיר",
                context="מיתוג עסקי",
            ),
            "landscape": PromptElements(
                subject="נוף הרים עם אגם",
                composition="wide angle",
                style="realistic",
                lighting="dramatic sunset",
                color="צבעי זהב וכתום",
                mood="calm",
                details="השתקפויות במים",
                context="צילום טבע",
            ),
        }

        if example_type in examples:
            self.set_elements(examples[example_type])
            self.status_var.set(f"נטענה דוגמא: {example_type}")


def main():
    """הפעלת הממשק הגרפי"""
    root = tk.Tk()

    # הגדרת RTL לעברית
    try:
        root.option_add("*Font", "Arial 10")
    except:
        pass

    app = SimplePromptGeneratorGUI(root)

    # מרכוז החלון
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
