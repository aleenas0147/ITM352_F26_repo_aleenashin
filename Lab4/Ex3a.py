survey_results = [5, 7, 3, 8]
respondent_IDs = (1012, 1035, 1021, 1053)

survey_results.append(0)
#add the response “6” to the list between the values 7 and 3 (in what will be the third position in the list) using the .insert() method.
survey_results.insert(2, 6)

print(survey_results)