import basicparser
import time
import sys
import os

# ANSI color codes 
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

class QuantumCalculator:
    def __init__(self):
        self.first_run = True
        
    def type_animation(self, text, speed=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def print_banner(self):
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║                       QuantumParser                      ║
║                                                          ║ 
║                                                          ║
║       Type 'help' for commands | 'exit' to quit          ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)

    def print_help(self):
        help_text = f"""
{Colors.GREEN}Available Commands:{Colors.RESET}
{Colors.YELLOW}╔════════════════════╦══════════════════════════════════╗
║ Command            ║ Description                      ║
╠════════════════════╬══════════════════════════════════╣
║ Basic Operations   ║ +, -, *, /, =, ^                      ║
║ Parentheses        ║ ( )                              ║
║ clear              ║ Clear screen                     ║
║ exit               ║ Exit program                     ║
║ help               ║ Show this help message           ║
╚════════════════════╩══════════════════════════════════╝{Colors.RESET}

{Colors.CYAN}Examples:{Colors.RESET}
- Basic: 1 + 1
- Complex: 2 * (3 + 4)
- Decimal: 5.5 / 2.2
- Equalities: 2 = 2 or 1+1 = 0+2
- Exponents: 2^2 = 4
"""
        print(help_text)

    def loading_bar(self):
        print(f"\n{Colors.CYAN}Initializing Quantum Calculator...{Colors.RESET}")
        total = 30
        for i in range(total + 1):
            # Creates progress bar using block characters
            progress = '█' * i + '░' * (total - i)
            percentage = (i * 100) // total
            sys.stdout.write(f'\r{Colors.CYAN}|{progress}| {percentage}%{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.03)
        print('\n')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def startup_sequence(self):
        self.print_banner()
        self.loading_bar()
        self.type_animation(f"{Colors.YELLOW}Welcome to QuantumParser{Colors.RESET}", 0.05)
        self.type_animation(f"{Colors.GREEN}Ready for parsing.{Colors.RESET}", 0.05)
        print()

    def run(self):
        # Show startup animations only on first run
        if self.first_run:
            self.startup_sequence()
            self.first_run = False

        while True:
            try:
                text = input(f'{Colors.CYAN}Quantum ~>{Colors.RESET} ')
                print(text)

                # Handle commands
                if text.lower() == 'exit':
                    self.type_animation(f"{Colors.YELLOW}Shutting down QuantumParser...{Colors.RESET}")
                    sys.exit()
                    
                elif text.lower() == 'help':
                    self.print_help()
                    continue
                    
                elif text.lower() == 'clear':
                    self.clear_screen()
                    self.print_banner()
                    continue

                # Process calculation
                result, error = basicparser.run('<stdin>', text)

                if error: 
                    print(f"{Colors.RED}{error.as_string()}{Colors.RESET}")
                else: 
                    print(f"{Colors.GREEN}{result}{Colors.RESET}")

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Use 'exit' to quit{Colors.RESET}")
                continue
            
            except Exception as e:
                print(f"{Colors.RED}An unexpected error occurred: {str(e)}{Colors.RESET}")

def main():
    calculator = QuantumCalculator()
    calculator.run()

if __name__ == "__main__":
    main()
