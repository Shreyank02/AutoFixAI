from app_rag.scanner import RepositoryScanner

scanner = RepositoryScanner(
    "workspace/repositories/licence-plate-detection-and-iot-integration"
)

context = scanner.scan()

print("=" * 60)

print("Repository :", context.name)
print("Language   :", context.language)
print("Files      :", len(context.files))

print()

for file in context.files:

    print(
        file.path,
        "|",
        file.language,
        "|",
        file.extension,
    )

print("=" * 60)

print("Repository :", context.name)

print("Language   :", context.language)

print("Project    :", context.project_type)

print("Framework  :", context.framework)

print()

print("Entry Points")

if context.entry_points:

    for entry in context.entry_points:

        print("-", entry)

else:

    print("None")

print()

print("Features")

for feature in context.features:

    print("-", feature)

print()

print("Files :", len(context.files))

print("=" * 60)

print()

print("Libraries")

for lib in context.libraries:

    print("-", lib)

print()

print("=" * 60)

print("Python File Structures")

print("=" * 60)

for file in context.files:

    if file.extension != ".py":
        continue

    print()

    print(file.path)

    print("Imports :", file.structure.imports)

    print("Classes :", file.structure.classes)

    print("Functions :", file.structure.functions)

    print("Globals :", file.structure.globals)

    print("Lines :", file.structure.line_count)