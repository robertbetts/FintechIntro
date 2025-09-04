# FinTech Course Orchestrator - Python Script Guide

## Overview

The `fintech_course_orchestrator.py` script is a robust Python-based solution that automates the entire FinTech course workflow using cursor-agent. It provides comprehensive error handling, status tracking, and automatic file management while ensuring all agents complete their steps and properly update topic files.

## Key Features

### 🚀 **Automated Workflow Management**
- **Sequential Processing**: Automatically progresses through all 20 topics
- **Agent Orchestration**: Manages the exact 6-step workflow for each topic
- **Status Tracking**: Real-time monitoring of topic and agent progress
- **File Management**: Automatic creation of discussion files and summaries

### 🔧 **Robust Error Handling**
- **Prerequisites Validation**: Checks all required files and cursor-agent availability
- **Completion Verification**: Validates that agents complete their steps
- **Backup Protection**: Creates backup files before any modifications
- **Graceful Recovery**: Handles failures and provides clear error messages

### 📊 **Comprehensive Logging**
- **File Logging**: All operations logged to `fintech_course.log`
- **Console Output**: Real-time status updates and progress indicators
- **Verbose Mode**: Detailed debugging information when needed

## Prerequisites

### 1. **Python Requirements**
- Python 3.7+ (uses dataclasses, pathlib, and modern typing)
- No external dependencies required (uses only standard library)

### 2. **cursor-agent Installation**
```bash
# Ensure cursor-agent is in your PATH
which cursor-agent

# Test cursor-agent functionality
cursor-agent --version
```

### 3. **Required Files**
- `fintech_topics.md` - Course topics with status tracking
- `moderator_agent.md` - Moderator agent prompt file
- `learner_agent.md` - Learner agent prompt file
- `positive_agent.md` - Positive agent prompt file
- `negative_agent.md` - Negative agent prompt file

## Quick Start

### 1. **Initialize the Course**
```bash
python fintech_course_orchestrator.py init
```
This will:
- Validate all prerequisites
- Create course directory structure
- Mark the first topic as `in_discussion`
- Set up logging and backup systems

### 2. **Run Complete Course**
```bash
python fintech_course_orchestrator.py run
```
This will:
- Process all topics sequentially
- Execute the complete 6-step workflow for each topic
- Update topic statuses automatically
- Create summaries and mark topics as completed

### 3. **Run Single Topic**
```bash
python fintech_course_orchestrator.py single --topic 5
```
This will:
- Process only topic 5
- Complete the full workflow for that topic
- Mark it as completed

### 4. **Check Status**
```bash
python fintech_course_orchestrator.py status
```
This will:
- Display current course progress
- Show status of all topics with visual indicators
- Indicate which topic is currently active

## Detailed Workflow

### **6-Step Agent Workflow for Each Topic:**

1. **Moderator Agent Introduction** 🔵
   - Initiates topic discussion
   - Provides framework and context
   - Updates topic file with introduction
   - Expected completion: `moderator_agent complete`

2. **Learner Agent Questions** 🟡
   - Asks thoughtful, clarifying questions
   - Explores basic concepts
   - Requests practical examples
   - Expected completion: `learner_agent complete`

3. **Positive Agent Response** 🟢
   - Provides optimistic, expert perspective
   - Highlights benefits and opportunities
   - Shares success stories
   - Expected completion: `positive_agent complete`

4. **Negative Agent Response** 🔴
   - Provides critical, skeptical perspective
   - Identifies risks and challenges
   - Offers constructive criticism
   - Expected completion: `negative_agent complete`

5. **Learner Agent Follow-up** 🟡
   - Asks follow-up questions
   - Seeks clarification on responses
   - Explores deeper aspects
   - Expected completion: `learner_agent complete`

6. **Moderator Agent Summary** 🔵
   - Synthesizes all agent perspectives
   - Provides key insights and takeaways
   - Marks topic as completed
   - Expected completion: `moderator_agent complete`

## Directory Structure Created

```
course_discussions/
├── topic_discussions/     # Individual topic discussion files
│   ├── topic_01_Introduction_to_Financial_Technology.md
│   ├── topic_02_Digital_Banking_and_Neobanks.md
│   └── ...
├── summaries/            # Topic summary files
│   ├── topic_01_summary.md
│   ├── topic_02_summary.md
│   └── ...
└── code_examples/        # Code examples (if any)
```

## File Naming Convention

- **Topic Discussions**: `topic_01_Introduction_to_Financial_Technology.md`
- **Summaries**: `topic_01_summary.md`
- **Backup Files**: Original files backed up with `.bak` extension
- **Log File**: `fintech_course.log` for comprehensive operation logging

## Command Line Options

### **Basic Commands**
```bash
python fintech_course_orchestrator.py <command> [options]
```

### **Available Commands**
- `init` - Initialize the course
- `run` - Run complete course workflow
- `single --topic N` - Run single topic workflow
- `status` - Show current course status
- `help` - Show help message

### **Additional Options**
- `--course-dir <path>` - Specify course directory (default: current directory)
- `--verbose` or `-v` - Enable verbose logging for debugging

### **Examples**
```bash
# Initialize course in specific directory
python fintech_course_orchestrator.py init --course-dir /path/to/course

# Run complete course with verbose logging
python fintech_course_orchestrator.py run --verbose

# Run specific topic
python fintech_course_orchestrator.py single --topic 3

# Check status
python fintech_course_orchestrator.py status
```

## Status Management

### **Topic Status Flow**
```
future_topic → in_discussion → completed
```

### **Status Indicators**
- ⏳ `future_topic` - Topic not yet started
- 🔄 `in_discussion` - Topic currently being processed
- ✅ `completed` - Topic discussion finished and summarized

### **Automatic Status Updates**
- Script automatically updates topic statuses in `fintech_topics.md`
- Next topic is automatically marked as `in_discussion` when current topic completes
- All status changes are logged and backed up

## Error Handling and Recovery

### **Prerequisites Validation**
- Checks all required files exist
- Validates cursor-agent availability and functionality
- Ensures proper file permissions

### **Completion Verification**
- Verifies each agent completes their step
- Looks for expected completion phrases
- Prompts user verification if completion is unclear

### **Backup and Recovery**
- Creates `.bak` files before any modifications
- Comprehensive logging for troubleshooting
- Graceful error handling with clear messages

### **Common Error Scenarios**
1. **Missing Files**: Script exits with clear error message
2. **cursor-agent Issues**: Validates functionality before starting
3. **Agent Failures**: Logs errors and stops workflow
4. **File Permission Issues**: Checks and reports access problems

## Logging and Monitoring

### **Log File (`fintech_course.log`)**
- Timestamped entries for all operations
- Error details and stack traces
- Agent execution results
- File modification tracking

### **Console Output**
- Real-time progress updates
- Status indicators and progress bars
- Error messages and warnings
- Success confirmations

### **Verbose Mode**
- Detailed debugging information
- Step-by-step execution details
- File content analysis
- Agent command details

## Best Practices

### **1. Always Start with Init**
```bash
python fintech_course_orchestrator.py init
```

### **2. Monitor Progress**
```bash
python fintech_course_orchestrator.py status
```

### **3. Use Verbose Mode for Debugging**
```bash
python fintech_course_orchestrator.py run --verbose
```

### **4. Check Logs Regularly**
```bash
tail -f fintech_course.log
```

### **5. Backup Important Files**
- Script creates automatic backups, but manual backups are recommended
- Keep copies of original agent prompt files

## Troubleshooting

### **Common Issues and Solutions**

#### **1. "cursor-agent not found in PATH"**
```bash
# Check if cursor-agent is installed
which cursor-agent

# Add to PATH if needed
export PATH=$PATH:/path/to/cursor-agent
```

#### **2. "Required file not found"**
```bash
# Check file existence
ls -la *.md

# Verify file permissions
ls -la fintech_topics.md
```

#### **3. "Agent completion phrase not found"**
- Check if agent actually completed the step
- Verify the topic file was updated
- Look for typos in completion phrase

#### **4. "Topic status update failed"**
- Check file permissions
- Verify file format matches expected pattern
- Check backup files for recovery

### **Recovery Procedures**

#### **Restore from Backup**
```bash
# Restore original topics file
cp fintech_topics.md.bak fintech_topics.md

# Restore other files if needed
cp *.md.bak *.md
```

#### **Manual Status Reset**
```bash
# Edit fintech_topics.md manually
# Change status back to desired state
# Re-run the script
```

## Advanced Usage

### **Custom Agent Instructions**
The script uses predefined instructions for each agent step. You can modify these in the `run_topic_workflow` method:

```python
workflow_steps = [
    {
        'agent': AgentType.MODERATOR,
        'instruction': 'Your custom instruction here...',
        'expected_phrase': 'moderator_agent complete'
    },
    # ... other steps
]
```

### **Custom Completion Phrases**
Modify the expected completion phrases to match your agent behavior:

```python
'expected_phrase': 'your_custom_completion_phrase'
```

### **Custom Directory Structure**
Modify the directory creation in `setup_course_directory`:

```python
# Add custom directories
(self.course_discussions_dir / "custom_folder").mkdir(parents=True, exist_ok=True)
```

## Performance Considerations

### **Timeout Settings**
- Agent execution timeout: 5 minutes (configurable)
- File update wait time: 2 seconds (configurable)

### **Memory Usage**
- Minimal memory footprint
- Efficient file parsing and processing
- No large data structures kept in memory

### **File I/O**
- Efficient file reading/writing
- Backup creation only when needed
- Minimal disk operations

## Support and Maintenance

### **Log Analysis**
```bash
# View recent logs
tail -n 50 fintech_course.log

# Search for errors
grep "ERROR" fintech_course.log

# Search for specific topic
grep "Topic 5" fintech_course.log
```

### **Debug Mode**
```bash
# Enable verbose logging
python fintech_course_orchestrator.py run --verbose

# Check specific command
python fintech_course_orchestrator.py status --verbose
```

### **File Validation**
```bash
# Check file integrity
python -m py_compile fintech_course_orchestrator.py

# Validate JSON/XML if used
python -c "import json; json.load(open('file.json'))"
```

---

## Summary

The Python-based FinTech Course Orchestrator provides a robust, automated solution for managing your course workflow. It ensures:

- ✅ **Complete Automation** of the 6-step agent workflow
- ✅ **Reliable Status Tracking** with automatic updates
- ✅ **Comprehensive Error Handling** and recovery
- ✅ **Detailed Logging** for monitoring and debugging
- ✅ **Flexible Usage** with multiple command options
- ✅ **Professional Quality** with proper backup and validation

This script transforms your manual course management into a streamlined, automated process while maintaining full control and visibility over the workflow.
