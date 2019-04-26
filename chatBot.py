import json
import re

def starting_input():
	#enter the path of the input file
	path = user_input("Enter the path of the input file")

    # read the selected input file
	with open(path, 'r') as fileData:
		inputData = json.loads(fileData.read())

	# call the chat from selected input files
        func1 = inputData["function"]
        func = func1.replace('-', '_').lower() 
	eval("{0}({1})".format(func, inputData["questions"]))

def sample_text_function(question_matrix):
	# interface to store local variables
	localVar = {}

    # iterating the structure in questionArray
	for value in question_matrix:
		if value.get('instruction'):
			extract_instruction(value, localVar)
		elif value.get("text"):
            # finding all rows of type row[i] in value["var"]
			rows = re.findall('.*(\[.*?\]).*', value["var"]) 
			if rows:
				tempList = input_variable(value, localVar)
                # function to append the input row
				listRow = "{0}.append('{1}')".format(value["var"].split("[")[0], tempList)
				eval(listRow, localVar)
			else:
				localVar[value["var"]] = input_variable(value, localVar)
		elif value.get("calculated_variable"):
			localVar[value["var"]] = calculated_variable(value, localVar)

def extract_instruction(value, localVar):
	output = value["instruction"]

	if value.get("list_var") and value.get("list_length"):
		for i in range(0, int(value["list_length"])):
			localVar["i"] = i
			args = [eval(x, localVar) for x in value["instruction_var"]]
			output = value["instruction"] % tuple(args)
			print(output)

		return
	elif value.get("instruction_var"):
		args = [localVar[value] for value in value["instruction_var"]]
		output = output % tuple(args)

	print(output)

def input_variable(value, localVar):
	var = value["var"]

    # get condition
	if value.get("conditions"):
		conditions = value.get("conditions")
		andCondition = ["(" + " and ".join(row) + ")" for row in conditions]
		cond = " or ".join(andCondition)

		while eval(cond, localVar):
			localVar[var] = user_input(value["text"], value.get("options"))
	else:
		# user input
		tempList = user_input(value["text"], value.get("options"))

	return localVar.get(var) or tempList

def calculated_variable(value, localVar):
	return eval(value["formula"], localVar)


def user_input(text, options=["assignment_1_input_1.json","assignment_1_input_2.json"]):
	queryInput, option = "", ""

    # making the option string to make it feasible for the user
	if options:
		option = "(" + " / ".join(options) + ")"

	# raw_input for python 2 & input for python 3 ....dependending on which version one is using
	try:
		queryInput =  raw_input("{0} {1}: ".format(text, option))
	except NameError:
		queryInput = input("{0} {1}: ".format(text, option))

    # check- if user entered incorrect or unexpected value
	if options and queryInput not in options:
		print("Invalid option entered. Please select any one among these {0}".format(option))
		queryInput = user_input(text, options)

	return queryInput

if __name__ == "__main__":
	starting_input()
