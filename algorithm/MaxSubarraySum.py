def findMaxCrossingSubarray(arr, low, mid, high):
	leftSum = -10000
	sum = 0
	for i in range(mid, low - 1, -1):
		sum = sum + arr[i]
		if (sum > leftSum):
			leftSum = sum

	rightSum = -10000
	sum = 0
	for j in range(mid + 1, high + 1):
		sum = sum + arr[j]
		if (sum > rightSum):
			rightSum = sum

	return max(rightSum + leftSum, leftSum, rightSum)


def findMaxSubarray(arr, low, high):
	if high == low:
		return arr[low]
	else:
		mid = (high + low) // 2

		leftSum = findMaxSubarray(arr, low, mid)
		rightSum = findMaxSubarray(arr, mid+1, high)
		crossSum = findMaxCrossingSubarray(arr, low, mid, high)
	return max(leftSum, rightSum, crossSum)


def main():
	arr = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7] 
	n = len(arr) 
	maxSum = findMaxSubarray(arr, 0, n-1) 
	print("Maximum subarray sum is ", maxSum) 



if __name__ == '__main__':
	main()
























