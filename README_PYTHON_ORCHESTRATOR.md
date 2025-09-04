# FinTech Course Orchestrator - Python Script

## Quick Start

### Prerequisites
- Python 3.7+
- cursor-agent installed and in PATH
- All agent prompt files present

### Basic Usage

```bash
# Initialize the course
python3 fintech_course_orchestrator.py init

# Check current status
python3 fintech_course_orchestrator.py status

# Run complete course (interactive)
python3 fintech_course_orchestrator.py run

# Run single topic
python3 fintech_course_orchestrator.py single --topic 5

# Get help
python3 fintech_course_orchestrator.py help
```

## What It Does

This Python script automates your entire FinTech course workflow:

1. **Initializes** the course structure
2. **Orchestrates** all 6 agent steps for each topic
3. **Tracks** topic status automatically
4. **Creates** discussion files and summaries
5. **Manages** the complete workflow from start to finish

## Key Features

- ✅ **Fully Automated** - No manual intervention needed
- ✅ **Status Tracking** - Real-time progress monitoring
- ✅ **Error Handling** - Robust error handling and recovery
- ✅ **Logging** - Comprehensive logging to `fintech_course.log`
- ✅ **Backup Protection** - Automatic backup creation
- ✅ **Validation** - Checks all prerequisites before starting

## Workflow

For each topic, the script runs this 6-step sequence:

1. **Moderator Agent** - Initiates discussion
2. **Learner Agent** - Asks questions
3. **Positive Agent** - Provides optimistic perspective
4. **Negative Agent** - Provides critical perspective
5. **Learner Agent** - Asks follow-up questions
6. **Moderator Agent** - Summarizes and marks complete

## Files Created

- `course_discussions/topic_discussions/` - Individual topic files
- `course_discussions/summaries/` - Topic summaries
- `course_discussions/code_examples/` - Code examples
- `fintech_course.log` - Operation log
- `fintech_topics.md.bak` - Backup of topics file

## Status Indicators

- ⏳ `future_topic` - Not started
- 🔄 `in_discussion` - Currently processing
- ✅ `completed` - Finished and summarized

## For More Details

See `PYTHON_ORCHESTRATOR_GUIDE.md` for comprehensive documentation.
