name: Bug Report
description: Report a bug in Agentic Website Builder
title: "[BUG] "
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug! Please fill out the form below.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear and concise description of the bug
      placeholder: "Describe the bug here..."
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Create agent with...
        2. Run task...
        3. See error...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen
      placeholder: "Expected behavior..."
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
      placeholder: "Actual behavior..."
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Python Version
      options:
        - "3.9"
        - "3.10"
        - "3.11"
        - "3.12"
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant Logs
      description: Any relevant log output (wrap in code block)
      placeholder: |
        ```
        Error logs here...
        ```

  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any additional context about the bug
      placeholder: "Additional information..."
