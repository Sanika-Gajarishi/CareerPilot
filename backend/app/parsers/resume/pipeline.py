def process(raw_text: str):

    sections = split_sections(raw_text)

    parsed_data = {
        "contact": extract_contact(sections),
        "summary": extract_summary(sections),
        "skills": extract_skills(sections),
        "experience": extract_experience(sections),
        "projects": extract_projects(sections),
        "education": extract_education(sections),
        "certifications": extract_certifications(sections),
        "publications": extract_publications(sections),
    }

    # Normalize skills here
    parsed_data["skills"] = normalize_skills(parsed_data["skills"])

    return parsed_data