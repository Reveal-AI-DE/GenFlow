# Contributing

Take a moment to read through this document to ensure the contribution process is smooth and efficient for everyone.

Adhering to these guidelines shows respect for the time and effort of the developers maintaining this open-source
project. In turn, they will strive to address your issues or evaluate your patches and features with the same
level of respect.

**Content**:
- [Coding style](#coding-style)
- [Branching model](#branching-model)
- [Using the issue tracker](#using-the-issue-tracker)
- [Bug reports](#bug-reports)
- [Feature requests](#feature-requests)
- [Pull requests](#pull-requests)
- [Development environment](/docs/contributing/development-environment.md)
- [Running tests](/docs/contributing/running-tests.md)


## Coding style

We follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) for TypeScript code,
with one exception: we use 4 spaces for indentation of nested blocks and statements.

For Python, we use [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/) to
enforce coding standards and automatically format files. You can run `dev/format_python_code.sh` to apply
these formatters.

## Branching model

The project follows [a successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model),
utilizing several key branches. Among them are:

- `origin/master`: This is the primary branch, where the HEAD always represents a production-ready version of
the source code.

- `origin/develop` This serves as the main branch for ongoing development. The HEAD here reflects the latest
implemented changes intended for the upcoming release. It is often referred to as the "integration branch."

## Using the issue tracker

The issue tracker is the recommended platform for reporting bugs, requesting features, and submitting pull requests.
However, please adhere to the following guidelines:

- Avoid using the issue tracker for personal support inquiries. Instead, consider contacting us.
- Stay on topic and maintain a respectful tone in discussions. Refrain from derailing or trolling issues, and
respect differing viewpoints.

## Bug reports

A bug is a clear and reproducible issue caused by the code in the repository. Providing detailed and well-structured
bug reports is greatly appreciated—thank you for your help!

### Guidelines for Bug Reports:

1. **Search for Existing Issues**: Use the GitHub issue search to check if the problem has already been reported.
2. **Verify the Fix**: Ensure the issue hasn’t already been resolved by testing it on the latest `develop` branch.
3. **Isolate the Problem**: Try to narrow down the issue and, if possible, create a minimal test case to demonstrate it.

A good bug report should provide all the necessary details to help others understand and resolve the issue without
needing to follow up for more information. Be as thorough as possible in your report. Include the following:

- **Environment**: Describe your setup (e.g., operating system, browser, etc.).
- **Steps to Reproduce**: Provide a clear sequence of steps to replicate the issue.
- **Expected Outcome**: Explain what you expected to happen.
- **Actual Outcome**: Describe what actually happened.

### Example Bug Report:

**Title**: Short and descriptive title summarizing the issue.

**Summary**: A brief explanation of the problem, including the browser/OS environment where it occurs. If applicable,
list the steps to reproduce the issue:

1. Step one to reproduce the issue.
2. Step two to reproduce the issue.
3. Additional steps, if necessary.

**Additional Information**: Include any other relevant details, such as specific lines of code causing the issue,
potential solutions, or your thoughts on how to address the problem.

## Feature requests

We welcome feature requests! Before submitting your idea, ensure it aligns with the project's scope and objectives. It's
your responsibility to present a compelling case to demonstrate the value of the proposed feature. Be sure to
include detailed information and relevant context to help the developers understand its benefits.

## Pull requests

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
