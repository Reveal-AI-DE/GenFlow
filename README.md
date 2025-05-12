<p align="center">
  <img src="/site/content/en/images/demo.gif" alt="GeniFlow Platform" width="100%" max-width="800px">
</p>
<p align="center">
  <a href="https://demo.geniflow.revealai.de/" target="_blank">
    <img src="https://img.shields.io/badge/Try%20GeniFlow%20Now-007fd6?style=for-the-badge&logoColor=white" alt="Try GeniFlow Now">
  </a>
</p>

# GeniFlow

[![CI][ci-img]][ci-url]
[![Coverage Status][coverage-img]][coverage-url]
![Endpoint Badge][server-pulls-url]
![Endpoint Badge][ui-pulls-url]
[![LinkedIn][linkedin-img]][linkedin-url]


**GeniFlow** is an open-source, low-code GenAI platform that empowers organizations to build and manage Generative
AI assistants that automate routine writing tasks and enhance access to internal knowledge.

## Designed for flexibility and collaboration, GeniFlow enables teams to 🌟:
- Create and deploy custom AI assistants tailored to their workflows.
- Select and configure the language models best suited for their needs.
- Monitor usage patterns and performance through built-in analytics.
- Operate in a team-based environment where each team can maintain its own assistants and dedicated knowledge base.

Whether you're streamlining documentation, automating reports, or enabling internal support bots, GeniFlow helps you
harness the power of GenAI — faster, smarter, and with minimal coding.

Watch the [YouTube video](https://www.youtube.com/watch?v=tP5Ox9R0naA&t=10s&ab_channel=RevealAI) to see how to get
started with GeniFlow and learn how to:

- 🔧 **Create an API Endpoint** – Set up and configure a backend API for your GenAI integration.
- ✍️ **Create a Prompt** – Design and test custom prompts for specific writing or Q&A tasks.
- 🤖 **Create an Assistant** – Build a fully functional GenAI assistant powered by your prompt and knowledge base.
- 📊 **View Usage Analytics** – Monitor assistant activity, prompt performance, and user engagement by
clicking on session properties.

Ready to explore GeniFlow? Try the [Online Demo](https://demo.geniflow.revealai.de/) to see the platform in action
(you will need an [API key from OpenAI](https://platform.openai.com/api-keys)).

Prefer a self-hosted solution? Follow the [Self-hosted Installation Guide](https://docs.geniflow.revealai.de/docs/administration/basic/installation/).
We also offer enterprise support with premium features, training, and dedicated assistance with a 24-hour SLA.
[Contact us](#contact-) to learn more.

## Quick Start ⚡

- [Installation guide](https://docs.geniflow.revealai.de/docs/administration/basic/installation/)
- [Contributing](https://docs.geniflow.revealai.de/docs/contributing/)
- [Server API](https://docs.geniflow.revealai.de/docs/api/)
- [AWS Deployment Guide](#)
- [Frequently asked questions](#)
- [Where to ask questions](#)

## Documentation 📖

Comprehensive documentation is available at [GeniFlow Documentation](https://docs.geniflow.revealai.de/docs/)

## Roadmap 🛣️

Here are the planned enhancements and upcoming features for [GeniFlow Roadmap](https://docs.geniflow.revealai.de/docs/roadmap/)
#### Currently in development:

- [ ] **Amazon Bedrock Integration**
  Enable API access to LLMs available via Amazon Bedrock for scalable, secure, and fully managed model deployment.

- [ ] **vLLM Integration**
  Provide support for connecting to LLMs deployed with [vLLM](https://github.com/vllm-project/vllm),
  enabling high-throughput, optimized inference.

- [ ] **Multi-Agent Assistant Framework**
  Introduce a flexible architecture for creating and coordinating multiple collaborative AI agents within a single
  workflow.

## Contributing 🤝

We welcome contributions! Please see [GeniFlow Contributing Guide](https://docs.geniflow.revealai.de/docs/contributing/) for guidelines.

## License 📄

This project is licensed under the Apache 2.0 License Extended - see the [GeniFlow LICENSE](LICENSE.md) file for details.

## Telemetry Notice 📊

GeniFlow collects domain information using telemetry for analytics purposes. The only data
sent to the telemetry server is the admin domain (e.g., `example.com`). No personal data is ever sent, and no
cookies are included in the response. The GeniFlow team uses these domains to track the usage of the platform.

If you prefer to disable telemetry, you can do so by modifying the `geniflow-ui/.env.production` file:

```bash
REACT_APP_TELEMETRY_DISABLED=true
```

## Contact 📬

For support or inquiries:

- **Email**: [info@revealai.de](mailto:info@revealai.de)
- [![LinkedIn][linkedin-img]][linkedin-url]
- **Address**: Darm Street 37, 64287 Darmstadt, Germany

<!-- Badges -->

[ci-img]: https://github.com/Reveal-AI-DE/GeniFlow/actions/workflows/main.yml/badge.svg?branch=develop
[ci-url]: https://github.com/Reveal-AI-DE/GeniFlow/actions
[coverage-img]: https://codecov.io/gh/Reveal-AI-DE/GeniFlow/graph/badge.svg
[coverage-url]: https://codecov.io/gh/Reveal-AI-DE/GeniFlow
[server-pulls-url]: https://img.shields.io/endpoint?url=https%3A%2F%2Fmwopc2qsfd.execute-api.eu-central-1.amazonaws.com%2Fdefault%2Ferc-pull-counter%3Frepo%3Dgeniflow%2Fserver%26alias%3Dz5d7y3x3&style=flat-square&label=server%20pulls

[ui-pulls-url]: https://img.shields.io/endpoint?url=https%3A%2F%2Fmwopc2qsfd.execute-api.eu-central-1.amazonaws.com%2Fdefault%2Ferc-pull-counter%3Frepo%3Dgeniflow%2Fui%26alias%3Dz5d7y3x3&style=flat-square&label=UI%20pulls

[linkedin-img]: https://img.shields.io/badge/LinkedIn-Follow-blue?logo=linkedin
[linkedin-url]: https://www.linkedin.com/company/76154575/
