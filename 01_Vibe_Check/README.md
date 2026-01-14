<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Introduction and Vibe Check</h1>

### [Quicklinks](https://github.com/AI-Maker-Space/AIE9/tree/main/00_AIE_Quicklinks)

| 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Vibe Check!](https://github.com/AI-Maker-Space/AIE9/blob/main/00_Docs/Session_Sheets/01_Vibe%20Check.md) | Coming Soon! | Coming Soon! | You are here! | Coming Soon! | Coming Soon! |

## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** – these will be questions that you will be expected to gather the answer to! These can appear as general questions, or questions meant to spark a discussion in your breakout rooms!

- 🏗️ **Activities** – these will be work or coding activities meant to reinforce specific concepts or theory components.

- 🚧 **Advanced Builds (optional)** – Take on a challenge! These builds require you to create something with minimal guidance outside of the documentation. Completing an Advanced Build earns full credit in place of doing the base assignment notebook questions/activities.

### Main Assignment

In the following assignment, you are required to take the app that you created for the AIE9 challenge (from [this repository](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge)) and conduct what is known, colloquially, as a "vibe check" on the application.

You will be required to submit a link to your GitHub, as well as screenshots of the completed "vibe checks" through the provided Google Form!

> NOTE: This will require you to make updates to your personal class repository, instructions on that process can be found [here](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Prerequisites/Initial_Setup)!


#### A Note on Vibe Checking

>"Vibe checking" is an informal term for cursory unstructured and non-comprehensive evaluation of LLM-powered systems. The idea is to loosely evaluate our system to cover significant and crucial functions where failure would be immediately noticeable and severe.
>
>In essence, it's a first look to ensure your system isn't experiencing catastrophic failure.

---

#### 🏗️ Activity #1: General Vibe Checking Evals

Please evaluate your system on the following questions:

1. Explain the concept of object-oriented programming in simple terms to a complete beginner.
    - Aspect Tested: Gave a one page answer, pretty thorough on the overall concepts.  Not a bad result.
2. Read the following paragraph and provide a concise summary of the key points…
    - Aspect Tested: Passed it a paragraph about the band "Phish". It made a more concise summary but not completely.  So I asked it "make it a bullet list" but then it had no idea what I was talking about.  I never implemented conversations or memory so this makes sense, its purely one-shot at this point, has no concept of longer conversations
3. Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.
    - Aspect Tested:
In a bustling city filled with towering skyscrapers, a lonely robot named Pixel roamed the streets. Day after day, it tirelessly cleaned litter and repaired broken streetlights, but each evening, it returned to its empty garage, longing for connection.

One rainy afternoon, while mopping the park, Pixel noticed a small, shivering puppy tucked beneath a bench. The puppy looked up with big, pleading eyes. Pixel, with its gentle mechanical fingers, reached out to the little creature, offering warmth and companionship.

To its surprise, the puppy snuggled against Pixel's metal leg, and in that moment, a spark ignited. Pixel felt a flicker of joy and purpose it had never known. Each day, they explored the city together—Pixel learned to laugh through wagging tails, and the puppy found solace in the rhythm of whirring gears.

In an unexpected friendship, they created a bond that turned solitude into adventure, proving love can flourish in the most unlikely of places.

-- THOUGHTS:
Its not bad.. its a story.. you dont 'Mop the park', but otherwise decent.  Its pretty cliche, but I guess thats what I asked for.

4. If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?
    - Aspect Tested:
To find out how many packs of apples and oranges you need to buy, you can set up the following equations based on the information given:

1. For apples: You need 12 apples and each pack contains 4 apples.
   \[
   \text{Number of packs of apples} = \frac{12 \text{ apples}}{4 \text{ apples per pack}} = 3 \text{ packs}
   \]

2. For oranges: You need 9 oranges and each pack contains 3 oranges.
   \[
   \text{Number of packs of oranges} = \frac{9 \text{ oranges}}{3 \text{ oranges per pack}} = 3 \text{ packs}
   \]

So, you need to buy **3 packs of apples** and **3 packs of oranges** to get exactly 12 apples and 9 oranges.

-- THOUGHTS:
* the answer is UGLY..  its doing some math out loud, but just placing it on the screen.  I love its showing its work, but since its trying to use some text formatting.. maybe thats markdown, and I haven't enabled a markdown parser in the front-end it looks bad
* The answer is factually accurate and work is shown so thats good

5. Rewrite the following paragraph in a professional, formal tone…
    - Aspect Tested:
I fed the puppy story.. 
In a vibrant urban environment characterized by its imposing skyscrapers, an isolated robotic entity known as Pixel traversed the streets. Daily, Pixel dedicated itself to the meticulous tasks of litter removal and the maintenance of malfunctioning streetlights; however, each evening concluded with its return to an unoccupied garage, accompanied by a profound yearning for connection.

On a particularly rainy afternoon, while engaged in the task of mopping the park, Pixel observed a small, trembling puppy seeking refuge beneath a bench. The puppy gazed upward, its large, imploring eyes reflecting a longing for companionship. In a moment of tenderness, Pixel extended its gentle mechanical appendage towards the small creature, offering warmth and a sense of belonging.

To Pixel's astonishment, the puppy nestled against its metallic leg, igniting a newfound spark within the robot. For the first time, Pixel experienced a flicker of joy and a sense of purpose that had long eluded it. Together, they ventured through the city each day—Pixel discovered the exuberance of mirth through the puppy's wagging tail, while the puppy found comfort in the rhythmic sounds of Pixel's whirring mechanisms.

Through this unexpected companionship, they forged a bond that transformed isolation into adventure, illustrating that love can indeed flourish in the most unforeseen circumstances.

--THOUGHTS
* its still mopping the park :(
* It is more formal
* vocaulbary is up a notch..   'mechanical appendage', 'exuberance of mirth'... etc.

#### ❓Question #1:

Do the answers appear to be correct and useful?
##### ✅ Answer:
* the answers all appear to be correct
* the markdown formatting on the math problem is an issue
* the lack of memory of prior conversations is an issue
* theres no sense of 'thinking' since the answers are being passed back in one blob and we didnt implement that
* also the text doesn't gracefully 'slowly load' to the user.. so some sort of streaming to make the text read-in is a nice UI/UX help
* Theres no control plane to upload files, connect to MCP, all the bells/whistles arent there

---

#### 🏗️ Activity #2: Personal Vibe Checking Evals (Your Assistant Can Answer)

Now test your assistant with personal questions it should be able to help with. Try prompts like:

- "Help me think through the pros and cons of [enter decision you're working on making]."
- "What are the pros and cons of [job A] versus [job B] as the next step in my career?"
- "Draft a polite follow-up [email, text message, chat message] to a [enter person details] who hasn't responded."
- "Help me plan a birthday surprise for [person]."
- "What can I cook with [enter ingredients] in fridge."

##### Your Prompts and Results:
1. Prompt: Help me think through the pros and cons of starting DBT therapy vs CBT therapy
   - Result:
Absolutely, it’s great that you’re considering your options for therapy. Both Dialectical Behavior Therapy (DBT) and Cognitive Behavioral Therapy (CBT) are effective approaches, but they serve different needs and can have distinct benefits and challenges. Let’s break down the pros and cons of each.

### DBT Therapy

**Pros:**
1. **Emotional Regulation:** DBT is specifically designed to help individuals regulate emotions and navigate intense feelings, making it beneficial for those with mood disorders or emotional dysregulation.
2. **Mindfulness Component:** DBT incorporates mindfulness practices, which can enhance self-awareness and promote a sense of calm in the face of distress.
3. **Interpersonal Effectiveness:** It teaches skills for improving relationships and setting boundaries, which can be helpful for individuals struggling with interpersonal issues.
4. **Focus on Validation:** DBT emphasizes the importance of both acceptance and change, which can be validating for clients who often feel misunderstood.
5. **Supportive Environment:** DBT often includes group therapy components that foster community and support among participants.

**Cons:**
1. **Time-Intensive:** DBT can require a significant time commitment, often including both individual and group therapy sessions.
2. **Structured Program:** The structured nature might feel rigid for some individuals, especially if they prefer a more flexible approach.
3. **Availability:** Depending on your location, finding a qualified DBT therapist may be more challenging than with CBT.
4. **Cost:** DBT may involve a longer duration of treatment, which can increase costs compared to shorter-term therapies.

### CBT Therapy

**Pros:**
1. **Shorter Duration:** CBT typically involves fewer sessions than DBT, making it more time-efficient for those seeking quicker support.
2. **Structured Framework:** The structured approach can help clients learn practical skills and strategies to address specific problems and change negative thought patterns.
3. **Proven Effectiveness:** CBT is well-established and has a strong evidence base for treating a variety of conditions, including anxiety, depression, and PTSD.
4. **Flexibility:** CBT can be tailored to a wide range of issues and is adaptable to individual preferences and needs.
5. **Focus on Specific Problems:** It is problem-focused and goal-oriented, allowing you to directly address and manage specific issues.

**Cons:**
1. **Limited Focus on Emotion:** While CBT addresses thoughts and behaviors, it may not delve deeply into emotional regulation or interpersonal skills as extensively as DBT.
2. **Self-Directed:** It often requires clients to actively engage in homework and practice, which can be a challenge for those who prefer guided support.
3. **Not for Everyone:** Some individuals might find CBT’s focus on cognition less helpful if they have not developed sufficient skills for emotional awareness.

### Conclusion

When considering whether to pursue DBT or CBT, reflect on your specific struggles and goals. If you're looking for support around emotional regulation, interpersonal relationships, and mindfulness, DBT might be more suitable. Conversely, if you have specific cognitive challenges or prefer a shorter-term intervention focused on particular problems, CBT could be a better fit.

Ultimately, it might also be helpful to talk to a mental health professional who can assess your needs and preferences to guide you towards the best therapeutic approach. Remember, choosing the right therapy is a personal journey, and it’s perfectly okay to explore different options before committing.

-- THOUGHTS:
* pretty good comparison. on target..

2. Prompt: I have a Turkey leg, cinnamon,  ice cream, GF flour, kiwi fruit, carrots, celery, onions, salt, pepper and all sorts of BBQ, soy, buffalo sauces in the fridge.. can you come up with a Gluten Free dinner and dessert
   - Result:
Absolutely! You have some great ingredients to work with. Here’s a suggestion for a delicious, gluten-free dinner and dessert:

### Dinner: BBQ Turkey Leg with Roasted Veggies

**Ingredients:**
- Turkey leg
- BBQ sauce (your choice)
- Carrots, celery, and onions
- Salt and pepper
- Olive oil or any cooking oil you have

**Instructions:**
1. **Preheat your oven** to 375°F (190°C).
2. **Prepare the Turkey Leg**: Rub the turkey leg with salt, pepper, and a generous amount of your BBQ sauce. Let it marinate for a bit if you have time.
3. **Chop the Vegetables**: Chop the carrots, celery, and onions into bite-sized pieces. 
4. **Season the Vegetables**: In a bowl, toss the chopped vegetables with olive oil, salt, and pepper.
5. **Bake**: Place the turkey leg on a baking sheet or dish. Scatter the seasoned veggies around it. Roast in the oven for about 45-60 minutes or until the turkey is cooked and reaches an internal temperature of 165°F (75°C). You may want to brush some extra BBQ sauce on the turkey leg halfway through cooking for extra flavor.
   
### Dessert: Cinnamon Kiwi Ice Cream Sundae

**Ingredients:**
- Ice cream (your choice)
- Kiwi fruit
- Cinnamon
- Optional: a drizzle of honey or agave (if you have it)

**Instructions:**
1. **Prepare the Kiwi**: Peel and slice the kiwi fruit.
2. **Serve Ice Cream**: In a bowl, scoop your ice cream.
3. **Add Kiwi**: Top the ice cream with the fresh kiwi slices.
4. **Sprinkle Cinnamon**: Lightly dust the top with cinnamon.
5. **Drizzle Optional Sweetener**: If you want, a drizzle of honey or agave adds extra sweetness.

### Enjoy your dinner and dessert!

This meal combines savory and sweet elements that should work well together while staying gluten-free. Enjoy cooking and your time at the table!

3. Prompt:  Plan a birthday surprise for Marge.  She is an Opera singer who works at the zoo, owns 10 snakes is a great cook and is extremely artistic and creative.
   - Result:
What a wonderful opportunity to celebrate Marge's unique personality and interests! Here’s a birthday surprise plan that incorporates her love for opera, animals, cooking, and creativity:

### **Theme:** "A Night at the Zoo"

#### **1. Venue Decoration:**
- **Location:** Host the surprise at a local park or even in your backyard, if possible, to mimic the zoo environment.
- **Theme Décor:** Decorate with animal prints, greenery, and perhaps some tasteful snake motifs. Use fairy lights to create a magical atmosphere.

#### **2. Invitations:**
- **Design:** Create invitations shaped like musical notes or animals. You can send them digitally or hand-deliver them for a personal touch.
- **Instruction:** Let guests know to come dressed as their favorite animal or in creative costumes.

#### **3. Celebrate with Music:**
- **Opera Performance:** Arrange for a surprise mini-opera performance featuring some of Marge’s favorite pieces, performed by friends or local artists. If possible, recruit a few of Marge's colleagues from the opera scene to join in.
- **Karaoke Booth:** Set up an area for opera karaoke where everyone can sing their hearts out, including Marge! 

#### **4. Creative Stations:**
- **Art Corner:** Set up a creative corner with canvases, paint, and art supplies where guests can create their own animal-themed art. 
- **Snake Display:** Have a comfortable and safe area to showcase a few of Marge’s snakes, educating guests on snake care and even allowing for a gentle meet-and-greet.

#### **5. Culinary Delights:**
- **Cooking Challenge:** Organize a fun cooking challenge with some of her recipes. Each guest can prepare one dish in small teams, and Marge can judge them.
- **Themed Cake:** Order or bake a cake that reflects her love for snakes and opera - perhaps a cake decorated with musical notes and snakes entwined around it.

#### **6. Tailored Gifts:**
- **Personalized Gift:** Create a scrapbook filled with memories from friends and family, including photos and notes about how Marge has touched their lives.
- **Art Supplies:** Gift her some high-quality art supplies or a cooking class to further explore her creative passions.

#### **7. Closing Ceremony:**
- **Toast:** End the evening with a lovely toast, expressing gratitude for Marge and her passions.
- **Final Surprise:** Consider a special reveal for an outdoor movie setup featuring an opera-themed film or a nature documentary that incorporates some of the zoo’s animals.

This birthday surprise not only celebrates Marge's interests but also brings her loved ones together for a memorable experience filled with joy, creativity, and love. Enjoy the celebration!   

#### ❓Question #2:

Are the vibes of this assistant's answers aligned with your vibes? Why or why not?
##### ✅ Answer:
 Answers are pretty solid.  
* The DBT/CBT distnction is on point
* The menu is not inventive, but it is not ridiculous either.  
** it didnt try to make me cook the kiwi or drizzle it with soy sauce.  
** It kindof ignored my Gluten Free notes though so I would have loved more care here (BBQ sauce has to be GF..  ice cream has to be GF... etc..)
* Marge's birthday..  its a lot of great ideas, way too much for my liking, but i can always pick and choose.  Opera singers may do Kareoke, but in general they sing for a living and dont like to do such things in their freetime.

---

#### 🏗️ Activity #3: Personal Vibe Checking Evals (Requires Additional Capabilities)

Now test your assistant with questions that would require capabilities beyond basic chat, such as access to external tools, APIs, or real-time data. Try prompts like:

- "What does my schedule look like tomorrow?"
- "What time should I leave for the airport?"

##### Your Prompts and Results:
1. Prompt: What does my schedule look like tomorrow?
   - Result:
   I’m unable to access your personal schedule or calendar. However, I can help you create or review your schedule for tomorrow! Do you have specific tasks or commitments you need to include? Let’s make sure you’re prepared and organized for a great day!


2. Prompt: What time should I leave for the airport?
   - Result:
To determine what time you should leave for the airport, consider the following factors:

1. **Flight Time**: What time is your flight scheduled to depart?
2. **Airport Arrival Time**: It's generally recommended to arrive at the airport at least 2 hours before a domestic flight and 3 hours before an international flight.
3. **Travel Time to Airport**: How long does it usually take to get to the airport? Consider traffic conditions and the time of day.
4. **Additional Time for Parking or Checking In**: If you're parking your car or checking bags, you may need to allow extra time for those activities.

Here's a simple formula to help you decide:

1. Flight departure time: **[insert time]**
2. Recommended airport arrival: **[insert 2 or 3 hours based on domestic/international]**
3. Travel time to airport: **[insert travel time]**

Add these times together to know when you should leave home. This way, you'll arrive stress-free and ready for your journey! If you provide specific details, I can help you with the calculations.

#### ❓Question #3:

What are some limitations of your application?
##### ✅ Answer:
* it has no access to my calendar to know appointments or flight time, or really anthing else
* it has no access to the web, to even know what today is.  it cant check if my flight is on-time or delayed, or what real travel time is
* it has no maps access to know how far away I am from the airport.

---

This "vibe check" now serves as a baseline, of sorts, to help understand what holes your application has.

### 🚧 Advanced Build (OPTIONAL):

Please make adjustments to your application that you believe will improve the vibe check you completed above, then deploy the changes to your Vercel domain [(see these instructions from your Challenge project)](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge/blob/main/README.md) and redo the above vibe check.

> NOTE: You may reach for improving the model, changing the prompt, or any other method.

#### 🏗️ Activity #1
##### Adjustments Made:
- _describe adjustment(s) here_

##### Results:
1. _Comment here how the change(s) impacted the vibe check of your system_
2.
3.
4.
5.


## Submitting Your Homework
### Main Assignment
Follow these steps to prepare and submit your homework:
1. Pull the latest updates from upstream into the main branch of your AIE9 repo:
    - For your initial repo setup see [Initial_Setup](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Prerequisites/Initial_Setup)
    - To get the latest updates from AI Makerspace into your own AIE9 repo, run the following commands:
    ```
    git checkout main
    git pull upstream main
    git push origin main
    ```
2. **IMPORTANT:** Start Cursor from the `01_Prototyping_Best_Practices_and_Vibe_Check` folder (you can also use the _File -> Open Folder_ menu option of an existing Cursor window)
3. Edit this `README.md` file (the one in your `AIE9/01_Prototyping_Best_Practices_and_Vibe_Check` folder)
4. Complete all three Activities:
    - **Activity #1:** Evaluate your system using the general vibe checking questions and define the "Aspect Tested" for each
    - **Activity #2:** Test your assistant with personal prompts it should be able to answer
    - **Activity #3:** Test your assistant with prompts requiring additional capabilities
5. Provide answers to all three Questions (`❓Question #1`, `❓Question #2`, `❓Question #3`)
6. Add, commit and push your modified `README.md` to your origin repository's main branch.

When submitting your homework, provide the GitHub URL to your AIE9 repo.

### The Advanced Build:
1. Follow all of the steps (Steps 1 - 6) of the Main Assignment above
2. Document what you changed and the results you saw in the `Adjustments Made:` and `Results:` sections of the Advanced Build
3. Add, commit and push your additional modifications to this `README.md` file to your origin repository.

When submitting your homework, provide the following on the form:
+ The GitHub URL to your AIE9 repo.
+ The public Vercel URL to your updated Challenge project on your AIE9 repo.
