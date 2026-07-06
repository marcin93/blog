Title: AI - chat or more?
Date: 2026.07.06
Tags: ai, llm, agent-ai, rag
Slug: ai-chat-or-more

# Intro

We are most familiar with AI and its clients - such as Web and Mobile Apps - yet some users still choose to stay on the first step. This is often due to a lack of time or convenience. Let’s look together at the available options and how to use them.

By "AI," I mean LLM chat clients like ChatGPT, Claude, or DeepSeek. I will take an everyday user’s perspective on using these systems to gain knowledge or speed up day-to-day work.

We have heard about Copilot, as many companies enable it across other parts of the Microsoft Office suite. From a personal perspective, we have seen or used apps and web clients to check and sometimes work with AI. However, there is usually a next step worth exploring.

## Types of AI Work Use Cases

Looking at the broad picture of how we can use AI, I distinguish the following types:

- Chat text
- Chat + doc as base
- Projects (partial RAG)
- RAG
- Agent AI

### Quick Comparison Table

| Use Case  | Best for           | Requires set‑up?  | Example             | Cost                  |
| --------- | ------------------ | ----------------- | ------------------- | --------------------- |
| Chat text | Quick Q&A          | No                | “Explain recursion” | free                  |
| Chat+doc  | Analysing one file | No (upload)       | Summarise a PDF     | free                  |
| Projects  | Ongoing work       | Yes (folder)      | Writing a novel     | free/paid             |
| RAG       | Many documents     | Yes (index)       | Company policy bot  | free/paid ~ $5 or $20 |
| Agent     | Task automation    | Yes (permissions) | Email follow‑ups    | free/paid ~ $5 or $20 |

# Chat

The easiest way is to visit chatgpt.com, claude.ai, or deepseek.com directly and use their chat interfaces. If one of those platforms interests you, you can install a mobile app for easier access. 

You can also use visual models to generate images by describing them.


# Chat with 'documents'

This is the next step in using AI: you can upload a document to the chat and talk with the AI. The idea is that a chatbot with internet access can validate, analyze your document, and add comments. This could be a presentation to be created or an official document that is hard to understand.

Another example of such a 'document' is a URL to a video, which can be analyzed and summarized. The user can then chat based on that summary.

# Projects

This level can sound esoteric, as developers often use AI based on their codebase to analyze best practices and suggest optimizations. But do not be afraid. Google launched an interesting tool called [Notebook LLM](https://notebooklm.google/). It allows users to create an online project, upload many files or links as sources, and get details based on them.

The advantage (for some) here is that answers are based on the provided sources, not just general internet data. Those summaries can even be generated in the form of a podcast.

# RAG (Retrieval-Augmented Generation)
This approach goes a step further. The user starts the AI and provides access to their own documents, like an Obsidian vault with mixed notes. They can be analyzed at once or left until needed.

With such an approach, it is also good to set up an Agent 'Persona' (more on that: [Agent.md](https://agents.md/)). Such a file instructs the AI about its role, how the user expects to receive answers, where the files are located, and what the structure is. This is already moving into the next step, but it can be kept as is.

At this level, we can already play with different desktop solutions from AI vendors (Codex, Claude, Gemini, etc.) and [OpenCode](https://opencode.ai/), which allows users to select their preferred model provider and, by using API keys, access one or many models depending on their needs.

# Agent AI

Here we reach a deeper level when working with large amounts of data. This level becomes necessary when there is a need for specialized agents for certain tasks. Some agents can read data and inform the user of what can be done—similar to standard chat—while others can have access to user data and create, write, delete files, or even perform system actions. For example, [OpenClaw](https://openclaw.ai/). A great write-up is available in the OpenCode documentation: [Agents](https://opencode.ai/docs/agents/)

Useful resources at this stage include model comparisons that provide model accuracy for specific tasks as well as cost data.

- [OpenRouter.ai](https://openrouter.ai/models?order=top-weekly)
- [LiveBench.ai](https://livebench.ai/#/?highunseenbias=true)

# Cost

Cost will vary depending on the user. We can stay on free plans across all the above solutions. This can be limiting, as access to the best-performing models is usually paid. However, for simpler tasks, free tiers can be fully sufficient.

In most cases, subscriptions are around $20/month. However, solutions like OpenRouter or OpenCode Zen offer pay-per-use pricing, which can help limit spending.

# Conclusion

If you've reached this note, I assume you are into LLM's/AI and are likely already aware of these use cases. If, by any chance, this is not the case, I encourage you to test these tools.

Use free tiers and have fun with image generation or talking to your data. Or maybe even create your own Agents to help you work with your health, finances, marketing, coding, or even learning new things.
