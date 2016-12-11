


def get_names(list_poke):
	poke = open("Pokenames.txt", "r" )

	for line in poke:
		print line
		list_poke.append(line)
	return list_poke



list_poke = []
print list_poke
list_poke = get_names(list_poke)

print list_poke





