<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 16: LLM Servers</h1>

| 📰 Session Sheet                                  | ⏺️ Recording                           | 🖼️ Slides                                   | 👨‍💻 Repo       | 📝 Homework                                              | 📁 Feedback                        |
| ------------------------------------------------- | -------------------------------------- | ------------------------------------------- | ------------- | -------------------------------------------------------- | ---------------------------------- |
| [LLM Servers](../00_Docs/Session_Sheets/16_LLM_Servers) |[Recording!](https://us02web.zoom.us/rec/share/HDunij9p7eCXeP_OgsRDRjTdWUqiEhDBGWrFJEn1bwWR1wz1jKX6EHXSOM45d0sC.rHiyo_znZ-R8Jh6S) <br> passcode: `D80X^YjL`| [Session 16 Slides](https://www.canva.com/design/DAG-EBu7B5A/POcowC5rDLENSPcSVpbf8g/edit?utm_content=DAG-EBu7B5A&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [Session 16 Assignment: LLM Servers](https://forms.gle/Riqvwf6KrZcCRKV86) <br><br> [Demo Day Submission (3/12)](https://forms.gle/7xyuBUn69GX4v6K98)  | [Feedback 3/5](https://forms.gle/W28QFWJXpSS4ZAR6A) |

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU'RE FINISHED YOUR ASSIGNMENT !!!⚠️**

# Build 🏗️

In today's assignment, we'll be creating Fireworks AI endpoints, and then building a RAG application.

- 🤝 Breakout Room #1
  - Set-up Open Source Endpoint (Instructions [here](./ENDPOINT_SETUP.md)) ((This process may take 15-20min.))
  - Test Endpoint and Embeddings with the `endpoint_slammer.ipynb` notebook.

- 🤝 Breakout Room #2
  - Use the Open Source Endpoints to build a RAG LangGraph application

# Ship 🚢

The completed notebook and your RAG app/notebook!

### Deliverables

- A short Loom of either:
  - the notebook and the RAG application you built for the Main Homework Assignment; or
  - the notebook you created for the Advanced Build

# Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a RAG application powered by open-source endpoints! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

# Submitting You Homework [OPTIONAL]

## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:

1. Follow the instructions in `ENDPOINT_SETUP.md`
2. Replace both `model` values in `endpoint_slammer.ipynb` with the `gpt-oss` endpoint you created in Step 1
3. Run the code cells in `endpoint_slammer.ipynb`
4. Respond to the questions in the section below
5. Build a sample RAG
6. Record a Loom video reviewing what you have learned from this session

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU HAVE FINISHED YOUR ASSIGNMENT !!!⚠️**

## Questions

### ❓ Question #1:

What is the difference between serverless and dedicated endpoints?

#### ✅ Answer:

##### Serverless
When we talk about serverless endpoints we're referencing buying time on on demand GPUs.  You pay more per hour technically, but if you only need the compute during business hours and during the week (40 hrs) then an on-demand GPU is a great choice.  Also if you have very unpredictable workloads, say an app where everyone asks a lot of questions around a specific daily event, like ordering lunch, then you'd want serverless to auto-scale up to meet the demand.  Again you wouldn't want to buy/rent GPUs to handle maxium capacity just for a few events.
The downside is there are cold start delays of seconds and up to minutes to spin up services and get them running, so you need strategies to compensate for this AND/OR user interfaces that alert the user that 'this could take a while'.

##### Dedicated
When using a dedicated ednpoing, you are paying for dedicated GPUs, RAM, CPUs, etc.  YOu are paying for this infrastructure 24x7 even if there is no traffic or no inference requests.  You will get consistent and higher higher performance, AND you need to consider scaling.  If your application has 'bursts' where you need lots of throughput, then a normal machine will queue requests, slow down and ultimately will return errors if you go far beyond its capacity.  These are the same concepts in web load balancing and autoscaling applied to LLM resources.  Amazon Lambda and GCP's Cloud Functions already provide a good mental model here.

##### Overall
If you are playing/prototyping then go serverless and spin them up/down like we are doing in this class.  You can even deploy serverless, but consider moving to dedicated when you have the budget and require performance at scale.



### ❓ Question #2:

Why is it important to consider token throughput and latency when choosing an LLM for user-facing applications?

#### ✅ Answer:

Both token throughput and latency are important when choosing an LLM because they directly affect user experience, system scalability, and operational efficiency.

Token throughput refers to how many tokens a model can process or generate per second. Higher throughput enables an application to handle larger prompts, longer responses, or many concurrent users without slowing down. In production systems—such as chatbots, copilots, or AI assistants—high throughput allows the system to scale efficiently as demand increases.

Latency refers to the time it takes for the model to begin producing a response after receiving a request. In interactive applications, latency strongly impacts perceived responsiveness. If a response takes several seconds to begin streaming, users may perceive the application as slow or unreliable.

The acceptable balance between throughput and latency depends on the specific use case:

Real-time applications (customer support chatbots, coding assistants, AI copilots) require very low latency so conversations feel natural.

Batch or background processing tasks (document analysis, data extraction, report generation) can tolerate higher latency because responses are not immediately visible to a user.

Complex reasoning tasks may require larger prompts and longer outputs, which increases both latency and token consumption.

Developers must therefore choose a model that provides the right trade-off between speed, scalability, and capability for the application's workload. Optimizing for token throughput and latency ensures that the application remains responsive for users while also controlling infrastructure costs and system performance at scale.


## Activity 1: RAGAS Evaluation with Cost Analysis

Use RAGAS to evaluate your open-source Fireworks AI powered RAG app against an OpenAI `gpt-4.1-mini` powered equivalent. Compare retrieval quality, answer faithfulness, and end-to-end accuracy across both providers.

Additionally, instrument both pipelines with **LangSmith** to capture token usage and cost per query. Use LangSmith's tracing and cost dashboards to compare the total cost of running each provider at scale. Include your evaluation results, cost breakdown, and analysis in your Loom video.

## Advanced Activity: Local Models

Swap out the Fireworks AI endpoints for **locally-running open-source models** using [Ollama](https://ollama.com/) or another local inference server of your choice. Run both your embedding model and your chat model locally, and rebuild the RAG pipeline on top of them.

- Compare quality and latency between the local setup and your Fireworks AI hosted endpoint.
- Reflect: what are the trade-offs of local models vs. managed endpoints in a production setting?

Include your findings and a demo in your Loom video.
