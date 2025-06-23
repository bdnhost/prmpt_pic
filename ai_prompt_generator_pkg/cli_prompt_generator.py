#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
גרסה פשוטה של מחולל פרומפטים ליצירת תמונות - ממשק שורת פקודה
Simple Prompt Generator for AI Images - CLI Version
"""

import json
import os
import argparse
from dataclasses import dataclass
from enum import Enum


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


class SimplePromptGenerator:
    """מחולל פרומפטים פשוט"""

    def __init__(self):
        """אתחול המחולל"""
        pass

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

    def save_template(self, elements, filename):
        """שמירת תבנית לקובץ"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(elements.__dict__, f, ensure_ascii=False, indent=2)
        print(f"התבנית נשמרה ב: {filename}")

    def load_template(self, filename):
        """טעינת תבנית מקובץ"""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return PromptElements(**data)


def print_examples():
    """הדפסת דוגמאות שימוש"""
    examples = """
דוגמאות שימוש:

1. יצירת פרומפט בסיסי:
   python cli_prompt_generator.py --subject "חתול פרסי לבן" --style "professional photography" --mood "calm"

2. שמירת תבנית:
   python cli_prompt_generator.py --subject "נוף הרים" --style "oil painting" --mood "calm" --save-template "mountain_template.json"

3. טעינת תבנית:
   python cli_prompt_generator.py --load-template "mountain_template.json"

4. שימוש בדוגמא מוכנה:
   python cli_prompt_generator.py --example "cat"
"""
    print(examples)


def main():
    """פונקציה ראשית"""
    parser = argparse.ArgumentParser(
        description="מחולל פרומפטים פשוט ליצירת תמונות - גרסת CLI"
    )

    # פרמטרים בסיסיים
    parser.add_argument("--subject", help="נושא התמונה")
    parser.add_argument(
        "--composition", choices=[c.value for c in CompositionType], help="קומפוזיציה"
    )
    parser.add_argument(
        "--style", choices=[s.value for s in StyleCategory], help="סגנון"
    )
    parser.add_argument(
        "--lighting", choices=[l.value for l in LightingType], help="תאורה"
    )
    parser.add_argument("--colors", help="צבעים")
    parser.add_argument("--mood", choices=[m.value for m in MoodType], help="מצב רוח")
    parser.add_argument("--details", help="פרטים נוספים")
    parser.add_argument("--context", help="הקשר")

    # פרמטרים לשמירה וטעינה
    parser.add_argument("--save-template", help="שמירת התבנית לקובץ")
    parser.add_argument("--load-template", help="טעינת תבנית מקובץ")

    # דוגמאות מוכנות
    parser.add_argument(
        "--example", choices=["cat", "logo", "landscape"], help="טעינת דוגמא מוכנה"
    )

    # עזרה
    parser.add_argument("--examples", action="store_true", help="הצגת דוגמאות שימוש")

    args = parser.parse_args()

    # הצגת דוגמאות
    if args.examples:
        print_examples()
        return

    generator = SimplePromptGenerator()

    # טעינת דוגמא מוכנה
    if args.example:
        elements = load_example(args.example)
    # טעינת תבנית מקובץ
    elif args.load_template:
        try:
            elements = generator.load_template(args.load_template)
            print(f"תבנית נטענה מהקובץ: {args.load_template}")
        except Exception as e:
            print(f"שגיאה בטעינת התבנית: {str(e)}")
            return
    # יצירת אלמנטים חדשים
    else:
        elements = PromptElements(
            subject=args.subject or "",
            composition=args.composition or "",
            style=args.style or "",
            lighting=args.lighting or "",
            color=args.colors or "",
            mood=args.mood or "",
            details=args.details or "",
            context=args.context or "",
        )

    # בדיקה שיש לפחות נושא
    if not elements.subject and not args.load_template:
        print("שגיאה: נא להזין לפחות נושא לתמונה (--subject)")
        return

    # יצירת הפרומפט
    prompt = generator.create_basic_prompt(elements)
    print("\nהפרומפט שנוצר:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)

    # שמירת התבנית
    if args.save_template:
        try:
            generator.save_template(elements, args.save_template)
        except Exception as e:
            print(f"שגיאה בשמירת התבנית: {str(e)}")


def load_example(example_type):
    """טעינת דוגמאות מוכנות"""
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

    print(f"נטענה דוגמא: {example_type}")
    return examples.get(example_type, PromptElements())


if __name__ == "__main__":
    main()
