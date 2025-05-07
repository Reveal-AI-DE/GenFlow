+++
title = 'Pull requests'
linkTitle= 'Pull requests'
description= 'Instructions on how to create a pull request.'
weight= 6
+++
High-quality pull requests—whether they are patches, improvements, or new features—are greatly appreciated.
To ensure they are effective, keep them focused on a single purpose and avoid including unrelated changes.

Before starting work on a significant pull request (e.g., adding new features or refactoring code), it’s a good idea to
discuss your plans with the project’s developers. This helps avoid spending time on changes that may not align with the
project’s goals or might not be accepted.

When submitting a pull request, make sure to follow the project's coding standards (e.g., indentation, clear comments)
and meet any additional requirements, such as providing adequate test coverage.

To have your contribution considered for inclusion in the project, follow this process:

1. [Fork the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo), clone
your fork locally, and set up the remotes:

   ```bash
   # Clone your fork of the repo into the current directory
   git clone https://github.com/<your-username>/<repo-name>
   # Navigate to the newly cloned directory
   cd <repo-name>
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/<upstream-owner>/<repo-name>
   ```

2. If your clone is outdated, update it by pulling the latest changes from the upstream repository:

   ```bash
   git checkout <dev-branch>
   git pull upstream <dev-branch>
   ```

3. Create a new branch based on the main development branch to work on your feature, fix, or change:

   ```bash
   git checkout -b <topic-branch-name>
   ```

4. Commit your changes in meaningful, logical chunks. Follow these [guidelines](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
for writing good commit messages to ensure your contributions are clear and professional. Use Git's
[interactive rebase](https://docs.github.com/en/github/using-git/about-git-rebase) to clean up your commit
history before sharing your work.

5. Merge or rebase the upstream development branch into your feature branch to keep it up to date:

   ```bash
   git pull [--rebase] upstream <dev-branch>
   ```

6. Push your feature branch to your forked repository:

   ```bash
   git push origin <topic-branch-name>
   ```

7. [Submit a Pull Request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
with a concise and descriptive title, along with a detailed explanation of your changes.

**IMPORTANT**: By contributing a patch, you consent to the project owner licensing your work under the same terms as the project's existing license.
