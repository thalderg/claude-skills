# Technical Resource Discovery & Knowledge Base System

**Purpose:** Systematically discover, analyze, and curate high-quality technical content across any domain (N8n workflows, Claude Code projects, LLM apps, automation tools, frameworks) from social platforms → create project-specific manuals → feed to NotebookLM for RAG knowledge base.

**Core Philosophy:** Perplexity for discovery → Specialized tools for extraction → Claude for analysis & manual creation → Project folder organization for reusability.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Supported Content Types](#supported-content-types)
3. [Manual Process (Current Implementation)](#manual-process-current-implementation)
4. [LLM Model Comparison Matrix](#llm-model-comparison-matrix)
5. [Project Folder Structure](#project-folder-structure)
6. [Creating Effective Manuals](#creating-effective-manuals)
7. [Automated Workflow (Future API Implementation)](#automated-workflow-future-api-implementation)
8. [Platform-Specific Strategies](#platform-specific-strategies)
9. [API Implementation Details](#api-implementation-details)
10. [NotebookLM Integration](#notebooklm-integration)
11. [Cost Analysis](#cost-analysis)
12. [Troubleshooting & Limitations](#troubleshooting--limitations)

---

## 🎯 System Overview

### The Process Chain

```
1. DISCOVERY (Perplexity Pro)
   ↓
2. EXTRACTION (Specialized tools per platform)
   ↓
3. INTELLIGENT FILTERING (Claude skill - if needed)
   ├─ Use when: 20+ resources OR single link with multiple items
   ├─ Ranks by quality + recency + modern alternatives
   └─ Outputs: Pruned list optimized for NotebookLM
   ↓
4. MANUAL CREATION (NotebookLM creates from filtered resources)
   ↓
5. PROJECT FOLDER (Organized for future reference)
   ↓
6. CLAUDE PROJECT (References manual for context)
```

### Why This Approach?

**Problem:** Each time you need to find N8n workflows, Claude Code examples, or LLM app patterns, you start from scratch.

**Solution:** Build a library of curated resources with AI-generated manuals that guide future searches within project folders.

**Example Use Case:**
- You ask: "Show me an N8n workflow for email automation"
- Claude checks the N8n project folder manual
- Finds 3 similar workflows already documented
- Provides them as inspiration/base instead of generic advice

---

## 📚 Supported Content Types

### Automation & Integration

| Tool | Content Types | Use Cases |
|------|--------------|-----------|
| **N8n** | Workflows (JSON), templates, custom nodes | API integrations, data transformation, scheduling |
| **Make.com** | Scenarios, blueprints | Visual automation, webhooks |
| **Zapier** | Zaps, multi-step workflows | SaaS integrations |
| **Pipedream** | Workflows, code components | Serverless automation with code |
| **Temporal** | Workflows, activities | Durable execution, microservices |
| **Apache Airflow** | DAGs, operators | Data pipelines, ETL |

### AI Development

| Category | Tools/Frameworks | Content Types |
|----------|------------------|---------------|
| **Agentic Coding** | Claude Code, Cursor, Aider | Project examples, prompts, workflows |
| **LLM Frameworks** | LangChain, LlamaIndex, Haystack | RAG implementations, chains, agents |
| **Agent Frameworks** | CrewAI, AutoGPT, BabyAGI | Multi-agent systems, task decomposition |
| **API Wrappers** | OpenAI SDK, Anthropic SDK | Integration patterns, best practices |
| **MCP** | Model Context Protocol servers | Custom tools, data sources |
| **Open-Source** | OpenClaude, LocalAI, Ollama | Self-hosted solutions, privacy-focused |

### Prompt Engineering

- Prompt templates and chains
- Few-shot examples
- System prompts for specific tasks
- Role-based prompts
- Chain-of-thought patterns
- Tree-of-thought implementations

### Development Patterns

- Code snippets and boilerplates
- Architecture patterns
- Best practices documentation
- Error handling approaches
- Testing strategies
- Deployment guides

---

## 🖐️ Manual Process (Current Implementation)

### Decision: When to Use Which Curator Skill

**You now have TWO curator skills:**

| Skill | Best For | Collection Size | Behavior |
|-------|----------|-----------------|----------|
| **Two-Phase Curator** | Any size (auto-detects) | 1-5000+ | Smart routing by count |
| **Original Curator** | Known moderate size | 20-100 | Always deep analysis |

**Two-Phase Curator (Recommended - Use First):**

```
Step 0: Automatically counts resources in collection
    ↓
IF ≤30 resources:
   → Phase 2 directly (deep quality analysis)
   → No Phase 1 needed
   
IF >30 resources:
   → Phase 1 (statistical metadata filter)
   → STOP → User can request Phase 2

Smart, automatic, works for everything.
```

**Decision Matrix:**

| Your Situation | Use This | Why |
|----------------|----------|-----|
| **Don't know collection size** | Two-Phase Curator | Auto-detects and routes |
| **1 file to check** | Two-Phase Curator | Goes straight to quality check |
| **5-30 resources** | Two-Phase Curator | Direct quality analysis |
| **50-3000+ resources** | Two-Phase Curator | Filters then analyzes |
| **Want metadata filter only** | Two-Phase Curator Phase 1 | Stop after filtering |
| **Know it's ~50 items, want deep analysis** | Original Curator | Simple, one-pass |

**Examples:**
- ✅ **Two-Phase:** "Check this workflow" (1 file, auto-detects)
- ✅ **Two-Phase:** github.com/repo with 3000 workflows (auto-filters)
- ✅ **Original:** 30 Claude Code projects you already counted
- ✅ **Two-Phase (safest):** Any unknown collection

**Recommendation:** Default to Two-Phase Curator. It's smart enough to handle everything.

---

### Step-by-Step Workflow

#### **Step 1: Discovery with Perplexity Pro**

**Why Perplexity First?**
- Best search across multiple platforms simultaneously
- Can access X/Twitter posts (where Claude cannot)
- Provides source citations automatically
- Multiple model options for different reasoning styles

**How to Use:**

1. **Go to Perplexity Pro** (perplexity.ai)
2. **Select Model:** 
   - **Claude Opus 4.5** → Best for technical analysis, code understanding
   - **GPT-4o** → Good for creative searches, broad coverage
   - **Reasoning** → For complex multi-step queries
3. **Craft Search Query:**

```plaintext
Example Queries:

N8n Workflows:
"best n8n workflows for API automation reddit OR github 2024-2025"
"advanced n8n custom nodes production-ready"
"n8n workflow templates youtube tutorials high engagement"

Claude Code Projects:
"claude code examples github projects"
"agentic coding with claude real-world applications"
"claude mcp servers implementation guide"

LLM Apps:
"langchain rag production implementation github"
"best crewai multi-agent examples"
"llm app architecture patterns 2024"

General Pattern:
"[tool/framework] [content type] [quality indicator] [platforms] [timeframe]"
```

4. **Review Results:**
   - Perplexity returns URLs with context snippets
   - Note engagement metrics (upvotes, views, stars)
   - Identify multiple sources covering same topic (validation)

5. **Extract URL List:**
   - Copy all relevant URLs to a text file
   - Categorize by platform (Reddit, YouTube, GitHub, etc.)
   - Note initial quality indicators

**Perplexity Limitations:**
- ❌ No full YouTube transcripts (only metadata)
- ❌ Cannot deeply analyze code repositories
- ❌ Limited iterative refinement
- ⚠️ Sometimes misses niche communities

---

#### **Step 2: Content Extraction by Platform**

| Platform | Extraction Tool | Process |
|----------|----------------|---------|
| **YouTube** | ChatGPT Plus or Gemini | Paste URL → "Extract full transcript" |
| **X/Twitter** | Perplexity or Manual | Already captured in Step 1, or screenshot/copy |
| **Reddit** | Direct Copy-Paste | Open thread, copy text + top comments |
| **GitHub** | Direct Access | Clone repo or view README/code in browser |
| **Articles** | Web Fetch | Copy full text or use reader mode |

**YouTube Transcript Extraction:**

**Using ChatGPT Plus:**
```
Prompt: "Extract the full transcript from this YouTube video and summarize the key technical steps: [URL]"
```

**Using Gemini Advanced:**
```
Prompt: "Get the complete transcript from [URL] and highlight code examples or workflow patterns"
```

**Save Transcripts:**
- Create a folder: `/raw-content/[topic]/youtube/`
- Name files: `video-title-transcript.txt`

**X/Twitter Extraction:**
- If Perplexity already captured it: use that
- Otherwise: manually screenshot or copy visible text
- **Reality:** X is difficult, deprioritize if content available elsewhere

**Reddit Extraction:**
- Open thread directly (no login required for viewing)
- Copy original post + top 5-10 comments
- Save as: `/raw-content/[topic]/reddit/thread-title.txt`

**GitHub Extraction:**
- Focus on: README, key code files, examples folder
- Clone if full repo needed: `git clone [url]`
- Otherwise copy relevant files via browser

---

### Workflow Decision Point

**At this point, you've gathered all raw content. Now decide your path:**

```
┌─────────────────────────────────────────────────────────┐
│         Do you have a large collection?                  │
│  (Single link with 20+ resources OR old content)         │
└────────────┬────────────────────────────────────────────┘
             │
       ┌─────┴─────┐
       │           │
      YES         NO
       │           │
       ▼           ▼
   ┌───────┐   ┌──────────┐
   │ STEP 3│   │ SKIP TO  │
   │ Filter│   │ STEP 4   │
   │ with  │   │ Notebook │
   │ Claude│   │ LM       │
   │ Skill │   │          │
   └───┬───┘   └────┬─────┘
       │            │
       │            │
       └─────┬──────┘
             ▼
      ┌────────────┐
      │  STEP 4    │
      │ NotebookLM │
      │  Creates   │
      │  Manual    │
      └──────┬─────┘
             ▼
      ┌────────────┐
      │  STEP 5    │
      │  Organize  │
      │  Project   │
      └──────┬─────┘
             ▼
      ┌────────────┐
      │  STEP 6    │
      │  Add to    │
      │  Claude    │
      │  Project   │
      └────────────┘
```

**Path A (Large/Old Collections):**
Step 1 → Step 2 → **Step 3 (Resource Curator)** → Step 4 (NotebookLM) → Step 5-6

**Path B (Small/Recent Collections):**
Step 1 → Step 2 → Step 4 (NotebookLM) → Step 5-6

**Path C (Tiny/Obvious):**
Step 1 → Step 2 → Step 6 (Straight to Claude Project)

---

#### **Step 3: Intelligent Filtering (Curator Skills)**

**Choose based on collection size (see decision matrix above).**

---

### Option A: Two-Phase Resource Curator (100-3000+ resources)

**Use for:** Large collections where metadata filtering is sufficient.

**Phase 1 - Automatic Metadata Filtering:**

1. **Invoke the skill:**

```
"Use two-phase-resource-curator on [URL]

Collection: github.com/awesome-n8n/workflows
(Contains 3000 workflows)"
```

2. **Claude will:**
   - Detect platform (GitHub/Reddit/YouTube)
   - Execute appropriate Python script
   - Filter by metadata (stars, forks, upvotes, etc.)
   - Adjust thresholds based on collection size

3. **Output example:**

```
✅ Phase 1 Complete: Metadata Filtering

Original: 3000 workflows
Filtered: 247 workflows (91.8% reduction)

Filtering criteria (auto-adjusted for large collection):
- Minimum 100 stars (doubled from base 50)
- Updated within 6 months (stricter for large set)
- At least 20 forks
- File size >2KB

Top 10 by metadata score:
1. advanced-api-retry.json (score: 9.2, 342 stars)
2. webhook-security.json (score: 8.9, 298 stars)
...

📥 Download: filtered_github.json (247 resources)

Next: Review list, OR say "do deep analysis" for Phase 2
```

4. **Default behavior:** STOPS here (no Phase 2 unless requested)

5. **If you want Phase 2 (optional):**

```
User: "Do deep analysis on these 247"

Claude executes Phase 2:
- Reads actual code/workflow content
- Quality scoring (1-10)
- Searches for modern alternatives
- Outputs detailed ranking like original curator
```

**When to use Phase 2:**
- Final curation before production use
- Need to verify technical quality, not just popularity
- Want to find modern alternatives to older resources

**When to skip Phase 2:**
- Metadata filtering is good enough (usually is)
- Time/cost sensitive
- Resources already look high quality

---

### Option B: Original Resource Curator (20-100 resources)

**Use for:** Moderate collections needing deep technical analysis.

1. **Invoke:**

```
"Use resource-curator-with-alternatives skill

Analyze collection: [GitHub URL or list]

Context:
- Topic: N8n workflows  
- Focus on production-ready, current resources
Generate ranking file for NotebookLM."
```

2. **Claude will:**
   - List all resources
   - Score technical quality (code, docs, patterns)
   - Apply recency weighting
   - Search for modern alternatives
   - Generate comprehensive ranking

3. **Output example:**

```markdown
# Resource Analysis

**Recommended (≥7/10):** 32 resources
**Deprecated (<7/10):** 18 resources

## Tier 1: Must-Use (9-10/10)
1. advanced-retry.json - 9/10
   
## Tier 4: Deprecated (<5/10)
45. old-scraper.json - 3/10
    - OBSOLETE: Use Perplexity API
    - Effort saved: 85%
```

4. **Behavior:** Does full deep analysis in one pass (no phases)

---

**Comparison:**

| Feature | Two-Phase | Original |
|---------|-----------|----------|
| **Size** | 100-3000+ | 20-100 |
| **Phase 1** | Metadata (automatic) | N/A |
| **Phase 2** | Optional deep analysis | Always deep |
| **Speed** | Fast (metadata only) | Thorough |
| **Stops** | After Phase 1 | No |

---

**After using either curator:**

You now have:
- ✅ Curated list
- ✅ Obsolete patterns identified
- ✅ Modern alternatives  
- ✅ Optimized for NotebookLM
   - Generate a ranked markdown file

4. **Expected Output:**

```markdown
# Resource Analysis: awesome-n8n-workflows

**Recommended for NotebookLM (≥7/10):** 22 resources
**Deprecated (<7/10):** 28 resources

## Tier 1: Must-Use (9-10/10)
1. advanced-api-retry.json - 9/10
   - Why: Production-ready, 3mo old, excellent error handling
   
2. webhook-security.json - 9/10
   - Why: Current best practices, well-documented

## Tier 2: Recommended (7-8/10)
[...]

## Tier 4: Deprecated (<5/10)
45. simple-email-sender.json - 3/10
    - Age: 18 months
    - OBSOLETE: Use Claude API directly (10 lines vs 50-node workflow)
    - Modern alternative: [link]
    - Effort saved: 85%

## Pruning Recommendations
Feed these 22 to NotebookLM: [list]
Skip these 28: [list with reasons]
```

5. **Download the ranking file**

6. **You now have:**
   - ✅ Curated list of valuable resources (top 20-30 instead of 50)
   - ✅ Understanding of what's obsolete
   - ✅ Modern alternatives identified
   - ✅ Optimized input for NotebookLM

**Important: The Filtering Philosophy**

The Resource Curator skill filters BY QUALITY, not by arbitrary numbers:

- ✅ If 40 out of 60 resources are genuinely ≥7/10 → **Keep all 40**
- ✅ If only 10 out of 60 resources are ≥7/10 → **Keep only 10**
- ❌ Don't artificially limit to "top 10" if more are high quality
- ❌ Don't inflate scores to reach a target number

**Example distributions:**
- Well-curated collection: Keep 75-90% (most are already good)
- Mixed collection: Keep 40-60% (moderate filtering)
- Poorly maintained: Keep 20-30% (heavy filtering needed)

The goal is removing NOISE, not hitting a reduction quota.

**When to Skip This Step:**
- You have <15 resources total
- All resources are <3 months old
- You already manually vetted everything

---

#### **Step 4: Manual Creation with NotebookLM**

**Now feed your curated resources to NotebookLM.**

#### **Step 4: Manual Creation with NotebookLM**

**Now feed your curated resources to NotebookLM.**

**What to Upload:**

If you used Resource Curator Skill:
- ✅ The ranking file from Step 3
- ✅ Only the top-ranked resource files (≥7/10)
- ✅ Skip the deprecated ones

If you skipped Resource Curator:
- ✅ All extracted content (transcripts, posts, READMEs)

**How to Use NotebookLM:**

1. **Go to NotebookLM** (notebooklm.google.com)

2. **Create New Notebook** for your topic

3. **Upload Sources:**
   - Drag and drop all resource files
   - If you have the ranking file, upload that too
   - NotebookLM accepts: PDF, TXT, MD, DOCX, web URLs

4. **Generate the Manual:**

```
Prompt to NotebookLM:

"Create a comprehensive project manual following this structure:

# [Topic] - Resource Manual

## How to Use This Manual
[Guide for Claude on where to find resources]

## Top Resources (Ranked)
For each resource:
- Name and file location
- Quality score (if from ranking file)
- Key features
- When to use
- Prerequisites
- Technical level

## Quick Lookup Table
| Use Case | Best Resource | File Location |
|----------|---------------|---------------|
[Table of common use cases → resources]

## Common Patterns Identified
[Extract patterns that appear across multiple resources]

## Known Issues & Solutions
[Problems mentioned and how to solve them]

Use the ranking file to prioritize resources.
Focus on production-ready examples.
Make it scannable and actionable."
```

5. **NotebookLM Will:**
   - Analyze all uploaded sources
   - Use the ranking file to prioritize (if provided)
   - Extract patterns across resources
   - Create structured manual
   - Provide citations to original sources

6. **Download the Manual:**
   - NotebookLM generates the manual
   - Export as markdown or PDF
   - Save as `manual.md`

**Advantages of NotebookLM:**
- ✅ Can process many documents simultaneously
- ✅ Creates citations automatically
- ✅ Synthesizes information across sources
- ✅ Good at creating structured output
- ✅ Understands the ranking context

**What if I Want Claude Instead?**

You can use Claude to create the manual, but NotebookLM is often faster for this task. If you prefer Claude:

```
Upload all resources + ranking file to Claude
Ask Claude to create the manual following the template
Claude will do a deeper technical analysis
Use this approach for highly technical content (complex code, workflows)
```

---

#### **Step 5: Organize Project Folder**

```markdown
# [Project Name] - Resource Manual

**Last Updated:** [Date]
**Curator:** [Your Name]
**Focus:** [e.g., "Production-ready N8n workflows for API automation"]

---

## 📖 How to Use This Manual

This document helps Claude locate relevant examples when you ask questions like:
- "Show me an N8n workflow for Slack notifications"
- "Find a similar pattern to what I'm building"
- "What's the best practice for error handling in N8n?"

**Claude should:**
1. Search this manual first before suggesting generic solutions
2. Reference specific files in `/examples/` or `/workflows/`
3. Cite the original source if recommending an approach

---

## 📁 Folder Structure

```
project-folder/
├── manual.md (this file)
├── raw-content/
│   ├── youtube/
│   ├── reddit/
│   ├── github/
│   └── articles/
├── workflows/ (N8n JSON files)
├── examples/ (code examples)
├── patterns/ (extracted patterns)
└── notebooklm/ (prepared for RAG)
```

---

## 🏆 Top Resources

### Tier 1: Production-Ready (Use These First)

#### 1. [Resource Name]
- **Source:** [URL]
- **Quality Score:** 9/10
- **Type:** [Workflow JSON / Tutorial / Documentation]
- **Location:** `/workflows/resource-name.json`
- **Key Features:**
  - Feature 1
  - Feature 2
- **When to Use:** [Specific use case]
- **Notes:** [Any caveats or requirements]

#### 2. [Resource Name]
...

### Tier 2: High Quality (Requires Adaptation)
...

### Tier 3: Learning Resources (Conceptual)
...

---

## 🔍 Quick Lookup Table

| Use Case | Best Resource | File Location |
|----------|---------------|---------------|
| Email automation | Resource A | `/workflows/email-automation.json` |
| API polling | Resource B | `/examples/api-poller.js` |
| Error handling | Resource C | `/patterns/error-handling.md` |
| ... | ... | ... |

---

## 🎯 Common Patterns Identified

### Pattern 1: [Name]
**Description:** [What it does]
**When to Use:** [Use case]
**Implementation:** 
```
[Code or workflow structure]
```
**Sources:** [Which resources use this]

---

## ⚠️ Known Issues & Pitfalls

- **Issue 1:** [Description] → **Solution:** [How to avoid]
- **Issue 2:** [Description] → **Solution:** [How to avoid]

---

## 🔗 External References

- Official Documentation: [URL]
- Community Forum: [URL]
- GitHub Discussions: [URL]

---

## 📊 Resource Changelog

| Date | Resource | Action | Notes |
|------|----------|--------|-------|
| 2024-02-10 | Workflow X | Added | Found via Perplexity |
| 2024-02-09 | Example Y | Updated | Fixed deprecated API |
```

**Claude Prompt to Generate Manual:**

```
"Based on the analyzed resources, create a project manual following this structure:
[Paste structure above]

Include:
- Clear categorization of resources by quality
- Specific file locations for each resource
- Quick lookup table for common use cases
- Extracted patterns with code examples
- Known issues and solutions

Format as markdown suitable for a project folder."
```

---

#### **Step 5: Organize Project Folder**

**Folder Structure:**

```
my-projects/
├── n8n-workflows/
│   ├── manual.md
│   ├── raw-content/
│   │   ├── youtube/
│   │   ├── reddit/
│   │   └── github/
│   ├── workflows/
│   │   ├── email-automation-advanced.json
│   │   └── api-polling-retry.json
│   ├── examples/
│   │   └── custom-nodes/
│   └── notebooklm/
│       └── n8n-knowledge-base.md
│
├── claude-code-projects/
│   ├── manual.md
│   ├── examples/
│   │   ├── cli-tools/
│   │   ├── mcp-servers/
│   │   └── automation-scripts/
│   └── patterns/
│
├── langchain-rag/
│   ├── manual.md
│   ├── implementations/
│   ├── vector-stores/
│   └── prompts/
│
└── prompt-engineering/
    ├── manual.md
    ├── templates/
    └── chains/
```

**File Naming Convention:**
- Workflows: `[tool]-[purpose]-[variant].json`
- Code: `[language]-[purpose]-[pattern].py/js/ts`
- Transcripts: `[source]-[title]-transcript.txt`
- Manuals: Always `manual.md`

---

#### **Step 5: Organize Project Folder**

**How Claude Projects Work:**
- Create a new project in Claude
- Upload the `manual.md` and key resource files
- Now when you chat in that project, Claude has context

**Example Interaction:**

```
You: "I need an N8n workflow for Slack notifications with retry logic"

Claude: [Checks manual.md in project]
"I found a similar workflow in our collection:

From manual.md → /workflows/slack-notification-retry.json

This workflow includes:
- Exponential backoff retry (3 attempts)
- Error logging to Airtable
- Success/failure Slack messages

Would you like me to:
1. Show you the complete workflow
2. Adapt it for your specific use case
3. Explain the retry mechanism in detail?"
```

**Project Custom Instructions:**

Add to project instructions:
```
"When I ask about [N8n workflows/Claude Code/LLM apps], always:
1. Check manual.md first for similar examples
2. Reference specific files in the project folder
3. Suggest adaptations rather than building from scratch
4. Cite the original source if using a pattern"
```

---

#### **Step 6: Add to Claude Projects**

**How Claude Projects Work:**
- Create a new project in Claude
- Upload the `manual.md` and key resource files
- Add the ranking file (if you used Resource Curator skill)
- Now when you chat in that project, Claude has context

**Example Interaction:**

```
You: "I need an N8n workflow for Slack notifications with retry logic"

Claude: [Checks manual.md in project]
"I found a similar workflow in our collection:

From manual.md → /workflows/slack-notification-retry.json
Ranked 9/10 in our analysis

This workflow includes:
- Exponential backoff retry (3 attempts)
- Error logging to Airtable
- Success/failure Slack messages

Would you like me to:
1. Show you the complete workflow
2. Adapt it for your specific use case
3. Explain the retry mechanism in detail?"
```

**Project Custom Instructions:**

Add to project instructions:
```
"When I ask about [N8n workflows/Claude Code/LLM apps], always:
1. Check manual.md first for similar examples
2. Reference the ranking file to understand quality context
3. Suggest adaptations of high-ranked resources rather than building from scratch
4. Cite the original source if using a pattern
5. Warn me if I'm about to use a deprecated resource (rank <5)"
```

**What to Upload:**
- ✅ manual.md (from NotebookLM)
- ✅ ranking file (if used Resource Curator skill)
- ✅ Top 5-10 actual resource files
- ✅ Pattern documentation (if extracted)

---

#### **Step 7: NotebookLM RAG (Optional Enhancement)**

**This step is optional but powerful for learning and exploration.**

#### **Step 7: NotebookLM RAG (Optional Enhancement)**

**This step is optional but powerful for learning and exploration.**

**Why Keep NotebookLM Active?**
- You've already used it to create the manual
- But you can also keep the notebook for ongoing queries
- Acts as a conversational RAG over your resources
- Good for exploration and learning

**Two Usage Patterns:**

**Pattern A: One-Time Manual Creation (Simpler)**
```
Use NotebookLM → Generate manual → Close notebook
→ Use Claude Project with the manual going forward
```

**Pattern B: Keep Both (More Powerful)**
```
NotebookLM: Exploratory learning, "explain concept X across all resources"
Claude Project: Implementation, "adapt workflow Y for my use case"
```

**When to Keep NotebookLM Active:**
- ✅ You're still learning the topic
- ✅ You want to explore connections between resources
- ✅ You need study guides or summaries
- ✅ Resources will keep growing (add new sources over time)

**Example NotebookLM Queries:**
- "Explain the error handling pattern used across these N8n workflows"
- "Compare the RAG implementations - which is best for my use case?"
- "Generate a study guide for building multi-agent systems"
- "What do all the top-ranked resources have in common?"

**When to Just Use Claude Project:**
- You have your manual
- You want to build/implement
- You're done with discovery phase
- You don't need the RAG exploration features

**Recommendation:** 
Start with Pattern B, transition to Pattern A once you're comfortable with the topic.

---

## 🎯 Complete Workflow Examples

### Example 1: Large Collection (Path A - Use Two-Phase Curator)

**Scenario:** Found `github.com/awesome-n8n-workflows` with 50+ workflows (unknown exact count)

**Your Process:**

```
1. DISCOVERY (Perplexity)
   → Search: "best n8n workflows github 2025"
   → Find: awesome-n8n-workflows repo

2. EXTRACTION
   → Note the URL (don't need to clone yet)

3. DECISION POINT
   → Unknown count, looks large
   → DECISION: Use Two-Phase Curator (it will auto-detect)

3. TWO-PHASE CURATOR
   Prompt Claude:
   "Use two-phase-curator on github.com/awesome-n8n-workflows"
   
   → Claude counts: 50 workflows detected
   → Decision: >30 resources → Run Phase 1
   → Executes: filter_github.py
   → Analyzes all 50, calculates N8n-specific percentiles
   → Filters 50 → 15 based on statistical ranking
   
   Results:
   - 15 workflows ranked ≥7/10
   - 35 workflows ranked <7/10 (filtered out)
   - Statistics shown: median 8 stars, p75 22 stars

4. REVIEW RESULTS
   → Download filtered list (15 workflows)
   → Optionally say "do deep analysis" for Phase 2

5. NOTEBOOKLM (if satisfied with 15)
   → Upload ranking file + 15 workflow files
   → Prompt: "Create manual.md with these top workflows"
   → Download generated manual

6. PROJECT FOLDER
   → Save manual.md
   → Save ranking file
   → Save top 15 workflow files

7. CLAUDE PROJECT
   → Create "N8n Workflows" project
   → Upload manual.md + ranking file
   → Add custom instructions

Result: 15 curated workflows instead of 50, with clear quality context
Note: Two-Phase Curator auto-detected size and chose right path
```

---

### Example 2: Small Collection (Path B - Two-Phase Direct to Phase 2)

**Scenario:** Found 5 blog posts about Claude Code from last month

**Your Process:**

```
1. DISCOVERY (Perplexity)
   → Search: "claude code best practices 2026"
   → Find: 5 blog posts, all <1 month old

2. EXTRACTION
   → Copy article text from each
   → Save as .txt files

3. DECISION POINT
   → Only 5 resources
   → DECISION: Use Two-Phase Curator (will auto-route)

3. TWO-PHASE CURATOR
   Prompt Claude:
   "Use two-phase-curator to analyze these 5 articles: [URLs]"
   
   → Claude counts: 5 articles detected
   → Decision: ≤30 resources → Run Phase 2 directly (skip Phase 1)
   → Reads all 5 articles
   → Quality scores each
   → Checks for modern alternatives
   
   Results:
   - All 5 ranked 7-10 (high quality, recent)
   - No deprecated patterns (all current)
   - Detailed analysis provided immediately

4. PROJECT FOLDER
   → Save analysis report
   → Save articles

5. CLAUDE PROJECT
   → Add to "Claude Code" project
   → No NotebookLM needed (only 5 items)

Result: Fast, direct quality analysis. No unnecessary filtering.
Note: Two-Phase Curator detected small count and went straight to deep analysis
```

---

### Example 3: Single Resource Quality Check (Two-Phase Direct)

**Scenario:** Found one repo with 1 complex RAG implementation to evaluate

**Your Process:**

```
1. DISCOVERY (Perplexity)
   → Find: github.com/user/advanced-rag-implementation

2. EXTRACTION
   → Note URL (single repo)

3. DECISION POINT
   → Single resource
   → DECISION: Use Two-Phase Curator

3. TWO-PHASE CURATOR
   Prompt Claude:
   "Use two-phase-curator to check quality of:
   github.com/user/advanced-rag-implementation"
   
   → Claude detects: 1 repository
   → Decision: ≤30 → Run Phase 2 directly
   → Reads implementation code
   → Quality analysis
   → Checks for modern alternatives
   
   Results:
   - Quality: 8/10 (solid implementation)
   - Age: 8 months (still current)
   - Alternative check: No simpler approach found
   - Recommendation: Use with minor updates

4. DECISION
   → Implementation is good, use it
   → Note minor updates needed in manual

5-6. PROJECT SETUP
   → Add to Claude Project with quality notes

Result: Quick quality verification of single resource
Note: Perfect for checking if ONE thing is worth using
```

---

### Example 4: Quick Reference (Path C - Minimal Process)

**Scenario:** 3 YouTube tutorials about a specific N8n pattern

**Your Process:**

```
1. DISCOVERY
   → Already know the 3 videos

2. EXTRACTION
   → Use ChatGPT: extract transcripts

3. DECISION POINT
   → Only 3 resources ✗
   → DECISION: Skip everything, direct to Claude

3. CLAUDE PROJECT (direct)
   → Create simple note with 3 transcripts
   → No need for NotebookLM or ranking
   → Just reference as needed

Result: Minimal overhead for small set
```

---

## 📊 LLM Model Comparison Matrix

### Complete Feature & Use Case Comparison

| Feature / Task | Perplexity Pro | Claude Opus 4.5 | GPT-4o | Gemini Advanced | Gemini Pro | Grok 2 |
|----------------|----------------|-----------------|---------|-----------------|------------|--------|
| **Web Search** | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐ Via tool | ⭐⭐⭐ Via tool | ⭐⭐⭐⭐ Native | ⭐⭐⭐⭐ Native | ⭐⭐⭐ Limited |
| **X/Twitter Access** | ⭐⭐⭐⭐ Good | ⭐ Poor | ⭐ Poor | ⭐⭐ Limited | ⭐⭐ Limited | ⭐⭐⭐⭐ Good (via X API) |
| **YouTube Transcripts** | ⭐⭐ Metadata only | ❌ None | ⭐⭐⭐⭐ Full | ⭐⭐⭐⭐⭐ Full + Video | ⭐⭐⭐⭐ Full | ⭐⭐ Metadata only |
| **Code Understanding** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Great | ⭐⭐⭐ Good | ⭐⭐⭐ Good | ⭐⭐⭐ Good |
| **Technical Analysis** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐ Great | ⭐⭐⭐⭐ Great | ⭐⭐⭐ Good | ⭐⭐⭐ Good |
| **Long Context** | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ 200K tokens | ⭐⭐⭐⭐ 128K tokens | ⭐⭐⭐⭐⭐ 2M tokens | ⭐⭐⭐⭐ 1M tokens | ⭐⭐⭐ ~32K tokens |
| **Structured Output** | ⭐⭐ Basic | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Great | ⭐⭐⭐⭐ Great | ⭐⭐⭐ Good |
| **Citation Quality** | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Okay | ⭐⭐⭐ Okay | ⭐⭐⭐ Okay | ⭐⭐ Poor |
| **API Availability** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **Cost (per 1M tokens)** | $20/mo unlimited | $15 input / $75 output | $5 input / $15 output | $20/mo unlimited | Free tier available | $16/mo unlimited |

### Detailed Strengths & Limitations

#### **Perplexity Pro**

**Best For:**
- ✅ Initial discovery across multiple platforms
- ✅ Finding recent content (2024-2025)
- ✅ Accessing X/Twitter posts
- ✅ Quick research with citations
- ✅ Broad topic exploration

**Limitations:**
- ❌ No full YouTube transcripts
- ❌ Limited deep code analysis
- ❌ Cannot iterate deeply on complex tasks
- ❌ Shorter context window
- ⚠️ Search quality varies by topic

**Use When:**
- Starting a new research topic
- Need to find URLs quickly
- Accessing hard-to-reach platforms (X)
- Want automatic citations

**API:** Yes (pplx-api) - $20/month for 600 queries

---

#### **Claude Opus 4.5**

**Best For:**
- ✅ Deep technical analysis
- ✅ Understanding complex code
- ✅ N8n workflow JSON analysis
- ✅ Creating structured manuals
- ✅ Comparing multiple implementations
- ✅ Long-form documentation
- ✅ Extracting patterns from messy data

**Limitations:**
- ❌ Cannot access X/Twitter directly
- ❌ No native YouTube transcript extraction
- ❌ Web search requires tool (less seamless than Perplexity)
- 💰 More expensive for API usage

**Use When:**
- Analyzing code quality
- Creating project manuals
- Comparing technical approaches
- Extracting insights from multiple sources
- Need precise, structured output
- Working with large codebases

**API:** Yes - $15/1M input, $75/1M output tokens

---

#### **GPT-4o**

**Best For:**
- ✅ YouTube transcript extraction
- ✅ Creative search queries
- ✅ Multimodal analysis (images + text)
- ✅ Good balance of cost and capability
- ✅ Fast response times

**Limitations:**
- ⚠️ Less precise for technical code analysis vs Claude
- ⚠️ Sometimes hallucinates sources
- ❌ Cannot access X/Twitter well
- ⚠️ Citation quality lower than Perplexity

**Use When:**
- Extracting YouTube transcripts
- Need fast responses
- Cost is a concern
- Multimodal tasks (analyzing screenshots)
- Creative brainstorming

**API:** Yes - $5/1M input, $15/1M output tokens

---

#### **Gemini Advanced (Gemini 1.5 Pro)**

**Best For:**
- ✅ YouTube video + transcript analysis
- ✅ Extremely long context (2M tokens)
- ✅ Multimodal tasks
- ✅ Good for video understanding
- ✅ Free tier available

**Limitations:**
- ⚠️ Less consistent for code analysis vs Claude
- ⚠️ Sometimes verbose
- ❌ Limited X/Twitter access
- ⚠️ Can be slower than GPT-4o

**Use When:**
- Working with very long documents
- Need to analyze video content
- Want free tier for experimentation
- Multimodal projects

**API:** Yes - Free tier with rate limits, paid via Google Cloud

---

#### **Gemini Pro**

**Best For:**
- ✅ Similar to Advanced but cheaper
- ✅ Good for routine tasks
- ✅ Free tier sufficient for many uses

**Limitations:**
- Same as Gemini Advanced but with:
- ⚠️ Lower quality outputs
- ⚠️ Fewer features

**Use When:**
- Budget is primary concern
- Tasks don't require highest quality
- Experimentation phase

**API:** Yes - Free tier available

---

#### **Grok 2**

**Best For:**
- ✅ X/Twitter integration (native access)
- ✅ Real-time social media monitoring
- ✅ Recent developments tracking

**Limitations:**
- ⚠️ Less proven for technical analysis
- ❌ Limited API access
- ⚠️ Smaller developer community
- ❌ No YouTube transcript extraction
- ⚠️ Documentation less comprehensive

**Use When:**
- Heavy focus on X/Twitter content
- Real-time social media trends
- Access to latest X discussions

**API:** Limited beta access

---

### Recommended Tool Chain by Task

| Task | Primary Tool | Secondary Tool | Verification/Filter Tool |
|------|--------------|----------------|--------------------------|
| **Find Resources** | Perplexity Pro | Grok 2 (for X) | Claude Resource Curator |
| **Filter Large Collections** | Claude Resource Curator Skill | - | Manual review of top picks |
| **Extract YouTube** | ChatGPT Plus / Gemini | - | Claude (analyze content) |
| **Analyze Code** | Claude Opus | GPT-4o | Manual testing |
| **Create Manuals** | NotebookLM | Claude (if very technical) | Human review |
| **Rank Resources** | Claude Resource Curator | - | NotebookLM (synthesis) |
| **X/Twitter Search** | Perplexity / Grok | Manual screenshots | Claude (analyze) |
| **Long Documents** | Gemini Advanced | Claude | - |
| **Cost-Sensitive** | Gemini Pro / GPT-4o | Claude (final check) | - |
| **Quick Lookups** | Perplexity | - | - |

---

### When to Use What (Decision Table)

| Scenario | Tool Sequence | Why |
|----------|---------------|-----|
| **Single link, 50+ resources** | Perplexity → Extract → **Resource Curator** → NotebookLM | Curator filters noise |
| **20+ resources, mixed ages** | Extract → **Resource Curator** → NotebookLM | Identify obsolete patterns |
| **5-15 resources, all recent** | Extract → NotebookLM | Skip curator, volume is manageable |
| **<5 resources** | Extract → Claude Project | No intermediaries needed |
| **Highly technical code** | Extract → **Claude analysis** → NotebookLM | Claude better for code quality |
| **Learning/exploration** | Extract → NotebookLM (keep active) | Use RAG for ongoing queries |
| **Implementation** | NotebookLM manual → Claude Project | Claude for building |

---

## 🤖 Automated Workflow (Future API Implementation)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRIGGER (Scheduled/Manual)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: DISCOVERY                                               │
│  Tool: Perplexity API                                            │
│  Action: Search for resources based on topics list               │
│  Output: List of URLs with metadata                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: PLATFORM ROUTING                                        │
│  Tool: Custom logic                                              │
│  Action: Route URLs by platform (YouTube/Reddit/GitHub/X)        │
│  Output: Categorized URL lists                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┬─────────────┐
                │             │             │             │
                ▼             ▼             ▼             ▼
    ┌──────────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────┐
    │   YouTube    │  │   Reddit    │  │  GitHub  │  │    X     │
    │   Transcript │  │   PRAW API  │  │  GitHub  │  │  Apify   │
    │   API        │  │             │  │  API     │  │  /Scraper│
    └──────────────┘  └─────────────┘  └──────────┘  └──────────┘
                │             │             │             │
                └─────────────┼─────────────┴─────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: CONTENT STORAGE                                         │
│  Tool: Database (Airtable/Supabase/PostgreSQL)                   │
│  Action: Store raw content with metadata                         │
│  Output: Structured database of sources                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: ANALYSIS                                                │
│  Tool: Claude API (Opus 4.5)                                     │
│  Action: Analyze quality, extract patterns, rank resources       │
│  Output: Scored and categorized resources                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: MANUAL GENERATION                                       │
│  Tool: Claude API                                                │
│  Action: Generate manual.md from analyzed resources              │
│  Output: Project manual file                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: FILE MANAGEMENT                                         │
│  Tool: GitHub API / Google Drive API                             │
│  Action: Commit manual to project repo or save to cloud          │
│  Output: Updated project folder                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: NOTIFICATION                                            │
│  Tool: Slack/Email/Discord webhook                               │
│  Action: Notify about new resources added                        │
│  Output: Summary report                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### Implementation Options

#### **Option A: N8n Workflow (Recommended for Start)**

**Why N8n?**
- Visual workflow builder
- Pre-built nodes for most APIs
- Easy to iterate and debug
- Can schedule or trigger manually
- Free self-hosted option

**Workflow Structure:**

```json
{
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "weeks", "value": 1}]
        }
      }
    },
    {
      "name": "Load Topics List",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "json": {
            "topics": [
              "n8n workflows API automation",
              "claude code mcp servers",
              "langchain rag implementation"
            ]
          }
        }
      }
    },
    {
      "name": "Search Perplexity",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.perplexity.ai/chat/completions",
        "authentication": "headerAuth",
        "options": {
          "bodyContentType": "json"
        },
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({
          model: 'sonar',
          messages: [{
            role: 'user',
            content: 'Find top 10 resources about: ' + $json.topic
          }]
        }) }}"
      }
    },
    {
      "name": "Extract URLs",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "javascript",
        "jsCode": "// Extract URLs from Perplexity response\nconst response = items[0].json;\nconst urls = [];\n// Logic to parse and extract URLs\nreturn urls.map(url => ({json: {url}}));"
      }
    },
    {
      "name": "Route by Platform",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": [
          {"value": "youtube.com", "output": 0},
          {"value": "reddit.com", "output": 1},
          {"value": "github.com", "output": 2},
          {"value": "twitter.com", "output": 3}
        ]
      }
    },
    {
      "name": "YouTube - Get Transcript",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.youtube-transcript.com/v1/transcript",
        "method": "GET"
      }
    },
    {
      "name": "Reddit - Fetch via API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://www.reddit.com/api/info.json?id={{$json.reddit_id}}",
        "method": "GET"
      }
    },
    {
      "name": "GitHub - Fetch README",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.github.com/repos/{{$json.owner}}/{{$json.repo}}/readme",
        "method": "GET",
        "headers": {
          "Accept": "application/vnd.github.v3.raw"
        }
      }
    },
    {
      "name": "X - Apify Scraper",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs",
        "method": "POST"
      }
    },
    {
      "name": "Store in Airtable",
      "type": "n8n-nodes-base.airtable",
      "parameters": {
        "operation": "create",
        "table": "Resources",
        "fields": {
          "url": "={{$json.url}}",
          "content": "={{$json.content}}",
          "platform": "={{$json.platform}}",
          "date_added": "={{$now}}"
        }
      }
    },
    {
      "name": "Claude - Analyze Quality",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "authentication": "headerAuth",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({
          model: 'claude-opus-4-5-20251101',
          max_tokens: 4096,
          messages: [{
            role: 'user',
            content: 'Analyze this resource and rate quality 1-10:\\n' + $json.content
          }]
        }) }}"
      }
    },
    {
      "name": "Claude - Generate Manual",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({
          model: 'claude-opus-4-5-20251101',
          max_tokens: 8000,
          messages: [{
            role: 'user',
            content: 'Generate a project manual for these resources:\\n' + JSON.stringify($json.resources)
          }]
        }) }}"
      }
    },
    {
      "name": "Save to GitHub",
      "type": "n8n-nodes-base.github",
      "parameters": {
        "operation": "createFile",
        "owner": "your-username",
        "repository": "your-repo",
        "filePath": "projects/{{$json.topic}}/manual.md",
        "content": "={{$json.manual}}"
      }
    },
    {
      "name": "Notify via Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#automation-updates",
        "text": "New resources added for {{$json.topic}}"
      }
    }
  ]
}
```

**Cost Estimate for N8n Workflow:**
- N8n: Free (self-hosted) or $20/month (cloud)
- APIs: See pricing section below
- Total: ~$50-100/month depending on volume

---

#### **Option B: Python Script with Make/Zapier**

**Why Python + No-Code?**
- More flexibility for complex logic
- Use Make/Zapier for scheduling and notifications
- Easy to customize scraping logic
- Good for learning automation

**Architecture:**

```
Make/Zapier (Scheduler)
  → Webhook → Python Script (hosted on Railway/Render/Heroku)
  → Script does: Discovery → Extraction → Claude Analysis
  → Returns results to Make/Zapier
  → Make/Zapier: Save to Google Drive + Notify
```

**Python Script Outline:**

```python
# main.py
import os
import requests
from anthropic import Anthropic
from youtube_transcript_api import YouTubeTranscriptApi
import praw  # Reddit API
from github import Github
import json

# Configuration
PERPLEXITY_API_KEY = os.environ['PERPLEXITY_KEY']
ANTHROPIC_API_KEY = os.environ['ANTHROPIC_KEY']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

class ResourceDiscovery:
    def __init__(self):
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
        
    def search_perplexity(self, query):
        """Search using Perplexity API"""
        response = requests.post(
            'https://api.perplexity.ai/chat/completions',
            headers={'Authorization': f'Bearer {PERPLEXITY_API_KEY}'},
            json={
                'model': 'sonar',
                'messages': [{'role': 'user', 'content': query}]
            }
        )
        return response.json()
    
    def extract_youtube_transcript(self, video_id):
        """Get YouTube transcript"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([t['text'] for t in transcript])
        except:
            return None
    
    def fetch_reddit_content(self, url):
        """Fetch Reddit post via API"""
        reddit = praw.Reddit(
            client_id=os.environ['REDDIT_CLIENT_ID'],
            client_secret=os.environ['REDDIT_SECRET'],
            user_agent='ResourceDiscovery/1.0'
        )
        submission = reddit.submission(url=url)
        return {
            'title': submission.title,
            'text': submission.selftext,
            'score': submission.score,
            'comments': [c.body for c in submission.comments.list()[:10]]
        }
    
    def fetch_github_readme(self, repo_url):
        """Fetch GitHub README"""
        g = Github(GITHUB_TOKEN)
        # Parse owner/repo from URL
        repo = g.get_repo(repo_path)
        readme = repo.get_readme()
        return readme.decoded_content.decode('utf-8')
    
    def analyze_with_claude(self, content):
        """Analyze content quality with Claude"""
        message = self.anthropic.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Analyze this technical resource and provide:
                1. Quality score (1-10)
                2. Is it production-ready? (yes/no/partial)
                3. Key strengths
                4. Potential issues
                5. Best use cases
                
                Content:
                {content}"""
            }]
        )
        return message.content[0].text
    
    def generate_manual(self, analyzed_resources):
        """Generate project manual"""
        message = self.anthropic.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": f"""Create a project manual following this structure:
                [Include manual template]
                
                Based on these analyzed resources:
                {json.dumps(analyzed_resources, indent=2)}"""
            }]
        )
        return message.content[0].text

def main():
    """Main workflow"""
    discovery = ResourceDiscovery()
    
    # Topics to search
    topics = [
        "n8n workflows API automation",
        "claude code projects github",
        "langchain rag implementation"
    ]
    
    all_resources = []
    
    for topic in topics:
        # Step 1: Search
        search_results = discovery.search_perplexity(f"best {topic} 2024-2025")
        
        # Step 2: Extract URLs from results
        urls = extract_urls(search_results)  # Helper function
        
        # Step 3: Fetch content by platform
        for url in urls:
            if 'youtube.com' in url:
                content = discovery.extract_youtube_transcript(extract_video_id(url))
            elif 'reddit.com' in url:
                content = discovery.fetch_reddit_content(url)
            elif 'github.com' in url:
                content = discovery.fetch_github_readme(url)
            # Add more platforms as needed
            
            # Step 4: Analyze with Claude
            analysis = discovery.analyze_with_claude(str(content))
            
            all_resources.append({
                'url': url,
                'content': content,
                'analysis': analysis,
                'topic': topic
            })
    
    # Step 5: Generate manual
    manual = discovery.generate_manual(all_resources)
    
    # Step 6: Save to file
    with open('manual.md', 'w') as f:
        f.write(manual)
    
    return {'status': 'success', 'resources_found': len(all_resources)}

if __name__ == '__main__':
    main()
```

**Deployment:**
```bash
# requirements.txt
anthropic>=0.18.0
requests>=2.31.0
youtube-transcript-api>=0.6.1
praw>=7.7.1
PyGithub>=2.1.1

# Deploy to Railway/Render
railway up
# Or use Docker
docker build -t resource-discovery .
docker run resource-discovery
```

**Integration with Make/Zapier:**

**Make.com Scenario:**
1. **Schedule** (weekly trigger)
2. **Webhook** → Call Python script
3. **Wait** for response
4. **Google Drive** → Save manual.md
5. **Slack** → Send notification

---

#### **Option C: Full Custom App (Advanced)**

**Tech Stack:**
- **Backend:** Node.js/Express or Python/FastAPI
- **Database:** Supabase (PostgreSQL) or Airtable
- **Frontend:** React/Next.js (optional dashboard)
- **Queue:** BullMQ or Celery for background jobs
- **Storage:** S3 or Google Cloud Storage
- **Hosting:** Vercel/Railway/Render

**Features:**
- Web interface to add topics
- Dashboard showing discovered resources
- Manual approval before adding to project
- Version control for manuals
- API endpoints for integrations

**Architecture:**

```
┌─────────────────┐
│   Frontend      │  React Dashboard
│   (Next.js)     │  - Add topics
└────────┬────────┘  - Review resources
         │           - Approve/reject
         ▼
┌─────────────────┐
│   API Layer     │  Express/FastAPI
│   (Backend)     │  - Handle requests
└────────┬────────┘  - Authentication
         │           - Job scheduling
         ▼
┌─────────────────┐
│   Job Queue     │  BullMQ/Celery
│   (Redis)       │  - Discovery jobs
└────────┬────────┘  - Analysis jobs
         │           - Manual generation
         ▼
┌─────────────────┐
│   Database      │  Supabase/PostgreSQL
│   (Supabase)    │  - Topics
└─────────────────┘  - Resources
                     - Manuals
                     - Users
```

This is overkill for manual use, but provides full control and scalability.

---

### Automation Workflow Logic (Pseudo-code)

```python
# Complete automated workflow logic

def automated_resource_discovery(topics_list):
    """
    Main automation function
    """
    results = []
    
    for topic in topics_list:
        # PHASE 1: DISCOVERY
        print(f"Discovering resources for: {topic}")
        
        # Search with Perplexity
        perplexity_results = search_perplexity(topic)
        urls = extract_urls(perplexity_results)
        
        # Optionally: Search with Grok for X content
        if needs_x_content(topic):
            grok_results = search_grok(topic)
            urls.extend(extract_urls(grok_results))
        
        # PHASE 2: PLATFORM ROUTING
        categorized_urls = categorize_by_platform(urls)
        
        # PHASE 3: CONTENT EXTRACTION
        extracted_content = []
        
        for platform, platform_urls in categorized_urls.items():
            if platform == 'youtube':
                for url in platform_urls:
                    transcript = get_youtube_transcript(url)
                    if transcript:
                        extracted_content.append({
                            'url': url,
                            'content': transcript,
                            'platform': 'youtube'
                        })
            
            elif platform == 'reddit':
                for url in platform_urls:
                    post_data = fetch_reddit_post(url)
                    extracted_content.append({
                        'url': url,
                        'content': post_data,
                        'platform': 'reddit'
                    })
            
            elif platform == 'github':
                for url in platform_urls:
                    readme = fetch_github_readme(url)
                    extracted_content.append({
                        'url': url,
                        'content': readme,
                        'platform': 'github'
                    })
            
            elif platform == 'x':
                # Use Apify or manual scraper
                for url in platform_urls:
                    tweet_data = scrape_tweet(url)
                    extracted_content.append({
                        'url': url,
                        'content': tweet_data,
                        'platform': 'x'
                    })
        
        # PHASE 4: QUALITY ANALYSIS
        print(f"Analyzing {len(extracted_content)} resources")
        
        analyzed_resources = []
        for resource in extracted_content:
            # Use Claude for analysis
            analysis = analyze_with_claude(
                content=resource['content'],
                prompt=f"""Analyze this {resource['platform']} resource about {topic}.
                
                Provide:
                1. Quality Score (1-10)
                2. Production-Ready Status (yes/no/needs-work)
                3. Key Strengths (bullet points)
                4. Potential Issues (bullet points)
                5. Best Use Cases
                6. Technical Level (beginner/intermediate/advanced)
                
                Content:
                {resource['content'][:4000]}  # Truncate if needed
                """
            )
            
            analyzed_resources.append({
                **resource,
                'analysis': analysis,
                'topic': topic
            })
        
        # PHASE 5: FILTERING
        # Only keep resources with quality score >= 7
        high_quality = filter_by_quality(analyzed_resources, min_score=7)
        
        # PHASE 6: MANUAL GENERATION
        print(f"Generating manual for {topic}")
        
        manual = generate_manual_with_claude(
            topic=topic,
            resources=high_quality,
            template=MANUAL_TEMPLATE
        )
        
        # PHASE 7: FILE MANAGEMENT
        save_to_project_folder(
            topic=topic,
            manual=manual,
            resources=high_quality
        )
        
        # PHASE 8: VERSION CONTROL
        commit_to_github(
            topic=topic,
            files=[f'projects/{topic}/manual.md']
        )
        
        # PHASE 9: NOTIFICATION
        send_notification(
            channel='slack',
            message=f"✅ Discovered {len(high_quality)} resources for {topic}"
        )
        
        results.append({
            'topic': topic,
            'resources_found': len(analyzed_resources),
            'high_quality_count': len(high_quality),
            'manual_generated': True
        })
    
    return results

# Helper functions

def filter_by_quality(resources, min_score):
    """Filter resources by quality score"""
    filtered = []
    for resource in resources:
        # Parse score from analysis
        score = extract_quality_score(resource['analysis'])
        if score >= min_score:
            filtered.append(resource)
    return filtered

def extract_quality_score(analysis_text):
    """Extract numeric score from Claude's analysis"""
    # Parse "Quality Score: 8/10" or similar
    import re
    match = re.search(r'Quality Score:?\s*(\d+)', analysis_text)
    if match:
        return int(match.group(1))
    return 0

def save_to_project_folder(topic, manual, resources):
    """Save manual and resources to organized folder"""
    import os
    
    # Create folder structure
    base_path = f"projects/{topic.replace(' ', '-')}"
    os.makedirs(f"{base_path}/raw-content", exist_ok=True)
    os.makedirs(f"{base_path}/workflows", exist_ok=True)
    
    # Save manual
    with open(f"{base_path}/manual.md", 'w') as f:
        f.write(manual)
    
    # Save individual resources
    for i, resource in enumerate(resources):
        filename = f"{base_path}/raw-content/{resource['platform']}-{i}.txt"
        with open(filename, 'w') as f:
            f.write(resource['content'])

def generate_manual_with_claude(topic, resources, template):
    """Generate manual using Claude"""
    prompt = f"""Create a comprehensive project manual for: {topic}

Resources to include:
{json.dumps(resources, indent=2)}

Follow this template:
{template}

Requirements:
- Rank resources by quality
- Create quick lookup table
- Extract common patterns
- Note known issues
- Provide file locations
"""
    
    return call_claude_api(prompt)
```

---

## 🗺️ Platform-Specific Strategies

### YouTube

**Manual Extraction:**
1. Use ChatGPT Plus: "Extract transcript from [URL]"
2. Or Gemini Advanced: Same prompt
3. Copy full transcript

**Automated Extraction:**

**Option 1: youtube-transcript-api (Python)**
```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([t['text'] for t in transcript_list])
        return full_text
    except:
        return None

# Usage
video_id = 'dQw4w9WgXcQ'  # From URL: youtube.com/watch?v=dQw4w9WgXcQ
transcript = get_transcript(video_id)
```

**Option 2: YouTube Transcript API (Web Service)**
```bash
# Via API call
curl -X GET "https://api.youtube-transcript.com/v1/transcript?video_id=dQw4w9WgXcQ"
```

**Option 3: N8n YouTube Transcript Node**
- Install community node: `n8n-nodes-youtube-transcript`
- Configure with video URL
- Returns formatted transcript

**Limitations:**
- Only works if video has captions
- Auto-generated captions may have errors
- Some videos disable transcripts

---

### Reddit

**Manual Extraction:**
- Direct copy-paste (no login needed for viewing)
- Use old.reddit.com for cleaner interface
- Copy post text + top comments

**Automated Extraction:**

**Option 1: PRAW (Python Reddit API Wrapper)**
```python
import praw

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='ResourceDiscovery/1.0'
)

# Get post by URL
submission = reddit.submission(url='https://reddit.com/r/n8n/comments/...')

data = {
    'title': submission.title,
    'text': submission.selftext,
    'score': submission.score,
    'num_comments': submission.num_comments,
    'upvote_ratio': submission.upvote_ratio,
    'comments': []
}

# Get top comments
submission.comments.replace_more(limit=0)
for comment in submission.comments.list()[:20]:
    data['comments'].append({
        'author': str(comment.author),
        'body': comment.body,
        'score': comment.score
    })
```

**Option 2: Reddit JSON API (No Auth)**
```bash
# Just add .json to any Reddit URL
curl "https://www.reddit.com/r/n8n/comments/abc123/my_workflow.json"
```

**Option 3: N8n Reddit Node**
- Use HTTP Request node
- URL: `https://www.reddit.com/r/SUBREDDIT/top.json?limit=25`
- Parse JSON response

**Best Subreddits for Your Topics:**
- N8n: r/n8n, r/nocode, r/automation
- Claude Code: r/ClaudeAI, r/LLMDevs
- LangChain: r/LangChain, r/LocalLLaMA
- General: r/programming, r/MachineLearning, r/learnprogramming

---

### X/Twitter

**Manual Extraction:**
- Screenshot or copy visible text
- **Hard Reality:** Most challenging platform
- Consider deprioritizing unless critical

**Automated Extraction:**

**Option 1: Apify Twitter Scraper**
```javascript
// Via Apify API
const response = await fetch('https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer YOUR_APIFY_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        startUrls: [{url: 'https://twitter.com/user/status/123'}],
        maxTweets: 100
    })
});
```

**Option 2: Bright Data Scraper**
- More reliable than Apify
- Higher cost but better quality
- Handles rate limits better

**Option 3: Grok API (If/When Available)**
- Native X access
- Limited beta currently

**Workaround:**
- Use Perplexity's search (often captures X content)
- Focus on other platforms where extraction is easier

---

### GitHub

**Manual Extraction:**
- Browse repos in browser
- Copy README and key files
- Note stars/forks as quality indicators

**Automated Extraction:**

**Option 1: GitHub API (Official)**
```python
from github import Github

g = Github('YOUR_GITHUB_TOKEN')

# Get repo
repo = g.get_repo('owner/repo-name')

# Get README
readme = repo.get_readme()
readme_content = readme.decoded_content.decode('utf-8')

# Get files
contents = repo.get_contents('path/to/folder')
for content in contents:
    if content.type == 'file':
        file_content = content.decoded_content.decode('utf-8')

# Get metadata
metadata = {
    'stars': repo.stargazers_count,
    'forks': repo.forks_count,
    'description': repo.description,
    'topics': repo.get_topics(),
    'language': repo.language,
    'last_updated': repo.updated_at
}
```

**Option 2: N8n GitHub Node**
- Built-in node with authentication
- Can read files, commits, issues
- Webhook support for monitoring

**Option 3: GitHub Search API**
```bash
# Search for repos
curl -H "Authorization: token YOUR_TOKEN" \
  "https://api.github.com/search/repositories?q=n8n+workflow+stars:>100"
```

**Quality Indicators:**
- Stars > 100 (popular)
- Forks > 20 (actively used)
- Recent commits (maintained)
- Good README (documented)
- Examples folder (practical)

---

### Dev.to & Medium

**Manual Extraction:**
- Direct copy-paste
- Reader mode in browser for clean text

**Automated Extraction:**

**Dev.to API:**
```bash
# Public API, no auth needed
curl "https://dev.to/api/articles?tag=n8n&top=7"
```

**Medium:** 
- No official API
- Use web_fetch or scraping
- Many articles behind paywall

---

## 📂 Project Folder Structure Best Practices

### Recommended Structure

```
my-technical-projects/
│
├── README.md (overall index)
│
├── n8n-workflows/
│   ├── manual.md ⭐ (Claude reads this first)
│   ├── quick-reference.md (optional: common patterns)
│   │
│   ├── raw-content/ (original sources)
│   │   ├── youtube/
│   │   │   ├── advanced-api-integration-transcript.txt
│   │   │   └── error-handling-best-practices-transcript.txt
│   │   ├── reddit/
│   │   │   ├── production-workflow-discussion.txt
│   │   │   └── custom-nodes-thread.txt
│   │   ├── github/
│   │   │   ├── repo-awesome-n8n-README.md
│   │   │   └── repo-n8n-templates-README.md
│   │   └── metadata.json (URL, date, scores)
│   │
│   ├── workflows/ (actual workflow files)
│   │   ├── email-automation-retry.json
│   │   ├── api-polling-webhook.json
│   │   └── data-transformation-pipeline.json
│   │
│   ├── patterns/ (extracted patterns)
│   │   ├── error-handling-pattern.md
│   │   ├── retry-logic-pattern.md
│   │   └── webhook-security-pattern.md
│   │
│   ├── examples/ (code snippets)
│   │   └── custom-nodes/
│   │       ├── custom-auth-node.js
│   │       └── data-validator-node.js
│   │
│   └── notebooklm/
│       └── n8n-knowledge-base-consolidated.md
│
├── claude-code-projects/
│   ├── manual.md
│   ├── raw-content/
│   ├── projects/ (full project examples)
│   │   ├── cli-tool-example/
│   │   ├── mcp-server-example/
│   │   └── automation-script-example/
│   ├── patterns/
│   │   ├── agentic-workflow-pattern.md
│   │   └── tool-calling-pattern.md
│   └── prompts/
│       ├── code-generation-prompts.md
│       └── debugging-prompts.md
│
├── langchain-rag/
│   ├── manual.md
│   ├── implementations/ (full RAG systems)
│   │   ├── basic-rag-python/
│   │   ├── advanced-rag-with-reranking/
│   │   └── multimodal-rag/
│   ├── vector-stores/
│   │   ├── pinecone-setup.md
│   │   ├── weaviate-setup.md
│   │   └── chroma-local-setup.md
│   └── evaluation/
│       └── rag-metrics-guide.md
│
└── prompt-engineering/
    ├── manual.md
    ├── templates/
    │   ├── chain-of-thought.md
    │   ├── few-shot-examples.md
    │   └── structured-output.md
    └── use-cases/
        ├── coding-assistant-prompts.md
        └── research-assistant-prompts.md
```

### File Naming Conventions

**Workflows:**
- Format: `[purpose]-[variant]-[version].json`
- Examples:
  - `email-automation-basic-v1.json`
  - `email-automation-retry-logic-v2.json`
  - `api-polling-with-webhook-v1.json`

**Code Files:**
- Format: `[language]-[purpose]-[pattern].ext`
- Examples:
  - `python-rag-implementation-basic.py`
  - `typescript-mcp-server-example.ts`
  - `javascript-custom-n8n-node.js`

**Content Files:**
- Format: `[platform]-[title-slug]-[type].txt`
- Examples:
  - `youtube-advanced-n8n-tutorial-transcript.txt`
  - `reddit-production-workflow-discussion-thread.txt`
  - `github-awesome-langchain-README.md`

**Pattern Files:**
- Format: `[pattern-name]-pattern.md`
- Examples:
  - `retry-logic-pattern.md`
  - `error-handling-pattern.md`
  - `webhook-security-pattern.md`

---

## 📝 Creating Effective Manuals

### Manual Template (Copy-Paste Ready)

```markdown
# [Project Name] - Resource Manual

**Last Updated:** [YYYY-MM-DD]
**Curator:** [Your Name]
**Focus:** [Brief description of what this collection covers]
**Status:** [Active / Under Development / Archive]

---

## 📖 How to Use This Manual

**Purpose:** This manual helps Claude (and you) quickly find relevant resources when working on [project type] tasks.

**For Claude:**
When the user asks about [topic], check this manual first before suggesting generic solutions. Reference specific files in this project folder and cite original sources.

**For Humans:**
Use the Quick Lookup Table to jump to relevant resources. All files are organized in the folder structure described below.

---

## 📁 Folder Structure

```
[project-name]/
├── manual.md (this file)
├── raw-content/ (original transcripts, posts, READMEs)
├── [specific folders for your project type]
└── notebooklm/ (consolidated for RAG)
```

---

## 🏆 Resource Rankings

### Tier 1: Production-Ready ⭐⭐⭐⭐⭐
**Use these as primary references for real projects**

#### 1. [Resource Name]
- **URL:** [Full URL]
- **Source Platform:** [YouTube / Reddit / GitHub / Article]
- **Quality Score:** [X/10]
- **Production Ready:** ✅ Yes
- **File Location:** `[path/to/file]`
- **Date Added:** [YYYY-MM-DD]

**What It Is:**
[2-3 sentence description]

**Key Features:**
- Feature 1 (with brief explanation)
- Feature 2 (with brief explanation)
- Feature 3 (with brief explanation)

**When to Use:**
- Use case 1
- Use case 2

**Technical Level:** [Beginner / Intermediate / Advanced]

**Prerequisites:**
- Requirement 1
- Requirement 2

**Notes / Caveats:**
- Any limitations or considerations
- Compatibility issues
- Version requirements

**Extracted Patterns:** 
- See `patterns/[pattern-name].md`

---

#### 2. [Next Resource]
[Same structure as above]

---

### Tier 2: High Quality (Needs Adaptation) ⭐⭐⭐⭐

[Same structure as Tier 1, but these need modification for production]

---

### Tier 3: Learning Resources ⭐⭐⭐

**Good for understanding concepts, not for production use**

[Simplified structure, focus on what they teach]

---

### Tier 4: Experimental / Incomplete ⭐⭐

**Interesting ideas but not fully developed**

[Brief listings]

---

## 🔍 Quick Lookup Table

| I Need To... | Best Resource | File Location | Difficulty |
|-------------|---------------|---------------|------------|
| [Task 1] | [Resource A] | `/path/to/file` | ⚠️ Intermediate |
| [Task 2] | [Resource B] | `/path/to/file` | ✅ Beginner |
| [Task 3] | [Resource C] | `/path/to/file` | 🔴 Advanced |
| ... | ... | ... | ... |

---

## 🎯 Common Patterns Identified

### Pattern 1: [Pattern Name]

**Description:**
[What this pattern does and why it's useful]

**When to Use:**
- Scenario 1
- Scenario 2

**How It Works:**
[Step-by-step explanation or diagram]

**Implementation Example:**
```[language]
[Code or configuration example]
```

**Used By:**
- [Resource 1] (`/path/to/file`)
- [Resource 2] (`/path/to/file`)

**Variations:**
- Variation A: [Description]
- Variation B: [Description]

**Common Pitfalls:**
- ⚠️ Pitfall 1 and how to avoid it
- ⚠️ Pitfall 2 and how to avoid it

---

### Pattern 2: [Pattern Name]
[Same structure]

---

## ⚠️ Known Issues & Solutions

| Issue | Affected Resources | Solution | Status |
|-------|-------------------|----------|--------|
| [Issue description] | [Resource A, B] | [How to fix] | ✅ Resolved |
| [Issue description] | [Resource C] | [Workaround] | ⚠️ In Progress |

---

## 🧪 Testing & Validation

**Resources with example test data:**
- [Resource A]: `/examples/test-data-a.json`
- [Resource B]: `/examples/test-data-b.json`

**Validation Checklist:**
Before using any resource in production:
- [ ] Tested with sample data
- [ ] Error handling verified
- [ ] Dependencies documented
- [ ] Performance acceptable
- [ ] Security reviewed (if applicable)

---

## 📚 Learning Path

**If you're new to [topic], follow this order:**

1. Start with: [Resource X] - Covers basics
2. Then: [Resource Y] - Intermediate concepts
3. Finally: [Resource Z] - Advanced patterns

**Estimated Time:** [X hours/days]

---

## 🔗 External References

**Official Documentation:**
- [Tool Name]: [URL]

**Community Resources:**
- Forum: [URL]
- Discord: [URL]
- Subreddit: r/[subreddit]

**Related Tools:**
- [Tool A]: [URL] - [Why it's relevant]
- [Tool B]: [URL] - [Why it's relevant]

---

## 📊 Resource Statistics

**Total Resources:** [X]
- Tier 1 (Production-Ready): [X]
- Tier 2 (High Quality): [X]
- Tier 3 (Learning): [X]
- Tier 4 (Experimental): [X]

**Source Breakdown:**
- YouTube: [X] resources
- Reddit: [X] resources
- GitHub: [X] resources
- Articles: [X] resources

**Last Discovery Session:** [YYYY-MM-DD]
**Next Planned Update:** [YYYY-MM-DD]

---

## 🔄 Changelog

| Date | Change | Notes |
|------|--------|-------|
| [YYYY-MM-DD] | Added [Resource X] | Found via Perplexity search |
| [YYYY-MM-DD] | Updated [Resource Y] | Fixed broken link |
| [YYYY-MM-DD] | Removed [Resource Z] | Deprecated/outdated |

---

## 🤝 Contributing

**To add a new resource:**
1. Discover via Perplexity/search
2. Extract content (transcript/thread/code)
3. Analyze with Claude for quality score
4. Add to appropriate tier in this manual
5. Update Quick Lookup Table
6. Update statistics

---

## 💡 Usage Examples

### Example 1: Finding Similar Work
```
You: "I need to build an N8n workflow for email notifications with retry logic"

Claude: [Checks manual.md]
"I found a similar workflow in our Tier 1 resources:

Resource: Advanced Email Automation System
Location: /workflows/email-automation-retry-v2.json
Quality Score: 9/10

This workflow includes:
- Exponential backoff retry (exactly what you need)
- Error logging to Airtable
- Success/failure notifications

It uses the 'retry-logic-pattern' (see /patterns/retry-logic-pattern.md)

Would you like me to:
1. Show you the workflow JSON
2. Adapt it for your specific use case
3. Explain how the retry mechanism works"
```

### Example 2: Learning New Concept
```
You: "How do I implement RAG with LangChain?"

Claude: [Checks manual.md]
"Based on our learning path in the LangChain RAG manual:

Start with:
1. 'Basic RAG Implementation' (Tier 3 - Learning)
   Location: /implementations/basic-rag-python/
   - Covers fundamentals
   - Working code example
   - Estimated time: 2 hours

Then move to:
2. 'Advanced RAG with Reranking' (Tier 1 - Production)
   Location: /implementations/advanced-rag-with-reranking/
   - Production-ready implementation
   - Includes evaluation metrics
   
Common patterns used:
- See /patterns/vector-store-selection.md
- See /patterns/chunking-strategies.md

Would you like me to walk you through the basic implementation first?"
```

---

## 🎓 Best Practices

**For maintaining this manual:**
- Update after each discovery session
- Remove outdated resources (mark as deprecated first)
- Keep tier rankings current
- Add new patterns as discovered
- Update Quick Lookup Table with new use cases

**For using this manual:**
- Always check manual before implementing from scratch
- Cite original sources when adapting code
- Test before using in production
- Contribute improvements back to manual

---

**End of Manual Template**
```

---

## 🔌 API Implementation Details

### Complete API Reference

#### **Perplexity API**

**Documentation:** https://docs.perplexity.ai/

**Authentication:**
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar",
    "messages": [
      {
        "role": "user",
        "content": "Find top resources about n8n workflows"
      }
    ]
  }'
```

**Python Example:**
```python
import requests

def search_perplexity(query):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",  # or "sonar-pro" for better quality
        "messages": [
            {"role": "user", "content": query}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Usage
result = search_perplexity("best n8n workflows 2024 github OR reddit")
print(result['choices'][0]['message']['content'])
```

**Node.js Example:**
```javascript
const axios = require('axios');

async function searchPerplexity(query) {
  const response = await axios.post(
    'https://api.perplexity.ai/chat/completions',
    {
      model: 'sonar',
      messages: [{
        role: 'user',
        content: query
      }]
    },
    {
      headers: {
        'Authorization': `Bearer ${process.env.PERPLEXITY_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data.choices[0].message.content;
}
```

**Pricing:**
- **Sonar:** $20/month for 600 queries
- **Sonar Pro:** Higher quality, same pricing
- Rate limits: 600 requests/month on standard plan

---

#### **Claude API (Anthropic)**

**Documentation:** https://docs.anthropic.com/

**Authentication:**
```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: YOUR_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-5-20251101",
    "max_tokens": 4096,
    "messages": [
      {
        "role": "user",
        "content": "Analyze this workflow for quality"
      }
    ]
  }'
```

**Python Example:**
```python
from anthropic import Anthropic

client = Anthropic(api_key="YOUR_API_KEY")

def analyze_with_claude(content, task):
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"{task}\n\nContent:\n{content}"
        }]
    )
    return message.content[0].text

# Usage
analysis = analyze_with_claude(
    content=workflow_json,
    task="Rate this N8n workflow's quality (1-10) and explain why"
)
```

**TypeScript Example:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function analyzeWithClaude(content: string, task: string) {
  const message = await client.messages.create({
    model: 'claude-opus-4-5-20251101',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: `${task}\n\nContent:\n${content}`
    }]
  });
  
  return message.content[0].text;
}
```

**Pricing:**
- **Claude Opus 4.5:** $15/1M input tokens, $75/1M output tokens
- **Claude Sonnet 4.5:** $3/1M input, $15/1M output
- **Claude Haiku 4.5:** $0.8/1M input, $4/1M output

**Use Case Recommendations:**
- Use **Opus** for: Quality analysis, manual generation, complex reasoning
- Use **Sonnet** for: General analysis, batch processing
- Use **Haiku** for: Quick classifications, simple extractions

---

#### **YouTube Transcript APIs**

**Option 1: youtube-transcript-api (Python Library)**

**Installation:**
```bash
pip install youtube-transcript-api
```

**Usage:**
```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text
        full_text = ' '.join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Extract video ID from URL
def extract_video_id(url):
    # Handle various YouTube URL formats
    if 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    elif 'watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    return None

# Usage
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_id = extract_video_id(url)
transcript = get_transcript(video_id)
```

**Limitations:**
- Only works if captions are available
- Free but rate-limited by YouTube
- No API key required

---

**Option 2: Web Service (youtube-transcript.com)**

```bash
curl "https://api.youtube-transcript.com/v1/transcript?video_id=dQw4w9WgXcQ"
```

**Python Wrapper:**
```python
import requests

def get_transcript_via_api(video_id):
    url = f"https://api.youtube-transcript.com/v1/transcript"
    params = {"video_id": video_id}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return ' '.join([item['text'] for item in data['transcript']])
    return None
```

---

#### **Reddit API (PRAW)**

**Installation:**
```bash
pip install praw
```

**Setup:**
1. Create Reddit app at https://www.reddit.com/prefs/apps
2. Get client_id and client_secret

**Usage:**
```python
import praw

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='ResourceDiscovery/1.0'
)

def fetch_reddit_post(url):
    submission = reddit.submission(url=url)
    
    data = {
        'title': submission.title,
        'text': submission.selftext,
        'score': submission.score,
        'upvote_ratio': submission.upvote_ratio,
        'num_comments': submission.num_comments,
        'created_utc': submission.created_utc,
        'author': str(submission.author),
        'url': submission.url,
        'comments': []
    }
    
    # Get top comments
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list()[:20]:
        data['comments'].append({
            'author': str(comment.author),
            'body': comment.body,
            'score': comment.score
        })
    
    return data

# Usage
post_data = fetch_reddit_post('https://reddit.com/r/n8n/comments/...')
```

**No-Auth Alternative (JSON API):**
```python
import requests

def fetch_reddit_json(url):
    # Add .json to any Reddit URL
    json_url = url + '.json'
    response = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()
```

**Rate Limits:**
- With authentication: 60 requests per minute
- Without authentication: Much more restrictive

---

#### **GitHub API**

**Installation:**
```bash
pip install PyGithub
```

**Setup:**
1. Create Personal Access Token at https://github.com/settings/tokens

**Usage:**
```python
from github import Github

g = Github('YOUR_GITHUB_TOKEN')

def fetch_github_repo(owner, repo_name):
    repo = g.get_repo(f"{owner}/{repo_name}")
    
    # Get README
    try:
        readme = repo.get_readme()
        readme_content = readme.decoded_content.decode('utf-8')
    except:
        readme_content = None
    
    # Get metadata
    data = {
        'name': repo.name,
        'description': repo.description,
        'stars': repo.stargazers_count,
        'forks': repo.forks_count,
        'language': repo.language,
        'topics': repo.get_topics(),
        'created_at': repo.created_at,
        'updated_at': repo.updated_at,
        'readme': readme_content,
        'url': repo.html_url,
        'homepage': repo.homepage
    }
    
    return data

# Search for repos
def search_github(query, sort='stars', order='desc'):
    repos = g.search_repositories(query=query, sort=sort, order=order)
    results = []
    
    for repo in repos[:20]:  # Top 20
        results.append({
            'name': repo.full_name,
            'stars': repo.stargazers_count,
            'description': repo.description,
            'url': repo.html_url
        })
    
    return results

# Usage
n8n_repos = search_github('n8n workflow stars:>50')
```

**Rate Limits:**
- Authenticated: 5,000 requests per hour
- Unauthenticated: 60 requests per hour

---

#### **X/Twitter Scraping (Apify)**

**Documentation:** https://apify.com/apidojo/tweet-scraper

**Usage:**
```python
import requests

def scrape_tweet(tweet_url):
    url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs"
    headers = {
        "Authorization": f"Bearer {APIFY_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "startUrls": [{"url": tweet_url}],
        "maxTweets": 1
    }
    
    # Start scraping run
    response = requests.post(url, headers=headers, json=data)
    run_id = response.json()['data']['id']
    
    # Wait for completion and get results
    results_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs/{run_id}/dataset/items"
    
    import time
    time.sleep(5)  # Wait for scraping to complete
    
    results = requests.get(results_url, headers=headers)
    return results.json()
```

**Alternative: Bright Data**
- More reliable but more expensive
- Better for large-scale scraping
- Documentation: https://brightdata.com

**Pricing:**
- Apify: Pay per scrape ($1-10 depending on volume)
- Bright Data: Subscription-based ($500+/month for serious use)

---

## 📊 Cost Analysis

### Monthly Cost Estimates

| Scenario | Tool Stack | Monthly Cost |
|----------|-----------|--------------|
| **Manual (Current)** | Perplexity Pro + Claude Pro | $40 |
| **Light Automation** | Perplexity API + Claude API (low volume) | $30-50 |
| **Medium Automation** | All APIs + N8n Cloud | $100-200 |
| **Heavy Automation** | All APIs + N8n + Apify | $200-500 |
| **Enterprise** | All tools + custom infrastructure | $500+ |

### Detailed Breakdown

**Free Tier (Learning Phase):**
- ❌ Not really feasible for this workflow
- Manual copy-paste only
- Limited Gemini Pro usage
- Total: $0 (but very time-consuming)

**Starter Pack ($40/month):**
- Perplexity Pro: $20/month
- Claude Pro: $20/month (use web interface)
- Manual extraction for YouTube/Reddit
- **Best for:** 1-2 discovery sessions per month

**Light Automation ($30-50/month):**
- Perplexity API: $20/month (600 queries)
- Claude API: $10-30/month (pay as you go)
- YouTube transcript API: Free
- Reddit API: Free
- GitHub API: Free
- **Best for:** Weekly discovery, ~10-20 resources per week

**Medium Automation ($100-200/month):**
- Above APIs: $30-50
- N8n Cloud: $20/month (starter plan)
- Apify: $50/month (for X scraping)
- Airtable/database: $10-20/month
- GitHub storage: $5/month
- **Best for:** Daily monitoring, ~50-100 resources per week

**Heavy Automation ($200-500/month):**
- Above APIs: $50-100
- N8n Cloud Pro: $50/month
- Apify Pro: $100/month
- Bright Data: $50+/month (for reliable X scraping)
- Database (Supabase): $25/month
- Storage: $10/month
- **Best for:** Multiple topics, 100+ resources per week

### Cost Optimization Tips

**Reduce API Costs:**
1. **Batch requests**: Combine multiple queries in single API call
2. **Cache results**: Don't re-analyze same content
3. **Use cheaper models**: Sonnet instead of Opus for simple tasks
4. **Rate limit yourself**: Spread requests over time
5. **Filter before analyzing**: Use simple heuristics before Claude API

**Example Savings:**
```python
# Instead of analyzing every resource with Opus ($$$)
def smart_analysis(resources):
    # Stage 1: Quick filter with simple rules
    high_engagement = [r for r in resources if r['score'] > 50]
    
    # Stage 2: Use Haiku for basic classification ($)
    candidates = classify_with_haiku(high_engagement)
    
    # Stage 3: Use Opus only for top candidates ($$)
    final_analysis = analyze_with_opus(candidates[:10])
    
    return final_analysis

# This reduces Opus calls by ~80%, saving ~$60/month at scale
```

**Free Alternatives:**
- Use GPT-4o instead of Claude for some tasks (cheaper)
- Use Gemini Pro (free tier) for transcript extraction
- Use Reddit JSON API instead of PRAW (no auth)
- Self-host N8n instead of cloud ($0 vs $20)

---

## ⚠️ Troubleshooting & Limitations

### Common Issues

**Issue 1: Perplexity Not Finding Recent Content**

**Symptoms:**
- Only returns results from 6+ months ago
- Missing obviously relevant recent resources

**Solutions:**
- Add date constraints to query: "best n8n workflows 2024-2025"
- Use "recent" or "latest" in search query
- Try different phrasings
- Supplement with direct subreddit searches

---

**Issue 2: YouTube Transcripts Not Available**

**Symptoms:**
- "No transcript available" error
- Auto-generated captions disabled by uploader

**Solutions:**
- Skip that video (most have captions nowadays)
- Use AI audio transcription (Whisper API) as fallback
- Check if video has manually added captions in other languages

---

**Issue 3: X/Twitter Scraping Blocked**

**Symptoms:**
- Login walls
- Rate limit errors
- Captchas

**Solutions:**
- Use Perplexity to get X content instead
- Use Apify or Bright Data (paid, more reliable)
- Deprioritize X content, focus on Reddit/GitHub
- Manual screenshots as last resort

---

**Issue 4: Claude Analysis Is Generic**

**Symptoms:**
- Claude gives surface-level analysis
- Doesn't identify nuanced technical issues
- Scores everything 7-8/10

**Solutions:**
- Provide more specific prompts:
  - ❌ "Analyze this workflow"
  - ✅ "Analyze this N8n workflow for: error handling quality, production-readiness, scalability issues, security concerns, and code organization. Rate each aspect separately."
- Include comparison references:
  - "Compare this to production-ready patterns in [resource X]"
- Ask for specific things:
  - "Identify any deprecated nodes, anti-patterns, or potential bugs"

---

**Issue 5: Too Many Low-Quality Results**

**Symptoms:**
- 80% of discovered resources are basic tutorials
- Hard to find production-ready examples

**Solutions:**
- Add quality filters to search:
  - "production-ready n8n workflows"
  - "advanced [topic] NOT tutorial"
  - "site:github.com [topic] stars:>100"
- Filter by engagement metrics before analysis:
  ```python
  high_quality = [r for r in results if
      r['stars'] > 100 or  # GitHub
      r['score'] > 50 or   # Reddit
      r['views'] > 10000   # YouTube
  ]
  ```

---

**Issue 6: Manual Becomes Outdated**

**Symptoms:**
- Resources from 2+ years ago
- Links are broken
- Tools/APIs have changed

**Solutions:**
- Schedule quarterly manual reviews
- Automate link checking:
  ```python
  import requests
  
  def check_links(manual_file):
      broken = []
      for url in extract_urls(manual_file):
          try:
              response = requests.head(url, timeout=5)
              if response.status_code >= 400:
                  broken.append(url)
          except:
              broken.append(url)
      return broken
  ```
- Add "last verified" dates to resources
- Archive outdated resources instead of deleting

---

### Platform-Specific Limitations

**Perplexity:**
- ❌ No access to paywalled content
- ❌ Search quality varies by topic
- ❌ Limited to ~600 queries/month on standard plan
- ⚠️ Sometimes misses niche communities

**Claude:**
- ❌ Cannot directly access web pages
- ❌ Knowledge cutoff (verify current info via search)
- ❌ Context window limits for very large codebases
- 💰 Opus is expensive for high-volume analysis

**YouTube:**
- ❌ No transcripts for videos with disabled captions
- ⚠️ Auto-generated captions may have errors
- ❌ Cannot transcribe if uploader disabled embedding

**Reddit:**
- ⚠️ Deleted posts not accessible
- ⚠️ Some communities are private
- ❌ Heavy moderation may hide content

**GitHub:**
- ⚠️ Private repos not accessible
- ❌ Large repos slow to fetch
- ⚠️ Archived repos may be outdated

**X/Twitter:**
- ❌ Login walls (biggest limitation)
- ❌ Rate limiting is aggressive
- ❌ Expensive to scrape at scale
- ⚠️ Content may be deleted

---

## 🚀 Future Enhancements

### Phase 1: Manual Optimization (Current)
- ✅ Define process
- ✅ Create templates
- ✅ Document workflows
- 🔄 Build first project collections

### Phase 2: Partial Automation (Next 1-2 months)
- 🎯 Build N8n workflow for discovery
- 🎯 Automate transcript extraction
- 🎯 Implement basic Claude analysis
- 🎯 Create Airtable database

### Phase 3: Full Automation (Next 3-6 months)
- 🎯 Scheduled weekly discovery runs
- 🎯 Automatic manual generation
- 🎯 Quality filtering pipeline
- 🎯 GitHub auto-commits
- 🎯 Slack notifications

### Phase 4: Advanced Features (Future)
- 🎯 Web dashboard for management
- 🎯 AI-powered resource recommendations
- 🎯 Duplicate detection
- 🎯 Trend analysis
- 🎯 Community contributions
- 🎯 Public API for sharing curated collections

---

## 📞 Getting Help

**If you're stuck:**

1. **Check this manual first** (you're reading it!)
2. **Review examples** in the workflows section
3. **Check platform-specific strategies** for your issue
4. **Search existing project manuals** for similar problems

**Community Resources:**
- N8n Community: https://community.n8n.io/
- Claude API Discord: https://discord.gg/anthropic
- LangChain Discord: https://discord.gg/langchain

**Debugging Checklist:**
- [ ] API keys are correct and active
- [ ] Rate limits not exceeded
- [ ] URLs are accessible (not behind paywall)
- [ ] Content format is supported
- [ ] Error messages checked carefully

---

## 📝 Quick Start Checklist

**To start using this system today:**

- [ ] Set up Perplexity Pro account ($20/month)
- [ ] Get Claude Pro account ($20/month) or API access
- [ ] Set up NotebookLM account (free with Google)
- [ ] (Optional) Set up ChatGPT Plus for YouTube transcripts
- [ ] Create project folder structure on your computer
- [ ] Check if Resource Curator skill is available in Claude
- [ ] Pick your first topic (e.g., "N8n workflows")
- [ ] Run your first manual discovery session
- [ ] **Decision:** Does your collection need filtering? (20+ resources or old content?)
  - [ ] YES: Use Resource Curator skill to filter
  - [ ] NO: Skip to NotebookLM
- [ ] Have NotebookLM create manual.md (with ranking context if used curator)
- [ ] Add manual to Claude Project
- [ ] Test by asking Claude questions about the topic

**For automation (later):**

- [ ] Sign up for API access (Perplexity, Claude, Anthropic)
- [ ] Get Reddit API credentials (if needed)
- [ ] Get GitHub Personal Access Token (if needed)
- [ ] Choose: N8n vs Python script vs custom app
- [ ] Build your first automated workflow
- [ ] Test with small batch first
- [ ] Scale up gradually

---

## 🔑 API Token Management

### GitHub Personal Access Token

**Current Token Status:**

| Created | Expiration | Remaining | Status |
|---------|------------|-----------|--------|
| Feb 10, 2026 | May 11, 2026 | 90 days | ✅ Active |

**Token Details:**
- **Name:** Claude Curator
- **Scope:** public_repo (read access to public repositories)
- **Use:** For two-phase-curator skill when filtering large GitHub repos (>1000 files)
- **Rate Limit:** 5,000 API calls per hour (vs 60 without token)

### Expiration Reminder Schedule

**⚠️ April 11, 2026 (30 days before expiration):**
- Review token usage
- Consider renewing if still needed
- Plan for token rotation

**🚨 May 1, 2026 (10 days before expiration):**
- **RENEW IMMEDIATELY**
- Generate new token
- Update environment variables
- Test with two-phase-curator skill

**❌ May 11, 2026 (Expiration Day):**
- Token becomes invalid
- Phase 1 filtering will fail on large repos
- Must regenerate before using skill

### How to Check Token Status

```bash
# Via GitHub web interface
https://github.com/settings/tokens
# Look for "Claude Curator" token and check expiration date
```

### How to Renew Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "Claude Curator" (or append version, e.g., "Claude Curator v2")
4. Select scope: **public_repo**
5. Set expiration: 90 days (or No expiration if preferred)
6. Click "Generate token"
7. Copy new token (starts with `ghp_...`)
8. Update in your environment:
   ```bash
   export GITHUB_TOKEN=ghp_new_token_here
   ```
9. Update this section with new dates

### When You Need the Token

**DON'T need token:**
- Small repos (<100 files)
- Occasional filtering (few repos per hour)
- Testing the skill

**DO need token:**
- Large repos (1000+ files like Zie619/n8n-workflows with 4,343 files)
- Filtering multiple repos in succession
- Heavy usage (>60 API calls per hour)

### Usage with Two-Phase Curator

```bash
# Method 1: Command line argument
python scripts/filter_github.py --url [URL] --token ghp_your_token_here

# Method 2: Environment variable (recommended)
export GITHUB_PUB_TOKEN10F26=ghp_your_token_here
python scripts/filter_github.py --url [URL]

# Method 3: Via Claude (automatic if env var set)
"Use two-phase-curator on https://github.com/large-repo"
```

**Environment Variable Names (in priority order):**
1. `GITHUB_PUB_TOKEN10F26` - Your specific token (expires May 11, 2026)
2. `GITHUB_TOKEN` - Fallback generic name
3. `--token` argument - Override both environment variables

**Set it permanently:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_PUB_TOKEN10F26=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### Token Security

✅ **DO:**
- Store in environment variables
- Add to `.gitignore` if in config files
- Rotate every 90 days
- Use minimal required scopes (public_repo only)

❌ **DON'T:**
- Commit tokens to git repositories
- Share tokens publicly
- Use tokens with unnecessary permissions
- Forget to rotate before expiration

### Other API Tokens (Future)

**Reddit:** No token needed (uses public JSON API)
**Perplexity:** Account-based (no token management needed)
**Claude API:** Manage separately if using for automation

---

## 🎓 Conclusion

This system transforms one-off research into reusable knowledge bases. Whether you're discovering N8n workflows, Claude Code projects, LangChain implementations, or any other technical topic, the process adapts to your needs:

**The Core Workflow:**

1. **Discover** with Perplexity
2. **Extract** with platform-specific tools  
3. **Filter (if needed)** with Resource Curator skill
   - Use when: 20+ resources OR old content OR fast-moving field
   - Skip when: <15 resources AND all recent
4. **Create Manual** with NotebookLM (or Claude for highly technical content)
5. **Organize** in project folders
6. **Reuse** via Claude Projects

**The Intelligence Layers:**

```
Perplexity → Discovery (find the resources)
    ↓
Resource Curator → Filtering (separate gold from noise)
    ↓
NotebookLM → Synthesis (create the manual)
    ↓
Claude Project → Implementation (build with context)
```

**Start manual, automate what's repetitive, and build up your personal library of curated technical resources.**

**Key Principles:**
- ✅ Quality over quantity (filter aggressively)
- ✅ Recency matters (especially in AI/automation)
- ✅ Modern alternatives exist (always check before implementing)
- ✅ The manual is your guide (Claude reads it before answering)
- ✅ Update regularly (quarterly reviews recommended)

**Remember:**
- The manual is your guide
- Claude reads it before answering
- Quality over quantity
- Filter obsolete patterns
- Update regularly
- Share learnings

Happy discovering! 🚀
