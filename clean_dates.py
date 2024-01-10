import csv
from datetime import datetime, timedelta


def get_correct_date(date_found, date_listed):
	# date_listed is in the format "prije 5 dana", "prije mjesec",...
	original_datetime = datetime.strptime(date_found, "%Y-%m-%d")
	vals = date_listed.split()
	offset_unit = vals[-1]

	# Check if its the same date
	same_day = ["minut", "minuta", "minute", "sat", "sati", "sata"]
	if offset_unit in same_day:
		return date_found

	if len(vals) == 3:
		offset_value = vals[1]
	else:
		offset_value = 1

	# Calculate the timedelta based on the offset
	if offset_unit in ["dan", "dana"]:
		offset_timedelta = timedelta(days=int(offset_value))
	elif offset_unit in ["mjeseci", "mjeseca", "mjesec"]:
		offset_timedelta = timedelta(days=int(offset_value) * 30)
	elif offset_unit in ["godina", "godine", "godinu"]:
		offset_timedelta = timedelta(days=int(offset_value) * 365)
	else:
		raise ValueError(f"Invalid input for {date_found} and {date_listed}")

	new_date = original_datetime - offset_timedelta
	new_date_str = new_date.strftime("%Y-%m-%d")
	return new_date_str


with open("raw_data.csv", "r") as f:
	reader = csv.reader(f, delimiter=";")
	data = list(reader)


clean_data = [data[0]]
for i, row in enumerate(data[1:]):
	if " u " in row[-4]:
		date = row[-4][:10]
		day, month, year = date.split(".")
		row[-4] = f"{year}-{month}-{day}"
	if "prije" in row[-4]:
		row[-4] = get_correct_date(row[-1], row[-4])
	clean_data.append(row)


with open("car_data.csv", "w") as f:
	writer = csv.writer(f, delimiter=";")
	writer.writerows(clean_data)
