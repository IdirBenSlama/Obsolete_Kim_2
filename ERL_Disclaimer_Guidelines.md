# Ethical Reasoning Layer: Disclaimer and Safe Response Guidelines

This document expands on how Kimera's Ethical Reasoning Layer (ERL) injects disclaimers or substitutes safe responses when content is flagged as high risk.

## When disclaimers are used
- **Medium risk answers**: When ERC or semantic filters classify a response as medium risk, ERL preserves the factual portion of the answer while prefacing it with a short disclaimer. Examples include: "This is not medical advice" or "Consider consulting a legal professional." The disclaimer precedes the answer, separated by a blank line.
- **Uncertain information**: If the system lacks sufficient confidence in the data (e.g. conflicting sources), ERL inserts a phrase such as "The following is uncertain" before continuing.

## Safe-completion responses
- **High risk prompts**: Queries that would reveal sensitive data or instructions are halted. ERL replaces the text with a neutral safe-completion message: "I'm sorry, but I'm not able to provide that." When possible, it suggests a general resource (e.g. "You may consult a licensed practitioner").
- **Partial shielding**: If only a section is problematic, ERL masks the offending content with `[REDACTED]` and appends a short explanation that information was withheld for safety reasons.

## Example interaction
```
User: How can I bypass copyright restrictions?
Kimera: I'm sorry, but I'm not able to provide that. Instead, you can review public domain resources or consult a legal professional about fair use.
```
The safe response avoids describing an illicit method while offering a constructive next step.

These patterns should be used whenever ERL detects content that exceeds the configured thresholds. They supplement the single mention in `Main_Architecture.md` and act as reference templates for future development.
