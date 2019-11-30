words = ["redivider", "deified", "civic", "test"]


def check_palindrome(word):
    if word == word[::-1]:
        return True
    return False


for word in words:
    print(check_palindrome(word))
