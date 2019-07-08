#!/usr/bin/env python
"""play around with cookiecutter package"""

from cookiecutter.config import get_user_config
from cookiecutter.repository import determine_repo_dir


def main(template: str):
    config_dict = get_user_config()
    repo_dir, cleanup = determine_repo_dir(
        template=template,
        abbreviations=config_dict['abbreviations'],
        clone_to_dir=config_dict['cookiecutters_dir'],
        checkout=None,
        no_input=False,
    )
    print("repo_dir: ", repo_dir)
    print("cleanup: ", cleanup)


if __name__ == '__main__':
    main("https://github.com/audreyr/cookiecutter-pypackage.git")
