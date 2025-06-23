#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחולל פרומפטים מקצועי ליצירת תמונות עם AI
מבוסס על מסגרת 8 האלמנטים ו-OpenAI API
"""

import os
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum
import openai
from openai import OpenAI
import argparse
import sys

# הגדרת מבנה הנתונים למסגרת 8 האלמנטים
@dataclass
class PromptElements:
    """מסגרת 8 האלמנטים ליצירת פרומפט מקצועי"""
    subject: str = ""           # נושא - מה/מי בתמונה
    composition: str = ""       # קומפוזיציה - איך מסודר
    style: str = ""            # סגנון - איזה מראה
    lighting: str = ""         # תאורה - איזה אור
    color: str = ""            # צבע - אילו צבעים
    mood: str = ""             # מצב רוח - איזו תחושה
    details: str = ""          # פרטים - מה לכלול/להשמיט
    context: str = ""          # הקשר - למה זה מיועד

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

class AIImagePromptGenerator:
    """מחולל פרומפטים מקצועי ליצירת תמונות"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        אתחול המחולל
        
        Args:
            api_key: מפתח API של OpenAI (אם לא מועבר, יחפש במשתנה הסביבה)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("נדרש מפתח API של OpenAI. הגדר את המשתנה OPENAI_API_KEY או העבר את המפתח בקונסטרקטור")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # בנק ביטויים מועילים
        self.style_keywords = {
            'realistic': ['photorealistic', 'lifelike', 'detailed', 'high resolution'],
            'artistic': ['painterly', 'artistic', 'expressive', 'creative'],
            'professional': ['commercial', 'marketing', 'brand', 'corporate'],
            'vintage': ['retro', 'classic', 'nostalgic', 'aged'],
            'modern': ['contemporary', 'sleek', 'clean', 'minimalist']
        }
        
        self.quality_enhancers = [
            "high quality", "detailed", "professional", "masterpiece",
            "8k resolution", "crisp", "sharp focus", "well composed"
        ]
    
    def create_basic_prompt(self, elements: PromptElements) -> str:
        """
        יצירת פרומפט בסיסי מאלמנטים
        
        Args:
            elements: מבנה נתונים של 8 האלמנטים
            
        Returns:
            פרומפט מעוצב
        """
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
    
    def enhance_prompt_with_ai(self, basic_prompt: str, target_use: str = "general") -> str:
        """
        שיפור הפרומפט באמצעות GPT
        
        Args:
            basic_prompt: הפרומפט הבסיסי
            target_use: מטרת השימוש (marketing, art, professional, etc.)
            
        Returns:
            פרומפט משופר
        """
        system_prompt = f"""
        אתה מומחה ליצירת פרומפטים איכותיים למערכות AI ליצירת תמונות.
        המטרה שלך היא לקחת פרומפט בסיסי ולשפר אותו למטרה: {target_use}
        
        עקרונות לשיפור:
        1. הוסף פרטים טכניים רלוונטיים (רזולוציה, סגנון צילום וכו')
        2. השתמש במילות מפתח שמניבות תוצאות איכותיות
        3. הוסף הוראות ספציפיות לקומפוזיציה ותאורה
        4. ודא שהפרומפט ברור ומובנה
        5. הוסף negative prompts לדברים שלא רוצים לראות
        
        החזר רק את הפרומפט המשופר, ללא הסברים נוספים.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"שפר את הפרומפט הבא: {basic_prompt}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content.strip()
            return enhanced_prompt
            
        except Exception as e:
            print(f"שגיאה בשיפור הפרומפט: {e}")
            return basic_prompt
    
    def reverse_engineer_prompt(self, image_description: str) -> PromptElements:
        """
        הנדסה לאחור - יצירת פרומפט מתיאור תמונה
        
        Args:
            image_description: תיאור התמונה
            
        Returns:
            מבנה אלמנטים שמתאים לתיאור
        """
        system_prompt = """
        אתה מומחה לניתוח תמונות וחילוץ אלמנטים ליצירת פרומפטים.
        קבל תיאור של תמונה וחלק אותו ל-8 האלמנטים הבאים:
        1. subject (נושא)
        2. composition (קומפוזיציה)
        3. style (סגנון)
        4. lighting (תאורה)
        5. color (צבע)
        6. mood (מצב רוח)
        7. details (פרטים)
        8. context (הקשר)
        
        החזר תשובה בפורמט JSON עם המפתחות האלה.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"נתח את התמונה הבאה: {image_description}"}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # ניסיון לחלץ JSON מהתשובה
            try:
                # חיפוש JSON בתשובה
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    elements_dict = json.loads(json_match.group())
                    return PromptElements(**elements_dict)
            except:
                pass
            
            # אם לא הצלחנו לחלץ JSON, ננסה לפרסר ידנית
            return self._parse_elements_from_text(result)
            
        except Exception as e:
            print(f"שגיאה בהנדסה לאחור: {e}")
            return PromptElements()
    
    def _parse_elements_from_text(self, text: str) -> PromptElements:
        """פענוח אלמנטים מטקסט חופשי"""
        elements = PromptElements()
        
        # פענוח בסיסי של הטקסט
        lines = text.split('\n')
        for line in lines:
            line = line.strip().lower()
            if 'subject' in line or 'נושא' in line:
                elements.subject = line.split(':')[-1].strip()
            elif 'composition' in line or 'קומפוזיציה' in line:
                elements.composition = line.split(':')[-1].strip()
            elif 'style' in line or 'סגנון' in line:
                elements.style = line.split(':')[-1].strip()
            elif 'lighting' in line or 'תאורה' in line:
                elements.lighting = line.split(':')[-1].strip()
            elif 'color' in line or 'צבע' in line:
                elements.color = line.split(':')[-1].strip()
            elif 'mood' in line or 'מצב רוח' in line:
                elements.mood = line.split(':')[-1].strip()
            elif 'details' in line or 'פרטים' in line:
                elements.details = line.split(':')[-1].strip()
            elif 'context' in line or 'הקשר' in line:
                elements.context = line.split(':')[-1].strip()
        
        return elements
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """
        יצירת תמונה באמצעות DALL-E
        
        Args:
            prompt: הפרומפט ליצירת התמונה
            size: גודל התמונה
            quality: איכות התמונה
            
        Returns:
            URL של התמונה שנוצרה
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
            
            return response.data[0].url
            
        except Exception as e:
            print(f"שגיאה ביצירת התמונה: {e}")
            return None
    
    def create_campaign_prompts(self, business_type: str, brand_colors: List[str] = None) -> Dict[str, str]:
        """
        יצירת סדרת פרומפטים לקמפיין שיווקי
        
        Args:
            business_type: סוג העסק
            brand_colors: צבעי המותג
            
        Returns:
            מילון עם פרומפטים שונים לקמפיין
        """
        colors_str = f"brand colors: {', '.join(brand_colors)}" if brand_colors else ""
        
        prompts = {
            "logo": f"minimalist logo design for {business_type}, {colors_str}, clean, professional, vector style",
            "instagram_post": f"Instagram post design for {business_type}, {colors_str}, engaging, modern, social media optimized",
            "hero_image": f"hero banner image for {business_type} website, {colors_str}, professional, engaging, wide format",
            "avatar": f"profile avatar for {business_type}, {colors_str}, circular, clean, recognizable"
        }
        
        # שיפור כל פרומפט עם AI
        enhanced_prompts = {}
        for key, prompt in prompts.items():
            enhanced_prompts[key] = self.enhance_prompt_with_ai(prompt, f"marketing for {business_type}")
        
        return enhanced_prompts
    
    def save_elements_template(self, elements: PromptElements, filename: str):
        """שמירת תבנית אלמנטים לקובץ"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(elements.__dict__, f, ensure_ascii=False, indent=2)
    
    def load_elements_template(self, filename: str) -> PromptElements:
        """טעינת תבנית אלמנטים מקובץ"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return PromptElements(**data)
        except Exception as e:
            print(f"שגיאה בטעינת התבנית: {e}")
            return PromptElements()

# ממשק שורת פקודה
def main():
    parser = argparse.ArgumentParser(description='מחולל פרומפטים מקצועי ליצירת תמונות')
    parser.add_argument('--api-key', help='מפתח API של OpenAI')
    parser.add_argument('--subject', required=True, help='נושא התמונה')
    parser.add_argument('--style', choices=[s.value for s in StyleCategory], help='סגנון התמונה')
    parser.add_argument('--mood', choices=[m.value for m in MoodType], help='מצב רוח')
    parser.add_argument('--composition', choices=[c.value for c in CompositionType], help='קומפוזיציה')
    parser.add_argument('--lighting', choices=[l.value for l in LightingType], help='תאורה')
    parser.add_argument('--colors', help='צבעים רצויים')
    parser.add_argument('--details', help='פרטים נוספים')
    parser.add_argument('--context', help='הקשר השימוש')
    parser.add_argument('--enhance', action='store_true', help='שיפור הפרומפט עם AI')
    parser.add_argument('--generate', action='store_true', help='יצירת התמונה')
    parser.add_argument('--save-template', help='שמירת התבנית לקובץ')
    parser.add_argument('--load-template', help='טעינת תבנית מקובץ')
    
    args = parser.parse_args()
    
    try:
        generator = AIImagePromptGenerator(args.api_key)
        
        # טעינת תבנית אם נדרשה
        if args.load_template:
            elements = generator.load_elements_template(args.load_template)
        else:
            elements = PromptElements(
                subject=args.subject,
                style=args.style or "",
                mood=args.mood or "",
                composition=args.composition or "",
                lighting=args.lighting or "",
                color=args.colors or "",
                details=args.details or "",
                context=args.context or ""
            )
        
        # יצירת פרומפט בסיסי
        basic_prompt = generator.create_basic_prompt(elements)
        print(f"פרומפט בסיסי:\n{basic_prompt}\n")
        
        # שיפור עם AI אם נדרש
        if args.enhance:
            enhanced_prompt = generator.enhance_prompt_with_ai(basic_prompt)
            print(f"פרומפט משופר:\n{enhanced_prompt}\n")
            final_prompt = enhanced_prompt
        else:
            final_prompt = basic_prompt
        
        # שמירת תבנית אם נדרשה
        if args.save_template:
            generator.save_elements_template(elements, args.save_template)
            print(f"התבנית נשמרה ב: {args.save_template}")
        
        # יצירת תמונה אם נדרשה
        if args.generate:
            print("יוצר תמונה...")
            image_url = generator.generate_image(final_prompt)
            if image_url:
                print(f"התמונה נוצרה: {image_url}")
            else:
                print("שגיאה ביצירת התמונה")
    
    except Exception as e:
        print(f"שגיאה: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# דוגמאות שימוש:
"""
# שימוש בסיסי
python ai_prompt_generator.py --subject "חתול פרסי לבן" --style "professional photography" --mood "calm" --generate

# יצירת קמפיין עסקי
generator = AIImagePromptGenerator()
campaign = generator.create_campaign_prompts("בית קפה אקולוגי", ["#2E8B57", "#DEB887"])

# הנדסה לאחור
elements = generator.reverse_engineer_prompt("תמונה של חתול יושב על ספה בסלון מעוצב")

# שמירה וטעינה של תבניות
generator.save_elements_template(elements, "cat_template.json")
loaded_elements = generator.load_elements_template("cat_template.json")
"""