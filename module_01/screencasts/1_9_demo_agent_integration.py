"""
Module: 1_9_demo_agent_integration.py
Purpose: Demonstrate ACTUAL registration of custom functions with OpenAI

This module shows the complete, real-world workflow of:
1. Loading function specifications
2. Registering functions with OpenAI using Responses API
3. Executing queries that trigger actual function calls
4. Logging the agent's function selection process

Learning Context:
    Demonstrated in Screencast 1.9 "Integrating Your Toolkit with an Agent"
    Shows the "magic moment" when custom functions work with a REAL agent.

    This is NOT a mock - it makes actual OpenAI API calls!

Prerequisites:
    - OPENAI_API_KEY environment variable must be set
    - OpenAI Python SDK installed (pip install openai)
    - 1_1_shipping_tool.py and 1_1_shipping_spec.json in the same directory

Run with: python 1_9_demo_agent_integration.py

Cost: Approximately $0.01-0.02 per run (3 queries with gpt-4o-mini)
"""

import os
import json
import logging
from typing import Dict, Any, Callable
from importlib import import_module

# Import from numbered module using importlib
_shipping_tool = import_module('1_1_shipping_tool')
calculate_shipping_cost = _shipping_tool.calculate_shipping_cost

# WHAT: Configure detailed logging to show agent's function selection
# WHY: Helps understand how agents decide which function to call
# HOW: Set logging to INFO level with detailed format

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# WHAT: Check for OpenAI API key
# WHY: Provide clear error message if key is missing
# HOW: Check environment variable and exit gracefully if not found

if not os.environ.get("OPENAI_API_KEY"):
    print("\n" + "=" * 70)
    print("ERROR: OPENAI_API_KEY environment variable not set!")
    print("=" * 70)
    print("\nPlease set it with: export OPENAI_API_KEY='your-key-here'")
    print("\nThis demo requires a valid OpenAI API key to run.")
    print("=" * 70)
    exit(1)

# WHAT: Import OpenAI SDK for actual API integration
# WHY: We need the real client to demonstrate actual function registration
# HOW: Import from openai package (modern SDK v1.x+)

try:
    from openai import OpenAI
except ImportError:
    print("\n" + "=" * 70)
    print("ERROR: OpenAI library not installed!")
    print("=" * 70)
    print("\nInstall it with: pip install openai")
    print("=" * 70)
    exit(1)

# WHAT: Initialize OpenAI client
# WHY: Required for all API interactions
# HOW: Create client instance with API key from environment

logger.info("Initializing OpenAI client...")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger.info("✓ OpenAI client initialized")


def execute_agent_query_demo(query: str, function_spec: Dict[str, Any]) -> None:
    """
    Execute REAL OpenAI agent query with actual function calling.

    This demonstrates the complete, production-ready workflow:
    1. Load function specification
    2. Register function with OpenAI via tools parameter
    3. Send query to agent
    4. Agent selects function and extracts parameters
    5. Execute function locally
    6. Send result back to agent
    7. Agent synthesizes natural language response

    Args:
        query: Natural language query from user
        function_spec: OpenAI function specification dict

    Note: This makes ACTUAL API calls to OpenAI!
    """

    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    try:
        # WHAT: Register function with OpenAI and send query
        # WHY: Agent needs function spec to decide when to call it
        # HOW: Use Responses API with tools parameter

        logger.info("Sending query to OpenAI with registered function...")

        # Convert function spec to tools format
        tools = [{
            "type": "function",
            "function": function_spec
        }]

        # System instructions for the agent
        instructions = "You are a helpful assistant for Innovate Logistics. Use the shipping cost function when customers ask about pricing."

        # Step 1: Initial API call with query and tools using Responses API
        response = client.responses.create(
            model="gpt-4o-mini",
            input=query,
            modalities=["text"],
            instructions=instructions,
            tools=tools
        )

        # Get the response output
        output = response.output[0]

        # WHAT: Check if agent wants to call our function
        # WHY: Agent may call function or answer directly
        # HOW: Check if output type is function_call

        # Collect all function calls from the output
        function_calls = []
        for item in response.output:
            if hasattr(item, 'type') and item.type == "function_call":
                function_calls.append(item)

        if function_calls:
            function_call = function_calls[0]  # Get first function call
            logger.info(f"✓ Agent selected function: {function_call.name}")

            # Extract function call details
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)

            logger.info(f"✓ Agent extracted parameters:")
            for key, value in function_args.items():
                logger.info(f"    {key}: {value}")

            # WHAT: Execute the function
            # WHY: Get result to send back to agent
            # HOW: Call calculate_shipping_cost with extracted args

            logger.info(f"Executing {function_name}...")
            function_result = calculate_shipping_cost(**function_args)

            logger.info(f"✓ Function result: {function_result}")

            # WHAT: Send function result back to agent
            # WHY: Agent needs result to formulate response
            # HOW: Second API call with function result

            logger.info("Sending function result back to agent...")

            # Prepare input array with function result
            input_items = [{
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": json.dumps(function_result)
            }]

            # Step 2: Second API call to get final response using Responses API
            second_response = client.responses.create(
                model="gpt-4o-mini",
                previous_response_id=response.id,  # Link to original response with function calls
                input=input_items,
                modalities=["text"],
                instructions=instructions
            )

            final_answer = second_response.output[0].content[0].text

        else:
            # Agent answered without function call
            logger.info("Agent answered directly without calling function")
            final_answer = output.content[0].text

        print(f"\n✓ AGENT RESPONSE:")
        print(f"{final_answer}")

    except Exception as e:
        logger.error(f"Error during query: {e}")
        print(f"\n✗ Error: {e}")

    print("=" * 70)


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("REAL AGENT INTEGRATION DEMONSTRATION")
    print("Innovate Logistics - Custom Shipping Cost Function")
    print("=" * 70)

    print("""
This demonstration shows ACTUAL OpenAI agent integration with custom functions.

Key Points:
- This makes REAL API calls to OpenAI
- The agent ACTUALLY selects and calls our function
- You'll see the complete registration and execution flow
- Estimated cost: ~$0.01-0.02 (using gpt-4o-mini)

The Process:
1. Load function specification from 1_1_shipping_spec.json
2. Register function with OpenAI via 'tools' parameter
3. Send query to agent
4. Agent decides whether to call function
5. If called, execute function and return result
6. Agent synthesizes final natural language response
    """)

    # WHAT: Load actual function specification from JSON file
    # WHY: Show real-world workflow of loading and using specs
    # HOW: Read 1_1_shipping_spec.json from same directory

    logger.info("Loading function specification from 1_1_shipping_spec.json...")

    try:
        spec_file = os.path.join(os.path.dirname(__file__), "1_1_shipping_spec.json")
        with open(spec_file, 'r') as f:
            spec = json.load(f)

        logger.info(f"✓ Loaded specification for: {spec['name']}")

    except FileNotFoundError:
        print("\nERROR: 1_1_shipping_spec.json not found!")
        print("Make sure 1_1_shipping_spec.json is in the same directory as this script.")
        exit(1)

    print("\n" + "=" * 70)
    print("FUNCTION SPECIFICATION (What the Agent Sees)")
    print("=" * 70)
    print(json.dumps(spec, indent=2))

    print("\n" + "=" * 70)
    print("EXECUTING TEST QUERIES WITH REAL AGENT")
    print("=" * 70)

    # WHAT: Test with various queries showing real agent behavior
    # WHY: Demonstrate how function descriptions affect selection
    # HOW: Execute multiple queries and observe real agent decisions

    # Test 1: Clear, unambiguous query
    print("\n### TEST 1: Clear Query ###")
    execute_agent_query_demo(
        "What's the shipping cost for a 15kg package to zone 4 for a Gold customer?",
        spec
    )

    # Test 2: Alternative phrasing
    print("\n### TEST 2: Natural Language Variation ###")
    execute_agent_query_demo(
        "How much would it cost to ship 20 kilograms to zone 2 for a Platinum customer?",
        spec
    )

    # Test 3: Testing function selection
    print("\n### TEST 3: Implicit Parameters ###")
    execute_agent_query_demo(
        "I need a price quote for shipping 10kg locally for a Bronze customer",
        spec
    )

    # WHAT: Provide key takeaways from REAL integration
    # WHY: Reinforce learning objectives with concrete experience
    # HOW: Summarize what was demonstrated

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS FROM REAL INTEGRATION")
    print("=" * 70)

    print("""
What You Just Saw (REAL, not simulated):

1. ACTUAL Function Registration:
   ✓ Loaded function spec from JSON file
   ✓ Converted to OpenAI tools format
   ✓ Sent to API via 'tools' parameter
   ✓ Agent received and understood the function

2. REAL Agent Decision-Making:
   ✓ Agent analyzed natural language queries
   ✓ Compared queries to function description
   ✓ Decided whether to call function or answer directly
   ✓ Extracted parameters from conversational text

3. The Complete Flow:
   Query → Agent Analysis → Function Call → Execution → Result → Synthesis

4. Why This Matters:
   - This is the EXACT workflow you'll use in production
   - No mocks, no simulations - real OpenAI integration
   - The code you saw is production-ready

5. The Registration Process:
   Step 1: Load specification (JSON file)
   Step 2: Format as tools: [{"type": "function", "function": spec}]
   Step 3: Pass to chat.completions.create(tools=tools)
   Step 4: Agent can now discover and use your function

Next Steps - Activity 1.10:
- You'll register YOUR THREE custom logistics functions
- Test with multiple queries from 1_10_START_mock_queries.txt
- Debug function selection by refining descriptions
- Experience the "magic moment" yourself with real agents!

Cost Note:
- This demo cost approximately $0.01-0.02
- Activity 1.10 will cost similar (2-5 queries)
- Always use gpt-4o-mini for cost-effective development
    """)

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
