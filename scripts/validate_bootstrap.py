import os

def test_repository_structure():
    required_dirs = [
        "docs/architecture/adr",
        "docs/prompts",
        "docs/schemas",
        "docs/templates",
        "docs/examples",
        "docs/reference-implementation",
        "scripts",
        "tests",
        ".github/workflows"
    ]

    for d in required_dirs:
        assert os.path.isdir(d), f"Directory {d} is missing"

def test_mandatory_files():
    required_files = [
        "README.md",
        "SUMMARY.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "mkdocs.yml",
        "docs/index.md",
        "docs/specifications/MASTER_ENGINEERING_SPECIFICATION.md"
    ]

    for f in required_files:
        assert os.path.isfile(f), f"File {f} is missing"

if __name__ == "__main__":
    try:
        test_repository_structure()
        test_mandatory_files()
        print("Repository bootstrap validation passed!")
    except AssertionError as e:
        print(f"Validation failed: {e}")
        exit(1)
