# azure-functions-recipes

Original Python v2 Azure Functions recipes with HTTP, timer, queue, Event Grid, Service Bus, and Graph notification handlers.

## Architecture

HTTP/timer/storage queue/Event Grid/Service Bus → Python v2 Functions app → validation and bounded processing. Graph sends HTTPS change notifications to a webhook; it is not a native Graph trigger.

## Prerequisites

Python 3.12, Azure Functions Core Tools v4, Azurite for storage development, Azure subscription for cloud tests. Service Bus requires a development namespace and Graph requires an Entra application/subscription.

## Setup

1. Run `python -m venv .venv`, activate it, and run `pip install -r requirements.txt`.
2. Copy `.env.example` values into an untracked `local.settings.json` with `IsEncrypted: false` and a `Values` object. Core Tools does not load .env automatically.
3. Start Azurite; use `AzureWebJobsStorage=UseDevelopmentStorage=true` locally.
4. Run `func start --script-root examples`. Disabled cloud-only functions remain disabled until their connections are configured.
5. Call `http://localhost:7071/api/hello?name=Curator`. Local Functions normally bypasses authorization; deployed HTTP endpoints require a function key.
6. Configure Service Bus connection and Graph client-state outside Git; enable each handler explicitly. Deploy manually to a development Flex Consumption app using `func azure functionapp publish <APP_NAME> --script-root examples`.

## Sample workflow

HTTP validates a name; timer emits a heartbeat; queue processes a small JSON job; Event Grid records event type; Service Bus validates a job; Graph webhook validates subscription requests and client-state. Handlers log metadata and do not perform business mutations.

## Security

Read [SECURITY.md](SECURITY.md). Environment examples contain placeholders only.
Never commit local environment values or production exports. No deployment is automated.

## Troubleshooting

Storage unavailable: start Azurite. Missing connection: leave Service Bus disabled until configured. Graph validation fails: check HTTPS reachability and validation-token response. Functions worker errors: verify Python 3.12 and runtime v4.

## License and attribution

Original implementations and documentation by Mudit Dholakia, licensed under MIT.
No upstream code was imported. These references informed the learning scope:
- https://github.com/Azure/azure-functions-templates
- https://github.com/Azure/azure-functions-durable-extension
Platform services, SDK distributions, and third-party content retain their own terms.

## Updating

This is an original repository and has no upstream remote. Run `git pull --ff-only origin main`.
Review Dependabot changes and current platform documentation before upgrading.

## Validation limits

Python syntax and local smoke tests are checked before publication. Cloud execution,
tenant integrations, Tableau workbook authoring, and live agent evaluation require
your development environments and have not been verified by local checks.
