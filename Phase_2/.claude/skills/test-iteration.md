# Skill: Test Iteration

## Description
Tests current implementation, identifies issues, and suggests fixes.

## Usage
/test-iteration [specific-feature]

## Instructions
- Review recently implemented code
- Check for common issues:
  - TypeScript/Python type errors
  - Missing error handling
  - Authentication/authorization gaps
  - UI/UX problems
  - API endpoint issues
- Describe how to run and test the feature
- List specific observed issues with file paths and line numbers
- Provide concrete fix suggestions or spec updates
- Prioritize issues by severity

## Output Format
1. **What was tested**: Feature/component description
2. **Issues found**: Numbered list with locations
3. **Suggested fixes**: Specific code changes or spec updates
4. **Next steps**: What to implement or test next

## Examples
- `/test-iteration`
- `/test-iteration "authentication flow"`