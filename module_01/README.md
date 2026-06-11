# AI Agents Course 2, Module 1: Building Custom Functions for Your Agents

This repository contains all course materials for Module 1 of "Advanced Tool Development and Integration" - part of the AI Agents with OpenAI Coursera specialization. For your own reference you may review the code that appears in the screencasts and you will also find the starter and solution code for each lab activity. The instructions that accompany this lab will indicate which files you'll need for any given lab activity.

## Module Overview

**Learning Theme**: Custom Function Development for AI Agents

In this module, learners build custom Python functions that extend AI agent capabilities beyond built-in tools. Using the **Praxis AI consultancy** working with **Innovate Logistics** as the narrative context, learners progress from basic function creation through production-ready implementations with comprehensive error handling, validation, and testing.

### Learning Objectives

By the end of this module, learners will be able to:

1. Design OpenAI-compatible function specifications with clear, agent-friendly descriptions
2. Implement production-ready Python functions with comprehensive input validation
3. Apply the standardized return format pattern: `{"success": bool, "result": Any, "error": str}`
4. Write comprehensive test suites using pytest
5. Apply the decorator pattern for cross-cutting concerns (logging, error handling, timing)
6. Integrate custom functions with OpenAI agents and refine descriptions for optimal function selection

---

## Repository Structure

```
module_01/
├── README.md                    # This file
├── CHANGELOG.md                 # Version history and updates
├── screencasts/                 # Files for instructor demonstrations
│   ├── innovative-logistics-demo.html  # Interactive demo for module introduction
│   ├── 1_1_shipping_spec.json          # OpenAI function specification example
│   ├── 1_1_shipping_tool.py            # Complete function implementation
│   ├── 1_1_test_shipping_tool.py       # Comprehensive test suite (368 lines)
│   ├── 1_5_demo_production_wrapper.py  # Decorator pattern with Innovate Logistics example
│   └── 1_9_demo_agent_integration.py   # REAL OpenAI agent integration (uses live API)
├── activities/                  # Starter files for learner activities
│   ├── 1_3_START_requirements.md       # Business requirements for logistics functions
│   ├── 1_3_START_naive_tools.py        # Intentionally flawed implementations
│   ├── 1_3_START_function_tests.py     # Test suite (will fail initially)
│   ├── 1_7_START_production_wrapper.py # Production decorator to import
│   ├── 1_7_START_test_logistics.py     # Test stubs for learners to complete
│   ├── 1_10_START_agent_base.py        # Agent integration template
│   └── 1_10_START_mock_queries.txt     # Test queries for agent testing
├── resources/                   # Reference materials and guides
│   ├── r1_function_contract.md         # Function contract pattern reference
│   └── r2_enterprise_patterns.md       # Production patterns guide
└── solutions/                   # Solution files for grading and reference
    ├── 1_3_SOLUTION_logistics_specs.json     # Complete function specifications
    ├── 1_3_SOLUTION_logistics_tools.py       # Production-ready implementations
    ├── 1_7_SOLUTION_logistics_tools.py       # Functions with decorator pattern applied
    ├── 1_7_SOLUTION_test_logistics.py        # Complete pytest suite (619 lines)
    ├── 1_10_SOLUTION_agent_base.py           # Completed agent integration
    └── 1_10_SOLUTION_agent_integration.py    # Complete OpenAI integration exemplar (280 lines)
```

---

## Content Types

### Screencast Files (`screencasts/`)

**Purpose**: Complete, working code for instructor demonstrations

These files are used in video screencasts to demonstrate concepts. All code is production-quality, fully commented, and ready to execute.

**Key Files**:
- **innovative-logistics-demo.html** (Module Introduction): Interactive demonstration of Innovate Logistics business scenario
- **1_1_shipping_spec.json** (Lesson 1.1): OpenAI function specification for `calculate_shipping_cost`
- **1_1_shipping_tool.py** (Lesson 1.1): Complete implementation with validation and error handling
- **1_1_test_shipping_tool.py** (Lesson 1.1): 30+ comprehensive tests demonstrating pytest best practices
- **1_5_demo_production_wrapper.py** (Lesson 1.5): Before/after comparison of decorator pattern using Innovate Logistics functions
- **1_9_demo_agent_integration.py** (Lesson 1.9): REAL OpenAI agent integration (uses live API, requires OPENAI_API_KEY)

**Usage**: Execute directly to see demonstrations in action

```bash
cd screencasts/

# View interactive Innovate Logistics demo (open in browser)
open innovative-logistics-demo.html

# Run test suite
pytest 1_1_test_shipping_tool.py -v

# Run decorator demonstration
python 1_5_demo_production_wrapper.py
```

### Activity Files (`activities/`)

**Purpose**: Starter files for hands-on learner activities

Files prefixed with `X_Y_START_` are provided to learners as starting points (where X.Y is the lesson number). Learners modify or complete these files as part of hands-on activities.

**Activity 1.3: Refactor Legacy Code**
- Learners receive: `1_3_START_requirements.md`, `1_3_START_naive_tools.py`, `1_3_START_function_tests.py`
- Learners create: `logistics_specs.json`, `logistics_tools.py`
- Outcome: Refactor naive code into production-ready agent functions

**Activity 1.7: Apply Production Decorator**
- Learners receive: `1_7_START_production_wrapper.py`, `1_7_START_test_logistics.py`
- Learners create: Complete test suite, apply decorator to their functions
- Outcome: Implement cross-cutting concerns using decorator pattern

**Activity 1.10: Agent Integration and Testing**
- Learners receive: `1_10_START_agent_base.py`, `1_10_START_mock_queries.txt`
- Learners create: Complete agent integration with function registration
- Outcome: Test agent function selection and refine descriptions

**Testing Activity Files**:

```bash
cd activities/

# This WILL FAIL against naive code (intentional)
pytest 1_3_START_function_tests.py

# After learners complete the activity, tests should pass
# pytest test against their logistics_tools.py
```

### Resource Files (`resources/`)

**Purpose**: Reference guides and copy-paste templates

These markdown files provide comprehensive references that learners can consult while completing activities.

- **r1_function_contract.md**: Explains the specification + implementation pattern with annotated examples
- **r2_enterprise_patterns.md**: Production decorator code and pytest patterns (1,100+ lines of commented examples)

### Solution Files (`solutions/`)

**Purpose**: Complete solutions for grading and reference

These files represent the expected output from learner activities. Files are prefixed with `X_Y_SOLUTION_` (where X.Y is the lesson number).

**Activity 1.3 Solutions**:
- **1_3_SOLUTION_logistics_specs.json**: Complete OpenAI function specifications for 3 logistics functions
- **1_3_SOLUTION_logistics_tools.py**: Production-ready implementations with full validation

**Activity 1.7 Solutions**:
- **1_7_SOLUTION_logistics_tools.py**: Functions with `@production_agent_function` decorator applied (450 lines)
- **1_7_SOLUTION_test_logistics.py**: Complete pytest suite with 90+ comprehensive tests (619 lines)

**Activity 1.10 Solutions**:
- **1_10_SOLUTION_agent_base.py**: Completed version of 1_10_START_agent_base.py with all TODOs filled in
- **1_10_SOLUTION_agent_integration.py**: Comprehensive OpenAI agent integration exemplar using Responses API (280 lines)

**Grading**: Compare learner submissions against these files, or run learner code against test suites

```bash
# Verify Activity 1.3 solution quality
cd solutions/
pytest ../activities/1_3_START_function_tests.py -v
# Should pass all 62 tests

# Verify Activity 1.7 solution quality
pytest 1_7_SOLUTION_test_logistics.py -v
# Should pass all 90+ tests

# Test Activity 1.10 solution (requires OPENAI_API_KEY)
python 1_10_SOLUTION_agent_integration.py
```

---

## Module Storyline

### Business Context: Praxis AI Consultancy

Learners take on the role of consultants at **Praxis AI**, a fictional consultancy specializing in agent development. Their first client is **Innovate Logistics**, a shipping company with legacy Python code that needs to be refactored into agent-callable functions.

### The Three Logistics Functions

Throughout the module, learners work with three core functions:

1. **get_tracking_status(tracking_code: str)**
   - Look up package delivery status
   - Validates 9-digit numeric tracking codes
   - Returns: "In Transit", "Delivered", or "Unknown"

2. **check_inventory(sku: str)**
   - Check product availability
   - Validates SKU format: 3 uppercase letters + 4 digits (e.g., "ABC1234")
   - Returns: Quantity in stock (integer)

3. **calculate_delivery_days(zone: int, service_level: str)**
   - Estimate delivery time
   - Validates zone (1-4) and service level ("Standard" or "Express")
   - Returns: Estimated delivery days (integer)

All functions follow the same pattern:
1. Type validation
2. Format validation
3. Business logic execution
4. Standardized return: `{"success": bool, "result": Any, "error": str}`

---

## Technical Standards

All code in this repository follows strict educational standards:

### "What-Why-How" Comment Pattern

Every 3-5 lines of code includes comments explaining:
- **WHAT**: What is being created or done
- **WHY**: The reasoning behind this approach
- **HOW**: Technical implementation details

Example:
```python
# WHAT: Validate tracking code format
# WHY: Prevent invalid codes from reaching the database
# HOW: Check length and ensure all characters are digits
if len(tracking_code) != 9 or not tracking_code.isdigit():
    raise ValueError("Tracking code must be exactly 9 digits")
```

### Standardized Return Format

All agent-callable functions return a consistent dictionary format:

```python
# Success case
{"success": True, "result": <value>, "error": None}

# Validation error
{"success": False, "result": None, "error": "<clear message>", "error_type": "validation"}

# System error
{"success": False, "result": None, "error": "<error details>", "error_type": "system"}
```

### Code Quality Requirements

- ✅ **Type hints**: All function parameters typed
- ✅ **Docstrings**: All functions documented
- ✅ **Error handling**: Comprehensive try/except blocks
- ✅ **Input validation**: Type, format, and range checking
- ✅ **Clear error messages**: Actionable feedback for users
- ✅ **Explicit variables**: No ambiguous or single-letter names

---

## Setup and Requirements

### Prerequisites

- **Python 3.8+**
- **OpenAI API key** (for agent integration activities only)
- **pytest** for running tests

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aiagents-course2-module1.git
cd aiagents-course2-module1

# Install dependencies
pip install pytest openai

# For agent integration activities, set your API key
export OPENAI_API_KEY='your-api-key-here'
```

### Running Tests

```bash
# Run screencast test suite
cd screencasts/
pytest 1_1_test_shipping_tool.py -v

# Run activity test suite (will fail against naive code)
cd activities/
pytest 1_3_START_function_tests.py -v

# Run against Activity 1.3 solutions (should pass all 62 tests)
cd solutions/
pytest ../activities/1_3_START_function_tests.py -v

# Run Activity 1.7 complete test suite (should pass all 90+ tests)
cd solutions/
pytest 1_7_SOLUTION_test_logistics.py -v
```

### Running Demonstrations

```bash
# Production decorator demonstration (using Innovate Logistics functions)
python screencasts/1_5_demo_production_wrapper.py

# Agent integration demonstration - screencast version (requires OPENAI_API_KEY)
python screencasts/1_9_demo_agent_integration.py

# Activity 1.10 solution - completed agent_base.py (requires OPENAI_API_KEY)
python solutions/1_10_SOLUTION_agent_base.py

# Comprehensive agent integration exemplar (requires OPENAI_API_KEY)
python solutions/1_10_SOLUTION_agent_integration.py
```

---

## Learning Path

### Lesson 1.1: Custom Function Creation
**Type**: Screencast (7 minutes)
**Files**: `1_1_shipping_spec.json`, `1_1_shipping_tool.py`, `1_1_test_shipping_tool.py`
**Concept**: Design function specifications and implement with validation

### Lesson 1.2: The Function Contract Pattern
**Type**: Reading (10 minutes)
**Files**: None (text-based lesson)
**Concept**: Specification + Implementation = Function Contract

### Lesson 1.3: Refactor Legacy Code (Activity)
**Type**: Hands-on Activity (30-40 minutes)
**Files**: `1_3_START_requirements.md`, `1_3_START_naive_tools.py`, `1_3_START_function_tests.py`
**Deliverable**: `logistics_specs.json`, `logistics_tools.py`
**Objective**: Refactor naive functions into production-ready implementations

### Lesson 1.4: Error Handling Strategies
**Type**: Reading (10 minutes)
**Files**: None (text-based lesson)
**Concept**: Validation errors vs system errors, clear error messages

### Lesson 1.5: Production Patterns with Decorators
**Type**: Screencast (6 minutes)
**Files**: `1_5_demo_production_wrapper.py`
**Concept**: Apply decorator pattern for logging, timing, error handling

### Lesson 1.6: Testing Agent Functions
**Type**: Reading (12 minutes)
**Files**: None (text-based lesson)
**Concept**: pytest fixtures, parametrize, comprehensive test coverage

### Lesson 1.7: Apply Production Decorator (Activity)
**Type**: Hands-on Activity (25-35 minutes)
**Files**: `1_7_START_production_wrapper.py`, `1_7_START_test_logistics.py`, `logistics_tools.py`
**Deliverable**: Hardened functions with `@production_agent_function` and a complete pytest suite
**Objective**: Apply the production decorator, remove repetitive try/except blocks, and provide full tests

Activity steps (Part A — C)

Part A — Harden Functions (Refactor with Decorator)
- Open `module_01/activities/logistics_tools.py` (your Activity 1.3 implementation).
- Import the decorator at the top:

```python
from 1_7_START_production_wrapper import production_agent_function
```

- Apply `@production_agent_function` directly above each function definition (`get_tracking_status`, `check_inventory`, `calculate_delivery_days`).
- Remove all internal `try/except` blocks — functions should only perform validation (raise `ValueError` on invalid input) and return the happy-path dictionary:

```python
return {"success": True, "result": ..., "error": None}
```

Refer to the examples at the end of `1_7_START_production_wrapper.py` for the expected structure.

Part B — Build the Test Suite
- Open `module_01/activities/1_7_START_test_logistics.py` and import your hardened functions from `logistics_tools.py`.
- Fill in each `test_` function per the TODO comments: include Happy Path tests, Input Validation tests, and Error Response Format assertions (expect `error_type == "validation"` for validation failures).

Part C — Validate Your Work
- Install pytest (if needed):

```bash
pip install pytest
```

- Run the tests from the `activities` folder:

```bash
cd module_01/activities
python3 -m pytest 1_7_START_test_logistics.py -v
```

- If tests fail, read pytest output, fix either `logistics_tools.py` or the tests, and re-run until all tests pass.

Notes and guidance
- The decorator converts `ValueError` to `{"success": False, "result": None, "error": str, "error_type": "validation"}` and other exceptions to `error_type: "system"`.
- Keep educational comments (What-Why-How) and type hints intact when refactoring.
- Use the solution files in `solutions/` for examples if you need reference implementations.

### Lesson 1.8: Agent Function Selection
**Type**: Reading (10 minutes)
**Files**: None (text-based lesson)
**Concept**: How agents choose functions, optimizing descriptions

### Lesson 1.9: Agent Integration
**Type**: Screencast (7 minutes)
**Files**: `1_9_demo_agent_integration.py`
**Concept**: Register functions with agents, observe selection process

### Lesson 1.10: Agent Testing and Refinement (Activity)
**Type**: Hands-on Activity (30-40 minutes)
**Files**: `1_10_START_agent_base.py`, `1_10_START_mock_queries.txt`
**Deliverable**: Working agent with custom functions
**Objective**: Integrate functions, test with queries, refine descriptions

---

## Assessment

### Practice Quiz (Lesson 1.4)
- 5 questions
- 15 minutes
- Topics: Function contracts, error handling, validation strategies

### Graded Quiz (Lesson 1.11)
- 10 questions
- 30 minutes
- Topics: All module concepts (specifications, implementation, testing, integration)

### Graded Activity (Lesson 1.3)
Learner submissions for Activity 1.3 are graded against:
- `solutions/1_3_SOLUTION_logistics_specs.json` (specifications match requirements)
- `activities/1_3_START_function_tests.py` (all 62 tests pass)
- Code quality standards (comments, docstrings, type hints)

---

## Code Quality Statistics

This repository contains:
- **~5,000 lines** of educational Python code
- **120+ comprehensive tests** (pytest)
- **40% documentation ratio** (~2,000 lines of comments)
- **100% type hint coverage**
- **100% docstring coverage**
- **100% error handling coverage**

All code follows the "What-Why-How" educational commenting standard.

---

## Instructor Notes

### Common Learner Challenges

1. **Forgetting type validation**: Learners often validate format before type, causing unhelpful error messages
   - **Tip**: Emphasize "fail fast" - check type first, then format, then range

2. **Vague error messages**: Initial implementations return generic errors like "Invalid input"
   - **Tip**: Show examples of helpful vs unhelpful error messages in lesson 1.4

3. **Incomplete test coverage**: Learners test happy path but forget edge cases
   - **Tip**: In lesson 1.7, emphasize the test categories: happy path, validation, edge cases, error handling

4. **Agent function selection confusion**: Learners struggle when agent picks wrong function
   - **Tip**: In lesson 1.10, walk through adding keywords from queries to descriptions

### Teaching Tips

- **Live coding**: Run tests frequently to show the red → green cycle
- **Error-driven development**: Intentionally trigger errors to show validation in action
- **Agent "magic moment"**: The first time agent correctly selects a custom function is powerful - build anticipation
- **Cost awareness**: Remind learners that most development uses mock data, live API calls only for final validation

---

## License

This educational content is part of the AI Agents with OpenAI Coursera specialization.

**Copyright**: Coursera Originals, 2025
**Usage**: Educational purposes for enrolled learners and authorized instructors

---

## Support and Feedback

For questions or issues with course materials:
- **Course Discussion Forums**: Primary support channel
- **Technical Issues**: Contact course support team
- **Content Feedback**: Use course feedback surveys

---

## Acknowledgments

This module was developed as part of the AI Agents with OpenAI specialization, designed to provide hands-on experience building production-ready agent systems.

**Course Design**: Coursera Learning Design Team
**Technical Development**: AI Agents Content Team
**Narrative Context**: Praxis AI consultancy and Innovate Logistics are fictional entities created for educational purposes

---

**Repository Version**: 1.1.0
**Last Updated**: 2025-11-20
**Course**: AI Agents with OpenAI - Course 2, Module 1
