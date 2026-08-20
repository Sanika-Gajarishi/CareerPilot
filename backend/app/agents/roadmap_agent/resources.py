from app.agents.roadmap_agent.schemas import LearningResource


class LearningResourceRecommender:

    RESOURCES = {

        "AI Engineer": [

            LearningResource(
                title="Python for Everybody",
                platform="Coursera",
                url="https://www.coursera.org",
                resource_type="Course",
                difficulty="Beginner",
                estimated_hours=40,
            ),

            LearningResource(
                title="Machine Learning Specialization",
                platform="Coursera",
                url="https://www.coursera.org",
                resource_type="Course",
                difficulty="Intermediate",
                estimated_hours=60,
            ),

            LearningResource(
                title="Deep Learning Specialization",
                platform="Coursera",
                url="https://www.coursera.org",
                resource_type="Course",
                difficulty="Intermediate",
                estimated_hours=80,
            ),

            LearningResource(
                title="FastAPI Documentation",
                platform="FastAPI",
                url="https://fastapi.tiangolo.com",
                resource_type="Documentation",
                difficulty="Intermediate",
                estimated_hours=20,
            ),

            LearningResource(
                title="LangGraph Documentation",
                platform="LangGraph",
                url="https://python.langchain.com",
                resource_type="Documentation",
                difficulty="Advanced",
                estimated_hours=25,
            ),

            LearningResource(
                title="LeetCode",
                platform="LeetCode",
                url="https://leetcode.com",
                resource_type="Practice",
                difficulty="All",
                estimated_hours=100,
            ),

        ]
        ,
        "QA Engineer": [
            LearningResource(
                title="Playwright Documentation",
                platform="Microsoft",
                url="https://playwright.dev/docs/intro",
                resource_type="Documentation",
                difficulty="Intermediate",
                estimated_hours=20,
            ),
            LearningResource(
                title="Postman API Testing",
                platform="Postman",
                url="https://learning.postman.com",
                resource_type="Practice",
                difficulty="Beginner",
                estimated_hours=15,
            ),
        ],
        "Mechanical Engineer": [
            LearningResource(
                title="Engineering Design and CAD Practice",
                platform="Coursera",
                url="https://www.coursera.org",
                resource_type="Course",
                difficulty="Intermediate",
                estimated_hours=45,
            ),
            LearningResource(
                title="Finite Element Analysis Fundamentals",
                platform="MIT OpenCourseWare",
                url="https://ocw.mit.edu",
                resource_type="Course",
                difficulty="Advanced",
                estimated_hours=50,
            ),
        ],

    }

    @classmethod
    def recommend(
        cls,
        target_role: str,
    ):

        resources = cls.RESOURCES.get(target_role)
        if resources:
            return resources

        role = target_role.strip() or "your target role"
        return [
            LearningResource(
                title=f"{role} Learning Path",
                platform="CareerPilot",
                url="https://www.coursera.org",
                resource_type="Course",
                difficulty="Beginner",
                estimated_hours=40,
            ),
            LearningResource(
                title=f"{role} Practice Portfolio",
                platform="CareerPilot",
                url="https://github.com",
                resource_type="Project",
                difficulty="Intermediate",
                estimated_hours=60,
            ),
        ]