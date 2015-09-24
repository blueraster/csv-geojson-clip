from operator import itemgetter
import csv
# ['2006', '582500.000000', '5942500.000000', '37']
# ['2014', '587500.000000', '5942500.000000', '66']
# ['2010', '752500.000000', '5942500.000000', '2']
# ['2014', '757500.000000', '5942500.000000', '2']
# ['2002', '697500.000000', '5942500.000000', '11']
# ['2009', '592500.000000', '5942500.000000', '36']
# ['2014', '667500.000000', '5942500.000000', '2']
root = '/Users/jnordling/projects/shape-temp/data/'
def main():
	data = []
	with open(root+'./NLD-5000-bubble.csv') as csvfile:
		rows = csv.reader(csvfile, delimiter=',')
		for row in rows:
			data.append(row)
	data = sorted(data, key=itemgetter(2), reverse=True)
	uniqueY = sorted(list(set([ i[2] for i in data])),reverse=True)
	uniqueX = sorted(list(set([ i[1] for i in data])),reverse=True)
	uniqueT = sorted(list(set([ i[0] for i in data])),reverse=False)
	dataForYear = []
	for year in uniqueT:
		for uy in uniqueY:
			x = sorted([row for row in data if row[0] == year and uy == row[2]],reverse=False)
			dataForYear = dataForYear+x
		break


	for i in dataForYear:
		print i
	print len(dataForYear)
	# for i in uniqueT:
	# 	print i
	# for id in uniqueY:
	# 	# print id
	# 	# # # z = sorted(data)
	# 	ys = sorted([row for row in data if id ==row[2]],key=itemgetter(1,0), reverse=False)
	# 	#uniqueYS = #sorted(ys, key=itemgetter(1), reverse=False)
	# 	# for row in data:
	# 	# 	if id == row[2]:
	# 	# 		print row
	# 	for i in ys[:28]:
	# 		print i
	# 	print '---'



if __name__ == '__main__':
	main()