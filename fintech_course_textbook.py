#!/usr/bin/env python3
"""
FinTech Course Textbook Generator

A Python script that generates textbook chapters for each topic in the course_discussions/topic_discussions folder.
Each chapter is written by calling cursor-agent with a specific prompt to create comprehensive textbook content
based on the workshop discussions.
"""

import os
import sys
import subprocess
import time
import re
from pathlib import Path
from typing import List, Dict, Optional
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('textbook_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class FinTechTextbookGenerator:
    def __init__(self, course_dir: str = "."):
        self.course_dir = Path(course_dir)
        self.topic_discussions_dir = self.course_dir / "course_discussions" / "topic_discussions"
        self.textbook_dir = self.course_dir / "course_discussions" / "textbook"
        self.topic_files: List[Path] = []
        
        # Validate setup
        self._validate_setup()
        
    def _validate_setup(self):
        """Validate that all required directories and files exist."""
        logger.info("Validating textbook generation setup...")
        
        # Check topic discussions directory
        if not self.topic_discussions_dir.exists():
            raise FileNotFoundError(f"Topic discussions directory not found: {self.topic_discussions_dir}")
        
        # Create textbook directory if it doesn't exist
        self.textbook_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Textbook directory: {self.textbook_dir}")
        
        # Check cursor-agent availability
        try:
            result = subprocess.run(['cursor-agent', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError("cursor-agent is not working properly")
            logger.info(f"cursor-agent version: {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise RuntimeError("cursor-agent not found in PATH. Please install it first.")
        
        logger.info("Textbook generation setup validation completed successfully")
    
    def get_topic_files(self) -> List[Path]:
        """Get all topic discussion files."""
        logger.info("Scanning for topic discussion files...")
        
        if not self.topic_discussions_dir.exists():
            logger.warning(f"Topic discussions directory not found: {self.topic_discussions_dir}")
            return []
        
        # Find all markdown files in topic_discussions directory
        topic_files = list(self.topic_discussions_dir.glob("*.md"))
        
        # Sort by topic number if possible
        def extract_topic_number(filepath: Path) -> int:
            match = re.search(r'topic_(\d+)_', filepath.name)
            return int(match.group(1)) if match else 999
        
        topic_files.sort(key=extract_topic_number)
        
        logger.info(f"Found {len(topic_files)} topic discussion files")
        return topic_files
    
    def get_existing_chapters(self) -> List[Path]:
        """Get list of existing textbook chapters."""
        if not self.textbook_dir.exists():
            return []
        
        chapter_files = list(self.textbook_dir.glob("Chapter_*.md"))
        
        # Sort by chapter number
        def extract_chapter_number(filepath: Path) -> int:
            match = re.search(r'Chapter_(\d+)_', filepath.name)
            return int(match.group(1)) if match else 999
        
        chapter_files.sort(key=extract_chapter_number)
        return chapter_files
    
    def get_next_topic_to_process(self) -> Optional[Path]:
        """Get the next topic file that needs a chapter generated."""
        topic_files = self.get_topic_files()
        existing_chapters = self.get_existing_chapters()
        
        # Extract topic numbers from existing chapters
        existing_topic_numbers = set()
        for chapter in existing_chapters:
            match = re.search(r'Chapter_(\d+)_', chapter.name)
            if match:
                existing_topic_numbers.add(int(match.group(1)))
        
        # Find the first topic that doesn't have a chapter yet
        for topic_file in topic_files:
            match = re.search(r'topic_(\d+)_', topic_file.name)
            if match:
                topic_number = int(match.group(1))
                if topic_number not in existing_topic_numbers:
                    return topic_file
        
        return None
    
    def extract_topic_info(self, topic_file: Path) -> Dict[str, str]:
        """Extract topic information from the discussion file."""
        content = topic_file.read_text()
        
        # Extract topic number and title
        topic_match = re.search(r'# Topic (\d+): (.+)', content)
        topic_number = topic_match.group(1) if topic_match else "Unknown"
        topic_title = topic_match.group(2) if topic_match else "Unknown Topic"
        
        # Extract date
        date_match = re.search(r'\*\*Date:\*\* (.+)', content)
        date = date_match.group(1) if date_match else time.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'number': topic_number,
            'title': topic_title,
            'date': date,
            'content': content
        }
    
    def create_chapter_filename(self, topic_info: Dict[str, str]) -> str:
        """Create a standardized filename for the chapter."""
        # Clean the title for filename
        clean_title = re.sub(r'[^\w\s-]', '', topic_info['title'])
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        clean_title = clean_title.strip('_')
        
        return self.textbook_dir / f"Chapter_{topic_info['number']:0>2}_{clean_title}.md"
    
    def generate_chapter_prompt(self, topic_info: Dict[str, str], topic_file: Path) -> str:
        """Generate the prompt for cursor-agent to create a textbook chapter."""
        
        prompt = f"""You are a university professor writing a textbook for your masters FinTech class. You ran a series of workshops across a range of FinTech topics. In each workshop there was a learner, an expert colleague bringing a positive perspective, and a colleague bringing a negative perspective, finally your summarization as the moderator.

You need to write a chapter in your textbook for every topic. You will need to keep in context the introduction and notes from all workshop topics when writing the chapter for a specific topic. These documents are stored as markdown files in ./course_discussions/topic_discussions/*.md

The structure of the chapter is up to you. You have chosen a conversational writing style, not one that appears similar to a bullet-pointed presentation. Make sure to keep references for all supporting information, quotes, and numerical quotes.

Write the next chapter taking direction from the topic discussion file: {topic_file.name}

Topic Information:
- Chapter Number: {topic_info['number']}
- Topic Title: {topic_info['title']}
- Workshop Date: {topic_info['date']}

Requirements:
1. Write in a conversational, academic style suitable for a masters-level textbook
2. Integrate insights from all workshop participants (learner, positive expert, negative expert, moderator)
3. Include proper references and citations for all claims
4. Maintain academic rigor while being accessible
5. Structure the chapter with clear sections and flow
6. Include practical examples and case studies where appropriate
7. Address both opportunities and challenges in the topic area
8. Save the chapter as: {self.create_chapter_filename(topic_info)}

Please write a comprehensive chapter that synthesizes the workshop discussion into a coherent textbook chapter."""
        
        return prompt
    
    def run_cursor_agent_for_chapter(self, topic_info: Dict[str, str], topic_file: Path) -> bool:
        """Run cursor-agent to generate a textbook chapter."""
        logger.info(f"Generating chapter for Topic {topic_info['number']}: {topic_info['title']}")
        
        # Create the prompt
        prompt = self.generate_chapter_prompt(topic_info, topic_file)
        
        # Prepare the command
        cmd = [
            'cursor-agent',
            '-p',
            prompt
        ]
        
        logger.info(f"Running cursor-agent for chapter generation...")
        logger.debug(f"Command: {' '.join(cmd)}")
        
        try:
            # Run cursor-agent
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minute timeout
            
            if result.returncode == 0:
                logger.info(f"Chapter generation completed successfully for Topic {topic_info['number']}")
                return True
            else:
                logger.error(f"Chapter generation failed with return code {result.returncode}")
                logger.error(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Chapter generation timed out after 10 minutes")
            return False
        except Exception as e:
            logger.error(f"Error running cursor-agent: {e}")
            return False
    
    def generate_next_chapter(self) -> bool:
        """Generate the next chapter that needs to be written."""
        next_topic = self.get_next_topic_to_process()
        
        if not next_topic:
            logger.info("No more topics to process. All chapters have been generated.")
            return False
        
        # Extract topic information
        topic_info = self.extract_topic_info(next_topic)
        
        logger.info(f"Processing Topic {topic_info['number']}: {topic_info['title']}")
        
        # Generate the chapter
        success = self.run_cursor_agent_for_chapter(topic_info, next_topic)
        
        if success:
            logger.info(f"Successfully generated chapter for Topic {topic_info['number']}")
            return True
        else:
            logger.error(f"Failed to generate chapter for Topic {topic_info['number']}")
            return False
    
    def generate_all_chapters(self) -> bool:
        """Generate all remaining chapters."""
        logger.info("Starting generation of all remaining chapters...")
        
        total_processed = 0
        total_failed = 0
        
        while True:
            next_topic = self.get_next_topic_to_process()
            
            if not next_topic:
                break
            
            success = self.generate_next_chapter()
            
            if success:
                total_processed += 1
                logger.info(f"Chapter {total_processed} completed successfully")
            else:
                total_failed += 1
                logger.error(f"Chapter generation failed")
                # Ask user if they want to continue
                response = input("Chapter generation failed. Continue with next chapter? (y/n): ").lower().strip()
                if response != 'y':
                    break
            
            # Wait a moment between chapters
            time.sleep(2)
        
        logger.info(f"Chapter generation completed. Processed: {total_processed}, Failed: {total_failed}")
        return total_failed == 0
    
    def show_status(self):
        """Show the current status of textbook generation."""
        topic_files = self.get_topic_files()
        existing_chapters = self.get_existing_chapters()
        
        print(f"\nFinTech Textbook Generation Status")
        print("=" * 50)
        print(f"Total topic discussions: {len(topic_files)}")
        print(f"Chapters generated: {len(existing_chapters)}")
        print(f"Chapters remaining: {len(topic_files) - len(existing_chapters)}")
        
        if existing_chapters:
            print(f"\nGenerated Chapters:")
            print("-" * 30)
            for chapter in existing_chapters:
                print(f"  ✅ {chapter.name}")
        
        # Show next topic to be processed
        next_topic = self.get_next_topic_to_process()
        if next_topic:
            topic_info = self.extract_topic_info(next_topic)
            print(f"\nNext Chapter to Generate:")
            print(f"  📝 Topic {topic_info['number']}: {topic_info['title']}")
        else:
            print(f"\n🎉 All chapters have been generated!")

def main():
    parser = argparse.ArgumentParser(description='FinTech Textbook Generator')
    parser.add_argument('command', choices=['next', 'all', 'status', 'help'],
                       help='Command to execute')
    parser.add_argument('--course-dir', default='.', help='Course directory (default: current directory)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        generator = FinTechTextbookGenerator(args.course_dir)
        
        if args.command == 'next':
            success = generator.generate_next_chapter()
            if success:
                print("✅ Next chapter generated successfully!")
            else:
                print("❌ Chapter generation failed")
                sys.exit(1)
                
        elif args.command == 'all':
            success = generator.generate_all_chapters()
            if success:
                print("✅ All chapters generated successfully!")
            else:
                print("❌ Some chapters failed to generate")
                sys.exit(1)
                
        elif args.command == 'status':
            generator.show_status()
            
        elif args.command == 'help':
            print("""
FinTech Textbook Generator

Commands:
  next              Generate the next chapter that needs to be written
  all               Generate all remaining chapters
  status            Show current textbook generation status
  help              Show this help message

Examples:
  python fintech_course_textbook.py next
  python fintech_course_textbook.py all
  python fintech_course_textbook.py status

Requirements:
  - cursor-agent must be installed and available in PATH
  - Topic discussion files must be present in course_discussions/topic_discussions/
  - Textbook chapters will be saved in course_discussions/textbook/

The script will:
1. Scan for topic discussion files
2. Check which chapters have already been generated
3. Generate the next chapter using cursor-agent
4. Save chapters in a standardized format
            """)
            
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
