# AI Prompt Generator

A tool for creating structured prompts for AI image generation using the 8 Elements Framework.

## Project Overview

This project provides tools for creating high-quality prompts for AI image generation services like DALL-E, Midjourney, or Stable Diffusion. It uses the "8 Elements Framework" to structure prompts in a way that produces better results.

The 8 Elements are:

1.  **Subject** - What/who is in the image
2.  **Composition** - How it's arranged
3.  **Style** - What look/style
4.  **Lighting** - What kind of light
5.  **Color** - What colors
6.  **Mood** - What feeling
7.  **Details** - What to include/exclude
8.  **Context** - What it's for

## Available Versions

This project includes multiple implementations:

### 1. Full Version with OpenAI Integration

- **Files**: `ai_prompt_generator_pkg/ai_prompt_generator.py` and `ai_prompt_generator_pkg/gui_prompt_generator.py`
- **Features**:
  - Create basic prompts using the 8 Elements Framework
  - Enhance prompts using AI (OpenAI's GPT-4)
  - Generate images using DALL-E
  - Save and load templates
  - Create campaign prompts for marketing
  - Reverse engineer prompts from image descriptions
  - GUI interface

### 2. Simple Version (No API Required)

- **Files**: `ai_prompt_generator_pkg/simple_prompt_generator.py` (GUI) and `ai_prompt_generator_pkg/cli_prompt_generator.py` (Command Line)
- **Features**:
  - Create basic prompts using the 8 Elements Framework
  - Save and load templates
  - Pre-defined examples
  - No API key or external dependencies required

### 3. HTML Version

- **File**: `prompt_generator.html`
- **Features**:
  - Pure HTML/JavaScript implementation
  - Works in any browser
  - No installation or dependencies required
  - Create basic prompts using the 8 Elements Framework

## Requirements

For the full version:

```
openai>=1.30.0
pillow>=9.0.0
requests>=2.28.0
tkinter  # Usually included with Python
```

For the simple version:

- Python 3.6+ with tkinter (for GUI version)
- No external dependencies for CLI or HTML versions

## Usage Examples

### Command Line Interface

```bash
# Basic example
python ai_prompt_generator_pkg/ai_prompt_generator.py --subject "Persian cat" --style "professional photography" --enhance

# Generate image immediately
python ai_prompt_generator_pkg/ai_prompt_generator.py --subject "Technology company logo" --style "minimalist" --colors "blue and white" --generate

# Save template
python ai_prompt_generator_pkg/ai_prompt_generator.py --subject "Mountain landscape" --style "oil painting" --mood "calm" --save-template "mountain_template.json"

# Load template
python ai_prompt_generator_pkg/ai_prompt_generator.py --load-template "mountain_template.json" --enhance --generate
```

### Simple CLI Version

```bash
# Basic example
python ai_prompt_generator_pkg/cli_prompt_generator.py --subject "Persian cat" --style "professional photography"

# Using a pre-defined example
python ai_prompt_generator_pkg/cli_prompt_generator.py --example "cat"
```

### GUI Versions

Run either of these commands:

```bash
python ai_prompt_generator_pkg/gui_prompt_generator.py  # Full version with OpenAI integration
python ai_prompt_generator_pkg/simple_prompt_generator.py  # Simple version without API requirements
```

### HTML Version

Simply open the `prompt_generator.html` file in any web browser.

## Tips for Better Prompts

1.  **Be Specific**: The more specific the details, the better the result

    - Bad: "a dog"
    - Good: "a golden retriever puppy, 3 months old, sitting on green grass"

2.  **Use Quality Keywords**:
    "high quality", "detailed", "professional", "8k resolution"

3.  **Use Negative Prompts** (in enhanced prompts):
    "no blurry, no low quality, no distorted"

4.  **Context Matters**:
    "for Instagram post", "for corporate website", "for children's book"

## Getting Started

To set up a virtual environment:

1.  Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2.  Activate the virtual environment:

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source venv/bin/activate
      ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## License

This project is available for personal and commercial use.
