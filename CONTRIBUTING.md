# Contributing to Slow Day Network Analyzer

Thank you for your interest in contributing to Slow Day! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Feature Requests](#feature-requests)
- [Bug Reports](#bug-reports)

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

## How to Contribute

There are many ways to contribute to Slow Day:

### 1. Report Bugs
Found a bug? Please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots

### 2. Suggest Features
Have an idea? Open an issue describing:
- The problem it solves
- Proposed solution
- Alternative solutions considered
- Additional context or mockups

### 3. Write Code
Contributions can include:
- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test coverage improvements

### 4. Improve Documentation
- Fix typos or clarify existing docs
- Add examples or tutorials
- Translate documentation
- Create video tutorials

### 5. Help Others
- Answer questions in issues
- Review pull requests
- Share your use cases
- Write blog posts or tutorials

## Development Setup

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Slow-Day.git
cd Slow-Day
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Make Your Changes
- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run the analyzer
sudo python3 analyzer.py -c 10

# Start the web server
sudo python3 web_server.py
# Then test in browser

# Test database operations
python3 database_manager.py --stats
```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to functions and classes
- Use type hints where appropriate

### Example:
```python
def capture_packets(interface: str = None, count: int = 0) -> list:
    """
    Capture network packets from specified interface.
    
    Args:
        interface: Network interface name (e.g., 'eth0')
        count: Number of packets to capture (0 = unlimited)
    
    Returns:
        List of captured packet objects
    """
    # Implementation
    pass
```

### Code Organization
- Keep related code together
- Use clear file and folder structure
- Separate concerns (UI, logic, data)
- Avoid circular dependencies

### Comments
```python
# Good: Explains WHY
# Use BPF filter to reduce CPU usage on high-traffic networks
sniff(filter="tcp port 80")

# Bad: Explains WHAT (obvious from code)
# Sniff with filter
sniff(filter="tcp port 80")
```

### Error Handling
```python
# Always handle potential errors
try:
    result = risky_operation()
except SpecificException as e:
    log_error(f"Operation failed: {e}")
    return None
```

## Submitting Changes

### 1. Commit Your Changes
```bash
git add .
git commit -m "Add feature: brief description"
```

### Commit Message Guidelines
- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable

Examples:
```
Add support for IPv6 packet capture
Fix database connection timeout issue
Update README with installation instructions
Refactor packet parser for better performance
```

### 2. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

### 4. Code Review Process
- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged!

## Areas for Contribution

Here are some ideas for contributions:

### High Priority
- [ ] Cross-platform support (Windows)
- [ ] Unit tests for core functions
- [ ] Performance optimization for high-traffic scenarios
- [ ] Additional protocol support (IPv6, ARP, etc.)
- [ ] Real-time packet filtering in UI

### Medium Priority
- [ ] PCAP file export
- [ ] Advanced visualization (charts, graphs)
- [ ] Packet payload search functionality
- [ ] GeoIP location lookup
- [ ] Alert system for suspicious traffic

### Low Priority
- [ ] Theme customization
- [ ] Mobile-responsive UI improvements
- [ ] Integration with other security tools
- [ ] Command-line TUI interface
- [ ] Docker containerization

## Feature Requests

When requesting a feature:

1. **Check existing issues** - It might already be planned!
2. **Describe the use case** - Why is this needed?
3. **Propose a solution** - How should it work?
4. **Consider alternatives** - Are there other approaches?
5. **Add context** - Screenshots, diagrams, examples

## Bug Reports

Good bug reports should include:

### Template
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Start the analyzer with...
2. Click on...
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 22.04
- Python: 3.10.6
- Slow Day version: 1.0.0

## Logs/Screenshots
```
Paste relevant logs or attach screenshots
```

## Additional Context
Any other relevant information
```

## Questions?

If you have questions:
- Open an issue with the "question" label
- Reach out via GitHub Discussions (if enabled)
- Check existing documentation first

## Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Given credit in commit history

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make Slow Day better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚀**
