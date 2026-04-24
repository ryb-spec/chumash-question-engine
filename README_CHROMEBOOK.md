# Chromebook Commands

Run the isolated curriculum extraction validator:

```bash
python scripts/validate_curriculum_extraction.py
```

Run the isolated loader summary:

```bash
python scripts/load_curriculum_extraction.py --summary
```

Run the Phase 1 scaffold tests:

```bash
python -m pytest tests/test_curriculum_extraction_schemas.py tests/test_curriculum_extraction_validation.py tests/test_curriculum_extraction_loader.py
```
