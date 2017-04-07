import nltk
import numpy
import random
import timeit

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped

def merge(l, r):
	merged_list = []
	l_i = 0
	r_i = 0
	len_list = len(l) + len(r)
	len_l = len(l)
	len_r = len(r)
	while len(merged_list) < len_list:
		if l_i >= len_l:
			merged_list += r[r_i:]
		elif r_i >= len_r:
			merged_list += l[l_i:]

		elif l[l_i] < r[r_i]:
			merged_list.append(l[l_i])
			l_i += 1
		else:
			merged_list.append(r[r_i])
			r_i += 1
	return merged_list

def merge_sort(u_list):
	len_u_list = len(u_list)
	if len_u_list == 1:
		return u_list
	else:
		l = merge_sort(u_list[:len_u_list/2])
		r = merge_sort(u_list[len_u_list/2:])
		return merge(l, r)

def partition(u_list, lo, hi):
	pivot = u_list[lo]
	i = lo-1
	j = hi+1
	while True:
		i += 1
		while u_list[i] < pivot:
			i += 1
		j -= 1
		while u_list[j] > pivot:
			j -= 1
		if i >= j:
			return j
		temp = u_list[i]
		u_list[i] = u_list[j]
		u_list[j] = temp

def quick_sort(u_list, lo, hi):
	if lo < hi:
		p = partition(u_list, lo, hi)
		l_list = quick_sort(u_list, lo, p)
		r_list = quick_sort(u_list, p+1, hi)
		return l_list
	else:
		return u_list
def main():
	unsorted = random.sample(xrange(1000000), 1000000)
	#unsorted = list(set(nltk.corpus.gutenberg.words('austen-emma.txt')))

	#unsorted = ["bobby", "crimi", "sam", "beckett", "backett"]
	#print unsorted
	wrapped = wrapper(merge_sort, unsorted)
	print timeit.timeit(wrapped, number=1)
	wrapped = wrapper(quick_sort, unsorted, 0, len(unsorted)-1)
	print timeit.timeit(wrapped, number=1)
	#sorted_list = merge_sort(unsorted)

if __name__ == "__main__":
	main()
