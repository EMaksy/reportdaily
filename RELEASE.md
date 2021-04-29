# Release workflow

- [ ] Finish and merge all issues to the related release.
- [ ] Create a release issue
- [ ] Add a release branch in this format: release/<new version>
- [ ] Get all commits from the latest release to the current state with: git log --oneline <LAST_RELEASE>...HEAD
- [ ] Update the Changelog.md with the new changes
- [ ] Update the version of the project with bump2version [major|minor|patch]
- [ ] Push your branch to github and open up a PR
- [ ] Request a review and address all comments
- [ ] Merge PR with main and delete the branch
- [ ] Tag the new release with: git tag -a <new_version> and enter the entry from the Changelog
- [ ] Go to Releases and create a new release (reuse the new entry from the Changelog)
- [ ] Publish the release
