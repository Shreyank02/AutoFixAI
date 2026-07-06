from pathlib import Path
from collections import Counter
import ast
from pathlib import Path

from app_rag.model import (
    RepositoryContext,
    FileInfo,
)
from app_rag.model import (
    RepositoryContext,
    FileInfo,
    FunctionInfo,
    ClassInfo,
)


class RepositoryScanner:

    STANDARD_LIBRARIES = {
        "os",
        "sys",
        "time",
        "math",
        "json",
        "re",
        "pathlib",
        "typing",
        "collections",
        "itertools",
        "functools",
        "datetime",
        "logging",
        "subprocess",
        "shutil",
        "glob",
        "random",
        "threading",
        "asyncio",
    }

    FRAMEWORK_MAP = {
        # Python
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "streamlit": "Streamlit",
        "gradio": "Gradio",
        "langchain": "LangChain",
        "langgraph": "LangGraph",

        # JavaScript
        "react": "React",
        "next": "Next.js",
        "express": "Express.js",
        "nestjs": "NestJS",
        "vue": "Vue",
        "angular": "Angular",

        # Java
        "spring": "Spring Boot",

        # Go
        "gin": "Gin",
        "fiber": "Fiber",
    }

    ENTRY_POINTS = {

        # Python
        "main.py",
        "app.py",
        "run.py",
        "manage.py",
        "server.py",

        # JavaScript
        "index.js",
        "main.js",
        "app.js",

        # TypeScript
        "index.ts",
        "main.ts",

        # React
        "index.jsx",
        "main.jsx",

        # TS React
        "index.tsx",
        "main.tsx",

        # Java
        "Application.java",
    }

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        ".idea",
        ".vscode",
        "node_modules",
        "venv",
        ".venv",
        "build",
        "dist",
        ".pytest_cache",
        ".mypy_cache",
    }

    IGNORED_SUFFIXES = {
        ".pyc",
        ".pyo",
        ".log",
        ".lock",
    }

    EXTENSION_LANGUAGE = {
        ".py": "Python",
        ".ipynb": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".php": "PHP",
        ".rb": "Ruby",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
    }

    def __init__(self, repository_path):

        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise FileNotFoundError(
                f"{self.repository_path} does not exist."
            )

    def _build_file_info(self, file_path):

        return FileInfo(
            path=file_path.relative_to(self.repository_path),
            extension=file_path.suffix,
            size=file_path.stat().st_size,
        )

    def _scan_files(self):

        files = []

        for path in self.repository_path.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in self.IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.suffix in self.IGNORED_SUFFIXES:
                continue

            files.append(
                self._build_file_info(path)
            )

        return files

    def _detect_language(self, context):

        languages = []

        for file in context.files:

            language = self.EXTENSION_LANGUAGE.get(
                file.extension
            )

            file.language = language

            if language:
                languages.append(language)

        if languages:

            context.language = Counter(
                languages
            ).most_common(1)[0][0]

        return context

    def scan(self):

        context = RepositoryContext(
            name=self.repository_path.name,
            root_path=self.repository_path,
        )

        context.files = self._scan_files()

        context = self._detect_language(context)

        context = self._profile_repository(context)

        return context
    
    def _detect_project_type(self, context):

        extensions = {
            file.extension.lower()
            for file in context.files
        }

        names = {
            file.path.name.lower()
            for file in context.files
        }

        libraries = {
            lib.lower()
            for lib in context.libraries
        }

        if ".ipynb" in extensions:
            context.project_type = "Machine Learning"

        elif "fastapi" in libraries or "flask" in libraries:
            context.project_type = "Backend API"

        elif "django" in libraries:
            context.project_type = "Web Application"

        elif "react" in libraries:
            context.project_type = "Frontend"

        elif "next" in libraries:
            context.project_type = "Full Stack"

        elif ".ino" in extensions:
            context.project_type = "IoT"

        return context
    
    def _profile_repository(self, context):

        profilers = [
            self._detect_requirements,
            self._detect_imports,
            self._detect_framework,
            self._detect_project_type,
            self._detect_entry_points,
            self._analyze_code,
        ]

        for profiler in profilers:
            context = profiler(context)
        return context
    
    def _detect_requirements(self, context):

        requirements = self.repository_path / "requirements.txt"

        if not requirements.exists():
            return context

        with open(
            requirements,
            "r",
            encoding="utf-8",
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                package = (
                    line
                    .split("==")[0]
                    .split(">=")[0]
                    .split("<=")[0]
                    .strip()
                )

                context.libraries.append(package)

        return context
    
    def _detect_imports(self, context):

        libraries = set(context.libraries)

        for file in context.files:

            if file.extension != ".py":
                continue

            file_path = self.repository_path / file.path

            try:

                source = file_path.read_text(
                    encoding="utf-8"
                )

                tree = ast.parse(source)

            except Exception:
                continue

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        libraries.add(
                            alias.name.split(".")[0]
                        )

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        libraries.add(
                            node.module.split(".")[0]
                        )
        
        libraries = {
            lib
            for lib in libraries
            if lib not in self.STANDARD_LIBRARIES
        }

        context.libraries = sorted(libraries)

        return context
    
    def _detect_framework(self, context):

        for library in context.libraries:

            framework = self.FRAMEWORK_MAP.get(
                library.lower()
            )

            if framework:

                context.framework = framework

                return context

        return context
    
    def _detect_entry_points(self, context):

        for file in context.files:

            if file.path.name in self.ENTRY_POINTS:

                context.entry_points.append(
                    file.path
                )

        return context
    
    def _analyze_python_file(
        self,
        file,
    ):

        path = self.repository_path / file.path

        try:

            source = path.read_text(
                encoding="utf-8"
            )

        except Exception:

            return

        file.structure.line_count = len(
            source.splitlines()
        )

        try:

            tree = ast.parse(source)

        except Exception:

            return

        imports = []

        classes = []

        functions = []

        globals_ = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    imports.append(
                        alias.name
                    )

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    imports.append(
                        node.module
                    )

            elif isinstance(node, ast.ClassDef):

                classes.append(

                    ClassInfo(
                        name=node.name,
                        start_line=node.lineno,
                        end_line=node.end_lineno,
                    )

                )

            elif isinstance(node, ast.FunctionDef):

                functions.append(

                    FunctionInfo(
                        name=node.name,
                        start_line=node.lineno,
                        end_line=node.end_lineno,
                    )

                )

            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(
                        target,
                        ast.Name,
                    ):

                        globals_.append(
                            target.id
                        )

        file.structure.imports = sorted(
            set(imports)
        )

        file.structure.functions = functions

        file.structure.classes = classes
        
        file.structure.globals = sorted(
            globals_
        )

    def _analyze_code(
        self,
        context,
    ):

        for file in context.files:

            if file.extension != ".py":

                continue

            self._analyze_python_file(
                file
            )

        return context
    
