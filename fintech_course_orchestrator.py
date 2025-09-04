#!/usr/bin/env python3
"""
FinTech Course Orchestrator

This Python script orchestrates the entire FinTech course workflow using cursor-agent,
managing agent interactions, topic progression, and file updates automatically.
"""

import os
import sys
import subprocess
import time
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fintech_course.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TopicStatus(Enum):
    FUTURE_TOPIC = "future_topic"
    IN_DISCUSSION = "in_discussion"
    COMPLETED = "completed"

class AgentType(Enum):
    MODERATOR = "moderator_agent"
    LEARNER = "learner_agent"
    POSITIVE = "positive_agent"
    NEGATIVE = "negative_agent"

@dataclass
class Topic:
    number: int
    title: str
    status: TopicStatus
    description: str

@dataclass
class AgentStep:
    agent: AgentType
    instruction: str
    expected_phrase: str
    status: str = "pending"

class FinTechCourseOrchestrator:
    def __init__(self, course_dir: str = "."):
        self.course_dir = Path(course_dir)
        self.topics_file = self.course_dir / "fintech_topics.md"
        self.course_discussions_dir = self.course_dir / "course_discussions"
        self.topics: List[Topic] = []
        self.current_topic_index = 0
        
        # Agent prompt files
        self.agent_files = {
            AgentType.MODERATOR: "moderator_agent.md",
            AgentType.LEARNER: "learner_agent.md",
            AgentType.POSITIVE: "positive_agent.md",
            AgentType.NEGATIVE: "negative_agent.md"
        }
        
        # Validate setup
        self._validate_setup()
        
    def _validate_setup(self):
        """Validate that all required files exist."""
        logger.info("Validating course setup...")
        
        # Check topics file
        if not self.topics_file.exists():
            raise FileNotFoundError(f"Topics file not found: {self.topics_file}")
        
        # Check agent files
        for agent, filename in self.agent_files.items():
            filepath = self.course_dir / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Agent file not found: {filepath}")
        
        # Check cursor-agent availability
        try:
            result = subprocess.run(['cursor-agent', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError("cursor-agent is not working properly")
            logger.info(f"cursor-agent version: {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise RuntimeError("cursor-agent not found in PATH. Please install it first.")
        
        logger.info("Course setup validation completed successfully")
    
    def parse_topics(self) -> List[Topic]:
        """Parse the fintech_topics.md file to extract topic information."""
        logger.info("Parsing topics file...")
        
        if not self.topics_file.exists():
            raise FileNotFoundError(f"Topics file not found: {self.topics_file}")
        
        topics = []
        content = self.topics_file.read_text()
        
        # Find all topic blocks
        topic_pattern = r'### (\d+)\. (.+?)\n\*\*Status:\*\* `([^`]+)`\n\*\*Description:\*\* (.+?)(?=\n\n|$)'
        matches = re.findall(topic_pattern, content, re.DOTALL)
        
        for match in matches:
            number = int(match[0])
            title = match[1].strip()
            status_str = match[2].strip()
            description = match[3].strip()
            
            try:
                status = TopicStatus(status_str)
            except ValueError:
                logger.warning(f"Unknown status '{status_str}' for topic {number}, defaulting to future_topic")
                status = TopicStatus.FUTURE_TOPIC
            
            topic = Topic(number=number, title=title, status=status, description=description)
            topics.append(topic)
        
        # Sort by topic number
        topics.sort(key=lambda x: x.number)
        
        logger.info(f"Parsed {len(topics)} topics")
        return topics
    
    def setup_course_directory(self):
        """Create the course directory structure."""
        logger.info("Setting up course directory structure...")
        
        # Create main directories
        (self.course_discussions_dir / "topic_discussions").mkdir(parents=True, exist_ok=True)
        (self.course_discussions_dir / "summaries").mkdir(parents=True, exist_ok=True)
        (self.course_discussions_dir / "code_examples").mkdir(parents=True, exist_ok=True)
        
        logger.info("Course directory structure created")
    
    def get_next_topic_for_discussion(self) -> Optional[Topic]:
        """Get the next topic that should be discussed."""
        for topic in self.topics:
            if topic.status == TopicStatus.FUTURE_TOPIC:
                return topic
        return None
    
    def update_topic_status(self, topic_number: int, new_status: TopicStatus):
        """Update the status of a topic in the fintech_topics.md file."""
        logger.info(f"Updating topic {topic_number} status to {new_status.value}")
        
        content = self.topics_file.read_text()
        
        # Create backup
        backup_file = self.topics_file.with_suffix('.bak')
        backup_file.write_text(content)
        
        # Update status
        pattern = rf'(### {topic_number}\..*?\n\*\*Status:\*\* `)[^`]+(`)'
        replacement = rf'\1{new_status.value}\2'
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if updated_content != content:
            self.topics_file.write_text(updated_content)
            # Update local topic object
            for topic in self.topics:
                if topic.number == topic_number:
                    topic.status = new_status
                    break
            logger.info(f"Topic {topic_number} status updated to {new_status.value}")
        else:
            logger.warning(f"Could not update status for topic {topic_number}")
    
    def create_topic_discussion_file(self, topic: Topic) -> Path:
        """Create a new topic discussion file."""
        filename = f"topic_{topic.number:02d}_{topic.title.replace(' ', '_').replace('(', '').replace(')', '')}.md"
        filepath = self.course_discussions_dir / "topic_discussions" / filename
        
        content = f"""# Topic {topic.number}: {topic.title}

**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Status:** {topic.status.value}

## Discussion Flow

### 1. Moderator Agent Introduction
*Status: pending*

### 2. Learner Agent Questions
*Status: pending*

### 3. Positive Agent Response
*Status: pending*

### 4. Negative Agent Response
*Status: pending*

### 5. Learner Agent Follow-up
*Status: pending*

### 6. Moderator Agent Summary
*Status: pending*

## Agent Contributions

### Moderator Agent
*Awaiting contribution...*

### Learner Agent
*Awaiting contribution...*

### Positive Agent
*Awaiting contribution...*

### Negative Agent
*Awaiting contribution...*

### Learner Agent Follow-up
*Awaiting contribution...*

### Learner Agent Follow-up
*Awaiting contribution...*

## Summary
*To be completed by moderator agent*

---
**Topic Status:** {topic.status.value}
**Last Updated:** {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        filepath.write_text(content)
        logger.info(f"Created topic discussion file: {filepath}")
        return filepath
    
    def run_cursor_agent(self, agent_type: AgentType, topic_file: Path, instruction: str) -> bool:
        """Run cursor-agent with the specified parameters."""
        agent_file = self.course_dir / self.agent_files[agent_type]
        
        agent_prompt = f""" "
prompt-file: {str(agent_file)}
context-file: {str(topic_file)}
instruction: {instruction} "
"""
        cmd = [
            'cursor-agent',
            '-p', 
            agent_prompt
        ]
        
        logger.info(f"Running {agent_type.value}: {instruction}")
        logger.info(f"Command: {' '.join(cmd)}")
        
        try:
            # Run cursor-agent
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode == 0:
                logger.info(f"{agent_type.value} completed successfully")
                return True
            else:
                logger.error(f"{agent_type.value} failed with return code {result.returncode}")
                logger.error(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"{agent_type.value} timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"Error running {agent_type.value}: {e}")
            return False
    
    def check_agent_completion(self, topic_file: Path, agent_type: AgentType, expected_phrase: str) -> bool:
        """Check if an agent has completed their step by looking for the expected phrase."""
        if not topic_file.exists():
            return False
        
        content = topic_file.read_text()
        return expected_phrase in content
    
    def run_topic_workflow(self, topic: Topic) -> bool:
        """Run the complete workflow for a single topic."""
        logger.info(f"Starting workflow for Topic {topic.number}: {topic.title}")
        
        # Create topic discussion file
        topic_file = self.create_topic_discussion_file(topic)
        
        # Define the workflow steps
        workflow_steps = [
            {
                'agent': AgentType.MODERATOR,
                'instruction': f'Initiate discussion on Topic {topic.number}: {topic.title}. Provide an introduction and framework for the topic. Update the topic file with your introduction.',
                'expected_phrase': 'Moderator Agent Complete'
            },
            {
                'agent': AgentType.LEARNER,
                'instruction': f'Ask thoughtful questions about Topic {topic.number}: {topic.title}. Request clarification on basic concepts and ask for practical examples. Update the topic file with your questions.',
                'expected_phrase': 'learner_agent complete'
            },
            {
                'agent': AgentType.POSITIVE,
                'instruction': f'Provide optimistic, expert perspective on Topic {topic.number}: {topic.title}. Highlight benefits, opportunities, and success stories. Update the topic file with your response.',
                'expected_phrase': 'positive_agent complete'
            },
            {
                'agent': AgentType.NEGATIVE,
                'instruction': f'Provide critical, skeptical perspective on Topic {topic.number}: {topic.title}. Identify risks, challenges, and potential problems. Update the topic file with your response.',
                'expected_phrase': 'negative_agent complete'
            },
            {
                'agent': AgentType.LEARNER,
                'instruction': f'Ask follow-up questions and seek clarification on Topic {topic.number}: {topic.title}. Explore deeper aspects and request additional examples. Update the topic file with your questions.',
                'expected_phrase': 'Learner Agent Complete'
            },
            {
                'agent': AgentType.MODERATOR,
                'instruction': f'Address the items raised in the learner agents follow-up to the discussion on Topic {topic.number}: {topic.title}. Update the topic file with your response',
                'expected_phrase': 'Moderator Agent Complete'
            },
            {
                'agent': AgentType.MODERATOR,
                'instruction': f'Summarize the discussion on Topic {topic.number}: {topic.title}. Synthesize all agent perspectives and provide key insights. Mark the topic as complete in the topic file.',
                'expected_phrase': 'Moderator Agent Complete'
            }
        ]
        
        # Execute each step
        for i, step in enumerate(workflow_steps, 1):
            logger.info(f"Step {i}/{len(workflow_steps)}: {step['agent'].value}")
            
            # Run the agent
            success = self.run_cursor_agent(step['agent'], topic_file, step['instruction'])
            if not success:
                logger.error(f"Step {i} failed. Stopping workflow.")
                return False
            
            # Wait a moment for file updates
            time.sleep(2)
            
            # Check completion
            if 0 and not self.check_agent_completion(topic_file, step['agent'], step['expected_phrase']):
                logger.warning(f"Step {i} completion phrase not found. Agent may not have completed properly.")
                # Ask user to verify
                response = input(f"Has {step['agent'].value} completed step {i}? (y/n): ").lower().strip()
                if response != 'y':
                    logger.error(f"Step {i} not completed. Stopping workflow.")
                    return False
            
            logger.info(f"Step {i} completed successfully")
        
        logger.info(f"Topic {topic.number} workflow completed successfully")
        return True
    
    def create_topic_summary(self, topic: Topic, topic_file: Path):
        """Create a summary file for the completed topic."""
        summary_file = self.course_discussions_dir / "summaries" / f"topic_{topic.number:02d}_summary.md"
        
        # Extract summary content from topic file
        summary_content = ""
        if topic_file.exists():
            content = topic_file.read_text()
            # Try to extract the summary section
            summary_match = re.search(r'## Summary\n(.*?)(?=\n---|\Z)', content, re.DOTALL)
            if summary_match:
                summary_content = summary_match.group(1).strip()
        
        summary = f"""# Topic {topic.number} Summary: {topic.title}

**Date Completed:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Status:** completed

## Key Insights

{summary_content if summary_content else "Summary content to be extracted from topic discussion file."}


## Next Steps

- Review and reflect on key concepts
- Explore related topics
- Apply knowledge to practical scenarios

---
**Topic Status:** completed
**Next Topic:** {topic.number + 1}
"""
        
        summary_file.write_text(summary)
        logger.info(f"Created topic summary: {summary_file}")
    
    def initialize_course(self):
        """Initialize the course and mark the first topic as in_discussion."""
        logger.info("Initializing FinTech course...")
        
        # Parse topics
        self.topics = self.parse_topics()
        
        # Setup directory structure
        self.setup_course_directory()
        
        # Mark first topic as in_discussion
        if self.topics:
            first_topic = self.topics[0]
            if first_topic.status == TopicStatus.FUTURE_TOPIC:
                self.update_topic_status(first_topic.number, TopicStatus.IN_DISCUSSION)
                logger.info(f"Course initialized. First topic '{first_topic.title}' marked as in_discussion")
            else:
                logger.info(f"Course already initialized. First topic status: {first_topic.status.value}")
        else:
            raise RuntimeError("No topics found in topics file")
    
    def run_complete_course(self):
        """Run the complete course workflow for all topics."""
        logger.info("Starting complete FinTech course workflow...")
        
        # Initialize if not already done
        if not self.topics:
            self.initialize_course()
        
        # Process topics sequentially
        for i, topic in enumerate(self.topics):
            logger.info(f"Processing topic {i+1}/{len(self.topics)}: {topic.title}")
            
            # Check if topic is ready for discussion
            if topic.status == TopicStatus.FUTURE_TOPIC:
                # Mark as in_discussion
                self.update_topic_status(topic.number, TopicStatus.IN_DISCUSSION)
                topic.status = TopicStatus.IN_DISCUSSION
            
            if topic.status == TopicStatus.IN_DISCUSSION:
                # Run topic workflow
                success = self.run_topic_workflow(topic)
                if success:
                    # Create summary
                    topic_file = self.course_discussions_dir / "topic_discussions" / f"topic_{topic.number:02d}_{topic.title.replace(' ', '_').replace('(', '').replace(')', '')}.md"
                    self.create_topic_summary(topic, topic_file)
                    
                    # Mark as completed
                    self.update_topic_status(topic.number, TopicStatus.COMPLETED)
                    topic.status = TopicStatus.COMPLETED
                    
                    logger.info(f"Topic {topic.number} completed successfully")
                    
                    # Mark next topic as in_discussion if it exists
                    if i + 1 < len(self.topics):
                        next_topic = self.topics[i + 1]
                        if next_topic.status == TopicStatus.FUTURE_TOPIC:
                            self.update_topic_status(next_topic.number, TopicStatus.IN_DISCUSSION)
                            next_topic.status = TopicStatus.IN_DISCUSSION
                            logger.info(f"Next topic '{next_topic.title}' marked as in_discussion")
                else:
                    logger.error(f"Topic {topic.number} workflow failed. Stopping course.")
                    return False
            else:
                logger.info(f"Topic {topic.number} status is {topic.status.value}, skipping")
        
        logger.info("Complete course workflow finished successfully!")
        return True
    
    def run_single_topic(self, topic_number: int) -> bool:
        """Run workflow for a single topic."""
        logger.info(f"Running single topic: {topic_number}")
        
        # Parse topics if not already done
        if not self.topics:
            self.topics = self.parse_topics()
        
        # Find the topic
        topic = next((t for t in self.topics if t.number == topic_number), None)
        if not topic:
            logger.error(f"Topic {topic_number} not found")
            return False
        
        # Mark as in_discussion if needed
        if topic.status == TopicStatus.FUTURE_TOPIC:
            self.update_topic_status(topic.number, TopicStatus.IN_DISCUSSION)
            topic.status = TopicStatus.IN_DISCUSSION
        
        # Run workflow
        success = self.run_topic_workflow(topic)
        if success:
            # Create summary
            topic_file = self.course_discussions_dir / "topic_discussions" / f"topic_{topic.number:02d}_{topic.title.replace(' ', '_').replace('(', '').replace(')', '')}.md"
            self.create_topic_summary(topic, topic_file)
            
            # Mark as completed
            self.update_topic_status(topic.number, TopicStatus.COMPLETED)
            topic.status = TopicStatus.COMPLETED
            
            logger.info(f"Topic {topic_number} completed successfully")
            return True
        else:
            logger.error(f"Topic {topic_number} workflow failed")
            return False
    
    def show_status(self):
        """Show the current status of all topics."""
        if not self.topics:
            self.topics = self.parse_topics()
        
        print(f"\nFinTech Course Status")
        print("=" * 50)
        print(f"Total topics: {len(self.topics)}")
        
        if self.topics:
            current_topic = next((t for t in self.topics if t.status == TopicStatus.IN_DISCUSSION), None)
            if current_topic:
                print(f"Current topic: {current_topic.number} - {current_topic.title}")
            else:
                print("Current topic: None")
        
        print("\nTopic Status Overview:")
        print("-" * 50)
        
        for topic in self.topics:
            status_icon = {
                TopicStatus.FUTURE_TOPIC: "⏳",
                TopicStatus.IN_DISCUSSION: "🔄",
                TopicStatus.COMPLETED: "✅"
            }
            print(f"{status_icon[topic.status]} Topic {topic.number:2d}: {topic.title:<40} [{topic.status.value}]")

def main():
    parser = argparse.ArgumentParser(description='FinTech Course Orchestrator')
    parser.add_argument('command', choices=['init', 'run', 'single', 'status', 'help'],
                       help='Command to execute')
    parser.add_argument('--topic', type=int, help='Topic number for single topic command')
    parser.add_argument('--course-dir', default='.', help='Course directory (default: current directory)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        orchestrator = FinTechCourseOrchestrator(args.course_dir)
        
        if args.command == 'init':
            orchestrator.initialize_course()
            print("✅ Course initialized successfully!")
            
        elif args.command == 'run':
            success = orchestrator.run_complete_course()
            if success:
                print("✅ Complete course workflow finished successfully!")
            else:
                print("❌ Course workflow failed")
                sys.exit(1)
                
        elif args.command == 'single':
            if not args.topic:
                print("❌ Topic number required for single topic command")
                print("Usage: python fintech_course_orchestrator.py single --topic <number>")
                sys.exit(1)
            
            success = orchestrator.run_single_topic(args.topic)
            if success:
                print(f"✅ Topic {args.topic} completed successfully!")
            else:
                print(f"❌ Topic {args.topic} failed")
                sys.exit(1)
                
        elif args.command == 'status':
            orchestrator.show_status()
            
        elif args.command == 'help':
            print("""
FinTech Course Orchestrator

Commands:
  init              Initialize the course and mark first topic as in_discussion
  run               Run the complete course workflow for all topics
  single --topic N  Run workflow for a single topic
  status            Show current course status
  help              Show this help message

Examples:
  python fintech_course_orchestrator.py init
  python fintech_course_orchestrator.py run
  python fintech_course_orchestrator.py single --topic 5
  python fintech_course_orchestrator.py status

Requirements:
  - cursor-agent must be installed and available in PATH
  - All agent prompt files must be present
  - fintech_topics.md must be properly formatted
            """)
            
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
