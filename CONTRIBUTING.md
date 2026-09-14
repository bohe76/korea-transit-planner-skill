# Contributing

Contributions that make Korean transit planning more accurate, transparent, accessible, or regionally useful are welcome.

## Before opening a change

- Keep the public core generic. Do not submit home addresses, calendar identities, account data, personal preference profiles, API keys, authenticated URLs, or copied proprietary datasets.
- Cite official operator/public sources for schedule, fare, eligibility, and service-boundary claims.
- Treat map planners as candidate generators, and respect their terms and asset licenses.
- Preserve the explicit-origin rule, hard station constraints, same-time door-to-door comparison, and strict GTX opt-in behavior.
- Use fictional or clearly generic examples.

## Local checks

Python 3.9+ is sufficient; the checks use only the standard library.

```bash
python scripts/validate_agent_skill.py korea-transit-planner
python scripts/validate.py .
python -m unittest discover -s tests -v
```

## Changes and releases

Use focused pull requests and explain source freshness, uncertainty, and privacy impact. Update `CHANGELOG.md` for user-visible changes.

This project uses Semantic Versioning:

- PATCH: compatible clarifications, source updates, and privacy-safe corrections.
- MINOR: compatible new modes, regions, references, or output capabilities.
- MAJOR: breaking changes to origin, GTX, station-constraint, privacy, or output contracts.

Generalized, privacy-safe lessons from real-world use may become releases after review. Do not automate a release or publish raw trip context. Every release requires maintainer review.

## Pull request checklist

- [ ] No private origin, personal identity, credential, or proprietary dataset is included.
- [ ] Official facts have an official source or a clearly labeled fallback.
- [ ] GTX remains explicit opt-in.
- [ ] Named station constraints and same-time comparisons remain intact.
- [ ] All three validation commands pass.
