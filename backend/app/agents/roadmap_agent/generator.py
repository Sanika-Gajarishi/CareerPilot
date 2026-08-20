from app.agents.roadmap_agent.schemas import (
    CareerGoalRequest,
    CareerRoadmap,
    MonthlyMilestone,
)
from app.agents.roadmap_agent.resources import LearningResourceRecommender
from app.agents.roadmap_agent.planner import RoadmapPlanner
from app.agents.roadmap_agent.recommender import ProjectRecommender
from app.agents.roadmap_agent.schemas import RoadmapProgress

class RoadmapGenerator:

    ROADMAP_TEMPLATES = {

        "AI Engineer": [

            {
                "title": "Python Fundamentals",
                "objective": "Master Python programming and problem solving.",
                "skills": [
                    "Python",
                    "OOP",
                    "Git",
                    "Problem Solving",
                ],
                "project": "Python CLI Task Manager",
            },

            {
                "title": "Machine Learning",
                "objective": "Build strong ML fundamentals.",
                "skills": [
                    "NumPy",
                    "Pandas",
                    "Scikit-Learn",
                    "Data Visualization",
                ],
                "project": "House Price Prediction",
            },

            {
                "title": "Deep Learning",
                "objective": "Understand neural networks and CNNs.",
                "skills": [
                    "TensorFlow",
                    "PyTorch",
                    "CNN",
                    "Transfer Learning",
                ],
                "project": "Image Classifier",
            },

            {
                "title": "LLMs & RAG",
                "objective": "Learn modern Generative AI.",
                "skills": [
                    "Transformers",
                    "RAG",
                    "Embeddings",
                    "Vector Database",
                ],
                "project": "PDF Chat Assistant",
            },

            {
                "title": "AI Agents",
                "objective": "Build production AI agents.",
                "skills": [
                    "LangChain",
                    "LangGraph",
                    "MCP",
                    "Tool Calling",
                ],
                "project": "Multi-Agent Assistant",
            },

            {
                "title": "Deployment",
                "objective": "Deploy production-ready AI systems.",
                "skills": [
                    "FastAPI",
                    "Docker",
                    "PostgreSQL",
                    "CI/CD",
                ],
                "project": "CareerPilot AI",
            },

        ]
        ,
        "QA Engineer": [
            {"title": "Testing Fundamentals", "objective": "Learn software testing principles, test design, and defect life cycles.", "skills": ["Test Cases", "Test Plans", "SDLC", "Defect Tracking"], "project": "Test Plan for a Web Application"},
            {"title": "Manual Testing", "objective": "Build confidence testing user flows, APIs, browsers, and edge cases.", "skills": ["Manual Testing", "API Testing", "Exploratory Testing", "Jira"], "project": "End-to-End Test Suite for an E-commerce App"},
            {"title": "Automation Testing", "objective": "Automate reliable regression tests for critical product workflows.", "skills": ["Selenium", "Playwright", "Python", "Page Object Model"], "project": "Playwright Regression Framework"},
            {"title": "Performance and Security", "objective": "Measure system behavior under load and identify common application risks.", "skills": ["JMeter", "Load Testing", "OWASP", "Postman"], "project": "Performance and API Quality Dashboard"},
            {"title": "CI/CD Quality Gates", "objective": "Integrate automated quality checks into a delivery pipeline.", "skills": ["GitHub Actions", "CI/CD", "Docker", "Quality Gates"], "project": "Automated Test Pipeline"},
        ],
        "Mechanical Engineer": [
            {"title": "Engineering Fundamentals", "objective": "Strengthen mechanics, materials, manufacturing, and engineering calculations.", "skills": ["Engineering Mechanics", "Materials", "Manufacturing", "Technical Drawing"], "project": "Component Design Calculation Report"},
            {"title": "CAD and Design", "objective": "Create accurate 3D models and production-ready engineering drawings.", "skills": ["CAD", "GD&T", "Assemblies", "Design for Manufacturing"], "project": "Parametric Mechanical Assembly"},
            {"title": "Analysis and Simulation", "objective": "Evaluate designs with structural, thermal, and motion analysis.", "skills": ["FEA", "ANSYS", "Stress Analysis", "Thermal Analysis"], "project": "FEA Validation of a Load-Bearing Part"},
            {"title": "Prototyping and Validation", "objective": "Turn designs into tested prototypes and document engineering decisions.", "skills": ["Prototyping", "Testing", "Root Cause Analysis", "Technical Reports"], "project": "Prototype Test and Validation Plan"},
            {"title": "Manufacturing and Delivery", "objective": "Prepare designs for production, cost review, and cross-functional delivery.", "skills": ["DFM", "BOM", "Six Sigma", "Project Management"], "project": "Manufacturing-Ready Product Package"},
        ],
        "Software Engineer": [
            {"title": "Programming Foundations", "objective": "Build strong programming, data structures, and version-control fundamentals.", "skills": ["Python", "Data Structures", "Algorithms", "Git"], "project": "Production-Quality CLI Application"},
            {"title": "Backend or Application Development", "objective": "Design maintainable applications with clear APIs and persistence.", "skills": ["REST APIs", "Databases", "Testing", "System Design"], "project": "Full-Stack Task Management API"},
            {"title": "Architecture and Reliability", "objective": "Design resilient services and reason about performance and failure modes.", "skills": ["Architecture", "Caching", "Observability", "Security"], "project": "Scalable Service Design"},
            {"title": "Deployment and Interview Readiness", "objective": "Ship a portfolio project and prepare for role-specific interviews.", "skills": ["Docker", "CI/CD", "Cloud", "Technical Interviews"], "project": "Deployed Production Application"},
        ],
    }

    ROLE_ALIASES = {
        "qa": "QA Engineer",
        "quality assurance": "QA Engineer",
        "quality assurance engineer": "QA Engineer",
        "mechanical": "Mechanical Engineer",
        "mechanical engineering": "Mechanical Engineer",
        "software": "Software Engineer",
        "software developer": "Software Engineer",
        "ai": "AI Engineer",
        "machine learning engineer": "AI Engineer",
    }

    @classmethod
    def _role_key(cls, target_role: str) -> str:
        normalized = " ".join(target_role.lower().strip().split())
        if normalized in cls.ROLE_ALIASES:
            return cls.ROLE_ALIASES[normalized]
        for role_name in cls.ROADMAP_TEMPLATES:
            if normalized == role_name.lower():
                return role_name
        return target_role.strip()

    @classmethod
    def _template_for(cls, target_role: str) -> list[dict]:
        role_key = cls._role_key(target_role)
        if role_key in cls.ROADMAP_TEMPLATES:
            return cls.ROADMAP_TEMPLATES[role_key]

        role = target_role.strip() or "the target role"
        return [
            {"title": f"{role} Foundations", "objective": f"Learn the core concepts and vocabulary used in {role}.", "skills": [role, "Industry Fundamentals", "Problem Solving", "Communication"], "project": f"{role} Fundamentals Portfolio"},
            {"title": f"{role} Tools and Practice", "objective": f"Practice the tools, workflows, and deliverables expected in {role} roles.", "skills": [role, "Professional Tools", "Documentation", "Quality Standards"], "project": f"{role} Practical Case Study"},
            {"title": f"{role} Portfolio Project", "objective": f"Complete a realistic project that demonstrates job-ready {role} capability.", "skills": [role, "Project Delivery", "Analysis", "Presentation"], "project": f"End-to-End {role} Project"},
            {"title": "Interview and Career Readiness", "objective": f"Prepare for {role} interviews and communicate your project impact clearly.", "skills": ["Interview Preparation", "Resume Storytelling", "Networking", "Negotiation"], "project": f"{role} Portfolio Review"},
        ]

    @classmethod
    def generate(
        cls,
        request: CareerGoalRequest,
    ) -> CareerRoadmap:

        role_key = cls._role_key(request.target_role)
        template = cls._template_for(role_key)

        monthly_plan = []

        months = min(
            request.timeline_months,
            len(template),
        )

        for month in range(months):

            phase = template[month]

            experience_note = (
                f" This {request.experience_level} track emphasizes "
                "guided practice and foundational outcomes."
                if request.experience_level.lower() in {"fresher", "0-1 years"}
                else " This track emphasizes independent delivery and interview depth."
            )
            company_note = (
                f" Prioritize examples relevant to {request.target_company}."
                if request.target_company
                else ""
            )

            weekly_tasks = RoadmapPlanner.create_weekly_plan(
                title=phase["title"],
                skills=phase["skills"],
                project=phase["project"],
                weekly_hours=request.weekly_hours,
            )

            monthly_plan.append(

                MonthlyMilestone(

                    month=month + 1,

                    title=phase["title"],

                    objective=phase["objective"] + experience_note + company_note,

                    skills=phase["skills"],

                    projects=[phase["project"]],

                    weekly_tasks=weekly_tasks,
                )

            )

        return CareerRoadmap(

            target_role=request.target_role,

            timeline_months=months,

            monthly_plan=monthly_plan,

            recommended_projects=ProjectRecommender.recommend(role_key),

            learning_resources=LearningResourceRecommender.recommend(role_key),

           progress=RoadmapProgress(),
        )