# FinTech Textbook Generator

## Overview

The `fintech_course_textbook.py` script automatically generates textbook chapters from your FinTech course workshop discussions. It uses cursor-agent to create comprehensive, academic-quality chapters based on the multi-agent workshop conversations.

## What It Does

1. **Scans** topic discussion files in `course_discussions/topic_discussions/`
2. **Identifies** which chapters still need to be generated
3. **Calls cursor-agent** with a specialized prompt to write textbook chapters
4. **Saves** chapters in `course_discussions/textbook/` with standardized naming

## Quick Start

### Prerequisites
- Python 3.7+
- cursor-agent installed and in PATH
- Topic discussion files present

### Basic Usage

```bash
# Check current status
python3 course_discussions/fintech_course_textbook.py status

# Generate next chapter
python3 course_discussions/fintech_course_textbook.py next

# Generate all remaining chapters
python3 course_discussions/fintech_course_textbook.py all

# Get help
python3 course_discussions/fintech_course_textbook.py help
```

## How It Works

### Chapter Generation Process

1. **Scans** for topic discussion files (e.g., `topic_01_Introduction_to_Financial_Technology.md`)
2. **Checks** which chapters already exist (e.g., `Chapter_01_Introduction_to_Financial_Technology.md`)
3. **Identifies** the next topic that needs a chapter
4. **Calls cursor-agent** with a comprehensive prompt that includes:
   - Role as university professor writing a masters textbook
   - Context about the workshop format (learner, positive expert, negative expert, moderator)
   - Specific requirements for academic writing style
   - Instructions to synthesize all workshop perspectives

### Generated Chapter Features

- **Academic Style**: Conversational but rigorous, suitable for masters-level students
- **Comprehensive Coverage**: Integrates insights from all workshop participants
- **Proper Citations**: Includes references and supporting evidence
- **Balanced Perspective**: Addresses both opportunities and challenges
- **Practical Examples**: Includes case studies and real-world applications

## File Structure

```
course_discussions/
├── topic_discussions/          # Source workshop discussions
│   ├── topic_01_Introduction_to_Financial_Technology.md
│   ├── topic_02_Digital_Banking_and_Neobanks.md
│   └── ...
└── textbook/                   # Generated textbook chapters
    ├── Chapter_01_Introduction_to_Financial_Technology.md
    ├── Chapter_02_Digital_Banking_and_Neobanks.md
    └── ...
```

## Status Tracking

The script provides clear status information:

- **Total topic discussions**: Number of workshop files found
- **Chapters generated**: Number of completed textbook chapters
- **Chapters remaining**: Number still to be generated
- **Next chapter**: Shows which topic will be processed next

## Example Output

```
FinTech Textbook Generation Status
==================================================
Total topic discussions: 20
Chapters generated: 3
Chapters remaining: 17

Generated Chapters:
------------------------------
  ✅ Chapter_01_Introduction_to_Financial_Technology.md
  ✅ Chapter_02_Digital_Banking_and_Neobanks.md
  ✅ Chapter_03_Mobile_Payments_and_Digital_Wallets.md

Next Chapter to Generate:
  📝 Topic 4: Cryptocurrency and Digital Assets
```

## Key Features

- ✅ **Automated Processing**: No manual intervention needed
- ✅ **Smart Tracking**: Knows which chapters exist and which are needed
- ✅ **Academic Quality**: Generates masters-level textbook content
- ✅ **Comprehensive Coverage**: Synthesizes all workshop perspectives
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Flexible Usage**: Generate one chapter or all remaining chapters

## Logging

All operations are logged to `textbook_generation.log` for monitoring and debugging.

## Integration with Course Workflow

This script is designed to work seamlessly with your FinTech course orchestrator:

1. **Course Orchestrator** runs workshops and creates topic discussions
2. **Textbook Generator** converts discussions into textbook chapters
3. **Result**: Complete textbook ready for your masters FinTech class

The textbook chapters maintain the academic rigor and comprehensive coverage that comes from the multi-agent workshop format, while presenting the content in a structured, textbook-appropriate format.
