from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from impeachment.models import Elector

from django.http import JsonResponse

def index(request):
	electors = Elector.objects.all()
	context = {
		'electors' : electors
	}
	return render(request, 
		'impeachment/index.html', 
		context)

def vote(request, register_id, vote_id):
	
	if(validation_id(request, register_id)):
		# validate vote. Only 0 = contra, 1 = a favor, 2 = indeciso
		if vote_id < 3:
			return JsonResponse({'result': 'fail'})

		elector_exist = Elector.objects.filter(register_id=register_id)

		# check elector exist, and update or not
		if elector_exist:
			for ee in elector_exist:
				if int(vote_id) == int(ee.vote):
					return JsonResponse({'result': 'fail'})
				ee.vote = int(vote_id)
				ee.save()	
				return JsonResponse({'result': 'updated'})

		elector = Elector(register_id=register_id, vote=vote_id)
		elector.save()
	
		return JsonResponse({'result': 'created'})
	else:
		return JsonResponse({'result': 'fail'})


def	validation_id(request, register_id):
	is_valid = '0'
	length = len(register_id)

	if( length == 12 ): # 12 caracters only
		r_id = list(register_id) # separete digits
		r_id = map(int, r_id)

		# Calculate validators
		# First divisor validator
		first_dv = (r_id[0] * 2)+(r_id[1] * 3)+(r_id[2] * 4)+(r_id[3] * 5)+(r_id[4] * 6)+(r_id[5] * 7)+(r_id[6] * 8)+(r_id[7] * 9)
		first_dv = first_dv % 11
		if(first_dv == 10): # When equal to ten, then set to zero
			first_dv = 0

		# Second divisor validator
		second_dv = (r_id[8] * 7)+(r_id[9] * 8)+(r_id[10] * 9);
		second_dv = second_dv % 11
		if(second_dv == 10):
			second_dv = 0
		
		# validate validators
		if( first_dv == r_id[10]):
			if(second_dv == r_id[11]):
				is_valid = '1'

	return JsonResponse({'isvalid': is_valid})

def all_votes(request):
	electors = Elector.objects.all()
	json = {}
	
	for el in electors:
		json[el.register_id] = el.vote

	return JsonResponse({'votes': json})


def counted_votes(request):
	electors = Elector.objects.all()
	
	in_favor = 0
	against = 0
	undecided = 0
	
	for el in electors:
		if(el.vote == 0):
			against = against+1
		elif(el.vote == 1):
			in_favor = in_favor+1
		elif(el.vote == 2):
			undecided = undecided+1

	json = {
		'in_favor': in_favor,
		'against': against,
		'undecided': undecided,
	}

	return JsonResponse(json)




