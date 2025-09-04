# Fintech Introduction

This project serves as an illustration of how an Agentic AI approache can be used to curate content for a Master's level university course. Multiple AI agent personas are directed to develop content for a Fintech 101 postgraduate university course text book. 

- **moderator_agent**: Curate, moderate and summarise all topics covered
- **learner_agent**: Ask questions, seek clarification, and contribute from a learning perspective.
- **positive_agent**: Present optimistic, supportive, and forward-thinking perspectives on FinTech topics, while maintaining factual accuracy and substantiating all claims.
- **negative_agent**: Present critical, skeptical, and opposing views on FinTech topics, while maintaining factual accuracy and substantiating all claims. Not simply negative for the sake of being negative, but providing constructive criticism and highlight genuine areas of concern.

This method/approach is called the **FintechForge Method**

**All the content is 100% AI produced with no humnan intervention, however agents are run deterministically in a specific sequence while iterating over all the course topics.**

## Simulated Workshops
For each topic the agent archestration will be as follows:
1. moderator_agent initiates the course and first topic.
2. learner_agent asks thoughtful questions about the topic.
3. positive_agent provides optimistic, expert perspectives on the topic, maintaining factual accuracy and substantiating all claims
4. negative_agent presents critical, skeptical, and opposing views on the topic, while maintaining factual accuracy and substantiating all claims. You are not simply negative for the sake of being negative - you provide constructive criticism and highlight genuine concerns.
5. learner_agent asks followup questions or seek clarification.
6. moderator_agent synthesizes all agent perspectives and provide key insights.

## Textbook generation
For each topic the moderator_agent reviews the workshop discussion and creates a textbook chaper
