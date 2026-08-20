class CertificationExtractor:

    ISSUERS = [
        "AWS",
        "Microsoft",
        "Google",
        "IBM",
        "Oracle",
        "Cisco",
        "Meta",
        "Coursera",
        "Udemy",
        "NPTEL",
        "Infosys",
        "HackerRank",
        "OpenAI",
        "Anthropic",
        "DeepLearning.AI"
    ]

    @classmethod
    def extract(cls, certification_text: str):

        if not certification_text.strip():
            return []

        certifications = []

        lines = [
            line.strip()
            for line in certification_text.splitlines()
            if line.strip()
        ]

        for line in lines:

            issuer = ""

            for company in cls.ISSUERS:

                if company.lower() in line.lower():
                    issuer = company
                    break

            certifications.append(
                {
                    "name": line,
                    "issuer": issuer,
                }
            )

        return certifications