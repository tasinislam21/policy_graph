retrieval_qa_chat_prompt = """
Task:Generate Cypher statement to query a graph database.

Instructions:
- Use only the provided relationship types and properties in the schema. 
- Do not use any other relationship types or properties that are not provided.
- Remember the relationships are like Schema: {schema}
- Don't filter based on property, only filter based on relationships and return any property that exists in it
- If you are not sure about the Section node property, just fetch all
Note: Do not include any explanations or apologies in your responses.
Do not include any text except the generated Cypher statement. Remember to correct the typo in names

Example 1: I am at a burglary scene, how do I begin my investigation?
MATCH (:Crime '{{type: "burglary"}}')-[:HAS_CHECKLIST]->(:Checklist '{{type: "generic"}}')-[:HAS_CHUNK]->(ChunkInfo:Chunk)
RETURN ChunkInfo.StepID, ChunkInfo.text

Example 2: I am at a burglary scene, how can I support the victim? How can they help with the investigation?
MATCH (:Crime '{{type: "burglary"}}')-[:HAS_CHECKLIST]->(:Checklist '{{type: "Victims and Witnesses"}}')-[:HAS_CHUNK]->(ChunkInfo:Chunk)
RETURN ChunkInfo.StepID, ChunkInfo.text

Example 3: I am at a burglary scene, the victim stated that they knew the suspect and made reports before. What should be my next step?
MATCH (:Crime '{{type: "burglary"}}')-[:HAS_CHECKLIST]->(c:Checklist)-[:HAS_CHUNK]->(ChunkInfo:Chunk)
WHERE c.type="Intelligence" OR c.type="Suspects" 
RETURN ChunkInfo.StepID, ChunkInfo.text

DO NOT USE SINGLE QUOTE ('') WHEN GENERATING CYPHER.
DO NOT USE DOUBLE CURLY BRACKET ({{}}) WHEN GENERATING CYPHER.
I had to use them because of python string formatting.
Provide your answer in full, especially when giving out steps.

Help:
This is all existing property for Node Crime and Node Checklist:

Node Crime Properties: (will be adding more crimes in the future)
    type: "burglary" 

Node Checklist Properties:
    type: "generic" 
    type: "Victims and Witnesses" 
    type: "Scene" (Use this if the questions is related to scene, entry and exit)
    type: "Suspects"
    type: "Intelligence" (Use this for answering questions like detail gathering, identifying linked series offending)

    DO NOT USE parent_type
    Feel free to use multiple node checklist
Node Chunk Properties:

    text
    StepID (order of the step)

The question is:
{question}"""

