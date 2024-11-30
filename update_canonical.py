import os
from pathlib import Path
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class CanonicalUpdater:
    def __init__(self):
        self.base_url = 'https://freeze-nova.github.io'
        self.updated_count = 0
        self.error_count = 0

    def get_canonical_url(self, file_path: str) -> str:
        """Generate the canonical URL for a given file path."""
        relative_path = os.path.relpath(file_path, '.')
        # Convert Windows path separators to forward slashes
        relative_path = relative_path.replace('\\', '/')
        
        # Handle index.html files
        if os.path.basename(relative_path) == 'index.html':
            relative_path = os.path.dirname(relative_path)
            if relative_path == '.':
                return self.base_url
            return f"{self.base_url}/{relative_path}/"
        
        return f"{self.base_url}/{relative_path}"

    def update_canonical(self, file_path: str) -> None:
        """Update canonical tag in HTML file."""
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            head = soup.find('head')
            
            if not head:
                print(f"{Fore.RED}No <head> tag found in {file_path}{Style.RESET_ALL}")
                self.error_count += 1
                return

            # Get the canonical URL for this file
            canonical_url = self.get_canonical_url(file_path)
            
            # Find existing canonical tag
            canonical_tag = soup.find('link', rel='canonical')
            
            if canonical_tag:
                old_url = canonical_tag.get('href', '')
                canonical_tag['href'] = canonical_url
                print(f"{Fore.YELLOW}Updated canonical in {file_path}")
                print(f"  Old: {old_url}")
                print(f"  New: {canonical_url}{Style.RESET_ALL}")
            else:
                # Create new canonical tag
                new_tag = soup.new_tag('link', rel='canonical', href=canonical_url)
                head.append('\n    ')  # Add indentation
                head.append(new_tag)
                head.append('\n')  # Add newline
                print(f"{Fore.GREEN}Added canonical to {file_path}")
                print(f"  URL: {canonical_url}{Style.RESET_ALL}")

            # Write the updated content back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            self.updated_count += 1

        except Exception as e:
            print(f"{Fore.RED}Error processing {file_path}: {str(e)}{Style.RESET_ALL}")
            self.error_count += 1

    def process_directory(self, directory: str) -> None:
        """Process all HTML files in directory and subdirectories."""
        try:
            for root, dirs, files in os.walk(directory):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__'}]
                
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        self.update_canonical(file_path)
        
        except Exception as e:
            print(f"{Fore.RED}Error accessing directory {directory}: {str(e)}{Style.RESET_ALL}")

    def run(self) -> None:
        """Run the canonical updater."""
        print(f"{Style.BRIGHT}Starting canonical URL updates...{Style.RESET_ALL}")
        print(f"Base URL: {self.base_url}\n")
        
        self.process_directory('.')
        
        print(f"\n{Style.BRIGHT}Update Complete:{Style.RESET_ALL}")
        print(f"✓ Successfully updated: {self.updated_count} files")
        if self.error_count > 0:
            print(f"✗ Errors encountered: {self.error_count} files")

if __name__ == '__main__':
    try:
        # First check if BeautifulSoup is installed
        try:
            import bs4
        except ImportError:
            print(f"{Fore.YELLOW}Installing required package: beautifulsoup4{Style.RESET_ALL}")
            import subprocess
            subprocess.check_call(['pip', 'install', 'beautifulsoup4'])
            
        updater = CanonicalUpdater()
        updater.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Update interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        colorama.deinit()