import os
import github
from datetime import datetime
from github import Github


def semver_to_int(val: str) -> int:
    parts = val.split(".")
    total = 0
    for idx, val in enumerate(parts):
        # Major release are worth 100 per version
        # Minors are worth 10 per version
        # Patches don't get a boost
        # example "2.6.3" -> 263, "2.12.0" -> 320
        total += int(val) * (10 ** (2 - idx))
    return total


def sort_tags(tag):
    return semver_to_int(tag.name)


def run(proposed_version: str=os.getenv("TBS_CLI_VERSION")):
    gh = Github(os.getenv("GITHUB_USERNAME"),
                os.getenv("GITHUB_PASSWORD"))

    repo = gh.get_organization("3blades").get_repo("python-cli-tools")

    tags = list(repo.get_tags())
    names_only = sorted([t.name for t in tags], key=semver_to_int, reverse=True)
    if proposed_version in names_only:
        raise ValueError(f"Proposed version {proposed_version} already exists as a release in Github")
    elif sorted(names_only + [proposed_version], key=semver_to_int, reverse=True)[0] != proposed_version:
        raise ValueError(f"Proposed version {proposed_version} would not be the highest version.")
    elif not os.getenv("TRAVIS_PULL_REQUEST"):
        tagger = github.InputGitAuthor(name="3Blades",
                                       email="auto-builds@3blades.io",
                                       date=datetime.now())
        repo.create_git_tag_and_release(tag=proposed_version,
                                        # TODO: Create a better tag_message
                                        tag_message="Created from test script",
                                        release_name=proposed_version,
                                        # TODO: Create a better release message
                                        release_message="Created from test script",
                                        object=os.getenv("TRAVIS_COMMIT"),
                                        type="commit",
                                        tagger=tagger,
                                        draft=True)
        print("Successfully created tag and release")


if __name__ == "__main__":
    run(os.getenv("TBS_CLI_VERSION"))
