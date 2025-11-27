# Contributing Guidelines

Thank you for considering contributing to the **MoTeC CSV Splitter & Corner Detection for ACC** project!  
This document outlines how you can help improve the project, whether through bug reports, feature requests, or code contributions.

---

## How to Contribute

### Reporting Issues
- Use the **Issues** tab to report bugs or suggest improvements.
- Clearly describe the problem, including:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment details (Python version, OS, ACC/MoTeC export version)

---

### Suggesting Features
- Open an issue with the label `enhancement`.
- Explain the motivation behind the feature (e.g., new metrics, visualization, AI integration).
- Provide examples of how the feature would be used.

---

### Submitting Code
1. Fork the repository.
2. Create a new branch for your changes:
   ```bash
   git checkout -b feature/my-new-feature
3. Make your changes with clear, modular code.

4. Add or update documentation in README.md or docs/ if relevant.

5. Write tests in the tests/ folder if applicable.

6. Commit with a descriptive message:
```bash
git commit -m "Add adaptive threshold refinement for corner detection"
```
7. Push to your fork and open a Pull Request.

---

### Code Style
<br>Follow PEP 8 guidelines for Python.
<br>Keep functions small and modular.
<br>Use descriptive variable names (steer_threshold, g_lat_threshold).
<br>Avoid broad exception clauses; catch specific errors (ValueError, TypeError).

---

### Pull Request Process
Ensure your PR addresses a single issue or feature.
<br>Link the related issue in your PR description.
<br>PRs will be reviewed for:
<br>Code clarity
<br>Functionality
<br>Documentation
<br>Tests (if applicable)

---

### Community Standards
Be respectful and constructive in discussions.

Collaborators are encouraged to share knowledge and help newcomers.

This project is intended to be a welcoming space for motorsport enthusiasts, data engineers, and AI developers.

---

### Roadmap Alignment
Contributions should align with the Roadmap, focusing on:

Short-term goals (combined CSV export, summary metrics).

Medium-term goals (advanced metrics, visualization).

Long-term goals (AI setup optimizer integration, track profiles).

---

### License
By contributing, you agree that your contributions will be licensed under the MIT License.
