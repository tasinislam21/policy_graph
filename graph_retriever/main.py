from langchain.chains import GraphCypherQAChain
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from KG.config import load_neo4j_graph
from LLM.prompt import retrieval_qa_chat_prompt
import argparse
from langchain_core.output_parsers import StrOutputParser
graph = load_neo4j_graph()

parser = argparse.ArgumentParser(
                    prog='Graph LLM')
parser.add_argument('-v', '--verbose', default=True)
args = parser.parse_args()

# Create LLM instance to be reused
llm = ChatOllama(model="llama3:8b", temperature=0)
# Create conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a router chain to determine the type of request
router_template = """
You are an assistant that helps determine how to handle user queries.
Based on the conversation history and the current question, determine if the query:
1. Requires querying a graph database about a crime e.g. "How do I start a crime investigation" (GRAPH_QUERY)
2. Is a general conversation question (CONVERSATION)

Chat History:
{chat_history}

Current question: {question}

RESPONSE_TYPE:
"""

router_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=router_template
)

router_chain = router_prompt | llm | StrOutputParser()

# Create a conversation chain for non-database questions
conversation_template = """
You are a helpful assistant engaging in a conversation.

Chat History:
{chat_history}

Current question: {question}

Your response:
"""

conversation_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=conversation_template
)

cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template=retrieval_qa_chat_prompt
    )

conversation_chain = conversation_prompt | llm | StrOutputParser()


# Create the graph query chain
cypher_chain = GraphCypherQAChain.from_llm(
        ChatOllama(model="llama3:8b", temperature=0),
        graph=graph,
        verbose=args.verbose,
        cypher_prompt=cypher_prompt,
        allow_dangerous_requests=True  # Acknowledge the risks here.
    )

# Function to get chat history as a string
def get_chat_history(memory):
    chat_history = ""
    for message in memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            chat_history += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            chat_history += f"AI: {message.content}\n"
    return chat_history


# Conversational loop
print("Welcome! I can answer questions about the graph database or have a general conversation. Type 'exit' to quit.")

while True:
    # Get user input
    question = input("\nYou: ")

    # Check for exit command
    if question.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    # Add user question to memory
    memory.chat_memory.add_user_message(question)

    # Determine how to handle the question
    chat_history = get_chat_history(memory)
    response_type = router_chain.run(chat_history=chat_history, question=question)

    try:
        if "GRAPH_QUERY" in response_type:
            # Use the graph database
            result = cypher_chain.invoke(question)
            answer = result
            print(f"\nAI: {answer}")

        else:
            # Default to conversation if classification is unclear
            response = conversation_chain.run(chat_history=chat_history, question=question)
            print(f"\nAI: {response}")
            answer = response

        # Add AI response to memory
        memory.chat_memory.add_ai_message(answer)

    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}"
        print(f"\nAI: {error_msg}")
        memory.chat_memory.add_ai_message(error_msg)