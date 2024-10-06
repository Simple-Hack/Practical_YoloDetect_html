class Solution:
    def isPalindrome(self, s: str) -> bool:
        str1=""
        str2=""
        for cha in s:
            if cha.isdigit() or cha.isalpha():
                str1.append(cha)
        str2=reversed(str1)
        if str1==str2:
            return True
        else:
            return False

        