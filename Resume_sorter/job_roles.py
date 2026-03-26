JOB_ROLES = {
    "Software Engineer": {
        "job_id": "swe_001",
        "title": "Software Engineer",
        "department": "Engineering",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Builds backend services, APIs, internal tools, and production software systems. Strong coding fundamentals, version control, debugging, and database knowledge are required.",

        "required_skills": [
            "python",
            "sql",
            "git",
            "api development",
            "debugging",
            "data structures",
            "algorithms",
            "software development",
            "object oriented programming"
        ],

        "preferred_skills": [
            "fastapi",
            "flask",
            "django",
            "docker",
            "aws",
            "azure",
            "gcp",
            "postgresql",
            "rest api",
            "microservices",
            "unit testing",
            "ci/cd",
            "linux",
            "react",
            "javascript"
        ],

        "required_tools": [
            "git",
            "github"
        ],

        "preferred_tools": [
            "docker",
            "jira",
            "postman",
            "github actions",
            "jenkins",
            "kubernetes"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "aws certified developer",
            "aws certified cloud practitioner"
        ],

        "required_education": [
            "computer science",
            "software engineering",
            "computer engineering",
            "electrical engineering"
        ],

        "preferred_education": [
            "bachelor",
            "master"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 4,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "software",
            "saas",
            "technology",
            "defense",
            "fintech"
        ],

        "keyword_groups": {
            "backend": ["python", "flask", "fastapi", "django", "backend", "api", "rest"],
            "database": ["sql", "postgresql", "mysql", "database", "query"],
            "cloud": ["aws", "azure", "gcp", "cloud"],
            "devops": ["docker", "kubernetes", "ci/cd", "jenkins", "github actions"],
            "frontend_bonus": ["react", "javascript", "typescript", "html", "css"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 4,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 12,
            "preferred_skill": 4,
            "required_tool": 6,
            "preferred_tool": 2,
            "required_certification": 8,
            "preferred_certification": 3,
            "required_education": 8,
            "preferred_education": 3,
            "minimum_experience_met": 15,
            "preferred_experience_met": 8,
            "industry_match": 2,
            "keyword_group_match": 3
        }
    },

    "Senior Software Engineer": {
        "job_id": "swe_002",
        "title": "Senior Software Engineer",
        "department": "Engineering",
        "seniority": "Senior",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Designs and builds scalable production systems, mentors engineers, contributes to architecture, and owns major engineering deliverables.",

        "required_skills": [
            "python",
            "sql",
            "git",
            "api development",
            "system design",
            "software architecture",
            "debugging",
            "unit testing",
            "code review",
            "scalable systems"
        ],

        "preferred_skills": [
            "aws",
            "docker",
            "kubernetes",
            "microservices",
            "distributed systems",
            "ci/cd",
            "postgresql",
            "leadership",
            "mentoring",
            "performance optimization"
        ],

        "required_tools": [
            "git",
            "github",
            "postman"
        ],

        "preferred_tools": [
            "docker",
            "kubernetes",
            "jira",
            "jenkins",
            "github actions"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "aws certified developer",
            "aws solutions architect"
        ],

        "required_education": [
            "computer science",
            "software engineering",
            "computer engineering",
            "electrical engineering"
        ],

        "preferred_education": [
            "bachelor",
            "master"
        ],

        "minimum_years_experience": 5,
        "preferred_years_experience": 7,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "software",
            "cloud",
            "saas",
            "defense",
            "enterprise technology"
        ],

        "keyword_groups": {
            "architecture": ["system design", "architecture", "distributed systems", "scalable systems"],
            "backend": ["python", "api", "backend", "rest", "microservices"],
            "cloud_devops": ["aws", "docker", "kubernetes", "ci/cd"],
            "leadership": ["mentor", "mentoring", "lead", "technical lead", "code review"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 5,
            "require_minimum_years": True,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 14,
            "preferred_skill": 5,
            "required_tool": 6,
            "preferred_tool": 3,
            "required_certification": 8,
            "preferred_certification": 4,
            "required_education": 8,
            "preferred_education": 3,
            "minimum_experience_met": 18,
            "preferred_experience_met": 10,
            "industry_match": 3,
            "keyword_group_match": 4
        }
    },

    "Data Analyst": {
        "job_id": "da_001",
        "title": "Data Analyst",
        "department": "Data / Analytics",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Analyzes business and operational data, creates dashboards, generates reports, and communicates insights to stakeholders.",

        "required_skills": [
            "sql",
            "excel",
            "data analysis",
            "reporting",
            "data cleaning",
            "data visualization",
            "communication"
        ],

        "preferred_skills": [
            "python",
            "power bi",
            "tableau",
            "statistics",
            "dashboards",
            "business intelligence",
            "etl",
            "automation"
        ],

        "required_tools": [
            "excel",
            "sql"
        ],

        "preferred_tools": [
            "power bi",
            "tableau",
            "python",
            "google sheets"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "microsoft power bi data analyst",
            "google data analytics"
        ],

        "required_education": [
            "data analytics",
            "statistics",
            "mathematics",
            "computer science",
            "information systems",
            "business analytics",
            "economics"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 4,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "finance",
            "operations",
            "technology",
            "healthcare",
            "government"
        ],

        "keyword_groups": {
            "analysis": ["data analysis", "analysis", "reporting", "insights", "metrics"],
            "bi": ["power bi", "tableau", "dashboard", "visualization"],
            "technical": ["sql", "python", "etl", "data cleaning"],
            "business": ["stakeholders", "operations", "kpi", "business intelligence"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 12,
            "preferred_skill": 4,
            "required_tool": 7,
            "preferred_tool": 3,
            "required_certification": 8,
            "preferred_certification": 4,
            "required_education": 7,
            "preferred_education": 2,
            "minimum_experience_met": 15,
            "preferred_experience_met": 7,
            "industry_match": 2,
            "keyword_group_match": 3
        }
    },

    "Operations Manager": {
        "job_id": "ops_001",
        "title": "Operations Manager",
        "department": "Operations",
        "seniority": "Manager",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Oversees business operations, cross-functional coordination, reporting, process improvement, and execution against organizational goals.",

        "required_skills": [
            "operations",
            "project management",
            "process improvement",
            "communication",
            "reporting",
            "team coordination",
            "excel"
        ],

        "preferred_skills": [
            "power bi",
            "erp",
            "budgeting",
            "forecasting",
            "vendor management",
            "supply chain",
            "kpi management",
            "leadership"
        ],

        "required_tools": [
            "excel"
        ],

        "preferred_tools": [
            "power bi",
            "asana",
            "monday.com",
            "jira",
            "sap",
            "oracle"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "pmp",
            "lean six sigma green belt"
        ],

        "required_education": [
            "business",
            "operations management",
            "supply chain",
            "industrial engineering",
            "management"
        ],

        "preferred_education": [
            "bachelor",
            "mba"
        ],

        "minimum_years_experience": 3,
        "preferred_years_experience": 5,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "manufacturing",
            "logistics",
            "government",
            "defense",
            "technology"
        ],

        "keyword_groups": {
            "operations": ["operations", "process", "workflow", "execution", "coordination"],
            "management": ["manager", "leadership", "team lead", "stakeholder management"],
            "analytics": ["reporting", "excel", "dashboard", "kpi", "power bi"],
            "process_improvement": ["lean", "six sigma", "process improvement", "optimization"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": True,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 12,
            "preferred_skill": 4,
            "required_tool": 6,
            "preferred_tool": 3,
            "required_certification": 8,
            "preferred_certification": 5,
            "required_education": 8,
            "preferred_education": 3,
            "minimum_experience_met": 16,
            "preferred_experience_met": 8,
            "industry_match": 3,
            "keyword_group_match": 3
        }
    },

    "Project Manager": {
        "job_id": "pm_001",
        "title": "Project Manager",
        "department": "Program / Project Management",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Manages timelines, deliverables, risks, stakeholders, documentation, and cross-functional execution for projects and programs.",

        "required_skills": [
            "project management",
            "scheduling",
            "risk management",
            "stakeholder management",
            "communication",
            "documentation",
            "coordination"
        ],

        "preferred_skills": [
            "budgeting",
            "agile",
            "scrum",
            "kanban",
            "process improvement",
            "reporting",
            "leadership"
        ],

        "required_tools": [
            "excel"
        ],

        "preferred_tools": [
            "jira",
            "asana",
            "monday.com",
            "smartsheet",
            "microsoft project"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "pmp",
            "certified scrum master",
            "prince2"
        ],

        "required_education": [
            "business",
            "management",
            "project management",
            "operations",
            "engineering"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 3,
        "preferred_years_experience": 5,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "technology",
            "construction",
            "government",
            "defense",
            "operations"
        ],

        "keyword_groups": {
            "project_core": ["project management", "timeline", "deliverables", "milestones", "coordination"],
            "stakeholders": ["stakeholder", "cross-functional", "communication", "meeting"],
            "methodologies": ["agile", "scrum", "kanban"],
            "execution": ["risk", "budget", "planning", "tracking"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": True,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 12,
            "preferred_skill": 4,
            "required_tool": 5,
            "preferred_tool": 3,
            "required_certification": 8,
            "preferred_certification": 6,
            "required_education": 7,
            "preferred_education": 2,
            "minimum_experience_met": 16,
            "preferred_experience_met": 8,
            "industry_match": 2,
            "keyword_group_match": 3
        }
    },

    "HR Generalist": {
        "job_id": "hr_001",
        "title": "HR Generalist",
        "department": "Human Resources",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Supports recruiting, onboarding, employee relations, HR operations, compliance, and HRIS administration.",

        "required_skills": [
            "human resources",
            "onboarding",
            "employee relations",
            "recruiting",
            "communication",
            "documentation",
            "compliance"
        ],

        "preferred_skills": [
            "hris",
            "benefits administration",
            "policy management",
            "performance management",
            "training",
            "interviewing"
        ],

        "required_tools": [
            "excel"
        ],

        "preferred_tools": [
            "bamboohr",
            "workday",
            "adp",
            "greenhouse"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "shrm-cp",
            "phr"
        ],

        "required_education": [
            "human resources",
            "business",
            "management",
            "psychology"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 4,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "corporate",
            "technology",
            "healthcare",
            "government"
        ],

        "keyword_groups": {
            "hr_core": ["human resources", "employee relations", "onboarding", "recruiting"],
            "compliance": ["compliance", "policy", "documentation", "records"],
            "systems": ["hris", "bamboohr", "workday", "adp"],
            "people_ops": ["training", "interviewing", "performance management", "benefits"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 11,
            "preferred_skill": 4,
            "required_tool": 5,
            "preferred_tool": 3,
            "required_certification": 8,
            "preferred_certification": 6,
            "required_education": 7,
            "preferred_education": 2,
            "minimum_experience_met": 14,
            "preferred_experience_met": 7,
            "industry_match": 2,
            "keyword_group_match": 3
        }
    },

    "Recruiter": {
        "job_id": "rec_001",
        "title": "Recruiter",
        "department": "Talent Acquisition",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Sources, screens, and manages candidates through the hiring pipeline while coordinating with hiring managers and HR systems.",

        "required_skills": [
            "recruiting",
            "sourcing",
            "screening",
            "candidate communication",
            "interview coordination",
            "communication",
            "pipeline management"
        ],

        "preferred_skills": [
            "boolean search",
            "ats",
            "offer management",
            "stakeholder management",
            "linkedin recruiting",
            "talent acquisition"
        ],

        "required_tools": [],
        "preferred_tools": [
            "linkedin recruiter",
            "greenhouse",
            "lever",
            "bamboohr",
            "workday"
        ],

        "required_certifications": [],
        "preferred_certifications": [],

        "required_education": [
            "human resources",
            "business",
            "communications",
            "psychology"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 4,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "staffing",
            "technology",
            "corporate",
            "agency recruiting"
        ],

        "keyword_groups": {
            "recruiting_core": ["recruiting", "sourcing", "screening", "candidate pipeline"],
            "ats": ["ats", "greenhouse", "lever", "workday", "bamboohr"],
            "outreach": ["candidate communication", "outreach", "interview scheduling"],
            "search": ["boolean search", "linkedin recruiter", "talent acquisition"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 11,
            "preferred_skill": 4,
            "required_tool": 4,
            "preferred_tool": 4,
            "required_certification": 6,
            "preferred_certification": 3,
            "required_education": 6,
            "preferred_education": 2,
            "minimum_experience_met": 14,
            "preferred_experience_met": 7,
            "industry_match": 2,
            "keyword_group_match": 3
        }
    },

    "Cybersecurity Analyst": {
        "job_id": "cyber_001",
        "title": "Cybersecurity Analyst",
        "department": "Security",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Monitors security events, supports incident response, conducts vulnerability analysis, and helps maintain organizational cybersecurity posture.",

        "required_skills": [
            "cybersecurity",
            "incident response",
            "vulnerability management",
            "security monitoring",
            "network security",
            "risk assessment",
            "documentation"
        ],

        "preferred_skills": [
            "siem",
            "splunk",
            "soc",
            "threat detection",
            "firewalls",
            "iam",
            "linux",
            "python"
        ],

        "required_tools": [],
        "preferred_tools": [
            "splunk",
            "wireshark",
            "nessus",
            "crowdstrike"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "security+",
            "cysa+",
            "cissp"
        ],

        "required_education": [
            "cybersecurity",
            "computer science",
            "information technology",
            "information systems"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 4,

        "required_clearance": None,
        "preferred_clearance": "secret",

        "preferred_industries": [
            "government",
            "defense",
            "technology",
            "finance"
        ],

        "keyword_groups": {
            "security_ops": ["incident response", "soc", "siem", "security monitoring"],
            "tools": ["splunk", "nessus", "wireshark", "crowdstrike"],
            "infra": ["network security", "firewall", "linux", "iam"],
            "analysis": ["risk assessment", "vulnerability", "threat detection"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 13,
            "preferred_skill": 4,
            "required_tool": 5,
            "preferred_tool": 4,
            "required_certification": 8,
            "preferred_certification": 6,
            "required_education": 7,
            "preferred_education": 2,
            "minimum_experience_met": 15,
            "preferred_experience_met": 7,
            "industry_match": 3,
            "keyword_group_match": 3
        }
    },

    "Defense Program Analyst": {
        "job_id": "def_001",
        "title": "Defense Program Analyst",
        "department": "Program / Defense",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Supports defense or government programs through reporting, data analysis, program coordination, documentation, and stakeholder support. Clearance and government environment familiarity are strong positives.",

        "required_skills": [
            "analysis",
            "reporting",
            "excel",
            "documentation",
            "communication",
            "program support",
            "coordination"
        ],

        "preferred_skills": [
            "power bi",
            "sql",
            "government contracting",
            "defense",
            "budget tracking",
            "risk tracking",
            "process improvement"
        ],

        "required_tools": [
            "excel"
        ],

        "preferred_tools": [
            "power bi",
            "sharepoint",
            "sql"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "pmp"
        ],

        "required_education": [
            "business",
            "public administration",
            "engineering",
            "management",
            "analytics"
        ],

        "preferred_education": [
            "bachelor"
        ],

        "minimum_years_experience": 2,
        "preferred_years_experience": 5,

        "required_clearance": "secret",
        "preferred_clearance": "top secret",

        "preferred_industries": [
            "defense",
            "government",
            "aerospace",
            "federal contracting"
        ],

        "keyword_groups": {
            "program": ["program support", "program analyst", "coordination", "deliverables"],
            "gov_defense": ["defense", "government", "federal", "dod", "contract"],
            "analytics": ["reporting", "excel", "power bi", "sql", "metrics"],
            "execution": ["budget", "risk", "documentation", "stakeholder"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 4,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": True
        },

        "weights": {
            "required_skill": 12,
            "preferred_skill": 4,
            "required_tool": 6,
            "preferred_tool": 3,
            "required_certification": 6,
            "preferred_certification": 4,
            "required_education": 7,
            "preferred_education": 2,
            "minimum_experience_met": 14,
            "preferred_experience_met": 8,
            "industry_match": 4,
            "keyword_group_match": 4,
            "required_clearance_met": 20,
            "preferred_clearance_met": 8
        }
    },

    "Electrical Engineer": {
        "job_id": "ee_001",
        "title": "Electrical Engineer",
        "department": "Engineering",
        "seniority": "Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Designs, analyzes, tests, and supports electrical systems, circuits, hardware, and embedded or electronic components depending on the role focus.",

        "required_skills": [
            "electrical engineering",
            "circuit analysis",
            "testing",
            "troubleshooting",
            "schematics",
            "documentation"
        ],

        "preferred_skills": [
            "pcb design",
            "embedded systems",
            "matlab",
            "altium",
            "labview",
            "fpga",
            "verilog",
            "power systems",
            "analog design",
            "digital design"
        ],

        "required_tools": [],
        "preferred_tools": [
            "matlab",
            "labview",
            "altium",
            "multisim",
            "quartus"
        ],

        "required_certifications": [],
        "preferred_certifications": [
            "fe",
            "pe"
        ],

        "required_education": [
            "electrical engineering",
            "computer engineering"
        ],

        "preferred_education": [
            "bachelor",
            "master"
        ],

        "minimum_years_experience": 1,
        "preferred_years_experience": 3,

        "required_clearance": None,
        "preferred_clearance": "secret",

        "preferred_industries": [
            "defense",
            "electronics",
            "manufacturing",
            "energy",
            "aerospace"
        ],

        "keyword_groups": {
            "hardware": ["schematic", "testing", "troubleshooting", "hardware"],
            "design": ["pcb", "analog", "digital", "embedded", "circuit"],
            "tools": ["matlab", "labview", "altium", "multisim", "quartus"],
            "digital_logic": ["fpga", "verilog", "digital design"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": True,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 13,
            "preferred_skill": 4,
            "required_tool": 5,
            "preferred_tool": 3,
            "required_certification": 7,
            "preferred_certification": 5,
            "required_education": 10,
            "preferred_education": 3,
            "minimum_experience_met": 14,
            "preferred_experience_met": 7,
            "industry_match": 3,
            "keyword_group_match": 3,
            "preferred_clearance_met": 4
        }
    },

    "Administrative Assistant": {
        "job_id": "admin_001",
        "title": "Administrative Assistant",
        "department": "Administrative",
        "seniority": "Entry / Mid-Level",
        "location_type": "Open",
        "employment_type": "Full-Time",

        "summary": "Supports office operations through scheduling, communication, documentation, reporting, and administrative coordination.",

        "required_skills": [
            "administrative support",
            "scheduling",
            "communication",
            "organization",
            "documentation",
            "customer service"
        ],

        "preferred_skills": [
            "calendar management",
            "travel coordination",
            "data entry",
            "reporting",
            "microsoft office",
            "excel"
        ],

        "required_tools": [],
        "preferred_tools": [
            "microsoft office",
            "excel",
            "outlook",
            "google workspace"
        ],

        "required_certifications": [],
        "preferred_certifications": [],

        "required_education": [
            "business",
            "communications",
            "general studies"
        ],

        "preferred_education": [
            "associate",
            "bachelor"
        ],

        "minimum_years_experience": 1,
        "preferred_years_experience": 3,

        "required_clearance": None,
        "preferred_clearance": None,

        "preferred_industries": [
            "corporate",
            "education",
            "government",
            "healthcare"
        ],

        "keyword_groups": {
            "admin": ["administrative support", "office support", "scheduling", "organization"],
            "communication": ["communication", "customer service", "front desk"],
            "systems": ["microsoft office", "excel", "outlook", "calendar"],
            "support": ["data entry", "documentation", "travel coordination", "reporting"]
        },

        "disqualifiers": [],

        "hard_fail_rules": {
            "missing_required_skills_threshold": 3,
            "require_minimum_years": False,
            "require_degree_match": False,
            "require_clearance": False
        },

        "weights": {
            "required_skill": 10,
            "preferred_skill": 3,
            "required_tool": 4,
            "preferred_tool": 3,
            "required_certification": 5,
            "preferred_certification": 2,
            "required_education": 6,
            "preferred_education": 2,
            "minimum_experience_met": 12,
            "preferred_experience_met": 6,
            "industry_match": 2,
            "keyword_group_match": 2
        }
    }
}