## # Session 15: Build & Serve Agentic Graphs with LangGraph


| 📰 Session Sheet                                                                                          | ⏺️ Recording                                                                                                                                          | 🖼️ Slides                                                                                                                                                                         | 👨‍💻 Repo    | 📝 Homework                                                                 | 📁 Feedback                                         |
| --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------- | --------------------------------------------------- |
| [Agent Servers](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Session_Sheets/15_Agent_Servers) | [Recording!](https://us02web.zoom.us/rec/share/lORjByDju6fv4TdE3r93dorY3aNgmSKL_Qk_cX_AMcCQ6cNfSW77unaA1LMVV60.OcI8uEnfVmRAgjSn) passcode: `Dc@&pv1T` | [Session 15 Slides](https://www.canva.com/design/DAG-EJqkRaM/FR3WG_yMA5_BqbWpQlHR9g/edit?utm_content=DAG-EJqkRaM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [Session 15 Assignment: Agent Servers](https://forms.gle/Vb3HNDsyVPQ1jqKX7) | [Feedback 3/3](https://forms.gle/kYmhbVUEMog16mKv8) |


### Prerequisites

Before starting, ensure you have the following:

- **Python 3.11+** installed
- An **OpenAI API Key**
- A **Tavily API Key**
- (Optional) **LangSmith** credentials for tracing

Create a `.env` file in this directory with your API keys:

1. Run `uv sync` to install dependencies.

# Build 🏗️

Run the repository and complete the following:

- 🤝 Breakout Room Part #1 — Building and serving your LangGraph Agent Graph
  - Task 1: Getting Dependencies & Environment
    - Configure `.env` (OpenAI, Tavily, optional LangSmith)
  - Task 2: Serve the Graph Locally
    - `uv run langgraph dev` (API on [http://localhost:2024](http://localhost:2024))
  - Task 3: Call the API from a different terminal
    - `uv run test_served_graph.py` (sync SDK example)
  - Task 4: Explore assistants (from `langgraph.json`)
    - `agent` → `simple_agent` (tool-using agent)
    - `agent_helpful` → `agent_with_helpfulness` (separate helpfulness node)
- 🤝 Breakout Room Part #2 — Using LangSmith Studio to visualize the graph
  - Task 1: Open Studio while the server is running
    - [https://smith.langchain.com/studio?baseUrl=http://localhost:2024](https://smith.langchain.com/studio?baseUrl=http://localhost:2024)
  - Task 2: Visualize & Stream
    - Start a run and observe node-by-node updates
  - Task 3: Compare Flows
    - Contrast `agent` vs `agent_helpful` (tool calls vs helpfulness decision)

🚧 Advanced Build 🚧 (OPTIONAL - *open this section for the requirements*)

> NOTE: This can be done in place of the Main Assignment

- Create and deploy a locally hosted MCP server with FastMCP.
- Extend your tools in `tools.py` to allow your LangGraph to consume the MCP Server.

When submitting, provide:

- Your Loom video link demonstrating the MCP server integration
- The GitHub URL to your completed Advanced Build

Have fun!

### Questions & Activities

#### Question 1:

What is the key architectural difference between the `simple_agent` and `agent_with_helpfulness` graphs? Specifically, explain how the helpfulness evaluation loop works and what mechanisms are in place to prevent it from running indefinitely.

##### Answer:

simple_agent has a DAG that basically
START -> agent <--> tools
          |
          -> END

It starts, calls the agent then tools as needed then ends.

with agent_with_helpfulness, there is another conditional edge.  If there are no more tool calls requested by the agent then you are routed to a 'helpfulness' node.
The helpfulness node determines if the response was 'helpful' then routes back to the agent if the answer was 'no', via way of a 'continue' return.
If the helpfulness agent returns '"HELPFULNESS:Y' then the next node is 'END' and the run is over.

The helpfulness agent wont run forever because after 10 messages it will return HELPFULNESS:END. 
This is picked up in the helpfulness_decision() method, which then will return the "END" node to finish the conversation

```
if len(state["messages"]) > 10:
    return {"messages": [AIMessage(content="HELPFULNESS:END")]}
```

#### Question 2:

What is the role of `langgraph.json` in the LangGraph Deployments? Describe each of its key fields and how the platform uses this file to discover and serve your graphs.

##### Answer:

langraph.json is read by the langgraph deployments to determine the available agents and their entrypoints in the codebase.

Heres a sample with some annotations with -->

```
{
  "version": 1, --> version of my current graph
  "dependencies": ["."], 
  "env": ".env", --> wheres the .env file.
  "python_version": "3.13", --> python version to use.
  "graphs": { --> Available graphs in the codebase
    "simple_agent": "app.graphs.simple_agent:graph", --> directory path and entry point function in the file ie app/graphs/simple_agent.py with the "graph" fucntion to be called on load.
    "agent_with_helpfulness": "app.graphs.agent_with_helpfulness:graph"  --> directory path and entry point
  },
  "assistants": {
    "agent": { --> key to identify this particular agent.
      "graph_id": "simple_agent", --> how to identify this agent, references the graphs.simple_agent above
      "name": "Simple Agent", --> display name
      "description": "Agent with tools using conditional tool-calling." --> description
    },
    "agent_helpful": {
      "graph_id": "agent_with_helpfulness",
      "name": "Agent with Helpfulness Check",
      "description": "Agent that uses tools and performs a helpfulness check with loop limit."
    }
  }
}

```

#### Activity #1:

Create your own agent graph! Build a new graph in `app/graphs/` with a custom evaluation node (e.g., a vibe checker, a fact verifier, a summarizer — get creative!). Register it in `langgraph.json`, serve it with `uv run langgraph dev`

##### Answer:

Ok, I added the ability to do spanish translation.

tr

in one window:

rm -rf  /Users/dereky/old/personal/code/ai-makerspace-code/AIE9/15_LangGraph_Deployments/.langgraph_api ; uv run langgraph dev --no-reload

Then in the other:

 uv run test_served_spanish_[graph.py](http://graph.py) 

YOu can see it in studio and it works via CLI.

# Ship 🚢

- The completed notebook.
- 5min. Loom Video

# Share 🚀

- Walk through your notebook and explain what you've completed in the Loom video
- Make a social media post about your final application and tag @AIMakerspace
- Share 3 lessons learned
- Share 3 lessons not learned

# Submitting Your Homework

### Main Homework Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:
  - *(You should have completed this process already.)* For your initial repo setup, see [Initial_Setup](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Prerequisites/Initial_Setup)
    - To get the latest updates from AI Makerspace into your own AIE9 repo, run the following commands:
    ```
    git checkout main
    git pull upstream main
    git push origin main
    ```
2. **IMPORTANT:** Start Cursor from the `15_LangGraph_Platform` folder (you can also use the *File -> Open Folder* menu option of an existing Cursor window)
3. Answer Questions 1 - 2 using the `##### Answer:` markdown cell below them in the README
4. Complete Activity #1 in the README
5. Add, commit and push your modified files to your GitHub repository.

When submitting your homework, provide:

- Your Loom video link
- The GitHub URL to the `15_LangGraph_Platform` folder on your assignment branch

