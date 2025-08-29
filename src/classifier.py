"""
Image classifier module for Face Catcher.
Handles organizing and classifying images based on analysis results.
"""

import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from .utils import save_json


class ImageClassifier:
    """Handles classification and organization of analyzed images."""
    
    def __init__(self, config: Dict):
        """
        Initialize the image classifier.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.age_groups = config.get('age_groups', {
            'child': (0, 12),
            'teen': (13, 19),
            'adult': (20, 59),
            'senior': (60, 100)
        })
        
        self.logger = logging.getLogger(__name__)
        
        # Create classification directories
        self._create_classification_dirs()
        
        # Track classification statistics
        self.classification_stats = {
            'total_classified': 0,
            'by_age': {},
            'by_ethnicity': {},
            'failed_classifications': 0
        }
    
    def _create_classification_dirs(self):
        """Create directories for classification."""
        # Age-based directories
        age_base = self.output_dir / 'by_age'
        for age_group, (min_age, max_age) in self.age_groups.items():
            age_dir = age_base / f"{age_group}_{min_age}-{max_age if max_age < 100 else '+'}"
            age_dir.mkdir(parents=True, exist_ok=True)
        
        # Ethnicity-based directories
        ethnicity_base = self.output_dir / 'by_ethnicity'
        ethnicities = ['asian', 'black', 'indian', 'latino_hispanic', 'middle_eastern', 'white', 'unknown']
        for ethnicity in ethnicities:
            ethnicity_dir = ethnicity_base / ethnicity
            ethnicity_dir.mkdir(parents=True, exist_ok=True)
    
    def get_age_group(self, age: int) -> str:
        """
        Determine age group for a given age.
        
        Args:
            age: Age in years
            
        Returns:
            Age group name
        """
        for group_name, (min_age, max_age) in self.age_groups.items():
            if min_age <= age <= max_age:
                return group_name
        
        # Default to adult if age doesn't fit any group
        return 'adult'
    
    def get_age_directory_name(self, age: int) -> str:
        """
        Get the directory name for a given age.
        
        Args:
            age: Age in years
            
        Returns:
            Directory name
        """
        age_group = self.get_age_group(age)
        min_age, max_age = self.age_groups[age_group]
        max_suffix = '+' if max_age >= 100 else str(max_age)
        return f"{age_group}_{min_age}-{max_suffix}"
    
    def classify_and_move(self, image_path: Path, analysis: Dict) -> bool:
        """
        Classify and move an image based on analysis results.
        
        Args:
            image_path: Path to the image file
            analysis: Analysis results dictionary
            
        Returns:
            True if classification successful, False otherwise
        """
        try:
            if not image_path.exists():
                self.logger.error(f"Image file not found: {image_path}")
                return False
            
            # Extract analysis data
            age = analysis.get('age', 0)
            ethnicity = analysis.get('dominant_race', 'unknown')
            
            # Classify by age
            success_age = self._classify_by_age(image_path, age)
            
            # Classify by ethnicity  
            success_ethnicity = self._classify_by_ethnicity(image_path, ethnicity)
            
            if success_age and success_ethnicity:
                self.classification_stats['total_classified'] += 1
                
                # Update statistics
                age_group = self.get_age_group(age)
                if age_group not in self.classification_stats['by_age']:
                    self.classification_stats['by_age'][age_group] = 0
                self.classification_stats['by_age'][age_group] += 1
                
                if ethnicity not in self.classification_stats['by_ethnicity']:
                    self.classification_stats['by_ethnicity'][ethnicity] = 0
                self.classification_stats['by_ethnicity'][ethnicity] += 1
                
                return True
            else:
                self.classification_stats['failed_classifications'] += 1
                return False
                
        except Exception as e:
            self.logger.error(f"Error classifying image {image_path}: {e}")
            self.classification_stats['failed_classifications'] += 1
            return False
    
    def _classify_by_age(self, image_path: Path, age: int) -> bool:
        """
        Classify image by age group.
        
        Args:
            image_path: Path to the image file
            age: Age in years
            
        Returns:
            True if successful, False otherwise
        """
        try:
            age_dir_name = self.get_age_directory_name(age)
            target_dir = self.output_dir / 'by_age' / age_dir_name
            
            # Create target filename with age info
            age_filename = f"age_{age:02d}_{image_path.name}"
            target_path = target_dir / age_filename
            
            # Copy file (not move, so we can also classify by ethnicity)
            shutil.copy2(image_path, target_path)
            
            self.logger.debug(f"Classified by age: {image_path.name} -> {age_dir_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error classifying by age: {e}")
            return False
    
    def _classify_by_ethnicity(self, image_path: Path, ethnicity: str) -> bool:
        """
        Classify image by ethnicity.
        
        Args:
            image_path: Path to the image file
            ethnicity: Ethnicity category
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Normalize ethnicity name
            ethnicity = ethnicity.lower().replace(' ', '_')
            target_dir = self.output_dir / 'by_ethnicity' / ethnicity
            
            # Create target directory if it doesn't exist
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Create target filename with ethnicity info
            ethnicity_filename = f"{ethnicity}_{image_path.name}"
            target_path = target_dir / ethnicity_filename
            
            # Copy file
            shutil.copy2(image_path, target_path)
            
            self.logger.debug(f"Classified by ethnicity: {image_path.name} -> {ethnicity}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error classifying by ethnicity: {e}")
            return False
    
    def save_analysis_results(self, analysis_results: List[Dict], statistics: Dict):
        """
        Save analysis results and statistics to JSON files.
        
        Args:
            analysis_results: List of analysis results
            statistics: Execution statistics
        """
        try:
            # Prepare detailed results
            detailed_results = []
            for result in analysis_results:
                detailed_results.append({
                    'filename': result['file'].name,
                    'analysis': result['analysis'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # Save detailed results
            results_file = self.output_dir / 'analysis_results.json'
            save_json(detailed_results, results_file)
            
            # Save statistics
            stats_file = self.output_dir / 'statistics.json'
            stats_data = {
                'execution_timestamp': datetime.now().isoformat(),
                'summary': statistics,
                'classification_stats': self.classification_stats,
                'configuration': {
                    'detector_backend': self.config.get('detector_backend'),
                    'age_groups': self.age_groups,
                    'total_images_requested': statistics.get('total_requested', 0)
                }
            }
            save_json(stats_data, stats_file)
            
            self.logger.info(f"Results saved to {results_file}")
            self.logger.info(f"Statistics saved to {stats_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
    
    def get_classification_summary(self) -> Dict:
        """
        Get classification summary statistics.
        
        Returns:
            Dictionary with classification statistics
        """
        return {
            'total_classified': self.classification_stats['total_classified'],
            'failed_classifications': self.classification_stats['failed_classifications'],
            'age_distribution': self.classification_stats['by_age'].copy(),
            'ethnicity_distribution': self.classification_stats['by_ethnicity'].copy()
        }
    
    def create_summary_report(self) -> str:
        """
        Create a text summary report of classifications.
        
        Returns:
            Summary report as string
        """
        lines = [
            "FACE CATCHER - CLASSIFICATION REPORT",
            "=" * 50,
            f"Total images classified: {self.classification_stats['total_classified']}",
            f"Failed classifications: {self.classification_stats['failed_classifications']}",
            "",
            "AGE DISTRIBUTION:",
            "-" * 20
        ]
        
        for age_group, count in self.classification_stats['by_age'].items():
            percentage = (count / self.classification_stats['total_classified']) * 100 if self.classification_stats['total_classified'] > 0 else 0
            lines.append(f"  {age_group}: {count} ({percentage:.1f}%)")
        
        lines.extend([
            "",
            "ETHNICITY DISTRIBUTION:",
            "-" * 25
        ])
        
        for ethnicity, count in self.classification_stats['by_ethnicity'].items():
            percentage = (count / self.classification_stats['total_classified']) * 100 if self.classification_stats['total_classified'] > 0 else 0
            lines.append(f"  {ethnicity}: {count} ({percentage:.1f}%)")
        
        lines.extend([
            "",
            f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 50
        ])
        
        return "\n".join(lines)
