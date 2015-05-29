#!/usr/bin/env python
import sys

from flake8.hooks import git_hook as flake8_hook
from flake8.hooks import get_git_param
from isort.hooks import git_hook as isort_hook

# `get_git_param` will retrieve configuration from your local git config and
# then fall back to using the environment variables that the hook has always
# supported.
# For example, to set the complexity, you'll need to do:
#   git config flake8.complexity 10
COMPLEXITY = get_git_param('FLAKE8_COMPLEXITY', 10)
STRICT = get_git_param('FLAKE8_STRICT', False)
IGNORE = get_git_param('FLAKE8_IGNORE', None)
LAZY = get_git_param('FLAKE8_LAZY', False)

if __name__ == '__main__':
    isort_result = isort_hook(strict=True)

    if isort_result:
        sys.stdout('Run `isort -rc .` from the repository root directory to sort imports.')

    flake8_result = flake8_hook(
        complexity=COMPLEXITY,
        strict=STRICT,
        ignore=IGNORE,
        lazy=LAZY,
    )

    sys.exit(isort_result | flake8_result)
