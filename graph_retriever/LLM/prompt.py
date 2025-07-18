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
MATCH (:Crime {type: "burglary"})-[:HAS_CHECKLIST]->(c:Checklist)-[:HAS_CHUNK]->(ChunkInfo:Chunk)
WHERE c.type="Intelligence" OR c.type="Suspects" 
RETURN ChunkInfo.StepID, ChunkInfo.text

Help:
This is all existing property for Node Crime and Node Checklist:

Node Crime Properties: (will be adding more crimes in the future)
    type: "burglary" 

Node Checklist Properties:
    type: "Victims and Witnesses" (Use this if the questions is related to witness and victim)
    type: "Scene"
    type: "Suspects"
    type: "Intelligence"
Node Person Properties:

    name: "Talleyrand"
    name: "Napoleon"

Node Section Properties:

    parent_name: "Battle_of_Waterloo"
    type: "Consequence"

    parent_name: "Battle_of_Waterloo"
    type: "General Information"

    parent_name: "Battle_of_Waterloo"
    type: "Reason"

    parent_name: "Battle_of_Waterloo"
    type: "Combatant"

    parent_name: "Talleyrand"
    type: "Career"

    parent_name: "Talleyrand"
    type: "Death"

    parent_name: "Talleyrand"
    type: "General Information"

    parent_name: "Napoleon"
    type: "Career"

    parent_name: "Napoleon"
    type: "Death"

    parent_name: "Napoleon"
    type: "General Information"

The question is:
{question}"""

