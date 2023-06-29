import pandas as pd

job_titles = [
    'data scientist',
    'software engineer',
    'web developer',
    'data analyst',
    'product manager',
    'UX/UI designer',
    'business analyst',
    'network administrator',
    'database administrator',
    'cybersecurity specialist',
    'AI researcher',
    'machine learning engineer',
    'frontend developer',
    'backend developer',
    'systems analyst',
    'cloud architect',
    'full-stack developer',
    'data engineer',
    'DevOps engineer',
    'IT project manager',
    'network engineer',
    'data architect',
    'software tester',
    'mobile app developer',
    'business intelligence analyst',
    'IT consultant',
    'data visualization specialist',
    'system administrator',
    'game developer',
    'IT support specialist',
    'IT security analyst',
    'database developer',
    'network security engineer',
    'data mining specialist',
    'UI designer',
    'system architect',
    'IT auditor',
    'QA engineer',
    'computer programmer',
    'artificial intelligence engineer',
    'network manager',
    'IT trainer',
    'IT business analyst',
    'data quality analyst',
    'software architect',
    'IT operations manager',
    'data warehouse developer',
    'big data engineer',
    'IT director',
    'IT service manager',
    'software quality assurance analyst'
]

skills = [
    'python, machine learning, data analysis, deep learning, natural language processing',
    'java, software development, problem-solving, object-oriented programming, algorithms',
    'html, css, javascript, web design, responsive design, front-end frameworks',
    'sql, data visualization, statistics, data cleaning, data modeling',
    'product development, project management, agile, market research, leadership',
    'user research, wireframing, prototyping, UI design, interaction design',
    'requirements gathering, business process modeling, data analysis, communication skills',
    'network configuration, troubleshooting, security protocols, network monitoring, routing protocols',
    'database management, SQL queries, performance tuning, backup and recovery, data integrity',
    'network security, vulnerability assessment, incident response, security frameworks, penetration testing',
    'machine learning algorithms, neural networks, reinforcement learning, data preprocessing, model evaluation',
    'data preprocessing, feature engineering, model training, model deployment, optimization algorithms',
    'html, css, javascript, front-end frameworks, responsive design, cross-browser compatibility',
    'python, java, c++, databases, debugging, version control',
    'requirements analysis, systems design, software testing, project management, documentation',
    'cloud platforms (e.g., AWS, Azure), infrastructure design, scalability, cost optimization, security',
    'html, css, javascript, backend frameworks, RESTful APIs, database integration',
    'data pipeline, data warehousing, ETL processes, data modeling, data transformation',
    'containerization, continuous integration/continuous deployment (CI/CD), infrastructure automation, monitoring, cloud services',
    'project management, risk assessment, stakeholder management, budgeting, quality assurance',
    'network protocols, routing and switching, network troubleshooting, network monitoring tools, WAN optimization',
    'data modeling, data integration, data governance, data quality, data warehouse design',
    'test planning, test case design, test execution, defect management, test automation',
    'mobile app development, iOS, Android, cross-platform frameworks, user experience (UX), mobile'
]

# Truncate the job_titles list to match the length of the skills list
job_titles = job_titles[:len(skills)]

# Create a DataFrame from the job_titles and skills lists
df = pd.DataFrame({"Job Title": job_titles, "Skills": skills})

# Print the DataFrame
# print(df)
df
