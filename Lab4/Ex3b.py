survey_results = [5, 7, 3, 8]
respondent_IDs = (1012, 1035, 1021, 1053)

survey_results.append(0)
#Do the same operations using list slicing (e.g. [:2]) and the “+” operator rather than .insert()
survey_results = survey_results[:2] + [6] + survey_results[2:]

print(survey_results)