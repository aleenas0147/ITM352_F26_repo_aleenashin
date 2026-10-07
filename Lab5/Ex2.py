miles = [1.1, 0.8, 2.5, 2.6]
fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
	"miles": miles,
	"fares": fares,
}

print(trips)

duration_fares = dict(zip(miles, fares))
print(duration_fares)

third_duration = list(duration_fares.keys())[2]
third_fare = duration_fares[third_duration]
print(f"3rd trip: {third_duration} miles, {third_fare}")
