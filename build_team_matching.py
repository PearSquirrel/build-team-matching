# Build team matching algorithm should be independant of race, gender, and academic standing.
# This algorithm uses experience, various skill levels, specific case
# preferences, learning goals, and team member requests to determine which
# team to assign a given member of Convergent.


import xlrd
import pandas
df = pandas.read_excel('bt_responses.xlsx')
df.columns = [
        'timestamp',
        'name',
        'email',
        'gender',
        'resume_link',
        'school_year',
        'was_in_build_team',
        'major',
        'finance_experience',
        'competitor_analysis_experience',
        'presentation_experience',
        'marketing_experience',
        'design_experience',
        'project_management_experience',
        'business_strategy_experience',
        'business_experience_short_answer',
        'java',
        'python',
        'front-end',
        'back-end',
        'mobile',
        'data_analysis',
        'technical_short_answer',
        'blockchain_interest',
        'bpa_interest',
        'health_interest',
        'nlp_interest',
        'consulting_interest',
        'financial_modeling_interest',
        'marketing_interest',
        'UX_interest',
        'app_dev_interest',
        'data_analysis_ml_interest',
        'additional_requests',
        'knows_to_pay_dues'
        ]
#print the column names
print(df.columns)
#get the values for a given column
academic_standings = set(df['school_year'].values)
previous_build_teams = set(df['was_in_build_team'].values)

technical_major = ['CS','MIS','EE/ECE', 'MIS, Economics', 'Math','CS, Other Business (e.g. Finance, Marketing, Management, Supply Chain, Accounting, etc.)']

business_major = [
        'Undeclared business looking at MIS, Finance, or Accounting',
        "Other Business (e.g. Finance, Marketing, Management, Supply Chain, Accounting, etc.)",
        "'I'm undeclared but interested in MIS",
        'Undeclared Business',
        'Unspecified Business but planning on MIS with minor in Finance',
        'MIS',
        'MIS, Economics',
        'Other Business (e.g. Finance, Marketing, Management, Supply Chain, Accounting, etc.)',
        'CS, Other Business (e.g. Finance, Marketing, Management, Supply Chain, Accounting, etc.)'
        ]

business_skills = [
        'finance_experience',
        'competitor_analysis_experience',
        'presentation_experience',
        'marketing_experience',
        'design_experience',
        'project_management_experience',
        'business_strategy_experience'
        ]

tech_skills = [
        'java',
        'python',
        'front-end',
        'back-end',
        'mobile',
        'data_analysis'
        ]

score_mapping = {
        'No experience': 0,
        'Some experience': 1,
        'A lot of experience': 2
        }

for skill in tech_skills:
    df[skill] = df[skill].map(score_mapping)

for skill in business_skills:
    df[skill] = df[skill].map(score_mapping)

case_interests = [
        'blockchain_interest',
        'bpa_interest',
        'health_interest',
        'nlp_interest',
        ]

interest_mapping = [
        "Not interested at all": 0,
        "Not sure whether I'd be interested": 1,
        "Wouldn't mind doing it": 2,
        "Pretty interested": 3,
        "Extremely interested": 4
        ]

for interest in case_interests:
    df[interest] = df[interest].map(score_mapping)

def get_score(df, skills):
    score = sum([df[skill] for skill in skills])
    return score


df = df.assign(technical_score = lambda x: get_score(x, tech_skills))
df = df.assign(business_score = lambda x: get_score(x, business_skills))


for index, row in df.iterrows():
    print(row['name'], row['technical_score'], row['business_score'])


tech_score_avg = ...
tech_score_variance = ...
business_score_avg = ...
business_score_variance = ...

# TODO: just make the z-scores into columns in the dataframe
def summarize_skills(student):
    # ideally, we'd be dealing with the raw columns instea of the
    # tech_score/business_score summaries, but this is good enough for now
    tech_z_score = (tech_score(student) - tech_score_avg)/math.sqrt(tech_score_variance)
    business_z_score = (business_score(student) - business_score_avg)/math.sqrt(business_score_variance)
    return [tech_z_score, business_z_score]


cases = [
        'blockchain',
        'bpa',
        'health',
        'nlp'
        ]

case_mapping = {
        'blockchain': 'blockchain_interest',
        'bpa': 'bpa_interest',
        'health': 'health_interest',
        'nlp': 'nlp_interest'
        }

number_of_veterans = sum(df[previous_build_teams])
number_of_cases = len(cases)

expected_veterans = num_veterans/num_cases
# scores how good a given group is, where each student is a row in the table
# group is one of 
def get_group_score(students, case):
    individual_skill_scores = [summarize(student) for student in students]
    individual_preference_scores = [student[case_mapping[case]] for student in students]
    num_veterans_in_group = sum([student[previous_build_teams] for student in
        students])
    # TODO: not sure what the variance would be here if I don't want to deal
    # with all groups at once
    veterans_z_score = (num_veterans_in_group - expected_veterans)
    # TODO: should use something like a softmax function for preferences
    # because most of the time score -> actual preference is non-linear
    group_score = 1.0*sum(individual_skill_scores) + 2.5*sum(individual_preference_scores) + 1.5*veterans_z_score
    return group_score

#print(academic_standings)
#print(previous_build_teams)

#get a data frame with selected columns
FORMAT = ['name', 'email']
df_selected = df[FORMAT]
