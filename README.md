<p align="center">
  <img src="/docs/img/demo.gif" alt="GenFlow Platform" width="100%" max-width="800px">
</p>
<p align="center">
  <a href="https://demo.genflow.revealai.de/" style="display: inline-block; background-color: #007fd6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
    Try GenFlow Now
  </a>
</p>

# GenFlow

[![CI][ci-img]][ci-url]
[![Coverage Status][coverage-img]][coverage-url]
![Endpoint Badge][server-pulls-url]
![Endpoint Badge][ui-pulls-url]
[![LinkedIn][linkedin-img]][linkedin-url]


**GenFlow** is an open-source, low-code GenAI platform that empowers organizations to build and manage Generative
AI assistants that automate routine writing tasks and enhance access to internal knowledge.

## Designed for flexibility and collaboration, GenFlow enables teams to 🌟:
- Create and deploy custom AI assistants tailored to their workflows.
- Select and configure the language models best suited for their needs.
- Monitor usage patterns and performance through built-in analytics.
- Operate in a team-based environment where each team can maintain its own assistants and dedicated knowledge base.

Whether you're streamlining documentation, automating reports, or enabling internal support bots, GenFlow helps you
harness the power of GenAI — faster, smarter, and with minimal coding.

Watch the [YouTube video](https://www.youtube.com/watch?v=tP5Ox9R0naA&t=10s&ab_channel=RevealAI) to see how to get
started with GenFlow and learn how to:

- 🔧 **Create an API Endpoint** – Set up and configure a backend API for your GenAI integration.
- ✍️ **Create a Prompt** – Design and test custom prompts for specific writing or Q&A tasks.
- 🤖 **Create an Assistant** – Build a fully functional GenAI assistant powered by your prompt and knowledge base.
- 📊 **View Usage Analytics** – Monitor assistant activity, prompt performance, and user engagement by
clicking on session properties.

Ready to explore GenFlow? Try the [Online Demo](https://demo.genflow.revealai.de/) to see the platform in action
(you will need an [API key from OpenAI](https://platform.openai.com/api-keys)).

Prefer a self-hosted solution? Follow the [Self-hosted Installation Guide](docs/administration/basics/installation.md).
We also offer enterprise support with premium features, training, and dedicated assistance with a 24-hour SLA.
[Contact us](#contact-) to learn more.

## Quick Start ⚡

- [Installation guide](/docs/administration/basics/installation.md)
- [Contributing](/docs/contributing/contributing.md)
- [Server API](#)
- [AWS Deployment Guide](#)
- [Frequently asked questions](#)
- [Where to ask questions](#)

## Documentation 📖

Comprehensive documentation is available at [GenFlow Documentation](docs/documentation.md)

## Roadmap 🛣️

Here are the planned enhancements and upcoming features for [GenFlow Roadmap](docs/roadmap.md)
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

We welcome contributions! Please see [GenFlow Contributing Guide](docs/contributing/contributing.md) for guidelines.

## License 📄

This project is licensed under the Apache 2.0 License Extended - see the [GenFlow LICENSE](LICENSE.md) file for details.

## Telemetry Notice 📊

GenFlow collects domain information using telemetry for analytics purposes. The only data
sent to the telemetry server is the admin domain (e.g., `example.com`). No personal data is ever sent, and no
cookies are included in the response. The GenFlow team uses these domains to track the usage of the platform.

If you prefer to disable telemetry, you can do so by modifying the `genflow-ui/.env.production` file:

```bash
REACT_APP_TELEMETRY_DISABLED=true
```

## Contact 📬

For support or inquiries:

- **Email**: [info@revealai.de](mailto:info@revealai.de)
- [![LinkedIn][linkedin-img]][linkedin-url]
- **Address**: Darm Street 37, 64287 Darmstadt, Germany

<!-- Badges -->

[ci-img]: https://github.com/Reveal-AI-DE/GenFlow/actions/workflows/main.yml/badge.svg?branch=develop
[ci-url]: https://github.com/Reveal-AI-DE/GenFlow/actions
[coverage-img]: https://codecov.io/gh/Reveal-AI-DE/GenFlow/graph/badge.svg
[coverage-url]: https://codecov.io/gh/Reveal-AI-DE/GenFlow
[server-pulls-url]: https://img.shields.io/endpoint?url=https%3A%2F%2Fmwopc2qsfd.execute-api.eu-central-1.amazonaws.com%2Fdefault%2Ferc-pull-counter%3Frepo%3Dgenflow%2Fserver%26alias%3Dz5d7y3x3&style=flat-square&label=server%20pulls

[ui-pulls-url]: https://img.shields.io/endpoint?url=https%3A%2F%2Fmwopc2qsfd.execute-api.eu-central-1.amazonaws.com%2Fdefault%2Ferc-pull-counter%3Frepo%3Dgenflow%2Fui%26alias%3Dz5d7y3x3&style=flat-square&label=UI%20pulls

[linkedin-img]: https://img.shields.io/badge/LinkedIn-Follow-blue?logo=linkedin
[linkedin-url]: https://www.linkedin.com/company/76154575/
