# Google ADK Agent Examples

This directory contains example agents built with the [Google Agent Development Kit (ADK)](https://google.adk.dev).

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Available Agents](#available-agents)
- [Running Agents](#running-agents)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before running these examples, ensure you have:

1. **Python 3.11+** installed
2. **Google Cloud credentials** configured (see [Setup](#setup))
3. **Dependencies installed** (see [Setup](#setup))

## Setup

### 1. Install Dependencies

From the repository root directory:

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- `google-adk` - The Google Agent Development Kit
- `google-genai` - Google Generative AI SDK
- Other required dependencies

### 2. Configure Google Cloud Credentials

The agents use Google's Gemini models, which require authentication. Choose one of these methods:

#### Option A: Application Default Credentials (Recommended)

```bash
# Install Google Cloud CLI if you haven't already
# See: https://cloud.google.com/sdk/docs/install

# Authenticate with your Google account
gcloud auth application-default login
```

#### Option B: Service Account Key

1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

#### Option C: API Key (for development/testing)

Set the API key in your environment:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Available Agents

### Parallelization Agent

**Location:** `examples/google/agents/parallelization/`

**Description:** Demonstrates parallel agent execution using the `ParallelAgent` pattern. This agent:
- Runs 3 research agents concurrently (Renewable Energy, Electric Vehicles, Carbon Capture)
- Each agent uses Google Search to gather information
- A synthesis agent combines all findings into a structured report

## Running Agents

```bash
# Run from the repository root
python3 -m google.adk.cli run examples/google/agents/<agent>
```

This will:
1. Start an interactive CLI session
2. Wait for your input
3. Type a query like: `"Please research the topics"` or `"Start the research"`
4. The agent will execute and display results
5. Type `exit` to quit

## Troubleshooting

### Authentication Errors

**Error:**
```
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials.
```

**Solution:** Follow the [Configure Google Cloud Credentials](#2-configure-google-cloud-credentials) section above.

### Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'google.adk'
```

**Solution:**
```bash
# Ensure you're in the repository root
pip install -r requirements.txt

# Or install google-adk directly
pip install google-adk
```

### Model Access Issues

**Error:**
```
Permission denied for model gemini-2.0-flash
```

**Solution:**
- Ensure your Google Cloud project has the Vertex AI API enabled
- Verify your credentials have access to Gemini models
- Try using `gemini-1.5-flash` or `gemini-1.5-pro` if 2.0 is not available

## Additional Resources

- [Google ADK Documentation](https://google.adk.dev)
- [Google Generative AI Documentation](https://ai.google.dev)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

## Contributing

When adding new agents to this directory:
1. Create a new subdirectory under `examples/google/agents/`
2. Include an `__init__.py` that exports `root_agent`
3. Add documentation to this README
4. Include example queries and expected outputs
