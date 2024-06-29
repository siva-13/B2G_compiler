import requests
from concurrent.futures import ThreadPoolExecutor

# URL for the POST request
url = "http://51.20.123.126/compiler"

# Larger payloads to test
payloads = [
    {"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},{"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},{"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},{"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},{"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},{"code": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(10))
"""},
    {"code": """
import random

def generate_random_numbers(n):
    return [random.randint(0, 1000) for _ in range(n)]

random_numbers = generate_random_numbers(1000)
print(sorted(random_numbers))
"""},
    {"code": """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

print(fibonacci(20))
"""},
    {"code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)
"""},
    {"code": """
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

llist = LinkedList()
llist.append(1)
llist.append(2)
llist.append(3)
llist.print_list()
"""},
    {"code": """
import math

def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes

print(find_primes(100))
"""},
    {"code": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(numbers))
"""},
    {"code": """
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root):
    res = []
    if root:
        res = inorder_traversal(root.left)
        res.append(root.val)
        res = res + inorder_traversal(root.right)
    return res

r = TreeNode(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

print(inorder_traversal(r))
"""},
    {"code": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

numbers = [3,6,8,10,1,2,1]
print(quicksort(numbers))
"""},
    {"code": """
import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "children": [
        {"name": "Anna", "age": 10},
        {"name": "Ella", "age": 5}
    ]
}

json_data = json.dumps(data, indent=4)
print(json_data)
"""},
{
    "code": """
import time
for x in range(5):
    print(x)
    time.sleep(1)
"""
}

]

# Function to send a POST request with a given payload
def send_request(payload):
    try:
        response = requests.post(url, json=payload)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)

# Use ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=len(payloads)) as executor:
    futures = [executor.submit(send_request, payload) for payload in payloads]
    for future in futures:
        status_code, response = future.result()
        if status_code is not None:
            print(f"Status Code: {status_code}, Response: {response}")
        else:
            print(f"Error: {response}")
