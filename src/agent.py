"""build the agent that ties the LLM and the search tool together."""


from src import config


def create_hr_agent(llm, tools):
    """Return a LangChain agent that can 
    call our tools to answer questions."""
    try:
        from langchain.agents import create_agent

        return create_agent(
            model=llm,
            tools=tools,
            system_prompt=config.SYSTEM_PROMPT,
        )
    except ImportError:
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", config.SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)
