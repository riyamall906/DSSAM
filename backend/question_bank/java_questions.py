
JAVA_QUESTIONS = [
    # EASY (5)
    {
        "id": 1,
        "title": "Sum of Two Numbers",
        "skill": "Java",
        "topic": "Basic Programming",
        "difficulty": "Easy",
        "description": "Read two integers and print their sum.",
        "input": "Two space-separated integers.",
        "output": "Their sum.",
        "examples": [{"input": "5 7", "output": "12"}],
        "test_cases": [
            {"input": "5 7", "expected_output": "12"},
            {"input": "0 0", "expected_output": "0"},
            {"input": "-3 8", "expected_output": "5"}
        ]
    },
    {
        "id": 2,
        "title": "Even or Odd",
        "skill": "Java",
        "topic": "Conditionals",
        "difficulty": "Easy",
        "description": "Read an integer and print Even if it is even, otherwise Odd.",
        "input": "One integer.",
        "output": "Even or Odd.",
        "examples": [{"input": "6", "output": "Even"}],
        "test_cases": [
            {"input": "6", "expected_output": "Even"},
            {"input": "7", "expected_output": "Odd"},
            {"input": "0", "expected_output": "Even"}
        ]
    },
    {
        "id": 3,
        "title": "Largest of Three Numbers",
        "skill": "Java",
        "topic": "Conditionals",
        "difficulty": "Easy",
        "description": "Read three integers and print the largest.",
        "input": "Three space-separated integers.",
        "output": "The largest integer.",
        "examples": [{"input": "4 9 2", "output": "9"}],
        "test_cases": [
            {"input": "4 9 2", "expected_output": "9"},
            {"input": "8 8 3", "expected_output": "8"},
            {"input": "-5 -2 -9", "expected_output": "-2"}
        ]
    },
    {
        "id": 4,
        "title": "Factorial",
        "skill": "Java",
        "topic": "Loops",
        "difficulty": "Easy",
        "description": "Read a non-negative integer n and print n factorial. Assume 0 <= n <= 20.",
        "input": "One integer n.",
        "output": "n factorial.",
        "examples": [{"input": "5", "output": "120"}],
        "test_cases": [
            {"input": "5", "expected_output": "120"},
            {"input": "0", "expected_output": "1"},
            {"input": "1", "expected_output": "1"}
        ]
    },
    {
        "id": 5,
        "title": "Reverse a Number",
        "skill": "Java",
        "topic": "Loops",
        "difficulty": "Easy",
        "description": "Read a non-negative integer and print its digits in reverse order. Print 0 if the input is 0.",
        "input": "One non-negative integer.",
        "output": "The reversed number.",
        "examples": [{"input": "1234", "output": "4321"}],
        "test_cases": [
            {"input": "1234", "expected_output": "4321"},
            {"input": "100", "expected_output": "1"},
            {"input": "0", "expected_output": "0"}
        ]
    },

    # MEDIUM (5)
    {
        "id": 6,
        "title": "Second Largest Element",
        "skill": "DSA",
        "topic": "Arrays",
        "difficulty": "Medium",
        "description": "Find the second largest distinct element in an array. If it does not exist, print -1.",
        "input": "First line: n. Second line: n integers.",
        "output": "Second largest distinct element or -1.",
        "examples": [{"input": "5\n10 5 8 10 3", "output": "8"}],
        "test_cases": [
            {"input": "5\n10 5 8 10 3", "expected_output": "8"},
            {"input": "4\n7 7 7 7", "expected_output": "-1"},
            {"input": "3\n1 3 2", "expected_output": "2"}
        ]
    },
    {
        "id": 7,
        "title": "Binary Search",
        "skill": "DSA",
        "topic": "Searching",
        "difficulty": "Medium",
        "description": "Given a sorted array and a target, print its index using zero-based indexing. Print -1 if absent.",
        "input": "First line: n. Second line: n sorted integers. Third line: target.",
        "output": "Index of target or -1.",
        "examples": [{"input": "5\n1 3 5 7 9\n7", "output": "3"}],
        "test_cases": [
            {"input": "5\n1 3 5 7 9\n7", "expected_output": "3"},
            {"input": "5\n1 3 5 7 9\n2", "expected_output": "-1"},
            {"input": "1\n4\n4", "expected_output": "0"}
        ]
    },
    {
        "id": 8,
        "title": "Check Palindrome String",
        "skill": "Java",
        "topic": "Strings",
        "difficulty": "Medium",
        "description": "Check whether a given string is a palindrome. Comparison is case-sensitive.",
        "input": "One string without spaces.",
        "output": "Yes or No.",
        "examples": [{"input": "madam", "output": "Yes"}],
        "test_cases": [
            {"input": "madam", "expected_output": "Yes"},
            {"input": "hello", "expected_output": "No"},
            {"input": "a", "expected_output": "Yes"}
        ]
    },
    {
        "id": 9,
        "title": "Two Sum",
        "skill": "DSA",
        "topic": "Arrays",
        "difficulty": "Medium",
        "description": "Find two distinct indices whose elements add up to the target. Print the smaller index first. Assume exactly one solution exists.",
        "input": "First line: n. Second line: n integers. Third line: target.",
        "output": "Two zero-based indices.",
        "examples": [{"input": "4\n2 7 11 15\n9", "output": "0 1"}],
        "test_cases": [
            {"input": "4\n2 7 11 15\n9", "expected_output": "0 1"},
            {"input": "3\n3 2 4\n6", "expected_output": "1 2"},
            {"input": "2\n3 3\n6", "expected_output": "0 1"}
        ]
    },
    {
        "id": 10,
        "title": "Valid Parentheses",
        "skill": "DSA",
        "topic": "Stack",
        "difficulty": "Medium",
        "description": "Check whether brackets in a string are correctly balanced. The string contains only (), {} and [].",
        "input": "One bracket string.",
        "output": "Valid or Invalid.",
        "examples": [{"input": "({[]})", "output": "Valid"}],
        "test_cases": [
            {"input": "({[]})", "expected_output": "Valid"},
            {"input": "([)]", "expected_output": "Invalid"},
            {"input": "(((", "expected_output": "Invalid"}
        ]
    },

    # HARD (5)
    {
        "id": 11,
        "title": "Longest Substring Without Repeating Characters",
        "skill": "DSA",
        "topic": "Sliding Window",
        "difficulty": "Hard",
        "description": "Find the length of the longest substring containing no repeated characters.",
        "input": "One string.",
        "output": "Length of the longest valid substring.",
        "examples": [{"input": "abcabcbb", "output": "3"}],
        "test_cases": [
            {"input": "abcabcbb", "expected_output": "3"},
            {"input": "bbbbb", "expected_output": "1"},
            {"input": "pwwkew", "expected_output": "3"}
        ]
    },
    {
        "id": 12,
        "title": "Maximum Subarray Sum",
        "skill": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Find the maximum sum of a non-empty contiguous subarray.",
        "input": "First line: n. Second line: n integers.",
        "output": "Maximum subarray sum.",
        "examples": [{"input": "5\n-2 1 -3 4 5", "output": "9"}],
        "test_cases": [
            {"input": "5\n-2 1 -3 4 5", "expected_output": "9"},
            {"input": "3\n-5 -2 -8", "expected_output": "-2"},
            {"input": "4\n1 2 3 4", "expected_output": "10"}
        ]
    },
    {
        "id": 13,
        "title": "Coin Change",
        "skill": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Given coin denominations and an amount, find the minimum number of coins needed. Print -1 if impossible. Assume unlimited coins of each denomination.",
        "input": "First line: n and amount. Second line: n coin values.",
        "output": "Minimum number of coins or -1.",
        "examples": [{"input": "3 11\n1 2 5", "output": "3"}],
        "test_cases": [
            {"input": "3 11\n1 2 5", "expected_output": "3"},
            {"input": "1 3\n2", "expected_output": "-1"},
            {"input": "1 0\n1", "expected_output": "0"}
        ]
    },
    {
        "id": 14,
        "title": "Number of Islands",
        "skill": "DSA",
        "topic": "Graphs",
        "difficulty": "Hard",
        "description": "Given a grid of 0s and 1s, count groups of connected 1s. Cells connect horizontally and vertically only.",
        "input": "First line: rows and columns. Next lines: grid rows containing 0s and 1s.",
        "output": "Number of islands.",
        "examples": [{"input": "3 3\n110\n010\n001", "output": "2"}],
        "test_cases": [
            {"input": "3 3\n110\n010\n001", "expected_output": "2"},
            {"input": "2 2\n11\n11", "expected_output": "1"},
            {"input": "2 3\n000\n000", "expected_output": "0"}
        ]
    },
    {
        "id": 15,
        "title": "Longest Common Subsequence",
        "skill": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "description": "Find the length of the longest common subsequence of two strings.",
        "input": "Two strings, one per line.",
        "output": "Length of their longest common subsequence.",
        "examples": [{"input": "abcde\nace", "output": "3"}],
        "test_cases": [
            {"input": "abcde\nace", "expected_output": "3"},
            {"input": "abc\ndef", "expected_output": "0"},
            {"input": "abc\nabc", "expected_output": "3"}
        ]
    }
]
