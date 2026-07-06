from agents.workflow import workflow

print("=" * 80)
print("AUTOFIX AI - END TO END WORKFLOW TEST")
print("=" * 80)

state = {

    "issue_title":
        "Database lookup fails",

    "issue_body":
        """
Vehicle is detected correctly.
The detected plate is printed correctly.

However, the lookup always returns False even though
the plate exists in the database.
""",

    "repository":
        "licence-plate-detection-and-iot-integration",

    "repository_summary": "",

    "retrieved_context": "",

    "implementation_plan": None,

    "generated_code": None,

    "review_status": False,

    "review_report": "",

}

print("\nStarting Workflow...\n")

result = workflow.invoke(state)

print("\n")
print("=" * 80)
print("WORKFLOW COMPLETED")
print("=" * 80)

#################################################################
# Repository Summary
#################################################################

print("\n[1] REPOSITORY SUMMARY")
print("-" * 80)

print(result["repository_summary"])

#################################################################
# Retrieved Context
#################################################################

print("\n[2] RETRIEVED CONTEXT")
print("-" * 80)

context = result["retrieved_context"]

print(context[:2500])

if len(context) > 2500:

    print("\n... Context Truncated ...")

#################################################################
# Analyzer
#################################################################

print("\n[3] ANALYZER OUTPUT")
print("-" * 80)

plan = result["implementation_plan"]

if plan is None:

    print("Analyzer returned nothing.")

else:

    print(f"Problem:\n{plan.problem}\n")

    print(f"Root Cause:\n{plan.root_cause}\n")

    print(f"Confidence : {plan.confidence}\n")

    print("Evidence")

    for item in plan.evidence:

        print(f"  • {item}")

    print()

    print("Missing Information")

    for item in plan.missing_information:

        print(f"  • {item}")

    print()

    print("Files To Modify")

    for file in plan.files_to_modify:

        print(f"  • {file}")

    print()

    print("Implementation Steps")

    for step in plan.implementation_steps:

        print(f"  • {step}")

    print()

    print("Testing Strategy")

    for step in plan.testing_strategy:

        print(f"  • {step}")

#################################################################
# Developer
#################################################################

print("\n[4] DEVELOPER OUTPUT")
print("-" * 80)

developer = result["generated_code"]

if developer is None:

    print("Developer did not generate patches.")

else:

    print(f"Total Patches : {len(developer.patches)}")

    for i, patch in enumerate(developer.patches, start=1):

        print("\n")
        print("=" * 60)
        print(f"PATCH {i}")
        print("=" * 60)

        print(f"File   : {patch.file}")
        print(f"Symbol : {patch.symbol}")
        print(f"Reason : {patch.reason}")

        print("\nOLD CODE")
        print("-" * 40)
        print(patch.old_code)

        print("\nNEW CODE")
        print("-" * 40)
        print(patch.new_code)

#################################################################
# Reviewer
#################################################################

print("\n[5] REVIEWER")
print("-" * 80)

print("Validation :", result["review_status"])

print()

if result["review_report"]:

    print(result["review_report"])

else:

    print("Patch validation passed.")

#################################################################
# State Validation
#################################################################

print("\n[6] WORKFLOW STATE")
print("-" * 80)

for key, value in result.items():

    print(f"{key:<25} -> {type(value).__name__}")

#################################################################
# Final Status
#################################################################

print("\n")
print("=" * 80)

if result["review_status"]:

    print("WORKFLOW PASSED")

else:

    print("WORKFLOW FAILED")

print("=" * 80)