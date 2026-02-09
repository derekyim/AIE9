# Life Coach Agent Advanced build

## ADVANCED BUILD NOTES

Here's the build plan I followed

starting bottom up from task 10 on the worksheet.
- [x] try the cli on a toy example
  - [x] cd 'workspace'; deepagents ;   
  - [x] then it can see prior convos, the cli flag passed in the example doesnt exist
- [x] reprompt the main system prompt to know about more specialists
- [x] add specialists
- [x] add skils
- [x] add multiphase planning with dependencies - enhanced todo store
  - [x] add phases
  - [x] get phases to go in order
- [x] add context management
- [x] implement workflow
- [x] confirm memory
- [x] testing

## A few of the Changes Implemented
* Added helper functions to build and print out the plan
* tested planner
* todo tracking, updating.
* Implemented 4 sub agent and a pile of new skills
* new advanced_build directory is populated with below hierarchy including memory and results
* prompt adjusted to cover multiple wellness areas





## Context management File system and namespace strategy

All context is currently stored in the filesystem due to the persistence requirement of the project.  THe structure is below.
Basically the store is split into user level "user_alex" and then other global topics, here its 'coaching'

```
advanced_build/
├── user_alex/                              # Per-user context
│   ├── profile/                            # (user_id, "profile")
│   │   ├── demographics.json               # Name, age, location, occupation
│   │   ├── values.json                     # Core values, priorities, motivations
│   │   └── life_situation.json             # Family, housing, employment
│   │
│   ├── goals/                              # (user_id, "goals")
│   │   ├── short_term.json                 # 0-3 months goals
│   │   ├── medium_term.json                # 3-12 months goals
│   │   └── long_term.json                  # 1-5+ years goals
│   │
│   ├── progress/                           # (user_id, "progress")
│   │   ├── milestones.json                 # Achieved & in-progress milestones
│   │   ├── setbacks.json                   # Setbacks with learnings
│   │   └── week_1_checkin.json             # Weekly check-ins
│   │
│   ├── preferences/                        # (user_id, "preferences")
│   │   ├── communication.json              # Style, tone, frequency
│   │   ├── coaching.json                   # Approach, accountability
│   │   └── learning.json                   # Learning style, pace
│   │
│   ├── assessments/                        # Additional context
│   ├── plans/
│   └── resources/
│
└── coaching/                               # Global context (shared)
    └── patterns/                           # ("coaching", "patterns")
        └── learned_patterns.json           # Anonymized patterns across users
```

Here is the  Namespace → Directory Mapping

| Namespace | Directory | Purpose |
|-----------|-----------|---------|
| `(user_id, "profile")` | `profile/` | Demographics, values, life situation |
| `(user_id, "goals")` | `goals/` | Short, medium, long-term goals |
| `(user_id, "progress")` | `progress/` | Milestones achieved, setbacks overcome |
| `(user_id, "preferences")` | `preferences/` | Communication style, coaching approach |
| `("coaching", "patterns")` | `coaching/patterns/` | Learned patterns across users (anonymized) |


## Screenshots provided of:
* generated plans "generated-plans.png"
* progress tracking "progress-tracking.png"




# Trace of an interaction 
Here I gave it a set of prompts.  Then refine it later.

---------------------------
## STEP 1:  start it off with some broad direction
---------------------------
INPUT:
result = life_coach.invoke({
    "messages": [{
        "role": "user",
        "content": """Hi! My user_id is user_alex. I'd like you to create a 90 Day Action Plan to be a better person.

I want to focus on:
1. Building a consistent exercise routine (I can exercise 3x per week for 30 mins)
2. Improve my finances and save money
3. Improve my relationships and social connections
4. Work towards a promotion at work

Please create comprehensive plans for each area and save them as separate files I can reference."""
    }]
})

OUTPUT:
Life Coach response:
Perfect! I've completed your comprehensive 90-day action plan to become a better person. Here's what I've created for you:

## 🎉 Your Complete 90-Day Transformation Package

I've created **5 detailed files** that you can reference throughout your journey:

### 📋 Master Plan
**`/alex_master_90day_action_plan.md`** - Your complete integrated 90-day roadmap with:
- Daily and weekly schedules combining all four focus areas
- Progress tracking templates
- Milestone celebrations and rewards system  
- Anxiety management strategies throughout
- Technology tools and apps to support success

### 📚 Individual Domain Plans

1. **`/alex_fitness_plan_90days.md`** - Complete exercise program featuring:
   - Progressive 12-week workout plan (3x/week, 30+ mins)
   - Anxiety-friendly exercises with mindfulness integration
   - Week-by-week progression from gentle yoga to circuit training
   - Morning routine optimization for energy and sleep improvement

2. **`/alex_financial_plan_90days.md`** - Comprehensive money management system:
   - Goal to save $1,200 over 90 days
   - Build $500 emergency fund
   - Practical money-saving strategies and budgeting system
   - Weekly and monthly financial tracking templates

3. **`/alex_relationships_plan_90days.md`** - Social connection expansion plan:
   - Anxiety-friendly approach to meeting new people
   - Strategies for deepening existing relationships  
   - Progressive challenges from comfort zone to hosting events
   - Online and offline relationship building techniques

4. **`/alex_career_plan_90days.md`** - Strategic promotion preparation:
   - Skills assessment and development plan
   - Professional networking and mentorship strategies
   - Leadership development opportunities
   - Performance improvement and visibility tactics

## 🌟 Key Features Tailored for You

✅ **Anxiety-Friendly**: Every plan considers your mild anxiety with gentle progressions and coping strategies  
✅ **Vegetarian-Optimized**: Fitness and financial plans account for your dietary preferences  
✅ **Morning-Focused**: Exercise routines designed for your preferred morning schedule  
✅ **Detailed Communication**: Comprehensive plans matching your communication style preference  
✅ **Energy & Sleep Goals**: All plans support your primary goals of better energy and sleep

## 🚀 Your Next Steps

1. **Review the Master Plan** to understand how everything integrates
2. **Set your official start date** and mark it in the master plan
3. **Set up tracking systems** (apps, calendar reminders, journal)
4. **Read through each domain-specific plan** to familiarize yourself with the details
5. **Begin Week 1** with confidence knowing you have a comprehensive roadmap

## 📈 Expected Outcomes After 90 Days

- **Fitness**: Established exercise habit with increased energy and better sleep
- **Finance**: $1,200+ saved with sustainable budgeting habits  
- **Relationships**: Expanded social network with deeper, more meaningful connections
- **Career**: Clear path toward promotion with enhanced skills and professional visibility

All plans are designed to work together synergistically - your morning exercise routine supports energy for career activities, your financial discipline creates confidence for social activities, and your relationship building supports professional networking.

You have everything you need to transform into the better person you want to become. The journey starts with your first morning workout and your first tracked expense. You've got this! 💪✨

---------------------------
## STEP 2:  NOW tell it to hone in on a few areas
---------------------------

result = life_coach.invoke({
    "messages": [{
        "role": "user",
        "content": """Hi! My user_id is user_alex. I asked for you to create a 90 Day Action Plan to be a better person.  
        Can your review the created files and make two more finance goals, I'd like to buy a car for 3k in 90 days.
        Can you also make the exercise goal more specific, I'd like to lose 10lbs in 90 days.
        """
    }]
})

Life Coach response:
Perfect! I've completed your 90 Day Action Plan with your requested updates. Here's what I've created and updated:

## 📋 **Plan Review & Updates Completed**

### 🆕 **New Comprehensive 90 Day Action Plan**
I've created a detailed `/user_alex/plans/90_day_action_plan.md` that integrates all aspects of becoming a better person:

**Key Features:**
- **Structured 90-day timeline** with monthly phases
- **Weekly milestones** and daily habits
- **Family-integrated activities** considering your dependent
- **Realistic scheduling** for your full-time software engineer role

### 💰 **Updated Finance Goals (As Requested)**
1. **Car Purchase Goal:** Save $3,000 in 90 days
   - Month 1: $500 + Month 2: $500 + Month 3: $1,000
   - Integrated with your existing emergency fund goal
   - Specific strategies for SF cost of living

2. **Emergency Fund Completion:** Add $1,800 over 90 days
   - $600/month to complete your 6-month fund
   - Currently at 40% → Target: 100% completion

### 🏃‍♂️ **Specific Exercise Goal (As Requested)**
**Goal:** Lose 10 pounds in 90 days through structured routine
- **Phase 1 (Month 1):** 3x/week foundation building
- **Phase 2 (Month 2):** 4x/week intensity building  
- **Phase 3 (Month 3):** 5x/week peak performance
- **Family-friendly:** Saturday activities include your dependent
- **Realistic:** Morning/evening options for your work schedule

### 🎯 **Integration with Existing Plans**
- **Maintained** your successful energy improvement plan (6:30 AM wake, sleep hygiene)
- **Built upon** your current 7/10 energy level goal
- **Aligned** with your values: health, family, financial security
- **Respected** your moderate coaching preference and detailed communication style

### 📊 **Updated Goal Files**
- **Short-term goals** now include specific 10lb weight loss and $3k car purchase
- **Medium-term goals** updated to reflect fitness routine evolution
- **All goals** have detailed tracking metrics and timelines

## 🎉 **Your Next Steps**
1. **Week 1 Actions:** Set up budget tracking, schedule first 3 workouts, take baseline measurements
2. **Car Research:** Start looking at vehicles in your $3k range
3. **Family Discussion:** Share the plan with your spouse for support
4. **Track Progress:** Weekly weigh-ins and financial check-ins

The plan is designed to work with your busy life as a software engineer and family person, while being ambitious enough to create real transformation. You've got this! 💪

Would you like me to explain any part of the plan in more detail or help you get started with the first week's action items?


## Multi-subagent Relationships Diagram



```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER REQUEST                                        │
│         "Create a 90-day action plan to be a better person"                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 LIFE COACH (Coordinator)                            │
│                         Claude Sonnet (Primary LLM)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│  TOOLS:                          │  CAPABILITIES:                               │
│  • write_todos                   │  • Breaks down complex requests              │
│  • update_todo                   │  • Delegates to specialist subagents         │
│  • list_todos                    │  • Coordinates workflow across domains       │
│  • get_next_todos                │  • Manages planning phases                   │
│  • get_user_profile              │  • Accesses long-term memory                 │
│  • save_user_preference          │  • Loads skills on demand                    │
│  • load_skill                    │                                              │
│  • File tools (ls, read, write)  │                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
    ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
    │  PHASE MANAGEMENT │ │  CONTEXT MEMORY   │ │  SKILL LOADING    │
    ├───────────────────┤ ├───────────────────┤ ├───────────────────┤
    │ 🔍 ASSESSMENT     │ │ 📁 profile/       │ │ 📚 26 Skills      │
    │ 🔎 DISCOVERY      │ │ 📁 goals/         │ │    available      │
    │ 📋 PLANNING       │ │ 📁 progress/      │ │    on-demand      │
    │ ⚡ EXECUTION      │ │ 📁 preferences/   │ │                   │
    └───────────────────┘ └───────────────────┘ └───────────────────┘
                                      │
                                      ▼
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   💼 CAREER COACH   │   │  💰 FINANCE COACH   │   │ 🤝 RELATIONSHIP     │
│                     │   │                     │   │       COACH         │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   🏃 WELLNESS COACH │   │  🌐 SHARED PATTERNS │   │                     │
│                     │   │   (coaching/        │   │                     │
│                     │   │    patterns/)       │   │                     │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
```

---

## Subagent Detail View

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 LIFE COACH (Coordinator)                            │
│                              Model: Claude Sonnet                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                              SPECIALIST SUBAGENTS                              │
│                            (All use GPT-4o-mini)                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│      💼 CAREER COACH            │  │     💰 FINANCE COACH            │
│         (3 specialists)         │  │        (3 specialists)          │
├─────────────────────────────────┤  ├─────────────────────────────────┤
│                                 │  │                                 │
│  📌 jobsearch-specialist        │  │  📌 budgeting-specialist        │
│     • Job search strategies     │  │     • Budget creation           │
│     • Resume optimization       │  │     • Expense tracking          │
│     • Interview preparation     │  │     • Cash flow management      │
│                                 │  │                                 │
│  📌 skilldevelopment-specialist │  │  📌 saving-specialist           │
│     • Learning strategies       │  │     • Emergency funds           │
│     • Skill gap analysis        │  │     • Savings strategies        │
│     • Certification guidance    │  │     • High-yield optimization   │
│                                 │  │                                 │
│  📌 professionalgrowth-specialist│ │  📌 financialgoals-specialist   │
│     • Career advancement        │  │     • Financial planning        │
│     • Leadership development    │  │     • Retirement planning       │
│     • Professional branding     │  │     • Debt payoff strategies    │
│                                 │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘

┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│    🤝 RELATIONSHIP COACH        │  │      🏃 WELLNESS COACH          │
│         (3 specialists)         │  │        (3 specialists)          │
├─────────────────────────────────┤  ├─────────────────────────────────┤
│                                 │  │                                 │
│  📌 communication-specialist    │  │  📌 exercise-specialist         │
│     • Active listening          │  │     • Workout programming       │
│     • Conflict resolution       │  │     • Exercise form & safety    │
│     • Assertive communication   │  │     • Progressive overload      │
│                                 │  │                                 │
│  📌 boundaries-specialist       │  │  📌 nutrition-specialist        │
│     • Boundary setting          │  │     • Meal planning             │
│     • Handling violations       │  │     • Macro/micronutrients      │
│     • Self-advocacy             │  │     • Dietary restrictions      │
│                                 │  │                                 │
│  📌 socialconnections-specialist│  │  📌 mindfulness-specialist      │
│     • Building friendships      │  │     • Stress reduction          │
│     • Networking strategies     │  │     • Sleep optimization        │
│     • Community building        │  │     • Meditation & breathing    │
│                                 │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

---

## Skills by Domain

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              📚 SKILLS LIBRARY                                   │
│                           (26 skills total)                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│      💼 CAREER SKILLS (7)       │  │     💰 FINANCE SKILLS (5)       │
├─────────────────────────────────┤  ├─────────────────────────────────┤
│  • resume-optimization          │  │  • budget-creation              │
│  • interview-preparation        │  │  • expense-reduction            │
│  • linkedin-optimization        │  │  • emergency-fund               │
│  • learning-path-design         │  │  • debt-payoff                  │
│  • skill-gap-assessment         │  │  • financial-goals              │
│  • career-roadmap               │  │                                 │
│  • leadership-development       │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘

┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│   🤝 RELATIONSHIP SKILLS (5)    │  │    🏃 WELLNESS SKILLS (9)       │
├─────────────────────────────────┤  ├─────────────────────────────────┤
│  • difficult-conversations      │  │  • wellness-assessment          │
│  • conflict-resolution          │  │  • meal-planning                │
│  • boundary-setting             │  │  • fitness-program              │
│  • networking-strategy          │  │  • exercise-routine             │
│  • social-confidence            │  │  • stress-management            │
│                                 │  │  • sleep-optimization           │
│                                 │  │  • mindfulness-practice         │
│                                 │  │  • health-habits                │
│                                 │  │  • emotional-wellness           │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

---

## Request Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST FLOW                                     │
└──────────────────────────────────────────────────────────────────────────────┘

    USER                    LIFE COACH                 SPECIALISTS
      │                         │                           │
      │  "Help me retire by 60" │                           │
      │────────────────────────▶│                           │
      │                         │                           │
      │                    ┌────┴────┐                      │
      │                    │ PHASE 1 │                      │
      │                    │ASSESSMENT                      │
      │                    └────┬────┘                      │
      │                         │                           │
      │                    Read user profile                │
      │                    Understand context               │
      │                         │                           │
      │                    ┌────┴────┐                      │
      │                    │ PHASE 2 │                      │
      │                    │DISCOVERY│                      │
      │                    └────┬────┘                      │
      │                         │                           │
      │                    Identify: Finance Coach needed   │
      │                    Skills: financial-goals,         │
      │                           emergency-fund            │
      │                         │                           │
      │                    ┌────┴────┐                      │
      │                    │ PHASE 3 │                      │
      │                    │PLANNING │                      │
      │                    └────┬────┘                      │
      │                         │                           │
      │                    Create todo list                 │
      │                    Assign to specialists            │
      │                         │                           │
      │                    ┌────┴────┐                      │
      │                    │ PHASE 4 │                      │
      │                    │EXECUTION│                      │
      │                    └────┬────┘                      │
      │                         │                           │
      │                         │──────────────────────────▶│
      │                         │    task("Calculate        │
      │                         │     retirement savings")  │
      │                         │                           │
      │                         │    financialgoals-        │
      │                         │    specialist works       │
      │                         │◀──────────────────────────│
      │                         │    Returns analysis       │
      │                         │                           │
      │                         │──────────────────────────▶│
      │                         │    task("Create savings   │
      │                         │     plan")                │
      │                         │                           │
      │                         │    saving-specialist      │
      │                         │    works                  │
      │                         │◀──────────────────────────│
      │                         │    Returns plan           │
      │                         │                           │
      │◀────────────────────────│                           │
      │  Complete retirement     │                           │
      │  plan with action steps  │                           │
      │                         │                           │
```

---

## Memory Architecture (CoALA Framework)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          MEMORY ARCHITECTURE                                  │
│                     (Aligned with CoALA Framework)                            │
└──────────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────────────┐
    │                        🧠 SHORT-TERM MEMORY                            │
    │                   (InMemoryStore, session-scoped)                      │
    ├───────────────────────────────────────────────────────────────────────┤
    │                                                                        │
    │   short_term_store = InMemoryStore()                                   │
    │                                                                        │
    │   Namespace: (thread_id, "messages")                                   │
    │   ┌──────────────────────────────────────────────────────────────┐    │
    │   │  thread_id: uuid4()     ◄── Unique per conversation          │    │
    │   │  user_id: "user_alex"   ◄── Links to long-term profile       │    │
    │   │                                                              │    │
    │   │  Keys:                                                       │    │
    │   │  • user_input       → {role, content, timestamp}             │    │
    │   │  • assistant_response → {role, content, timestamp}           │    │
    │   └──────────────────────────────────────────────────────────────┘    │
    │                                                                        │
    │   Lifecycle: Created at session start, discarded when session ends    │
    │                                                                        │
    └───────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Links to
                                    ▼
    ┌───────────────────────────────────────────────────────────────────────┐
    │                        📁 LONG-TERM MEMORY                             │
    │                   (Filesystem-backed, persistent)                      │
    └───────────────────────────────────────────────────────────────────────┘
```

---

## Context Management (Long-Term Storage)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          CONTEXT MANAGEMENT                                   │
└──────────────────────────────────────────────────────────────────────────────┘

    advanced_build/
    │
    ├── user_alex/                          ◄── Per-User Context
    │   │
    │   ├── profile/                        ◄── (user_id, "profile")
    │   │   ├── demographics.json               Demographics, values
    │   │   ├── values.json                     Life situation
    │   │   └── life_situation.json
    │   │
    │   ├── goals/                          ◄── (user_id, "goals")
    │   │   ├── short_term.json                 0-3 months
    │   │   ├── medium_term.json                3-12 months
    │   │   └── long_term.json                  1-5+ years
    │   │
    │   ├── progress/                       ◄── (user_id, "progress")
    │   │   ├── milestones.json                 Achievements
    │   │   ├── setbacks.json                   Learnings
    │   │   └── week_N_checkin.json             Weekly reviews
    │   │
    │   ├── preferences/                    ◄── (user_id, "preferences")
    │   │   ├── communication.json              Style, tone
    │   │   ├── coaching.json                   Approach
    │   │   └── learning.json                   Learning style
    │   │
    │   ├── assessments/                        Completed assessments
    │   ├── plans/                              Active & archived plans
    │   └── resources/                          Curated resources
    │
    └── coaching/                           ◄── Global Context
        └── patterns/                       ◄── ("coaching", "patterns")
            └── learned_patterns.json           Anonymized cross-user patterns
```

---

## Technology Stack

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            TECHNOLOGY STACK                                   │
└──────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                           ORCHESTRATION                                  │
    │                                                                          │
    │    deepagents          LangGraph          LangChain                     │
    │    ┌─────────┐         ┌─────────┐        ┌─────────┐                   │
    │    │ create_ │         │ state   │        │ tools   │                   │
    │    │ deep_   │◀───────▶│ machine │◀──────▶│ prompts │                   │
    │    │ agent   │         │         │        │ chains  │                   │
    │    └─────────┘         └─────────┘        └─────────┘                   │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                              MODELS                                      │
    │                                                                          │
    │    ┌──────────────────────┐        ┌──────────────────────┐             │
    │    │   Claude Sonnet      │        │    GPT-4o-mini       │             │
    │    │   (Coordinator)      │        │    (Specialists)     │             │
    │    │                      │        │                      │             │
    │    │   • Complex reasoning│        │   • Fast responses   │             │
    │    │   • Planning         │        │   • Cost-effective   │             │
    │    │   • Coordination     │        │   • Domain-specific  │             │
    │    └──────────────────────┘        └──────────────────────┘             │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                            STORAGE                                       │
    │                                                                          │
    │    ┌──────────────────┐    ┌──────────────────┐    ┌────────────────┐   │
    │    │ FilesystemBackend│    │  TODO_STORE      │    │ Skills (MD)    │   │
    │    │ (workspace/)     │    │  (in-memory)     │    │ (skills/)      │   │
    │    │ LONG-TERM        │    │                  │    │ PROCEDURAL     │   │
    │    └──────────────────┘    └──────────────────┘    └────────────────┘   │
    │                                                                          │
    │    ┌──────────────────────────────────────────────────────────────────┐ │
    │    │                    SHORT-TERM MEMORY                             │ │
    │    │  short_term_store = InMemoryStore()                              │ │
    │    │  Namespace: (thread_id, "messages") → user_input, assistant_resp │ │
    │    └──────────────────────────────────────────────────────────────────┘ │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

---

## Namespace Strategy

| Category            | Namespace Pattern                  | Example                              | Persistence Scope |
|---------------------|-----------------------------------|--------------------------------------|-------------------|
| Conversation        | `(thread_id, "messages")`         | `("abc-123-uuid", "messages")`       | **Single session only** (discarded after thread ends) |
| User Profile        | `(user_id, "profile")`            | `("user_alex", "profile")`           | **Cross-session, same user** (long-lived, personal) |
| User Goals          | `(user_id, "goals")`              | `("user_alex", "goals")`             | **Cross-session, same user** (long-lived, personal) |
| User Progress       | `(user_id, "progress")`           | `("user_alex", "progress")`          | **Cross-session, same user** (long-lived, personal) |
| User Preferences    | `(user_id, "preferences")`        | `("user_alex", "preferences")`       | **Cross-session, same user** (long-lived, personal) |
| Coaching Patterns   | `("coaching", "patterns")`        | Shared learned patterns              | **Cross-session, multi-user** (affects future users) |
