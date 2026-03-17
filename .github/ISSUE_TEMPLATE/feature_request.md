name: Feature Request
description: Suggest a new feature for Agentic Website Builder
title: "[FEATURE] "
labels: ["enhancement"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature! Please fill out the form below.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the feature
      placeholder: "Describe the feature..."
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problem It Solves
      description: What problem does this feature solve?
      placeholder: "This feature solves..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this feature work?
      placeholder: "The feature should work like..."

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: Alternative approaches or solutions
      placeholder: "Alternative approaches..."

  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any additional context or examples
      placeholder: "Additional context..."
