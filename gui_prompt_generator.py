#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ממשק גרפי למחולל פרומפטים מקצועי ליצירת תמונות
GUI for AI Image Prompt Generator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import webbrowser
import threading
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json

# ייבוא המחלקה שיצרנו קודם
from ai_prompt_generator import AIImagePromptGenerator, PromptElements, StyleCategory, LightingType, MoodType, CompositionType

class PromptGeneratorGUI:
    """ממשק גרפי למחולל פרומפטים"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("מחולל פרומפטים מקצועי - AI Image Prompt Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # משתנים
        self.generator = None
        self.current_image_url = None
        
        # יצירת הממשק
        self.create_widgets()
        
        # סגנון
        self.setup_styles()
    
    def setup_styles(self):
        """הגדרת סגנונות הממשק"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # צבעים מותאמים
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Generate.TButton', font=('Arial', 12, 'bold'))
    
    def create_widgets(self):
        """יצירת רכיבי הממשק"""
        # כותרת ראשית
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎨 מחולל פרומפטים מקצועי ליצירת תמונות",
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # מסגרת ראשית
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # מסגרת הגדרות API
        self.create_api_frame(main_frame)
        
        # מסגרת 8 האלמנטים
        self.create_elements_frame(main_frame)
        
        # מסגרת פרומפטים ותמונה
        self.create_output_frame(main_frame)
    
    def create_api_frame(self, parent):
        """יצירת מסגרת הגדרות API"""
        api_frame = ttk.LabelFrame(parent, text="🔑 הגדרות API", padding=10)
        api_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(api_frame, text="מפתח OpenAI API:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.api_key_var = tk.StringVar(value=os.getenv('OPENAI_API_KEY', ''))
        api_entry = tk.Entry(api_frame, textvariable=self.api_key_var, width=50, show='*')
        api_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        
        connect_btn = ttk.Button(api_frame, text="התחבר", command=self.connect_api)
        connect_btn.grid(row=0, column=2)
        
        self.connection_status = tk.Label(api_frame, text="❌ לא מחובר", fg='red', font=('Arial', 10))
        self.connection_status.grid(row=0, column=3, padx=(10, 0))
        
        api_frame.columnconfigure(1, weight=1)
    
    def create_elements_frame(self, parent):
        """יצירת מסגרת 8 האלמנטים"""
        elements_frame = ttk.LabelFrame(parent, text="🎯 מסגרת 8 האלמנטים", padding=10)
        elements_frame.pack(fill='x', pady=(0, 10))
        
        # יצירת שתי עמודות
        left_frame = tk.Frame(elements_frame, bg='#f8f9fa')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = tk.Frame(elements_frame, bg='#f8f9fa')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # עמודה שמאל
        self.create_element_input(left_frame, "1. נושא (Subject) *", "subject", 0, required=True)
        self.create_element_combobox(left_frame, "2. קומפוזיציה (Composition)", "composition", 1, 
                                   [c.value for c in CompositionType])
        self.create_element_combobox(left_frame, "3. סגנון (Style)", "style", 2, 
                                   [s.value for s in StyleCategory])
        self.create_element_combobox(left_frame, "4. תאורה (Lighting)", "lighting", 3, 
                                   [l.value for l in LightingType])
        
        # עמודה ימין
        self.create_element_input(right_frame, "5. צבעים (Colors)", "color", 0)
        self.create_element_combobox(right_frame, "6. מצב רוח (Mood)", "mood", 1, 
                                   [m.value for m in MoodType])
        self.create_element_input(right_frame, "7. פרטים (Details)", "details", 2)
        self.create_element_input(right_frame, "8. הקשר (Context)", "context", 3)
        
        # כפתורי פעולה
        actions_frame = tk.Frame(elements_frame, bg='#f8f9fa')
        actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(actions_frame, text="💾 שמור תבנית", command=self.save_template).pack(side='left', padx=(0, 5))
        ttk.Button(actions_frame, text="📁 טען תבנית", command=self.load_template).pack(side='left', padx=(0, 5))
        ttk.Button(actions_frame, text="🗑️ נקה הכל", command=self.clear_all).pack(side='left', padx=(0, 5))
        
        # דוגמאות מהירות
        examples_frame = tk.Frame(actions_frame, bg='#f8f9fa')
        examples_frame.pack(side='right')
        
        tk.Label(examples_frame, text="דוגמאות מהירות:", font=('Arial', 9), bg='#f8f9fa').pack(side='left', padx=(0, 5))
        ttk.Button(examples_frame, text="חתול", command=lambda: self.load_example("cat")).pack(side='left', padx=2)
        ttk.Button(examples_frame, text="לוגו", command=lambda: self.load_example("logo")).pack(side='left', padx=2)
        ttk.Button(examples_frame, text="נוף", command=lambda: self.load_example("landscape")).pack(side='left', padx=2)
    
    def create_element_input(self, parent, label_text, var_name, row, required=False):
        """יצירת שדה קלט לאלמנט"""
        color = '#e74c3c' if required else '#34495e'
        label = tk.Label(parent, text=label_text, font=('Arial', 10, 'bold'), 
                        fg=color, bg='#f8f9fa')
        label.grid(row=row*2, column=0, sticky='w', pady=(5, 2))
        
        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)
        
        entry = tk.Entry(parent, textvariable=var, width=40, font=('Arial', 10))
        entry.grid(row=row*2+1, column=0, sticky='ew', pady=(0, 10))
        
        parent.columnconfigure(0, weight=1)
    
    def create_element_combobox(self, parent, label_text, var_name, row, values):
        """יצירת רשימה נפתחת לאלמנט"""
        label = tk.Label(parent, text=label_text, font=('Arial', 10, 'bold'), 
                        fg='#34495e', bg='#f8f9fa')
        label.grid(row=row*2, column=0, sticky='w', pady=(5, 2))
        
        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)
        
        combo = ttk.Combobox(parent, textvariable=var, values=[''] + values, 
                           width=37, font=('Arial', 10), state='readonly')
        combo.grid(row=row*2+1, column=0, sticky='ew', pady=(0, 10))
        
        parent.columnconfigure(0, weight=1)
    
    def create_output_frame(self, parent):
        """יצירת מסגרת פלטים ותמונה"""
        output_frame = tk.Frame(parent, bg='#f0f0f0')
        output_frame.pack(fill='both', expand=True)
        
        # מסגרת פרומפטים
        prompt_frame = ttk.LabelFrame(output_frame, text="📝 פרומפטים", padding=10)
        prompt_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # כפתורי יצירה
        buttons_frame = tk.Frame(prompt_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(buttons_frame, text="🔄 צור פרומפט בסיסי", 
                  command=self.generate_basic_prompt, style='Generate.TButton').pack(side='left', padx=(0, 5))
        ttk.Button(buttons_frame, text="✨ שפר עם AI", 
                  command=self.enhance_prompt, style='Generate.TButton').pack(side='left', padx=(0, 5))
        ttk.Button(buttons_frame, text="🎨 צור תמונה", 
                  command=self.generate_image, style='Generate.TButton').pack(side='left')
        
        # טקסט פרומפט בסיסי
        tk.Label(prompt_frame, text="פרומפט בסיסי:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.basic_prompt_text = scrolledtext.ScrolledText(prompt_frame, height=6, font=('Arial', 10))
        self.basic_prompt_text.pack(fill='both', expand=True, pady=(5, 10))
        
        # טקסט פרומפט משופר
        tk.Label(prompt_frame, text="פרומפט משופר:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.enhanced_prompt_text = scrolledtext.ScrolledText(prompt_frame, height=6, font=('Arial', 10))
        self.enhanced_prompt_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # מסגרת תמונה
        image_frame = ttk.LabelFrame(output_frame, text="🖼️ תמונה", padding=10)
        image_frame.pack(side='right', fill='both', padx=(5, 0))
        image_frame.configure(width=400)
        image_frame.pack_propagate(False)
        
        # תצוגת התמונה
        self.image_label = tk.Label(image_frame, text="התמונה תופיע כאן", 
                                   bg='white', relief='sunken', width=50, height=20)
        self.image_label.pack(fill='both', expand=True, pady=(0, 10))
        
        # כפתורי תמונה
        image_buttons = tk.Frame(image_frame)
        image_buttons.pack(fill='x')
        
        ttk.Button(image_buttons, text="🔗 פתח בדפדפן", 
                  command=self.open_image_in_browser).pack(side='left', padx=(0, 5))
        ttk.Button(image_buttons, text="💾 שמור תמונה", 
                  command=self.save_image).pack(side='left')
        
        # פס סטטוס
        self.status_var = tk.StringVar(value="מוכן לשימוש")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief='sunken', anchor='w', bg='#ecf0f1')
        status_bar.pack(side='bottom', fill='x')
    
    def connect_api(self):
        """התחברות ל-API"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("שגיאה", "נא להזין מפתח API")
            return
        
        try:
            self.generator = AIImagePromptGenerator(api_key)
            self.connection_status.config(text="✅ מחובר", fg='green')
            self.status_var.set("התחבר בהצלחה ל-OpenAI API")
            messagebox.showinfo("הצלחה", "התחברות ל-API הצליחה!")
        except Exception as e:
            self.connection_status.config(text="❌ שגיאה", fg='red')
            messagebox.showerror("שגיאה", f"שגיאה בהתחברות: {str(e)}")
    
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
            context=self.context_var.get().strip()
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
    
    def generate_basic_prompt(self):
        """יצירת פרומפט בסיסי"""
        if not self.generator:
            messagebox.showerror("שגיאה", "נא להתחבר תחילה ל-API")
            return
        
        elements = self.get_elements()
        if not elements.subject:
            messagebox.showerror("שגיאה", "נא להזין לפחות נושא לתמונה")
            return
        
        try:
            prompt = self.generator.create_basic_prompt(elements)
            self.basic_prompt_text.delete(1.0, tk.END)
            self.basic_prompt_text.insert(1.0, prompt)
            self.status_var.set("פרומפט בסיסי נוצר בהצלחה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה ביצירת הפרומפט: {str(e)}")
    
    def enhance_prompt(self):
        """שיפור הפרומפט עם AI"""
        if not self.generator:
            messagebox.showerror("שגיאה", "נא להתחבר תחילה ל-API")
            return
        
        basic_prompt = self.basic_prompt_text.get(1.0, tk.END).strip()
        if not basic_prompt:
            messagebox.showerror("שגיאה", "נא ליצור תחילה פרומפט בסיסי")
            return
        
        self.status_var.set("משפר פרומפט עם AI...")
        
        def enhance_thread():
            try:
                enhanced = self.generator.enhance_prompt_with_ai(basic_prompt)
                self.root.after(0, lambda: self._update_enhanced_prompt(enhanced))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("שגיאה", f"שגיאה בשיפור: {str(e)}"))
        
        threading.Thread(target=enhance_thread, daemon=True).start()
    
    def _update_enhanced_prompt(self, enhanced_prompt):
        """עדכון הפרומפט המשופר"""
        self.enhanced_prompt_text.delete(1.0, tk.END)
        self.enhanced_prompt_text.insert(1.0, enhanced_prompt)
        self.status_var.set("פרומפט שופר בהצלחה עם AI")
    
    def generate_image(self):
        """יצירת תמונה"""
        if not self.generator:
            messagebox.showerror("שגיאה", "נא להתחבר תחילה ל-API")
            return
        
        # בחירת הפרומפט המשופר אם קיים, אחרת הבסיסי
        enhanced_prompt = self.enhanced_prompt_text.get(1.0, tk.END).strip()
        basic_prompt = self.basic_prompt_text.get(1.0, tk.END).strip()
        
        prompt = enhanced_prompt if enhanced_prompt else basic_prompt
        if not prompt:
            messagebox.showerror("שגיאה", "נא ליצור תחילה פרומפט")
            return
        
        self.status_var.set("יוצר תמונה... (זה יכול לקחת מספר שניות)")
        
        def generate_thread():
            try:
                image_url = self.generator.generate_image(prompt)
                if image_url:
                    self.root.after(0, lambda: self._load_image(image_url))
                else:
                    self.root.after(0, lambda: messagebox.showerror("שגיאה", "שגיאה ביצירת התמונה"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("שגיאה", f"שגיאה ביצירת התמונה: {str(e)}"))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def _load_image(self, image_url):
        """טעינת התמונה לממשק"""
        try:
            self.current_image_url = image_url
            
            # הורדת התמונה
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # שינוי גודל לממשק
            image.thumbnail((380, 380), Image.Resampling.LANCZOS)
            
            # המרה לפורמט tkinter
            photo = ImageTk.PhotoImage(image)
            
            # עדכון התווית
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # שמירה של הרפרנס
            
            self.status_var.set("תמונה נוצרה בהצלחה!")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת התמונה: {str(e)}")
    
    def open_image_in_browser(self):
        """פתיחת התמונה בדפדפן"""
        if self.current_image_url:
            webbrowser.open(self.current_image_url)
        else:
            messagebox.showwarning("אזהרה", "אין תמונה זמינה")
    
    def save_image(self):
        """שמירת התמונה"""
        if not self.current_image_url:
            messagebox.showwarning("אזהרה", "אין תמונה זמינה")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                response = requests.get(self.current_image_url)
                with open(filename, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo("הצלחה", f"התמונה נשמרה ב: {filename}")
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בשמירת התמונה: {str(e)}")
    
    def save_template(self):
        """שמירת תבנית"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                elements = self.get_elements()
                self.generator.save_elements_template(elements, filename) if self.generator else None
                
                # שמירה ישירה אם אין generator
                if not self.generator:
                    with open(filename, 'w', encoding='utf-8') as f:
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
                if self.generator:
                    elements = self.generator.load_elements_template(filename)
                else:
                    # טעינה ישירה
                    with open(filename, 'r', encoding='utf-8') as f:
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
        self.basic_prompt_text.delete(1.0, tk.END)
        self.enhanced_prompt_text.delete(1.0, tk.END)
        self.image_label.config(image='', text="התמונה תופיע כאן")
        self.current_image_url = None
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
                context="צילום מקצועי"
            ),
            "logo": PromptElements(
                subject="לוגו מינימליסטי",
                composition="symmetrical",
                style="minimalist",
                lighting="clean lighting",
                color="כחול וצבעי אמון",
                mood="professional",
                details="פשוט וזכיר",
                context="מיתוג עסקי"
            ),
            "landscape": PromptElements(
                subject="נוף הרים עם אגם",
                composition="wide angle",
                style="realistic",
                lighting="dramatic sunset",
                color="צבעי זהב וכתום",
                mood="calm",
                details="השתקפויות במים",
                context="צילום טבע"
            )
        }
        
        if example_type in examples:
            self.set_elements(examples[example_type])
            self.status_var.set(f"נטענה דוגמא: {example_type}")

def main():
    """הפעלת הממשק הגרפי"""
    root = tk.Tk()
    
    # הגדרת RTL לעברית
    try:
        root.option_add('*Font', 'Arial 10')
    except:
        pass
    
    app = PromptGeneratorGUI(root)
    
    # מרכוז החלון
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()