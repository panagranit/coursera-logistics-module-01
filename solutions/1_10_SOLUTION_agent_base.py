"""
Innovate Logistics Agent Integration - SOLUTION

This is the completed solution for Activity 1.10, showing all TODOs filled in.

This script demonstrates the complete agent integration workflow:
1. Loading function specifications from JSON
2. Importing function implementations
3. Creating function mapping
4. Executing queries with OpenAI agent using Responses API
5. Testing with queries from 1_10_START_mock_queries.txt

Learning Context:
    This solution shows how to properly complete 1_10_START_agent_base.py by
    filling in all TODO sections with production-ready code.

Prerequisites:
    - OPENAI_API_KEY environment variable must be set
    - logistics_specs.json file (from Activity 1.3)
    - logistics_tools.py file (from Activity 1.3/1.7)
    - 1_10_START_mock_queries.txt for testing
"""

import os
import json
import logging
from typing import Dict, List, Any, Callable

# WHAT: Check for OpenAI API key before proceeding
# WHY: Provide clear error message if key is missing
# HOW: Check environment variable and exit gracefully if not found

if not os.environ.get("OPENAI_API_KEY"):
    print("\n" + "=" * 70)
    print("ERROR: OPENAI_API_KEY environment variable not set!")
    print("=" * 70)
    print("\nPlease set your OpenAI API key:")
    print("  export OPENAI_API_KEY='your-key-here'")
    print("\nThis activity requires a valid OpenAI API key to function.")
    print("=" * 70)
    exit(1)

# WHAT: Import OpenAI library for agent interaction
# WHY: Need OpenAI client to create and interact with agents
# HOW: Import from openai package

try:
    from openai import OpenAI
except ImportError:
    print("\n" + "=" * 70)
    print("ERROR: OpenAI library not installed!")
    print("=" * 70)
    print("\nPlease install the OpenAI library:")
    print("  pip install openai")
    print("=" * 70)
    exit(1)

# WHAT: Configure logging to see agent's function selection process
# WHY: Helps debug which functions the agent selects and why
# HOW: Set logging to INFO level with clear format

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# STEP 1: LOAD FUNCTION SPECIFICATIONS
# ==============================================================================

# WHAT: Load function specifications from JSON file
# WHY: Agent needs specs to understand when to use each function
# HOW: Read JSON file and parse into list of dictionaries

# SOLUTION: Complete implementation of JSON loading
logger.info("Loading function specifications...")

try:
    # WHAT: Open and parse the logistics_specs.json file
    # WHY: Contains the OpenAI function specifications for our 3 logistics functions
    # HOW: Use json.load() with file handle

    with open('logistics_specs.json', 'r') as f:
        function_specs = json.load(f)

    logger.info(f"✓ Successfully loaded {len(function_specs)} function specifications")

except FileNotFoundError:
    logger.error("Could not find logistics_specs.json in current directory")
    logger.error("Make sure you're running from the correct directory or adjust the path")
    exit(1)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in logistics_specs.json: {e}")
    exit(1)

# Log which functions were loaded
for spec in function_specs:
    logger.info(f"  - {spec['name']}")


# ==============================================================================
# STEP 2: IMPORT FUNCTION IMPLEMENTATIONS
# ==============================================================================

# WHAT: Import your actual function implementations
# WHY: Agent needs the actual Python functions to execute
# HOW: Import from your logistics_tools module

# SOLUTION: Import the three logistics functions
logger.info("Importing function implementations...")

try:
    # WHAT: Import all three logistics functions
    # WHY: These are the implementations that will be called by the agent
    # HOW: Standard Python import from logistics_tools module

    from logistics_tools import (
        get_tracking_status,
        check_inventory,
        calculate_delivery_days
    )

    logger.info("✓ Successfully imported all function implementations")

except ImportError as e:
    logger.error(f"Could not import logistics_tools: {e}")
    logger.error("Make sure logistics_tools.py is in the Python path")
    exit(1)

# WHAT: Create function mapping dictionary
# WHY: Allows us to look up Python functions by name from agent's function calls
# HOW: Dictionary with function names as keys, function objects as values

function_map = {
    "get_tracking_status": get_tracking_status,
    "check_inventory": check_inventory,
    "calculate_delivery_days": calculate_delivery_days,
}

logger.info(f"✓ Created function map with {len(function_map)} registered functions")


# ==============================================================================
# STEP 3: INITIALIZE OPENAI CLIENT
# ==============================================================================

# WHAT: Initialize OpenAI client with API key
# WHY: Required to create and interact with agents
# HOW: Create OpenAI client instance with key from environment variable

logger.info("Initializing OpenAI client...")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logger.info("✓ OpenAI client initialized successfully")


# ==============================================================================
# STEP 4: QUERY EXECUTION FUNCTION
# ==============================================================================

def execute_agent_query(query: str, verbose: bool = True) -> str:
    """
    Execute a query against the agent with custom functions.

    This function implements the complete function calling flow:
    1. Sends the query to the agent with available functions
    2. Agent analyzes which function(s) to call
    3. Executes the selected function(s) locally
    4. Sends results back to agent
    5. Returns the agent's natural language response

    Args:
        query: Natural language query from user
        verbose: Whether to log detailed information

    Returns:
        str: Agent's natural language response

    Note: This implementation handles the basic function calling pattern.
          In production, you would add:
          - Multiple sequential function calls
          - Error handling for API failures
          - Conversation history management
          - Rate limiting and retries
    """

    if verbose:
        logger.info(f"\n{'=' * 70}")
        logger.info(f"Query: {query}")
        logger.info(f"{'=' * 70}")

    # SOLUTION: Complete implementation of agent query with function calling

    try:
        # WHAT: Convert function specs to OpenAI tools format
        # WHY: OpenAI Responses API requires tools in specific format
        # HOW: Wrap each spec in {"type": "function", "function": spec}

        tools = []
        for spec in function_specs:
            tools.append({
                "type": "function",
                "function": spec
            })

        # System instructions for the agent
        instructions = (
            "You are a helpful assistant for Innovate Logistics. "
            "Use the provided functions to answer questions about "
            "package tracking, inventory, and delivery times. "
            "Always provide clear, friendly responses."
        )

        # WHAT: Create response with function calling enabled using Responses API
        # WHY: This is how we send queries to agent with custom functions
        # HOW: Use client.responses.create() with input, modalities, instructions, and tools

        response = client.responses.create(
            model="gpt-4o-mini",  # Cost-efficient model for demonstrations
            input=query,
            modalities=["text"],
            instructions=instructions,
            tools=tools
        )

        # Get the response output
        output = response.output[0]

        # WHAT: Check if agent wants to call functions
        # WHY: Agent may call one or more functions to answer the query
        # HOW: Check if output type is function_call

        # Collect all function calls from the output
        function_calls = []
        for item in response.output:
            if hasattr(item, 'type') and item.type == "function_call":
                function_calls.append(item)

        if function_calls:
            if verbose:
                logger.info(f"Agent selected {len(function_calls)} function(s) to call")

            # Prepare input array for second API call with function results
            input_items = []

            # WHAT: Execute each function call
            # WHY: Get actual results to send back to agent
            # HOW: Loop through function_calls, execute functions, build input items

            for function_call in function_calls:
                function_name = function_call.name
                function_args = json.loads(function_call.arguments)

                if verbose:
                    logger.info(f"\nFunction Call:")
                    logger.info(f"  Name: {function_name}")
                    logger.info(f"  Arguments: {json.dumps(function_args, indent=4)}")

                # WHAT: Execute the function
                # WHY: Get results to send back to agent
                # HOW: Look up function in map and call with parsed arguments

                if function_name in function_map:
                    function_to_call = function_map[function_name]
                    function_response = function_to_call(**function_args)

                    if verbose:
                        logger.info(f"  Result: {json.dumps(function_response, indent=4)}")

                    # WHAT: Add function result to input array
                    # WHY: Agent needs function results to synthesize final answer
                    # HOW: Append function_call_output with result

                    input_items.append({
                        "type": "function_call_output",
                        "call_id": function_call.call_id,
                        "output": json.dumps(function_response)
                    })
                else:
                    logger.error(f"Unknown function: {function_name}")
                    input_items.append({
                        "type": "function_call_output",
                        "call_id": function_call.call_id,
                        "output": json.dumps({
                            "success": False,
                            "error": f"Function {function_name} not found",
                            "error_type": "system"
                        })
                    })

            # WHAT: Get final response from agent
            # WHY: Agent synthesizes function results into user-friendly answer
            # HOW: Send function results back to API with previous_response_id to link context

            if verbose:
                logger.info("\nGetting final response from agent...")

            second_response = client.responses.create(
                model="gpt-4o-mini",
                previous_response_id=response.id,  # Link to original response with function calls
                input=input_items,
                modalities=["text"],
                instructions=instructions
            )

            final_answer = second_response.output[0].content[0].text

        else:
            # No function calls needed - agent answered directly
            if verbose:
                logger.info("Agent answered directly without function calls")
            final_answer = output.content[0].text

        if verbose:
            logger.info(f"\nFinal Response: {final_answer}")
            logger.info(f"{'=' * 70}\n")

        return final_answer

    except Exception as e:
        logger.error(f"Error during agent query: {e}")
        return f"Error: {str(e)}"


# ==============================================================================
# STEP 5: LOAD AND TEST WITH MOCK QUERIES
# ==============================================================================

def load_test_queries(filename: str = "1_10_START_mock_queries.txt") -> List[str]:
    """
    Load test queries from file.

    Args:
        filename: Name of file containing test queries

    Returns:
        List of query strings (excluding comments and blank lines)
    """

    # WHAT: Load queries from file
    # WHY: Need test queries to verify agent function selection
    # HOW: Read file, filter out comments and blank lines

    queries = []

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments (lines starting with #) and blank lines
                if line and not line.startswith('#'):
                    queries.append(line)

        logger.info(f"Loaded {len(queries)} test queries from {filename}")

    except FileNotFoundError:
        logger.warning(f"Could not find {filename}")
        logger.warning("Using default test queries instead")
        queries = [
            "What is the status of tracking code 123456789?",
            "How many units of SKU ABC1234 are in stock?",
            "How long will delivery take to zone 2 with standard service?",
        ]

    return queries


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("INNOVATE LOGISTICS AGENT INTEGRATION - SOLUTION")
    print("=" * 70)
    print("\nThis script demonstrates the complete agent integration workflow.")
    print("All TODOs from 1_10_START_agent_base.py have been filled in.")
    print("=" * 70)

    # WHAT: Load test queries
    # WHY: Need queries to test agent function selection
    # HOW: Call load_test_queries function

    test_queries = load_test_queries()

    # WHAT: Test with sample queries
    # WHY: Verify agent can select and execute functions correctly
    # HOW: Call execute_agent_query for each test query

    print("\n" + "=" * 70)
    print("TESTING AGENT WITH SAMPLE QUERIES")
    print("=" * 70)

    # Test with first 3 queries as examples
    for i, query in enumerate(test_queries[:3], 1):
        print(f"\n\nTest {i}:")
        response = execute_agent_query(query)
        print(f"Response: {response}")

    print("\n" + "=" * 70)
    print("SOLUTION COMPLETE")
    print("=" * 70)
    print("""
This solution demonstrates:

✓ Loading function specifications from JSON
✓ Importing function implementations
✓ Creating function mapping dictionary
✓ Initializing OpenAI client
✓ Implementing complete function calling flow
✓ Handling agent's function selection
✓ Executing functions and returning results
✓ Getting final synthesized response

Key Differences from 1_10_START_agent_base.py:

1. All TODO sections are completed
2. JSON loading is implemented with error handling
3. Functions are imported and mapped
4. execute_agent_query() is fully implemented
5. Complete Responses API function calling flow
6. Proper tool formatting and execution

Next Steps for Learning:

1. Run this script with different queries
2. Observe which functions agent selects
3. Modify function descriptions and test again
4. Try ambiguous queries to see selection behavior
5. Add logging to understand agent's reasoning

Cost Estimate:
- Each query costs ~$0.003-0.005 with gpt-4o-mini
- 3 test queries ≈ $0.01-0.02 total
    """)
    print("=" * 70)
