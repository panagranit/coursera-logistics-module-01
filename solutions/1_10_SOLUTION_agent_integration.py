"""
Complete Agent Integration Solution - Activity 1.10

This is the exemplar solution demonstrating how to integrate custom logistics
functions with an OpenAI agent using the Responses API.

Key Concepts Demonstrated:
1. Loading function specifications from JSON
2. Importing custom Python functions
3. Creating function mapping dictionary
4. Registering functions with OpenAI agent
5. Executing queries with function calling
6. Handling function execution and result synthesis

Learning Context:
    This complete solution shows learners how to properly integrate their
    custom functions with OpenAI agents for production use.

Prerequisites:
    - OPENAI_API_KEY environment variable set
    - logistics_specs.json (function specifications)
    - logistics_tools.py (function implementations)
    - 1_10_START_mock_queries.txt (test queries)
"""

import os
import json
import logging
import sys
from typing import Dict, List, Any, Callable

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# WHAT: Check for OpenAI API key
# WHY: Prevent confusing errors later if key is missing
# HOW: Check environment variable early and provide clear error message

if not os.environ.get("OPENAI_API_KEY"):
    print("\n" + "=" * 70)
    print("ERROR: OPENAI_API_KEY environment variable not set!")
    print("=" * 70)
    print("\nSet your key with: export OPENAI_API_KEY='your-api-key'")
    print("=" * 70)
    sys.exit(1)

# WHAT: Import OpenAI SDK
# WHY: Required for agent creation and interaction
# HOW: Use modern OpenAI Python SDK (v1.x+)

try:
    from openai import OpenAI
except ImportError:
    print("\nERROR: OpenAI library not installed!")
    print("Install with: pip install openai")
    sys.exit(1)

# WHAT: Import custom logistics functions
# WHY: These are the functions we'll register with the agent
# HOW: Import from solutions directory

try:
    from logistics_tools import (
        get_tracking_status,
        check_inventory,
        calculate_delivery_days
    )
except ImportError:
    print("\nERROR: Could not import logistics_tools.py")
    print("Make sure logistics_tools.py is in the same directory")
    sys.exit(1)

# WHAT: Configure logging
# WHY: Shows agent's function selection and execution process
# HOW: Set to INFO level with clear formatting

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# LOAD FUNCTION SPECIFICATIONS AND CREATE FUNCTION MAP
# ==============================================================================

def load_function_specs() -> List[Dict[str, Any]]:
    """
    Load function specifications from JSON file.

    Returns:
        List of function specification dictionaries

    Raises:
        FileNotFoundError: If logistics_specs.json doesn't exist
        json.JSONDecodeError: If JSON is malformed
    """
    # WHAT: Load function specifications from JSON
    # WHY: Agent needs specs to understand when to use each function
    # HOW: Read and parse JSON file

    spec_file = os.path.join(os.path.dirname(__file__), 'logistics_specs.json')

    logger.info(f"Loading function specifications from {spec_file}")

    try:
        with open(spec_file, 'r') as f:
            specs = json.load(f)

        logger.info(f"✓ Loaded {len(specs)} function specifications")

        # Log function names
        for spec in specs:
            logger.info(f"  - {spec['name']}")

        return specs

    except FileNotFoundError:
        logger.error(f"File not found: {spec_file}")
        logger.error("Make sure logistics_specs.json is in the solutions directory")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {spec_file}: {e}")
        raise


def create_function_map() -> Dict[str, Callable]:
    """
    Create mapping of function names to actual Python functions.

    Returns:
        Dictionary mapping function names (str) to callable functions

    Note:
        Function names must match exactly what's in logistics_specs.json
    """
    # WHAT: Create function name to Python function mapping
    # WHY: Allows dynamic function execution based on agent's selection
    # HOW: Dictionary with name strings as keys, function objects as values

    function_map = {
        "get_tracking_status": get_tracking_status,
        "check_inventory": check_inventory,
        "calculate_delivery_days": calculate_delivery_days,
    }

    logger.info(f"✓ Created function mapping with {len(function_map)} functions")

    return function_map


# ==============================================================================
# AGENT INTERACTION
# ==============================================================================

def query_agent(
    client: OpenAI,
    query: str,
    function_specs: List[Dict],
    function_map: Dict[str, Callable]
) -> str:
    """
    Execute a query against the agent with function calling support.

    Args:
        client: OpenAI client instance
        query: User query string
        function_specs: List of function specifications
        function_map: Dictionary mapping function names to implementations

    Returns:
        Agent's final response as string

    This implements the complete function calling flow:
    1. Send query with available functions
    2. Agent decides which function(s) to call
    3. Execute function(s) locally
    4. Send results back to agent
    5. Agent synthesizes final response
    """
    logger.info("\n" + "=" * 70)
    logger.info(f"QUERY: {query}")
    logger.info("=" * 70)

    try:
        # WHAT: Create response with function calling using Responses API
        # WHY: Allows agent to use our custom functions
        # HOW: Pass functions via 'tools' parameter in Responses API

        logger.info("Sending query to agent...")

        # Convert function specs to OpenAI tools format
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

        # Create response with function calling using Responses API
        response = client.responses.create(
            model="gpt-4o-mini",  # Cost-efficient model
            input=query,
            modalities=["text"],
            instructions=instructions,
            tools=tools
        )

        # Get the response output
        output = response.output[0]

        # WHAT: Check if agent wants to call functions
        # WHY: Agent may call one or more functions to answer query
        # HOW: Check if output type is function_call

        # Collect all function calls from the output
        function_calls = []
        for item in response.output:
            if hasattr(item, 'type') and item.type == "function_call":
                function_calls.append(item)

        if function_calls:
            logger.info(f"Agent selected {len(function_calls)} function(s) to call")

            # Prepare input array for second API call with function results
            input_items = []

            # Execute each function call
            for function_call in function_calls:
                function_name = function_call.name
                function_args = json.loads(function_call.arguments)

                logger.info(f"\nFunction Call:")
                logger.info(f"  Name: {function_name}")
                logger.info(f"  Arguments: {json.dumps(function_args, indent=4)}")

                # WHAT: Execute the function
                # WHY: Get results to send back to agent
                # HOW: Look up function in map and call with parsed arguments

                if function_name in function_map:
                    function_to_call = function_map[function_name]
                    function_response = function_to_call(**function_args)

                    logger.info(f"  Result: {json.dumps(function_response, indent=4)}")

                    # Add function result to input array
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
            # No function calls needed
            logger.info("Agent answered directly without function calls")
            final_answer = output.content[0].text

        logger.info(f"\nFINAL RESPONSE: {final_answer}")
        logger.info("=" * 70 + "\n")

        return final_answer

    except Exception as e:
        logger.error(f"Error during agent query: {e}")
        raise


def main():
    """
    Main execution function demonstrating complete agent integration.
    """
    print("\n" + "=" * 70)
    print("INNOVATE LOGISTICS AGENT - COMPLETE INTEGRATION")
    print("=" * 70 + "\n")

    # WHAT: Initialize OpenAI client
    # WHY: Required for all API interactions
    # HOW: Use API key from environment

    logger.info("Initializing OpenAI client...")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    logger.info("✓ OpenAI client initialized\n")

    # WHAT: Load function specifications and create mapping
    # WHY: Agent needs specs to select functions, we need map to execute them
    # HOW: Use helper functions defined above

    function_specs = load_function_specs()
    function_map = create_function_map()

    print("\n" + "=" * 70)
    print("SETUP COMPLETE - Ready to process queries")
    print("=" * 70 + "\n")

    # WHAT: Load test queries from file
    # WHY: Systematic testing of agent's function selection
    # HOW: Read queries from 1_10_START_mock_queries.txt

    queries_file = os.path.join(
        os.path.dirname(__file__),
        '../activity/1_10_START_mock_queries.txt'
    )

    test_queries = []

    try:
        with open(queries_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    test_queries.append(line)

        logger.info(f"Loaded {len(test_queries)} test queries\n")

    except FileNotFoundError:
        logger.warning(f"Could not find {queries_file}")
        logger.info("Using default test queries instead\n")

        test_queries = [
            "What is the status of tracking code 123456789?",
            "How many units of SKU ABC1234 are in stock?",
            "How long will delivery take to zone 3 with Standard service?",
        ]

    # WHAT: Execute test queries
    # WHY: Demonstrate agent function calling in action
    # HOW: Call query_agent for each test query

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST QUERY {i}/{len(test_queries)}")
        print(f"{'='*70}")

        try:
            response = query_agent(client, query, function_specs, function_map)
            print(f"\n✓ Query completed successfully")

        except Exception as e:
            logger.error(f"Query failed: {e}")
            print(f"\n✗ Query failed: {e}")

        # Small delay between queries
        import time
        time.sleep(1)

    print("\n" + "=" * 70)
    print("ALL QUERIES COMPLETED")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
