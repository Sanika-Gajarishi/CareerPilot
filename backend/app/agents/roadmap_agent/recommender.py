from app.agents.roadmap_agent.schemas import ProjectRecommendation


class ProjectRecommender:

    PROJECTS = {

        "AI Engineer": [

            ProjectRecommendation(
                title="Python Automation Toolkit",
                difficulty="Beginner",
                duration_weeks=2,
                description=(
                    "Build automation scripts using Python to strengthen "
                    "programming fundamentals."
                ),
                skills=[
                    "Python",
                    "File Handling",
                    "OOP",
                ],
            ),

            ProjectRecommendation(
                title="House Price Prediction",
                difficulty="Intermediate",
                duration_weeks=3,
                description=(
                    "Develop a machine learning regression model "
                    "using Scikit-Learn."
                ),
                skills=[
                    "Machine Learning",
                    "Pandas",
                    "Scikit-Learn",
                ],
            ),

            ProjectRecommendation(
                title="Image Classification System",
                difficulty="Intermediate",
                duration_weeks=4,
                description=(
                    "Train a CNN model for image classification."
                ),
                skills=[
                    "Deep Learning",
                    "TensorFlow",
                    "CNN",
                ],
            ),

            ProjectRecommendation(
                title="RAG PDF Assistant",
                difficulty="Advanced",
                duration_weeks=4,
                description=(
                    "Create a Retrieval-Augmented Generation application "
                    "using FastAPI and ChromaDB."
                ),
                skills=[
                    "LLMs",
                    "RAG",
                    "ChromaDB",
                    "FastAPI",
                ],
            ),

            ProjectRecommendation(
                title="CareerPilot AI",
                difficulty="Advanced",
                duration_weeks=8,
                description=(
                    "Develop a production-ready AI career platform "
                    "with multiple AI agents."
                ),
                skills=[
                    "FastAPI",
                    "PostgreSQL",
                    "LangGraph",
                    "Authentication",
                ],
            ),

        ]
        ,
        "QA Engineer": [
            ProjectRecommendation(
                title="Playwright E-commerce Test Suite",
                difficulty="Intermediate",
                duration_weeks=4,
                description="Create a maintainable browser and API regression suite for an e-commerce workflow.",
                skills=["Playwright", "Python", "API Testing", "Page Object Model"],
            ),
            ProjectRecommendation(
                title="CI Quality Gate",
                difficulty="Advanced",
                duration_weeks=3,
                description="Run automated tests in CI and publish actionable quality reports for every change.",
                skills=["GitHub Actions", "CI/CD", "Test Reporting", "Docker"],
            ),
        ],
        "Mechanical Engineer": [
            ProjectRecommendation(
                title="Parametric Mechanical Assembly",
                difficulty="Intermediate",
                duration_weeks=5,
                description="Design a constrained assembly with production drawings, tolerances, and a bill of materials.",
                skills=["CAD", "GD&T", "Assemblies", "BOM"],
            ),
            ProjectRecommendation(
                title="FEA Design Validation",
                difficulty="Advanced",
                duration_weeks=6,
                description="Validate a load-bearing component through simulation, hand calculations, and a technical report.",
                skills=["FEA", "ANSYS", "Stress Analysis", "Technical Reporting"],
            ),
        ],
    }

    @classmethod
    def recommend(
        cls,
        target_role: str,
    ) -> list[ProjectRecommendation]:

        projects = cls.PROJECTS.get(target_role)
        if projects:
            return projects

        role = target_role.strip() or "your target role"
        return [
            ProjectRecommendation(
                title=f"{role} Portfolio Case Study",
                difficulty="Beginner",
                duration_weeks=3,
                description=f"Solve a realistic {role} problem and document your approach, decisions, and results.",
                skills=[role, "Problem Solving", "Documentation"],
            ),
            ProjectRecommendation(
                title=f"{role} End-to-End Project",
                difficulty="Intermediate",
                duration_weeks=6,
                description=f"Build and present an end-to-end project that demonstrates practical {role} skills.",
                skills=[role, "Project Delivery", "Quality Standards"],
            ),
        ]