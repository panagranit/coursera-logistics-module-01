"""
Innovate Logistics Agent Integration Template

This script sets up an OpenAI agent with your custom logistics functions.

Your tasks in Activity 1.10:
1. Load your function specifications from logistics_specs.json
2. Import your function implementations from logistics_tools.py
3. Register the functions with the agent
4. Test with queries from 1_10_START_mock_queries.txt
5. Iteratively refine function descriptions based on agent selection behavior

Learning Context:
    This is a Medium scaffolding exercise. The agent setup structure is provided,
    but you need to complete the function loading and registration sections.

Prerequisites:
    - OPENAI_API_KEY environment variable must be set
    - Your logistics_specs.json file (from Activity 1.3)
    - Your logistics_tools.py file (from Activity 1.3/1.7)
    - 1_10_START_mock_queries.txt for testing

Expected Outcome:
    - Agent successfully selects correct function for each query
    - Function parameters are correctly extracted from queries
    - Agent provides helpful responses using function results
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

# TODO: Load your logistics_specs.json file
# Hint: Use json.load() with open()
# Your code should:
# 1. Open the file 'logistics_specs.json' in read mode
# 2. Use json.load() to parse the JSON
# 3. Store result in function_specs variable

logger.info("Loading function specifications...")

# TODO: Replace None with your file loading code
function_specs = None  # Should be a list of function specification dictionaries

# Example structure you should see:
# [
#     {
#         "name": "get_tracking_status",
#         "description": "...",
#         "parameters": {...}
#     },
#     {
#         "name": "check_inventory",
#         "description": "...",
#         "parameters": {...}
#     },
#     ...
# ]

if function_specs is None:
    logger.error("Failed to load function specifications!")
    logger.error("Make sure logistics_specs.json exists in the current directory")
    exit(1)

logger.info(f"Loaded {len(function_specs)} function specifications")
for spec in function_specs:
    logger.info(f"  - {spec['name']}")


# ==============================================================================
# STEP 2: IMPORT FUNCTION IMPLEMENTATIONS
# ==============================================================================

# WHAT: Import your actual function implementations
# WHY: Agent needs the actual Python functions to execute
# HOW: Import from your logistics_tools module

# TODO: Import your functions from logistics_tools.py
# Hint: from logistics_tools import get_tracking_status, check_inventory, calculate_delivery_days

logger.info("Importing function implementations...")

# TODO: Add your import statement here

# After importing, uncomment and complete the function_map:
# function_map = {
#     "get_tracking_status": get_tracking_status,
#     "check_inventory": check_inventory,
#     "calculate_delivery_days": calculate_delivery_days,
# }

# For now, using a placeholder:
function_map = {}

if not function_map:
    logger.error("Function map is empty!")
    logger.error("Make sure to import your functions and create the function_map dictionary")
    exit(1)

logger.info(f"Registered {len(function_map)} function implementations")


# ==============================================================================
# STEP 3: INITIALIZE OPENAI CLIENT
# ==============================================================================

# WHAT: Initialize OpenAI client with API key
# WHY: Required to create and interact with agents
# HOW: Create OpenAI client instance with key from environment variable

logger.info("Initializing OpenAI client...")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logger.info("OpenAI client initialized successfully")


# ==============================================================================
# STEP 4: QUERY EXECUTION FUNCTION
# ==============================================================================

def execute_agent_query(query: str, verbose: bool = True) -> str:
    """
    Execute a query against the agent with custom functions.

    This function:
    1. Sends the query to the agent
    2. Agent analyzes which function(s) to call
    3. Executes the selected function(s)
    4. Returns the agent's natural language response

    Args:
        query: Natural language query from user
        verbose: Whether to log detailed information

    Returns:
        str: Agent's natural language response

    Note: This is a simplified implementation for educational purposes.
          In production, you would handle:
          - Multiple function calls
          - Error handling for API failures
          - Streaming responses
          - Conversation history
    """

    if verbose:
        logger.info(f"\n{'=' * 70}")
        logger.info(f"Query: {query}")
        logger.info(f"{'=' * 70}")

    # TODO: This is where you would implement the agent query logic
    # For Activity 1.10, you'll need to:
    # 1. Create a chat completion with function calling
    # 2. Pass your function_specs to the agent
    # 3. If agent calls a function, execute it using function_map
    # 4. Return the result to the agent
    # 5. Get the final response

    # Placeholder response:
    response = "Agent integration not yet implemented. Complete the TODOs above!"

    if verbose:
        logger.info(f"Agent Response: {response}")
        logger.info(f"{'=' * 70}\n")

    return response


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
    print("INNOVATE LOGISTICS AGENT INTEGRATION")
    print("=" * 70)
    print("\nThis script demonstrates agent integration with custom functions.")
    print("\nYour tasks:")
    print("  1. Complete the TODO sections above")
    print("  2. Load your logistics_specs.json file")
    print("  3. Import your logistics_tools functions")
    print("  4. Implement the agent query logic")
    print("  5. Test with queries from 1_10_START_mock_queries.txt")
    print("=" * 70)

    # WHAT: Load test queries
    # WHY: Need queries to test agent function selection
    # HOW: Call load_test_queries function

    test_queries = load_test_queries()

    # WHAT: Test with a few sample queries
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
    print("NEXT STEPS")
    print("=" * 70)
    print("""
After completing the TODOs:

1. Test with clear queries first
   - Verify agent selects correct function
   - Verify parameters are extracted correctly

2. Test with ambiguous queries
   - Note which function agent selects
   - Identify weak descriptions

3. Refine function descriptions
   - Add keywords from queries agent struggled with
   - Make descriptions more specific
   - Test again until reliable

4. Test with invalid inputs
   - Verify validation errors are returned correctly
   - Check error messages are clear

5. Test edge cases
   - Boundary values
   - Unknown codes/SKUs
   - All zone/service combinations

Success Criteria:
✓ Agent selects correct function for all clear queries
✓ Agent extracts parameters correctly
✓ Validation errors are handled gracefully
✓ Error messages are clear and helpful

Tips for Success:
- Start simple, test often
- One query at a time
- Log agent's reasoning
- Iterate on descriptions
- Don't expect perfection immediately!

The "magic moment" happens when agent reliably selects the right
function and your business logic just works through natural language!
    """)
    print("=" * 70)
