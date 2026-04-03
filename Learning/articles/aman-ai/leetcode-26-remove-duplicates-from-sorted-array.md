# LeetCode • 26. Remove Duplicates from Sorted Array

**Source:** https://aman.ai/lc_old/remove-dups-from-sorted-array/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

problem algorithm code complexity analysisproblem given a sorted array nums remove the duplicates in place such that each element appears only once and returns the new length do not allocate extra space for another array you must do this by modifying the input array in place with o 1 extra memory see problem on leetcode algorithm since the array is already sorted we can keep two pointers i and j where i is the slow runner while j is the fast runner as long as nums i nums j we increment j to skip the duplicate when we encounter nums j neq nums i the duplicate run has ended so we must copy its value to nums i 1 i is then incremented and we repeat the same process again until j reaches the end of array codeclass solution def removeduplicates self nums list int gt int param a list of integers return an integer handle the special case that a is empty if not nums or if not len nums or if len a 0 return 0 i 0 for j in range 1 len nums not a duplicate item if nums i nums j i 1 nums i nums j return i 1complexity analysis time complexity o n assume that n is the length of array each of i and j traverses at most n steps space complexity o 1
